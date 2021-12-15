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
        Initialize with the in-cluster configuration and the required
        APIs
        """
#         kubernetes.config.load_incluster_config()
#         self.api = kubernetes.client.CustomObjectsApi()
#         self.core_api = kubernetes.client.CoreV1Api()
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
                       operation=transaction_type, sub_operation='new_intent')
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
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response

    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
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
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response
    except HTTPException as e:
        return e
    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        response.status_code = 500
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
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
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response
    except HTTPException as e:
        return e
    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        response.status_code = 500
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response


@proxy.route("/transactions/<service_owner>/<transaction_uuid>",  methods=['DELETE'])
def transactions_delete(service_owner, transaction_uuid):
    sys.stdout.write('Received delete request for '
                     '[service_owner=%s, transaction_uuid=%s] \n' %
                     (service_owner, transaction_uuid))
    try:
        proxy_server.delete_transaction(service_owner, transaction_uuid)
        response = flask.jsonify({})
        response.status_code = 200
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response
    except HTTPException as e:
        return e
    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        response.status_code = 500
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response


@proxy.route("/transactions_types",  methods=['GET'])
def transactions_types():
    sys.stdout.write('Received get types\n')
    response = flask.jsonify(TRANSACTION_TYPES)
    response.status_code = 200
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
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
