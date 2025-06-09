import json
from pymongo import MongoClient
from avro_kafka_producer import produce_context_result,build_summary_from_doc
import os 

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/"
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
VECTOR_FIELD = "contentEmbedding"
K = 1


def lambda_handler(event, context):

    for events in event:
        search_event = events['payload']['value']
        query = search_event.get('query')
        message = search_event.get('message')
        employee_id = search_event.get('employee_id')
        message_id = search_event.get('message_id', 'unknown')
        user_email = search_event.get('user_email', 'unknown')
        session_id = search_event.get('session_id')
        timestamp = search_event.get('timestamp')
        input_vector = search_event['query_embedding']
        if not input_vector or not isinstance(input_vector, list):
            return {"statusCode": 400, "body": "Invalid or missing 'query_vector' in request."}

        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        collection = client[DB_NAME][COLLECTION_NAME]

        # Perform vector search
        pipeline = [
            {
                "$vectorSearch": {
                    "queryVector": input_vector,
                    "path": VECTOR_FIELD,
                    "numCandidates": 100,
                    "limit": K,
                    "index": "knowledge_index"
                }
            },
            {"$project": {"_id": 0, "score": {"$meta": "vectorSearchScore"}, "doc": "$$ROOT"}}
        ]

        results = list(collection.aggregate(pipeline))
        summary_parts = [build_summary_from_doc(res["doc"]) for res in results]
        search_result_summary = "\n-----\n".join(summary_parts)

        produce_context_result(
            query=query,
            message=message,
            message_id=message_id,
            employee_id=employee_id,
            user_email=user_email,
            session_id=session_id,
            search_result_summary=search_result_summary
        )
        print("Results", results)
    return {
        'statusCode': 200,
        'body': json.dumps('Messages sent to Kafka!')
    }
