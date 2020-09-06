import json
import os
from confluent_kafka import Producer, KafkaError

conf = {
    # 'bootstrap.servers': os.environ['CCLOUD_BOOTSTRAP_SERVERS'],
    # 'sasl.mechanisms': os.environ['CCLOUD_SASL_MECHANISMS'],
    # 'security.protocol': os.environ['CCLOUD_SECURITY_PROTOCOL'],
    # 'sasl.username': os.environ['CCLOUD_USERNAME'],
    # 'sasl.password': os.environ['CCLOUD_PASSWORD'],
    'debug': "msg,topic",
    'error_cb': lambda x: print("error_cb", x),
    'api.version.request.timeout.ms': 30,
    'enable.ssl.certificate.verification': False,
}
producer = Producer(conf)

final_response = None

FAILURE_RESPONSE = {
    "statusCode": 408,
    "body": "Failed: Request Timeout",
}

# Use Schema Registry to fetch Schema.


def acked(err, msg):
    """Delivery report handler called on
    successful or failed delivery of message
    """
    global final_response
    if err is not None:
        failed_response = {
            'statusCode': 500,
            'body': "Failed to deliver message: {}".format(err),
        }
        final_response = failed_response
    else:
        success_response = {
            'statusCode': 200,
            'body': "Produced record to topic {} partition [{}] @ offset {}".format(msg.topic(), msg.partition(), msg.offset()),
        }
        final_response = success_response
    print("final_response", final_response)


def send_to_stream(event_name, event_data, error=False):
    """
    Put this event down in the metric event stream
    """
    event = {
        "event_type": event_name,
        **event_data
    }
    print("DATA", event)
    """
    if(error is not None):
        producer.produce('METRICS', json.dumps(event).encode('utf-8'),
                         callback=acked)
    else:
        producer.produce('ERRORS', json.dumps(event).encode('utf-8'),
                         callback=acked)
    producer.poll(20)
    """
