from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models import BedrockChat
import os
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional, Union
import json
import re
import boto3
from botocore.exceptions import ClientError, CredentialRetrievalError
from botocore.config import Config

class HRSQLAgent:
    """A SQL agent specialized for HR data retrieval only."""
    
    def __init__(self, db_path: str,  aws_region: Optional[str] = None):
        """
        Initialize the HR SQL Agent.
        
        Args:
            db_path: Path to the SQLite database file
            aws_region: AWS region (optional if set in environment)
        """
        # Load environment variables
        load_dotenv()
        
        # Set AWS credentials
        self.aws_region = aws_region or os.getenv("AWS_REGION", "us-east-1")
        
        # Create database URI
        db_uri = f"sqlite:///{db_path}"
        
        # Connect to the database
        self.db = SQLDatabase.from_uri(db_uri)
        
        try:
            # Create AWS session with credentials
            session_kwargs = {
                'region_name': self.aws_region
            }
            
            
            session = boto3.Session(**session_kwargs)
            
            # Initialize AWS Bedrock client using the session
            self.bedrock_client = session.client(
                service_name='bedrock-runtime',
                region_name=self.aws_region,
                config=Config(
                    retries=dict(
                        max_attempts=3
                    )
                )
            )
            
            # Initialize the language model with Claude Sonnet
            self.llm = BedrockChat(
                client=self.bedrock_client,
                model_id="anthropic.claude-3-sonnet-20240229-v1:0",
                model_kwargs={
                    "temperature": 0,
                    "max_tokens": 4096,
                    "top_p": 1,
                    "stop_sequences": ["\n\nHuman:"]
                }
            )
            
            # Create SQL toolkit and agent
            self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            
            # Initialize the SQL agent
            self.agent = create_sql_agent(
                llm=self.llm,
                toolkit=self.toolkit,
                verbose=True,
                handle_parsing_errors=True
            )
            
        except CredentialRetrievalError as e:
            raise ValueError(
                "Failed to retrieve AWS credentials. Please verify your AWS credentials are correct "
                "and have the necessary permissions to access AWS Bedrock."
            ) from e
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            if error_code == 'UnrecognizedClientException':
                raise ValueError(
                    "Invalid AWS credentials. This could be due to:\n"
                    "1. Missing or invalid session token for temporary credentials\n"
                    "2. Expired credentials\n"
                    "3. Incorrect access key or secret key or insufficient permissions\n"
                    "Please verify your AWS credentials and ensure they are current."
                ) from e
            else:
                raise ValueError(
                    f"AWS Authentication Error: {error_code} - {error_message}\n"
                    "Please verify your AWS credentials and ensure they have the necessary permissions "
                    "to access AWS Bedrock."
                ) from e
    
    def get_employee_context(self, employee_id: str) -> Dict[str, Any]:
        """
        Retrieve employee context data for policy lookup.
        
        Args:
            employee_id: The employee's unique identifier
            
        Returns:
            Dictionary containing the employee context
        """
        query = f"""
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name as full_name,
            e.job_title,
            e.department,
            e.email,
            e.phone,
            e.hire_date,
            e.tenure,
            e.salary,
            e.manager_id,
            m.first_name || ' ' || m.last_name as manager_name,
            e.country,
            e.region,
            e.employee_type
        FROM employees e
        LEFT JOIN employees m ON e.manager_id = m.employee_id
        WHERE e.employee_id = '{employee_id}'
        """
        try:
            result = self.agent.invoke({"input": query})
            output = result.get("output", "")
            
            # Initialize employee context with basic info
            employee_context = {
                "employee_id": employee_id,
                "raw_output": output
            }
            
            # Parse the structured data from the output
            if output:
                # Split the output into lines and process each line
                for line in output.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        clean_key = key.strip().lower().replace(' ', '_')
                        clean_value = value.strip()
                        employee_context[clean_key] = clean_value
            
            # Get department information if available
            if "department" in employee_context:
                department_name = employee_context["department"]
                try:
                    department_context = self.get_department_context(department_name)
                    if department_context and "departmentContext" in department_context:
                        employee_context["department_data"] = department_context["departmentContext"]
                except Exception:
                    # If there's an error getting department data, just continue without it
                    pass
            
            return employee_context
            
        except Exception as e:
            return {
                "employee_id": employee_id,
                "error": str(e),
                "raw_output": "Failed to retrieve employee information"
            }
    
    def get_department_context(self, department_name: str) -> Dict[str, Any]:
        """
        Retrieve department context for policy lookup.
        
        Args:
            department_name: Name of the department
            
        Returns:
            Dictionary containing the department context
        """
        query = f"""
        SELECT 
            d.department_id,
            d.department_name,
            d.location,
            d.head_id,
            e.first_name || ' ' || e.last_name as head_name,
            COUNT(e2.employee_id) as employee_count
        FROM departments d
        LEFT JOIN employees e ON d.head_id = e.employee_id
        LEFT JOIN employees e2 ON e2.department = d.department_name
        WHERE d.department_name = '{department_name}'
        GROUP BY d.department_id, d.department_name, d.location, d.head_id, e.first_name, e.last_name
        """
        try:
            result = self.agent.invoke({"input": query})
            output = result.get("output", "")
            
            # Initialize department context
            department_context = {
                "department_name": department_name,
                "raw_output": output
            }
            
            # Parse the structured data from the output
            if output:
                # Split the output into lines and process each line
                for line in output.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        clean_key = key.strip().lower().replace(' ', '_')
                        clean_value = value.strip()
                        department_context[clean_key] = clean_value
            
            return {"departmentContext": department_context}
            
        except Exception as e:
            return {
                "department_name": department_name,
                "error": str(e),
                "raw_output": "Failed to retrieve department information"
            }
    
    def extract_query_entities(self, query: str) -> Dict[str, Any]:
        """
        Analyze a query and extract relevant entities (employee or department).
        
        Args:
            query: Natural language query
            
        Returns:
            Dictionary containing the entities extracted from the query
        """
        # Check for direct employee ID mentions (e.g., E001)
        employee_id_match = re.search(r'(?:E|emp)\d{3}', query, re.IGNORECASE)
        
        if employee_id_match:
            employee_id = employee_id_match.group(0).upper()
            if not employee_id.startswith('E'):
                employee_id = 'E' + employee_id[3:]
            return {"entity_type": "employee", "employee_id": employee_id}
        
        # Look for first-person references that suggest the employee is asking about themselves
        first_person_patterns = [r'\bmy\b', r'\bI\b', r'\bme\b', r'\bmine\b']
        for pattern in first_person_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return {"entity_type": "self_reference", "needs_employee_id": True}
        
        # Check for department mentions
        department_check_query = f"""
        The following is a user query: "{query}"
        If this query mentions a specific department, respond with ONLY the exact department name as found in your database.
        If it mentions an employee by name (not ID), respond with ONLY "EMPLOYEE_NAME: " followed by their full name.
        If neither, respond with ONLY "GENERAL".
        """
        
        entity_response = self.agent.run(department_check_query).strip()
        
        if entity_response.upper() == "GENERAL":
            return {"entity_type": "general"}
        
        elif entity_response.upper().startswith("EMPLOYEE_NAME:"):
            employee_name = entity_response[13:].strip()
            # Get employee ID for the named employee
            employee_id_query = f"""
            Find the employee_id for an employee named {employee_name}.
            Respond with ONLY the employee_id in the format E###.
            """
            employee_id = self.agent.run(employee_id_query).strip()
            if re.match(r'E\d{3}', employee_id):
                return {"entity_type": "employee", "employee_id": employee_id, "employee_name": employee_name}
            else:
                return {"entity_type": "employee_not_found", "employee_name": employee_name}
        
        else:
            # Assume entity_response contains a department name
            return {"entity_type": "department", "department_name": entity_response}
    
    def _generate_summary(self, query: str, context: Dict[str, Any]) -> str:
        """
        Generate a natural language summary of the query results.
        
        Args:
            query: The original query
            context: The context data retrieved from the database
            
        Returns:
            A natural language summary of the results
        """
        try:
            # Prepare the prompt for summary generation
            prompt = f"""
            Based on the following query and retrieved information, provide a clear and concise summary:
            
            Query: {query}
            
            Retrieved Information:
            {json.dumps(context, indent=2)}
            
            Please provide a natural language summary that:
            1. Directly answers the query
            2. Includes relevant details from the retrieved information
            3. Is clear and easy to understand
            4. Maintains a professional tone
            5. If the information is not available, clearly state that
            
            Summary:
            """
            
            # Get summary from the model
            result = self.llm.invoke(prompt)
            return result.content.strip()
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def run_hr_query(self, query: str, requesting_employee_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process an HR query and return both the query result and relevant context.
        
        Args:
            query: Natural language query about HR data
            requesting_employee_id: ID of the employee making the request (for self-referential queries)
            
        Returns:
            Dictionary containing query results and context for policy lookup
        """
        try:
            # Add requesting employee ID to query for context
            if requesting_employee_id:
                query = f"{query} (Requested by employee: {requesting_employee_id})"
            print(query)
            # Extract entities from the query
            entity_info = self.extract_query_entities(query)
            
            # Initialize response structure
            response_data = {
                "raw_output": "",
                "context": {}
            }
            
            # Handle different entity types
            if entity_info.get("entity_type") == "employee":
                employee_id = entity_info.get("employee_id")
                employee_context = self.get_employee_context(employee_id)
                response_data["context"]["employeeContext"] = employee_context
                response_data["raw_output"] = f"Retrieved information for employee {employee_id}"
                
            elif entity_info.get("entity_type") == "department":
                department_name = entity_info.get("department_name")
                # For department queries, get both department and employee information
                department_context = self.get_department_context(department_name)
                response_data["context"]["departmentContext"] = department_context.get("departmentContext", {})
                
                # Get all employees in the department
                employee_query = f"""
                SELECT 
                    e.employee_id,
                    e.first_name || ' ' || e.last_name as full_name,
                    e.job_title,
                    e.email,
                    e.phone,
                    e.hire_date,
                    e.tenure,
                    e.salary,
                    e.manager_id,
                    m.first_name || ' ' || m.last_name as manager_name
                FROM employees e
                LEFT JOIN employees m ON e.manager_id = m.employee_id
                WHERE e.department = '{department_name}'
                ORDER BY e.employee_id
                """
                try:
                    result = self.agent.invoke({"input": employee_query})
                    if result and result.get("output"):
                        response_data["context"]["departmentEmployees"] = {
                            "raw_output": result.get("output", ""),
                            "employee_count": len(result.get("output", "").strip().split('\n'))
                        }
                except Exception:
                    pass
                
                response_data["raw_output"] = f"Retrieved information for department {department_name}"
                
            elif entity_info.get("entity_type") == "self_reference" and requesting_employee_id:
                employee_context = self.get_employee_context(requesting_employee_id)
                response_data["context"]["employeeContext"] = employee_context
                response_data["raw_output"] = f"Retrieved information for requesting employee {requesting_employee_id}"
                
            elif entity_info.get("entity_type") == "general":
                # For general queries, try to get relevant information
                if "how many" in query.lower() and "department" in query.lower():
                    # Extract department name from query
                    dept_match = re.search(r'in the (\w+) department', query.lower())
                    if dept_match:
                        dept_name = dept_match.group(1).title()
                        dept_context = self.get_department_context(dept_name)
                        response_data["context"]["departmentContext"] = dept_context.get("departmentContext", {})
                        
                        # Get employee count
                        count_query = f"""
                        SELECT COUNT(*) as employee_count
                        FROM employees
                        WHERE department = '{dept_name}'
                        """
                        try:
                            result = self.agent.invoke({"input": count_query})
                            if result and result.get("output"):
                                response_data["context"]["employeeCount"] = {
                                    "department": dept_name,
                                    "count": result.get("output", "").strip()
                                }
                        except Exception:
                            pass
                
                response_data["raw_output"] = "Processed general query"
                
            else:
                response_data["raw_output"] = "No specific entity found in query"
            
            # Generate a natural language summary of the results
            if response_data["context"]:
                summary = self._generate_summary(query, response_data["context"])
                response_data["summary"] = summary
            
            return self._standardize_response(response_data)
            
        except Exception as e:
            error_message = f"Error processing querys: {str(e)}"
            return self._standardize_response(
                {"raw_output": error_message, "context": {}},
                error=error_message
            )
    
    def _extract_structured_data(self, text: str) -> Dict[str, Any]:
        """
        Extract structured data from text output.
        
        Args:
            text: Text containing information
            
        Returns:
            Dictionary of structured data
        """
        structured_data = {}
        
        # Extract key-value pairs using regex
        # Look for patterns like "Key: Value" or "Key - Value"
        patterns = [
            r'([A-Za-z\s]+):\s*(.*?)(?=\n[A-Za-z\s]+:|$)',
            r'([A-Za-z\s]+)\s*-\s*(.*?)(?=\n[A-Za-z\s]+\s*-|$)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for key, value in matches:
                clean_key = key.strip().lower().replace(' ', '_')
                clean_value = value.strip()
                structured_data[clean_key] = clean_value
        
        return structured_data

    def _standardize_response(self, data: Dict[str, Any], error: Optional[str] = None) -> Dict[str, Any]:
        """
        Standardize the response format.
        
        Args:
            data: The data to include in the response
            error: Optional error message
            
        Returns:
            Dictionary with standardized response format
        """
        return {
            "status": "error" if error else "success",
            "data": {
                "raw_output": error if error else data.get("raw_output", ""),
                "context": data.get("context", {}),
                "summary": data.get("summary", "No summary available")
            }
        }


# Example setup code (sqlite database creation) - unchanged from original
def setup_hr_database(db_path="/tmp/hr_database.db"):
    """Create a sample HR database for testing."""
    import sqlite3
    import os
    
    # Delete the database file if it exists to ensure we create a fresh one with the new schema
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create employees table with the new columns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        hire_date TEXT,
        job_title TEXT,
        department TEXT,
        manager_id TEXT,
        salary REAL,
        tenure TEXT,
        country TEXT,
        region TEXT,
        employee_type TEXT
    )
    ''')
    
    # Create departments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        department_id TEXT PRIMARY KEY,
        department_name TEXT,
        location TEXT,
        head_id TEXT
    )
    ''')
    
    # Insert sample employees with country, region, and employee type
    sample_employees = [
        ("E001", "John", "Smith", "john.smith@company.com", "555-1234", "2020-06-15", "Senior Software Engineer", "Engineering", "E101", 110000.00, "2.5 years", "United States", "North America", "Full Time"),
        ("E002", "Emma", "Johnson", "emma.johnson@company.com", "555-2345", "2021-02-10", "HR Specialist", "Human Resources", "E102", 75000.00, "2 years", "Europe", "Europe", "Full Time"),
        ("E003", "Michael", "Williams", "michael.williams@company.com", "555-3456", "2022-01-05", "Financial Analyst", "Finance", "E103", 85000.00, "1 year", "United States", "North America", "Contract"),
        ("E004", "Rajesh", "Kumar", "rajesh.kumar@company.com", "555-4567", "2019-11-20", "Product Manager", "Product", "E104", 120000.00, "3 years", "Asia/Pacific", "India", "Full Time"),
        ("E005", "Robert", "Davis", "robert.davis@company.com", "555-5678", "2020-03-15", "Senior Software Engineer", "Engineering", "E101", 115000.00, "3 years", "Asia/Pacific", "India", "Full Time"),
        ("E101", "David", "Miller", "david.miller@company.com", "555-6789", "2018-07-01", "Engineering Director", "Engineering", "E201", 160000.00, "4.5 years", "United States", "North America", "Full Time"),
        ("E102", "Jennifer", "Wilson", "jennifer.wilson@company.com", "555-7890", "2017-09-12", "HR Director", "Human Resources", "E201", 155000.00, "5 years", "United States", "North America", "Full Time"),
        ("E103", "James", "Taylor", "james.taylor@company.com", "555-8901", "2018-04-30", "Finance Director", "Finance", "E201", 165000.00, "4.5 years", "Europe", "Europe", "Full Time"),
        ("E104", "Vaishnavi", "Deshpande", "vaishnavi.deshpande@company.com", "555-9012", "2019-03-22", "Product Director", "Product", "E201", 170000.00, "4 years", "Asia/Pacific", "India", "Full Time"),
        ("E201", "Richard", "Thomas", "richard.thomas@company.com", "555-0123", "2015-10-18", "COO", "Executive", "E301", 250000.00, "8 years", "United States", "Latin America", "Full Time"),
        ("E301", "Elizabeth", "Jackson", "elizabeth.jackson@company.com", "555-1122", "2010-01-05", "CEO", "Executive", None, 350000.00, "13 years", "United States", "Latin America", "Full Time")
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO employees 
    (employee_id, first_name, last_name, email, phone, hire_date, job_title, department, manager_id, salary, tenure, country, region, employee_type) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_employees)
    
    # Insert sample departments
    sample_departments = [
        ("D001", "Engineering", "Building A, Floor 2", "E101"),
        ("D002", "Human Resources", "Building B, Floor 1", "E102"),
        ("D003", "Finance", "Building A, Floor 3", "E103"),
        ("D004", "Product", "Building B, Floor 2", "E104"),
        ("D005", "Executive", "Building A, Floor 4", "E301")
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO departments 
    (department_id, department_name, location, head_id) 
    VALUES (?, ?, ?, ?)
    ''', sample_departments)
    
    conn.commit()
    conn.close()
    
    print(f"HR database created at {db_path}")
    return os.path.abspath(db_path)

