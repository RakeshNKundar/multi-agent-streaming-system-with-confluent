from agent import HRSQLAgent, setup_hr_database
import os
from dotenv import load_dotenv
import json

def main():
    # Load environment variables
    load_dotenv()

    # Get AWS credentials
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.getenv("AWS_SESSION_TOKEN")  # Optional for temporary credentials
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    # Prompt for credentials if not found in environment
    if not aws_access_key_id:
        print("AWS Access Key ID not found in .env file")
        aws_access_key_id = input("Enter your AWS Access Key ID: ").strip()
        if not aws_access_key_id:
            print("No AWS Access Key ID provided. Exiting.")
            return

    if not aws_secret_access_key:
        print("AWS Secret Access Key not found in .env file")
        aws_secret_access_key = input("Enter your AWS Secret Access Key: ").strip()
        if not aws_secret_access_key:
            print("No AWS Secret Access Key provided. Exiting.")
            return

    # Setup the database
    print("Setting up the HR database...")
    db_path = setup_hr_database()

    # Initialize the agent
    print("Initializing the HR SQL agent...")
    try:
        agent = HRSQLAgent(
            db_path=db_path,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,  # Optional
            aws_region=aws_region
        )

        print("\nHR SQL Agent is ready!")
        print("Simply ask any HR-related question. Type 'exit' to quit.")
        print("\nExample questions:")
        print("- Tell me about employee E001")
        print("- What leave policies apply to John Smith?")
        print("- How many employees are in the Engineering department?")

        while True:
            # Get natural language query
            query = input("\n> ").strip()

            if query.lower() in ['exit', 'quit', 'bye']:
                print("\nGoodbye!")
                break

            try:
                # Process the query 
                result = agent.run_hr_query(query)
                print(result)
                # Display the answer
                print("\nANSWER:")
                if 'error' in result.get('data', {}).get('raw_output', ''):
                    print(f"Error: {result['data']['raw_output']}")
                else:
                    # Format the raw output for better readability
                    raw_output = result['data']
                    if raw_output and "Agent stopped" not in raw_output:
                        print(raw_output)
                    else:
                        print("Retrieved employee information directly from database.")

                # Show the extracted context that would be used for policy lookup
                # print(raw_output)
             

            except Exception as e:
                print(f"\nError processing query: {str(e)}")

            print("\n" + "-" * 50)

    except Exception as e:
        print(f"\nError initializing agent: {str(e)}")
        return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")