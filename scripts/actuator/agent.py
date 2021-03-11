import argparse
import json
import threading
import uuid


from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError, TopicAlreadyExistsError


KAFKA_API_VERSION = (0, 10, 1)
KAFKA_TIMEOUT = 10  # seconds
KAFKA_TOPIC = 'issm-topic'


# Singleton
PROCESSED_INTENT = {}


def publish_intent(kafka_ip, kafka_port, intent):
    """
    Send the intent to the ISSM kafka bus
    """
    producer = KafkaProducer(bootstrap_servers="%s:%s" % (kafka_ip, kafka_port),
                             api_version=KAFKA_API_VERSION,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    print('[INTENT] %s' % intent)
    t = producer.send(KAFKA_TOPIC, intent)

    # Block for 'synchronous' send; set timeout on X seconds
    try:
        t.get(timeout=KAFKA_TIMEOUT)
    except KafkaError as ke:
        print('[ERROR] KafkaError: %s' % str(ke))

    producer.close()


def process_file(f, **kwargs):
    """
    Process a given intent file parsing it and publishing into ISSM Workflow
    Manager gateway
    """
    data = {}
    try:
        data = json.load(f)
    except Exception as e:
        print ('[ERROR] Error [%s] occurred on json load from file: %s. '
               % (str(e), f))
        raise
    try:
        data['qos_parameters']
        data['offered_price']
        data['latitude']
        data['longitude']
        data['slice_segment']
        data['category']
        return data

    except KeyError as e:
        print ('[ERROR] File %s failed schema validation. Error: %s' % (f.name, str(e)))
        raise


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

def _consume_issm(kafka_ip, kafka_port, callback_topic):
    """
    Separate consumer thread.
    """
    client_id='%s-%s' % (callback_topic, 'client-id')
    kafka_server = '%s:%s' % (kafka_ip, kafka_port)
    consumer = KafkaConsumer(
        bootstrap_servers=kafka_server,
        client_id=client_id,
        enable_auto_commit=True,
        api_version=KAFKA_API_VERSION)

    consumer.subscribe(pattern=callback_topic)
    print ('\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print ("Starting Kafka thread..\n\n"
           "KAFKA_CLIENT_ID: '%s' \n"
           "KAFKA_SERVER '%s' "
           "KAFKA_API_VERSION '%s' " %
           (client_id, kafka_server, KAFKA_API_VERSION))
    print ('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n')

    for msg in consumer:
        try:
            message = json.loads(msg.value.decode('utf-8'))
            print('[kafka] Received message: {}'.format(message))
        except Exception as e:
            print ('Exception: %s' % str(e))

def main():
    """
    Main entry point of the application
    """
    parser = argparse.ArgumentParser(description='ISSM Agent.')
    parser.add_argument('--kafka_ip', help='ISSM kafka ipaddress', required=True)
    parser.add_argument('--kafka_port', type=int, help='ISSM kafka port (default 9092)', default=9092)
    parser.add_argument('--intent_file', help='Full path to intent file (json)', required=True)
    parser.add_argument('--service_owner', help='Service owner publishing this intent', required=True)

    args = parser.parse_args()

    topic_name = args.service_owner
    # create callback topic
    topic_create(kafka_ip=args.kafka_ip, kafka_port=args.kafka_port,
                 topic_name=topic_name)

    print ('** Start _consume_issm thread from topic [%s]..' % args.service_owner)
    threading.Thread(target=_consume_issm,
                     args=[args.kafka_ip, args.kafka_port,topic_name]).start()

    global PROCESSED_INTENT
    with open(args.intent_file) as f:
        PROCESSED_INTENT = process_file(f)

    event_uuid = str(uuid.uuid4()).replace('-','')
    print ('** event_uuid: %s' % event_uuid)

    # add required metadata
    PROCESSED_INTENT['operation'] = 'submit_intent'

    PROCESSED_INTENT['event_uuid'] = event_uuid
    PROCESSED_INTENT['callback'] = dict(type='kafka', kafka_topic=topic_name)
    PROCESSED_INTENT['service_owner'] = args.service_owner

    publish_intent(args.kafka_ip, args.kafka_port, PROCESSED_INTENT)


if __name__=="__main__":
    main()