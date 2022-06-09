# Copyright 2020 - 2021 IBM Corporation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import flask
import json
import os
import requests
import sys
import uuid

from gevent.wsgi import WSGIServer
from werkzeug.exceptions import HTTPException

import kubernetes
from kubernetes.client.rest import ApiException

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError, TopicAlreadyExistsError

import iso8601


import kubernetes
from kubernetes.client import V1Namespace
from kubernetes.client import V1ObjectMeta
from kubernetes.client.rest import ApiException


KAFKA_API_VERSION = (0, 10, 1)
KAFKA_TIMEOUT = 10  # seconds


KAFKA_IP = os.getenv('ISSM_KAFKA_HOST')
KAFKA_PORT = os.getenv('ISSM_KAFKA_PORT', 9092)

if not KAFKA_IP:
    print ('ISSM_KAFKA_HOST not set')
    raise sys.exit(1)

ARGO_SERVER = os.getenv('ARGO_SERVER')

if not ARGO_SERVER:
    print ('ARGO_SERVER not set')
    raise sys.exit(1)

LB_ARGO_SERVER = os.getenv('LB_ARGO_SERVER')

if not LB_ARGO_SERVER:
    print ('LB_ARGO_SERVER not set')
    raise sys.exit(1)


TRANSACTION_TYPES = ['instantiate', 'scaleout']
DOMAIN_SENSOR_NAME='issm-branch'


def find(l, predicate):
    results = [x for x in l if predicate(x)]
    return results[0] if len(results) > 0 else None


def parse_isotime(timestr):
    """Parse time from ISO 8601 format."""
    try:
        return iso8601.parse_date(timestr)
    except iso8601.ParseError as e:
        raise Exception(str(e))
    except TypeError as e:
        raise Exception(str(e))


