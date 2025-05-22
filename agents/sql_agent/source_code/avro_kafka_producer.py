import argparse
import os
from uuid import uuid4
from datetime import datetime
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

class HRResultProducer:
    """
    SQL Result record for HR queries
    
    Args:
        message_id (str): Unique identifier for the query
        employee_id (str): Unique identifier for the employee
        timestamp (str): ISO-8601 timestamp
        query (str): Original text of the user's query
        status (str): Status of query processing (success/error)
        sql_result (str): Extracted context information
        source (str): Source of the original query
        sessionId (str, optional): Session identifier
    """
    def __init__(self, message_id=None, employee_id=None, timestamp=None, 
                 query=None, status=None, sql_result=None, source=None, sessionId=None):
        self.message_id = message_id
        self.employee_id = employee_id
        self.timestamp = timestamp
        self.query = query
        self.status = status
        self.sql_result = sql_result
        self.source = source
        self.sessionId = sessionId

def result_to_dict(result, ctx):
    """
    Returns a dict representation of a HRResultProducer instance for serialization.

    Args:
        result (HRResultProducer): HRResultProducer instance.
        ctx (SerializationContext): Metadata pertaining to the serialization operation.

    Returns:
        dict: Dict populated with result attributes to be serialized.
    """
    return {
        'message_id': result.message_id,
        'employee_id': result.employee_id,
        'timestamp': result.timestamp,
        'query': result.query,
        'status': result.status,
        'sql_result': result.sql_result,
        'source': result.source,
        'sessionId': result.sessionId
    }

def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """
    if err is not None:
        print(f"Delivery failed for message {msg.key()}: {err}")
        return
    print(f'Message {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def produce(result):
    """
    Produce a message to Kafka using the SQL result schema.
    
    Args:
        result (dict): Dictionary containing the result data matching the schema
    """
    topic = 'sql_result'
    schema = "sql_result.avsc"

    # Read schema file
    path = os.path.realpath(os.path.dirname(__file__))
    with open(f"{path}/{schema}") as f:
        schema_str = f.read()

    # Configure Schema Registry client
    sr_conf = {
        'url': os.getenv("SCHEMA_REGISTRY_ENDPOINT"),
        'basic.auth.user.info': f'{os.getenv("SCHEMA_REGISTRY_API_KEY")}:{os.getenv("SCHEMA_REGISTRY_API_SECRET")}'
    }
    schema_registry_client = SchemaRegistryClient(sr_conf)

    # Create serializers
    avro_serializer = AvroSerializer(
        schema_registry_client,
        schema_str,
        result_to_dict
    )
    string_serializer = StringSerializer('utf_8')

    # Configure Kafka producer
    producer_conf = {
        'bootstrap.servers': os.getenv("BOOTSTRAP_ENDPOINT"),
        'sasl.mechanisms': 'PLAIN',
        'security.protocol': 'SASL_SSL',
        'sasl.username': os.getenv("KAFKA_API_KEY"),
        'sasl.password': os.getenv("KAFKA_API_SECRET"),
    }
    producer = Producer(producer_conf)

    try:
        # Create result object
        result_obj = HRResultProducer(
            message_id=result.get('message_id'),
            employee_id=result.get('employee_id'),
            timestamp=result.get('timestamp'),
            query=result.get('query'),
            status=result.get('status'),
            sql_result=result.get('sql_result'),
            source=result.get('source'),
            sessionId=result.get('sessionId')
        )

        # Produce message
        producer.produce(
            topic=topic,
            key=string_serializer(str(uuid4())),
            value=avro_serializer(result_obj, SerializationContext(topic, MessageField.VALUE)),
            on_delivery=delivery_report
        )

        # Flush to ensure delivery
        producer.flush()
        print(f"Successfully produced result for message_id: {result.get('message_id')}")

    except Exception as e:
        print(f"Error producing message: {str(e)}")
        raise

