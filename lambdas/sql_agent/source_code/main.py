from agent import HRSQLAgent, setup_hr_database
from avro_kafka_producer import HRResultProducer , produce
import os
import logging
from dotenv import load_dotenv
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('hr_agent_main')

# Global variables for Lambda container reuse
_agent = None
_producer = None

def initialize_resources():
    """Initialize resources that can be reused across Lambda invocations."""
    global _agent, _producer
    
    if _agent is None:
        # Load environment variables
        load_dotenv()    
        
        # Get AWS credentials
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        
        # Set up the HR database and agent
        logger.info("Setting up HR database and agent...")
        try:
            db_path = setup_hr_database()
            _agent = HRSQLAgent(
                db_path=db_path,
                aws_region=aws_region
            )
            logger.info("HR SQL Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize HR SQL Agent: {str(e)}")
            raise
        
        # Initialize Kafka components
        _producer = HRResultProducer()
        
        logger.info("Resources initialized successfully")

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    
    Args:
        event (dict): The event data from AWS Lambda
        context (LambdaContext): The runtime information from AWS Lambda
        
    Returns:
        dict: Response containing the processing result
    """
    try:
        # Initialize resources if not already done
        initialize_resources()
        # Extract message from the event
        # Assuming the event contains the Kafka message in the body
        # message = json.loads(event.get('body', '{}'))
        message = event[0]['payload']['value']
        print(message)
        if not message:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No message provided in event'})
            }
        
        # Extract query and employee ID
        query = message.get('query')
        employee_id = message.get('employee_id')
        message_id = message.get('message_id', 'unknown')
        source = message.get('source', 'unknown')
        session_id = message.get('session_id')
        
        logger.info(f"Processing query: '{query}' (ID: {message_id})")
        
        # Process query with the agent
        result = _agent.run_hr_query(query, requesting_employee_id=employee_id)

        print(result)
        sql_result={}
        print("\nANSWER:")
        if 'error' in result.get('data', {}).get('raw_output', ''):
            print(f"Error: {result['data']['raw_output']}")
            sql_result['status'] = 'error'
        else:
            # Format the raw output for better readability
            
            raw_output = result['data']
            if raw_output and "Agent stopped" not in raw_output:
                print(raw_output)
            else:
                print("Retrieved employee information directly from database.")
            sql_result['status'] = 'success'
            sql_result['sql_result'] = str(raw_output)

        # Show the extracted context that would be used for policy lookup
        
        # Add message metadata to result
        
        sql_result['message_id'] = message_id
        sql_result['employee_id'] = employee_id
        sql_result['timestamp'] = str(message.get('timestamp'))
        sql_result['query'] = query
        sql_result['source'] = source
        if session_id:
            sql_result['session_id'] = session_id
        
        #Send result to Kafka
        
        produce(sql_result)
        logger.info(f"Result sent for message ID: {raw_output}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

if __name__ == "__main__":
    lambda_handler([{'payload': {'value': {'query': 'What is my department located?', 'employee_id': 'E001', 'message_id': 'test-123', 'source': 'test', 'session_id': 'test-session'}}}], {})