def publish_intent(kafka_ip, kafka_port, topic, payload):
    """
    Send the intent to the ISSM kafka bus

    :param kafka_ip: kafka broker ipaddress
    :type kafka_ip: ``str``

    :param kafka_port: kafka broker port
    :type kafka_port: ``int``

    :param payload: the payload (intent) to send
    :type payload: ``dict``
    """
    producer = KafkaProducer(bootstrap_servers="%s:%s" % (kafka_ip, kafka_port),
                             api_version=KAFKA_API_VERSION,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    print('[INTENT] %s' % payload)
    t = producer.send(topic, payload)

    # Block for 'synchronous' send; set timeout on X seconds
    try:
        t.get(timeout=KAFKA_TIMEOUT)
    except KafkaError as ke:
        print('[ERROR] KafkaError: %s' % str(ke))
        raise ke
    finally:
        producer.close()


class Proxy:
    def __init__(self):
        """
        Initialize the proxy with the in-cluster configuration and the required
        APIs
        """
        kubernetes.config.load_incluster_config()
        self.api = kubernetes.client.CustomObjectsApi()
        sys.stdout.write('ISSM-API initialized\n')

    def instantiate(self, service_owner, transaction_type, intent):
        """
        Instantiate ISSM flow with the given intent on-behalf of the service_owner.

        :param service_owner: the name of the service owner.
        :type service_owner: ``str``

        :param transaction_type: the operation for this flow. Currently 'instantiate',
                          'scaleout' are supported.
        :type transaction_type: ``str``

        :param intent: intent payload e.g. slice creation intent
        :type intent: ``dict``
        """
        event_uuid = str(uuid.uuid4()).replace('-','')
        print ('** event_uuid: %s' % event_uuid)

        payload = dict(event_uuid=event_uuid, transaction_uuid=event_uuid,
                       service_owner=service_owner,
                       operation=transaction_type, sub_operation='API')
        payload['callback'] = dict(type='kafka', kafka_topic=service_owner)
        payload.update(intent)
        publish_intent(KAFKA_IP, KAFKA_PORT,
                       topic='issm-in-%s' % service_owner, payload=payload)
        return {'transaction_uuid': event_uuid}

    def get_transactions(self, service_owner, transaction_type=None):
        """
        Return a list of transactions belonging to the given service owner.
        If transaction_type supplied then filter by operation.

        :param service_owner: the service owner
        :type service_owner: ``str``

        :param transaction_type: the transaction type
        :type transaction_type: ``str``
        """
        sys.stdout.write (
            'Enter get_transactions [service_owner=%s, transaction_type=%s]\n' %
                          (service_owner, transaction_type))

        query_str = "fields=items.metadata.name,items.metadata.creationTimestamp,"\
        "items.metadata.labels.transaction_uuid,"\
        "items.metadata.labels.operation,items.status.phase&"\
        "listOptions.labelSelector=issm=true"

        if transaction_type:
            query_str = query_str + \
                ",operation=%s" % transaction_type

        headers = {'Content-Type': 'application/json'}
        r = requests.get("http://%(argo_server)s/api/v1/workflows/%(namespace)s?%(query)s" %
                        {
                           "argo_server": ARGO_SERVER,
                           "namespace": "domain-"+service_owner,
                           "query": query_str
                        }, headers=headers)

        sys.stdout.write ('Parsing result [r.json=%s]..\n' % r.json())
        items = r.json()['items'] if r.json().get('items') is not None else []
        transactions = dict()
        for i in items:
            # transaction key points to list of its subflows
            transactions.setdefault(i['metadata']['labels']['transaction_uuid'], []).append(i)
        # prepare the output
        res = []
        for k in transactions:
            subflows = transactions[k]
            status_set = set()
            t_type = subflows[0]['metadata']['labels']['operation']
            for sf in subflows:
                status_set.add(sf['status']['phase'])

            dates = [parse_isotime(sf['metadata']['creationTimestamp']) for sf in subflows]
            dates.sort()
            sorteddates = [datetime.datetime.isoformat(ts) for ts in dates]
            sys.stdout.write ('sorteddates of transaction [%s]: [%s]\n' % (k, sorteddates))

            # at least one Failed
            if 'Failed' in status_set:
                status = 'Failed'

            # at least one Running
            elif 'Running' in status_set:
                status = 'Running'

            # all Succeeded
            elif len(status_set) == 1 and 'Succeeded' in status_set:
                status = 'Succeeded'

            res.append(
                dict(transaction_uuid=k, transaction_type=t_type, status=status,
                     created=sorteddates[0],
                    ref='http://%s/workflows/domain-%s?label=transaction_uuid=%s'
                    % (LB_ARGO_SERVER, service_owner, k)))

        return res


    def delete_transaction(self, service_owner, transaction_uuid):
        """
        Delete a transaction of a given service owner.

        Delete all subflows belonging to the given transaction uuid for this
        service owner.

        :param service_owner: the service owner owning the transaction
        :type service_owner: ``str``

        :param transaction_uuid: the transaction uuid
        :type transaction_uuid: ``str`` in uuid format
        """
        sys.stdout.write (
            'Enter delete_transaction [service_owner=%s, transaction_uuid=%s]\n' %
            (service_owner, transaction_uuid))

        headers = {'Content-Type': 'application/json'}
        query_str = "fields=items.metadata.name,"\
        "items.metadata.labels.transaction_uuid&"\
        "listOptions.labelSelector=transaction_uuid=%s" % transaction_uuid

        sys.stdout.write ('Retrieve workflows [namespace=%s] [query=%s]' %
                          ('domain'+service_owner, query_str))
        r = requests.get("http://%(argo_server)s/api/v1/workflows/%(namespace)s?%(query)s" %
                       {
                          "argo_server": ARGO_SERVER,
                          "namespace": "domain-"+service_owner,
                          "query": query_str
                       }, headers=headers)
        sys.stdout.write ('Parsing result [r.json=%s]..\n' % r.json())

        items = r.json()['items'] if r.json().get('items') is not None else []
        if not items:
            raise Exception(
                "[transaction_uuid=%s] does not exist for [service_owner=%s]" %
                (transaction_uuid, service_owner))

        for i in items:
            name = i['metadata']['name']
            sys.stdout.write ('Deleting workflow [name=%s]..\n' % name)
            requests.delete("http://%(argo_server)s/api/v1/workflows/%(namespace)s/%(name)s" %
                        {
                            "argo_server": ARGO_SERVER,
                            "namespace": "domain-"+service_owner,
                            "name": name
                        }, headers=headers)

    def get_workflow(self, transaction_uuid):
        """
        Retrieve the *first* workflow object of a given transaction_uuid.
        This operation is cross namespace and hence goes through k8s API.
        """
        sys.stdout.write('Requesting workflows\n')

        res = {}
        # Filter also by metadata.name so that we get the *first* transaction flow
        workflows = self.api.list_cluster_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            plural="workflows",
            label_selector="transaction_uuid=%s" % transaction_uuid,
            field_selector="metadata.name=%s" % transaction_uuid)
        if workflows and workflows.get('items'):
            #sys.stdout.write(str(workflows['items'][0]) + '\n')
            sys.stdout.write(str(len(workflows['items'])) + '\n')
            wf = (workflows['items'][0])
            wf_params = wf.get('spec', {}).get('arguments', {}).get('parameters', [])
            res = {
                'name': wf['metadata']['name'],
                'phase': wf['status']['phase'],
                'progress': wf['status']['progress'],
                'workflow_parameters': wf_params
            }

        return res
    
    def getSensor(self, service_owner, name):
        sys.stdout.write('Requesting getSensor for name '+name+'\n')

        sensor = self.api.get_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="domain-%s" % service_owner,
            plural="sensors",
            name=name)
        sys.stdout.write(str(sensor)+'\n')
        return sensor

    def _update_sensor(self, service_owner, sensor_json):
        return self.api.replace_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            plural="sensors",
            name=DOMAIN_SENSOR_NAME,
            namespace="domain-%s" % service_owner,
            body=sensor_json
        )

    def snfvo_add(self, service_owner, snfvo_name, criteria_name, sensor_json):
        sys.stdout.write('snfvo_add..\n')
        sys.stdout.write(str(sensor_json))
        sys.stdout.write('\n')

        templates = sensor_json['spec']['triggers'][0]['template']['k8s']['source']\
            ['resource']['spec']['templates']

        update = False
        # instantiate
        template_inst = find (templates, lambda t: t['name'] == 'instantiate-invoke-snfvo')
        steps = template_inst['steps']

        # NOTE: steps is nested list
        snfvo_step = find (steps, lambda s: s[0]['name'] == 'snfvo-%s' % snfvo_name)
        if snfvo_step:
            sys.stdout.write('snfvo [%s] already exists for instantiate\n' % snfvo_name)
        else:
            snfvo_step = {
                "name": "snfvo-%s" % snfvo_name,
                "templateRef": {
                    "name": "snfvo-%s-flow" % snfvo_name,
                    "template": "instantiate"
                },
                "when": "\"{{steps.get-order-from-catalog.outputs.parameters.name}}\" == \"%s\"" % criteria_name
            }
            steps.append([snfvo_step])
            update = True

        # scaleout
        template_sa = find (templates, lambda t: t['name'] == 'scaleout-invoke-snfvo')
        steps = template_sa['steps']
        # NOTE: steps is nested list
        snfvo_step = find (steps, lambda s: s[0]['name'] == 'snfvo-%s' % snfvo_name)
        if snfvo_step:
            sys.stdout.write('snfvo [%s] already exists for scaleout\n' % snfvo_name)
        else:
            snfvo_step = {
                "name": "snfvo-%s" % snfvo_name,
                "templateRef": {
                    "name": "snfvo-%s-flow" % snfvo_name,
                    "template": "scaleout"
                },
                "when": "\"{{steps.get-order-from-catalog.outputs.parameters.name}}\" == \"%s\"" % criteria_name
            }
            steps.append([snfvo_step])
            update = True

        if update:
            self._update_sensor(service_owner, sensor_json)
    
    def snfvo_delete(self, service_owner, snfvo_name, criteria_name, sensor_json):
        sys.stdout.write('snfvo_delete..\n')
        sys.stdout.write(str(sensor_json))
        sys.stdout.write('\n')

        templates = sensor_json['spec']['triggers'][0]['template']['k8s']['source']\
            ['resource']['spec']['templates']

        update = False

        # instantiate
        template_inst = find (templates, lambda t: t['name'] == 'instantiate-invoke-snfvo')
        steps = template_inst['steps']

        snfvo_step = find (steps, lambda s: s['name'] == 'snfvo-%s' % snfvo_name)
        if not snfvo_step:
            sys.stdout.write('snfvo [%s] was not found for instantiate\n' % snfvo_name)
        else:
            steps.remove(snfvo_step)
            update = True

        # scaleout
        template_sa = find (templates, lambda t: t['name'] == 'scaleout-invoke-snfvo')
        steps = template_sa['steps']

        snfvo_step = find (steps, lambda s: s['name'] == 'snfvo-%s' % snfvo_name)
        if not snfvo_step:
            sys.stdout.write('snfvo [%s] was not found for scaleout\n' % snfvo_name)
        else:
            steps.remove(snfvo_step)
            update = True

        if update:
            self._update_sensor(service_owner, sensor_json)


