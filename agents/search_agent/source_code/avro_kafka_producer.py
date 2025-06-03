import os
from uuid import uuid4
from datetime import datetime
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

class ContextResult:
    """
    Context search result for employee support queries.

    Args:
        message_id (str): Unique identifier for the query message
        employee_id (str): ID of the employee
        timestamp (int): Timestamp in epoch millis
        query (str): Original query string
        user_email (str): Email ID of the employee
        message (str): Original full message
        session_id (str): Session ID of the conversation
        search_result_summary (str): Search result summary extracted from vector DB
    """
    def __init__(self, message_id, employee_id, timestamp, query, user_email,
                 message, session_id, search_result_summary=None):
        self.message_id = message_id
        self.employee_id = employee_id
        self.timestamp = timestamp
        self.query = query
        self.user_email = user_email
        self.message = message
        self.session_id = session_id
        self.search_result_summary = search_result_summary

def context_result_to_dict(result, ctx):
    return {
        "message_id": result.message_id,
        "employee_id": result.employee_id,
        "timestamp": result.timestamp,
        "query": result.query,
        "user_email": result.user_email,
        "message": result.message,
        "session_id": result.session_id,
        "search_result_summary": result.search_result_summary
    }

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed for message {msg.key()}: {err}")
    else:
        print(f"Message {msg.key()} produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def build_summary_from_doc(doc):
    return (
        f"Policy ID: {doc.get('policyId')}\n"
        f"Title: {doc.get('title')}\n"
        f"Region: {doc.get('region')}\n"
        f"Category: {doc.get('category')}\n"
        f"Last Updated: {doc.get('lastUpdated')}\n\n"
        f"{doc.get('content')}"
    )

def produce_context_result(search_result_summary, query, message, message_id, employee_id, user_email, session_id):
    topic = os.getenv("search_agent_result_topic")
    schema_file = "search_agent_response.avsc"

    # Load Avro schema
    schema_path = os.path.join(os.path.dirname(__file__), schema_file)
    with open(schema_path) as f:
        schema_str = f.read()

    # Schema Registry setup
    sr_conf = {
        'url': os.getenv("SCHEMA_REGISTRY_ENDPOINT"),
        'basic.auth.user.info': f"{os.getenv('SCHEMA_REGISTRY_API_KEY')}:{os.getenv('SCHEMA_REGISTRY_API_SECRET')}"
    }
    schema_registry_client = SchemaRegistryClient(sr_conf)

    avro_serializer = AvroSerializer(
        schema_registry_client,
        schema_str,
        context_result_to_dict
    )
    string_serializer = StringSerializer('utf_8')

    producer_conf = {
        'bootstrap.servers': os.getenv("BOOTSTRAP_ENDPOINT"),
        'sasl.mechanisms': 'PLAIN',
        'security.protocol': 'SASL_SSL',
        'sasl.username': os.getenv("KAFKA_API_KEY"),
        'sasl.password': os.getenv("KAFKA_API_SECRET"),
    }
    producer = Producer(producer_conf)

    try:
        result_obj = ContextResult(
            message_id=message_id,
            employee_id=employee_id,
            timestamp=int(datetime.utcnow().timestamp() * 1000),
            query=query,
            user_email=user_email,
            message=message,
            session_id=session_id,
            search_result_summary=search_result_summary
        )

        # Produce
        producer.produce(
            topic=topic,
            key=string_serializer(str(uuid4())),
            value=avro_serializer(result_obj, SerializationContext(topic, MessageField.VALUE)),
            on_delivery=delivery_report
        )

        producer.flush()
        print(f"Sent context result for message_id: {message_id}")

    except Exception as e:
        print(f"Error producing message: {e}")
        raise
