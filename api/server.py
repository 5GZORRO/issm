import flask
import json
import os
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
KAFKA_TOPIC = 'issm-topic'


KAFKA_IP = os.getenv('ISSM_KAFKA_HOST')
KAFKA_PORT = os.getenv('ISSM_KAFKA_PORT', 9092)

if not KAFKA_IP:
    print ('ISSM_KAFKA_HOST not set')
    raise sys.exit(1)


def topic_create(kafka_ip, kafka_port, topic_name):
    """
    Helper method to create a kafka topic on kafka broker used by this agent. No
    error returned if topic already exists

    :param kafka_ip: kafka broker ipaddress
    :type kafka_ip: ``str``

    :param kafka_port: kafka broker port
    :type kafka_port: ``int``

    :param topic_name: kafka tpoic to create
    :type topic_name: ``str``

    """
    print ('[INFO] Request to create topic [%s] on kafka [%s]' %
          (topic_name, kafka_ip+':'+str(kafka_port)))
    admin_client = KafkaAdminClient(bootstrap_servers="%s:%s" % (kafka_ip, kafka_port),
    client_id='%s-%s' % (topic_name, 'client-id'))

    topic_list = []
    topic_list.append(NewTopic(name=topic_name, num_partitions=1,
                               replication_factor=1))

    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except TopicAlreadyExistsError as e:
        print ('[DEBUG] Topic %s already exists' % topic_name)


def publish_intent(kafka_ip, kafka_port, payload):
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
    t = producer.send(KAFKA_TOPIC, payload)

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

    def instantiate(self, service_owner, operation, intent):
        """
        Instantiate ISSM flow with the given intent on-behalf of the service_owner.

        :param service_owner: the name of the service owner e.g. tenant name.
        :type service_owner: ``str``

        :param operation: the operation for this flow. Currently
                          'submit_intent' is supported
        :type operation: ``str``

        :param intent: intent payload e.g. slice creation intent
        :type intent: ``dict``
        """
        topic_create(kafka_ip=KAFKA_IP, kafka_port=KAFKA_PORT,
                     topic_name=service_owner)

        event_uuid = str(uuid.uuid4()).replace('-','')
        print ('** event_uuid: %s' % event_uuid)

        payload = dict(event_uuid=event_uuid, transaction_uuid=event_uuid,
                       service_owner=service_owner,
                       operation=operation)
        payload['callback'] = dict(type='kafka', kafka_topic=service_owner)
        payload.update(intent)
        publish_intent(KAFKA_IP, KAFKA_PORT, payload)
        return {'transaction_uuid': event_uuid}


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


@proxy.route("/instantiate",  methods=['POST'])
def instantiate():
    def _validate(intent):
        try:
            intent['qos_parameters']
            intent['offered_price']
            intent['latitude']
            intent['longitude']
            intent['slice_segment']
            intent['category']
        except KeyError as e:
            raise Exception ('[ERROR] Failed schema validation: Missing '
                   'key: "%s" in the supplied payload: %s' %
                   (str(e), intent))

    sys.stdout.write('Received flow instantiate request\n')
    try:
        value = getMessagePayload()

        service_owner=value['service_owner']
        operation='submit_intent'
        intent = value['intent']
        _validate(intent=intent)
        response = flask.jsonify(
            proxy_server.instantiate(
                service_owner=service_owner, operation=operation,
                intent=intent))

        response.status_code = 200
        return response

    except Exception as e:
        response = flask.jsonify({'error': 'Internal error. {}'.format(e)})
        response.status_code = 500

    sys.stdout.write('Exit /instantiate %s\n' % str(response))
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