proxy = flask.Flask(__name__)
proxy.debug = True
server = None

proxy_server = None


def setServer(s):
    global server
    server = s


def setProxy(p):
    global proxy_server
    proxy_server = p


def getMessagePayload():
    message = flask.request.get_json(force=True, silent=True)
    if message and not isinstance(message, dict):
        flask.abort(400, 'message payload is not a dictionary')
    else:
        value = message if (message or message == {}) else {}
    if not isinstance(value, dict):
        flask.abort(400, 'message payload did not provide binding for "value"')
    return value


@proxy.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
    return response


@proxy.route("/hello")
def hello():
    sys.stdout.write ('Enter /hello\n')
    return ("Greetings from the ISSM-API server! ")


@proxy.route("/transactions/<service_owner>/<transaction_type>",  methods=['POST'])
def transactions_submit(service_owner, transaction_type):
    sys.stdout.write('Received submit request for '
                     '[service_owner=%s, transaction_type=%s] \n' %
                     (service_owner, transaction_type))
    try:
        value = getMessagePayload()
        if transaction_type not in TRANSACTION_TYPES:
            raise Exception(
                'transaction_type value does not match: %s' % 
                TRANSACTION_TYPES)

        intent = value
        response = flask.jsonify(
            proxy_server.instantiate(
                service_owner=service_owner, transaction_type=transaction_type,
                intent=intent))

        response.status_code = 200
        #response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        #response.headers["Access-Control-Allow-Origin"] = "*"
        response.status_code = 500

    sys.stdout.write('Exit /instantiate %s\n' % str(response))
    return response


@proxy.route("/transactions/<service_owner>",  methods=['GET'])
def transactions_get_all(service_owner):
    sys.stdout.write('Received get request for '
                     '[service_owner=%s] \n' % service_owner)
    try:
        flow_json = proxy_server.get_transactions(service_owner)
        response = flask.jsonify(flow_json)
        response.status_code = 200
        #response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except HTTPException as e:
        return e
    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        response.status_code = 500
        #response.headers["Access-Control-Allow-Origin"] = "*"
        return response


@proxy.route("/transactions/<service_owner>/<transaction_type>",  methods=['GET'])
def transactions_get(service_owner, transaction_type):
    sys.stdout.write('Received get request for '
                     '[service_owner=%s, transaction_type=%s] \n' %
                     (service_owner, transaction_type))
    try:
        flow_json = proxy_server.get_transactions(service_owner, transaction_type)
        response = flask.jsonify(flow_json)
        response.status_code = 200
        #response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except HTTPException as e:
        return e
    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        response.status_code = 500
        #response.headers["Access-Control-Allow-Origin"] = "*"
        return response


@proxy.route("/transactions/<service_owner>/<transaction_uuid>",  methods=['DELETE'])
def transactions_delete(service_owner, transaction_uuid):
    sys.stdout.write('Received delete request for '
                     '[service_owner=%s, transaction_uuid=%s] \n' %
                     (service_owner, transaction_uuid))
    try:
        proxy_server.delete_transaction(service_owner, transaction_uuid)
        response = flask.jsonify({'OK': 200})
        response.status_code = 200
        #response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except HTTPException as e:
        return e
    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        response.status_code = 500
        #response.headers["Access-Control-Allow-Origin"] = "*"
        return response


@proxy.route("/transactions_types",  methods=['GET'])
def transactions_types():
    sys.stdout.write('Received get types\n')
    response = flask.jsonify(TRANSACTION_TYPES)
    response.status_code = 200
    #response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@proxy.route("/workflows/<transaction_uuid>",  methods=['GET'])
def workflows_get(transaction_uuid):
    sys.stdout.write('Received get workflows for [transaction_uuid=%s]\n' %
                     transaction_uuid)
    try:
        flow_json = proxy_server.get_workflow(transaction_uuid)
        if not flow_json:
            response = flask.jsonify({'error': 'Workflow not found'})
            response.status_code = 404
        else:
            response = flask.jsonify(flow_json)
            response.status_code = 200
        return response
    except HTTPException as e:
        return e
    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        response.status_code = 500
        return response


@proxy.route("/snfvo/<service_owner>",  methods=['POST'])
def snfvo_create(service_owner):
    sys.stdout.write('Received snfvo request for '
                     '[service_owner=%s] \n' % service_owner)
    try:
        value = getMessagePayload()
        snfvo_name=value['snfvo_name']
        criteria_name=value['criteria_name']

        sensor_json = proxy_server.getSensor(
            service_owner=service_owner, name=DOMAIN_SENSOR_NAME)
        if not sensor_json:
            response = flask.jsonify({'error': 'Sensor [%s] not found' %
                                      DOMAIN_SENSOR_NAME})
            response.status_code = 404
            return response

        response = flask.jsonify(
            proxy_server.snfvo_add(
                service_owner=service_owner, snfvo_name=snfvo_name,
                criteria_name=criteria_name, sensor_json=sensor_json)
            )

        response.status_code = 200
        return response

    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        response.status_code = 500

    sys.stdout.write('Exit /snfvo %s\n' % str(response))
    return response


@proxy.route("/snfvo/<service_owner>/<snfo_name>",  methods=['DELETE'])
def snfvo_delete(service_owner, snfo_name):
    sys.stdout.write('Received snfvo delete request for '
                     '[service_owner=%s, snfo_name=%s] \n' %
                     (service_owner, snfo_name))
    try:
        sensor_json = proxy_server.getSensor(
            service_owner=service_owner, name=DOMAIN_SENSOR_NAME)
        if not sensor_json:
            response = flask.jsonify({'error': 'Sensor [%s] not found' %
                                      DOMAIN_SENSOR_NAME})
            response.status_code = 404
            return response

        flask.jsonify(
            proxy_server.snfvo_delete(
                service_owner=service_owner, snfvo_name=snfvo_name,
                sensor_json=sensor_json)
            )

        response.status_code = 200
        response = flask.jsonify({'OK': 200})        
        return response

    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        response.status_code = 500

    sys.stdout.write('Exit [DELETE] /snfvo %s\n' % str(response))
    return response



def main():
    port = int(os.getenv('LISTEN_PORT', 8080))
    server = WSGIServer(('0.0.0.0', port), proxy, log=None)
    setServer(server)
    print ('\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print ("Starting ISSM-API .. ready to serve requests on PORT: %s..\n\n"
           "KAFKA_SERVER '%s:%s' "
           "KAFKA_API_VERSION '%s' " %
           (int(port), KAFKA_IP, str(KAFKA_PORT), KAFKA_API_VERSION))
    print ('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n')

    server.serve_forever()


if __name__ == '__main__':
    setProxy(Proxy())
    main()
