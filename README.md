# 🧠 Multi-Agent Workplace Engagement System 

Welcome to the workshop on building a **Multi-Agent System for Workplace Engagement** using **Apache Kafka**, **Apache Flink**, and **Amazon Bedrock**. In this workshop, you'll learn to orchestrate multiple intelligent agents that collaborate to handle real-world workplace queries like scheduling meetings, retrieving company data, or answering knowledge base questions.

---

## 📘 Overview

This project demonstrates how to build an LLM-powered multi-agent system for workplace engagement. It combines real-time streaming (Flink), event-driven architecture (Kafka), vector search, and Generative AI (Amazon Bedrock) to enable interactive workflows such as:

- Querying company/employee data from SQL databases
- Searching context from internal documents using embeddings
- Executing tasks like scheduling and sending emails using automation agents

Participants will walk away with hands-on experience building a scalable and fault-tolerant GenAI application with real-time agent coordination.

---

## 🗺️ Architecture

![Architecture Diagram](assets/img/architecture.png)

This architecture includes:
- **Orchestrator Agent**: Uses Bedrock LLM to decide which agents to invoke based on incoming user queries.
- **Query Agent**: Fetches data from relational databases (SQL).
- **Research Agent**: Searches company documents using vector search and embeddings.
- **Task Agent**: Performs action-oriented tasks like scheduling meetings , reminders and events via sns.
- **Final Response Builder**: Joins all agent results and converts structured data into a final natural language response.

---

## ⚙️ Technologies Used

- **Apache Kafka** – Stream backbone for agent communication
- **Apache Flink** – Real-time stream processing & orchestrator logic
- **Amazon Bedrock** – Foundation model for prompt routing and response generation
- **AWS Lambda** – Task & query handler functions
- **PostgreSQL** – SQL data store
- **Mongo Vector DB** – Semantic search engine
- **LangChain / Custom Agents** – Agent interfaces

---


## Requirements
- **Access:** 
    - *Confluent Cloud Account Access* - https://cnfl.io/getstarted

    - *MongoDB Atlas Account Access*
      - MongoDB provides a free-tier (M0) cluster, ideal for development and workshops. We’ll be using this during today’s session.
      - You can proceed with your existing MongoDB Atlas account if you already have one.
      - If not, you can sign up for a free account here: https://www.mongodb.com/cloud/atlas/register. 
      

    - *AWS Account Access*
      - Will be shared with you by your workshop co-ordinator.

- **Local Software Requirements:** 
    - [Python3 > 3.9](https://www.python.org/downloads/)
    - [Terraform CLI](https://developer.hashicorp.com/terraform/install)
    - [Confluent Cloud CLI](https://docs.confluent.io/confluent-cli/current/install.html)
    - [MongoDB Database Tools](https://www.mongodb.com/docs/database-tools/installation/)
    
    ```bash
    chmod +x ./setup/install_dependencies.sh
    ./setup/install_dependencies.sh
    ```

- **Sign up for Confluent Cloud**
    - Navigate to [Confluent Cloud Sign Up](https://cnfl.io/getstarted).
    - Sign up with any of the desired identity providers or your email ID.
        <p><img src="assets/img/signup.png" alt="sign-up" width="300" /></p>
    - Finish creating your account by filling in a couple of details.
        <p><img src="assets/img/finish.png" alt="finish" width="300" /></p>
    - Click on skip for adding your teammates for now. Feel free to add your teammates at a later point in time.
        <p><img src="assets/img/teammates.png" alt="finish" width="300" /></p>
    - Answer a couple of questions, and you are set to create your first cluster!
        <p><img src="assets/img/questions.png" alt="questions" width="300" /></p>
    - Click on "Next" to create a cluster and enter promo code details.
        <p><img src="assets/img/cluster.png" alt="cluster" width="300" /></p>
    - Please click on the "click_here" link on the UI to enter a promo code.
        <p><img src="assets/img/paywall.png" alt="paywall" width="300" /></p>
    - Enter the promo code : CONFLUENTDEV1
        <p><img src="assets/img/promo.png" alt="promo" width="300" /></p>

---

## 🚀 Quick Start (TL;DR)

1. ### Clone the workshop Github Repo on your local
    ```bash
    git clone https://github.com/RakeshNKundar/multi-agent-streaming-system-with-confluent.git
    ```

2. ### Create a Confluent Cloud API Key
    Create Confluent Cloud API Key for your confluent cloud account with resource scope as Cloud resource management.
    - Go to https://confluent.cloud/settings/api-keys
    - Click on My Account (Make sure you have Organization Admin RBAC role)
    - Add API Key 
    - Cloud resource management 
    - Download API Key 

    <p><img src="assets/img/apikey.png" alt="nim" width="300" /></p>


3. ### Create a MongoDB Programmatic Access API Key
    Get the MongoDB Atlas Organization ID - https://cloud.mongodb.com/v2/
    - Click on the ORGANIZATON <br>
      <p><img src="assets/img/mongo_organization.png" alt="nim"" /></p> <br>
    - Click on the gear icon(⚙️) beside Organization Overview. <br>
      <p><img src="assets/img/mongo_organization_gear_icon.png" alt="nim" width="300" /></p> <br>
    - Copy the Organization ID. This is used by the terraform script to create a project and a mongodb free tier cluster. <br>
      <p><img src="assets/img/mongo_atlas_organization_id.png" alt="nim"/></p> <br>

    
    Create MongoDB Programmatic Access api key for your mongo account - https://www.mongodb.com/docs/atlas/configure-api-access-org/
    * In Atlas, go to the Organization Access Manager page.
    * Click the Applications tab
    * Choose API Keys and Click on Create API Key with Organization Owner Permissions
    * Save the API Key for further use.
      <p><img src="assets/img/apikeymongo.png" alt="nim" width="300" /></p>

4. ### Retrieve your AWS Access Keys from a Confluent-provided AWS account
    If an AWS account is being provided to you for this workshop, follow the below instructions. 
    * Navigate to https://catalog.us-east-1.prod.workshops.aws/event/dashboard
    * Sign in using the `Email One Time Password` option. 
    * Once logged in, input the Event access code that you were given for this workhop. If you do not have your event access code, please notify an event supporter to obtain an access code.
    ![alt text](assets/img/event_access_code.png)
    * Agree to the Terms and Conditions to continue
    * You'll arrive at the page where you can access your Confluent-provided AWS account. The first link will allow you to access the AWS console of your AWS account. Go ahead and click the link to open the AWS console in a new tab.

      ![alt text](assets/img/console.png)
    * The other link provides the necessary access keys and session token to deploy resources into your Confluent-provided AWS account using Terraform. Copy and paste these values in a .txt file. You will uses these values multiple times throughout the workshop.

      ![alt text](assets/img/get_keys.png)
      ![alt text](assets/img/ws_keys.png) <br>
<br> **⚠️ NOTE:** Please use **US-WEST-2** region for this workshop as some LLM models used in this workshop might not have the same functionalities in other regions.

4. ### [Alternative] Retrieve your AWS Access Keys from an AWS account you provide
    In the event an AWS account is not provided to you for this workshop, you can use your own AWS account. When doing so you can deploy the upcoming Terraform script using [IAM Access Keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) or the [AWS CLI Profile](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-options.html) (ex. `aws configure --profile <profilename>`). <br><br>
    **⚠️ NOTE:** Please use **US-WEST-2** region for this workshop as some LLM models used in this workshop might not have the same functionalities in other regions. 

   
5. ### Setup environment variables

1. Go to the AWS Console and navigate to the Amazon Bedrock service.
2. On the left hand panel, click on the `Model Access` option

    ![alt text](assets/img/model_access.png)
3. Click the `Modify Access` button

    ![alt text](assets/img/modify_access.png)
4. Enable the following models (it is strongly recommended to only enable these models or else enablement will stall and require AWS Support):
    - Titan Embeddings G1 - Text
    - Claude 3.5 Haiku
  
    It should only take 1-5 minutes for the models to enable. You will see the following when models are ready.
    ![alt text](assets/img/model_active.png)
    ![alt text](assets/img/model_active_2.png) 

  * Navigate to <b>setup/init.sh</b> and edit the following:

    ```bash
    # setup/init.sh

    export TF_VAR_cc_cloud_api_key="<Confluent Cloud API Key>"
    export TF_VAR_cc_cloud_api_secret="<Confluent Cloud API Secret>"
    export TF_VAR_mongodbatlas_public_key="<MongoDB Public API Key>"
    export TF_VAR_mongodbatlas_private_key="<MongoDB Private API Key>"
    export AWS_DEFAULT_REGION="us-west-2" #If using a Confluent-provided AWS account, make sure this region matches the region found in the above steps (most likely it will be us-west-2)
    export AWS_ACCESS_KEY_ID="<AWS Access Key ID"
    export AWS_SECRET_ACCESS_KEY="<AWS Access Key Secret>"
    export AWS_SESSION_TOKEN="<AWS Session Token>" #Only necessary if you are using a Confluent-provided AWS account or using the temporary credentials from your personal AWS account.
    ```
  * After Setting the variables, run:

    ```bash
    chmod +x ./setup/init.sh
    ./setup/init.sh
    ```
    **⚠️ NOTE:** Terraform would take around 5 minutes to provision the infrastructure.
  

## Task 01 – Orchestrator Agent (LLM-based Decision Making)
In Confluent Cloud, a connection for Apache Flink® represents an external service that your Flink statements can interact with. These connections let you access systems such as databases, APIs, and other services directly from Flink SQL.

In our use case, we have set up connections to:

Claude for text generation: `bedrock-text-connection`

Embed-Titan for embeddings: `bedrock-embed-connection`

MongoDB for text and vector search: `mongodb-search-connection`

1. In the navigation menu, click Environments, and click the tile for the environment where you’re using Flink SQL.
  - In the navigation menu, click `Integrations`.
  - Click `Connections`.

The available connections are listed.
![alt text](assets/img/connections.png)

2. Navigate to Flink with Confluent Cloud and open your SQL workspace. 

    ![alt text](assets/img/flink_nav.png)

3. Run following queries within the SQL workspace you've opened up:

    ```sql
   CREATE MODEL BedrockGeneralModel INPUT (text STRING) OUTPUT (response STRING) COMMENT 'General model with no system prompt.'
   WITH
    (
        'task' = 'text_generation',
        'provider' = 'bedrock',
        'bedrock.PARAMS.max_tokens' = '200000',
        'bedrock.PARAMS.temperature' = '0.1',
        'bedrock.connection' = 'bedrock-text-connection'
    );
    ```

    ```sql
    CREATE TABLE `orchestrator_metadata` AS 
    SELECT 
        JSON_VALUE(response, '$.mongo_agent') AS mongo_agent,
        JSON_VALUE(response, '$.mongo_agent_metadata.query') AS mongo_agent_query,
        JSON_VALUE(response, '$.mongo_agent_metadata.user_email') AS mongo_agent_user_email,
        JSON_VALUE(response, '$.mongo_agent_metadata.employee_id') AS mongo_agent_employee_id,

        JSON_VALUE(response, '$.search_agent') AS search_agent,
        JSON_VALUE(response, '$.search_agent_metadata.query') AS search_agent_query,

        JSON_VALUE(response, '$.scheduler_agent') AS scheduler_agent,
        JSON_VALUE(response, '$.scheduler_agent_metadata.title') AS scheduler_title,
        JSON_VALUE(response, '$.scheduler_agent_metadata.description') AS scheduler_description,
        JSON_VALUE(response, '$.scheduler_agent_metadata.location') AS scheduler_location,
        JSON_VALUE(response, '$.scheduler_agent_metadata.start') AS scheduler_start,
        JSON_VALUE(response, '$.scheduler_agent_metadata.end') AS scheduler_end,
        JSON_QUERY(response, '$.scheduler_agent_metadata.attendees') AS scheduler_attendees,
        JSON_QUERY(response, '$.sequence') AS execution_sequence,`timestamp`,
    message_id,user_email,session_id,employee_id,message
    FROM 
        queries ,
    LATERAL TABLE(
        ML_PREDICT(
            'BedrockGeneralModel',(
                'You are a query router for a multi-agent workplace assistant.

    Given the user input, extract:

    1. Which agents are required
    2. A relevant fragment of the query for each agent — do not copy the full query unless necessary
    3. Agent-specific metadata in structured JSON
    4. An execution sequence, if applicable.

    Descriptions of agents:

    * sql\_agent: Handles employee- or department-level data queries from SQL using employee\_id or user\_email.
    * search\_agent: Retrieves top documents or policies using vector search based on semantic meaning.
    * scheduler\_agent: Schedules meetings or creates events using provided attendees, title, and time.

    Return the result in strict JSON using this structure:

    {
      "mongo_agent": true | false,
      "mongo_agent_metadata": {
        "query": "<original message from user>",
        "user_email": "<original user_email>",
        "employee_id": "<original employee_id>"
      },

      "search_agent": true | false,
      "search_agent_metadata": {
        "query": "<original message from user>"
      },

      "scheduler_agent": true | false,
      "scheduler_agent_metadata": {
        "title": "Meeting Title",
        "description": "Purpose of the meeting",
        "location": "Virtual",
        "start": "2025-05-06T15:00:00Z",
        "end": "2025-05-06T16:00:00Z",
        "attendees": ["<user_email or mentioned email>"]
      },

      "sequence": ["scheduler_agent", "search_agent", "mongo_agent"]
    }

      
    ' || '\n User prompt: ' ||
                '{
      message_id: ' || message_id || ','
      'employee_id: '||  employee_id || ','
      'user_email:' || user_email || ','
      'message:'|| message || '}'
            )
        )
    );
    ```


    13. Navigate to the Topics tab and find the `queries` topic. ![alt text](assets/img/queries_topic.png)

    14. Insert a sample query in the `queries` topic to test out our flink agent. 
        ```json
        {
          "message_id": "d7a97c0a-8e5b-4c65-90cb-7ea5934ae6d4",
          "employee_id": "E001",
          "user_email": "john.smith@company.com",
          "session_id": "sess-01",
          "message": "What is company's maternal leave policy? How much am I eligible for ?",
          "timestamp": 1746717000000
        }
        ```
        ![alt text](assets/img/produce.png)

15. Verify the data exists in the respective topics - **queries** and **orchestrator_metadata**. 

16. Click the record in the `orchestrator_metadata` topic to view the field values. Take a look at the agent flags and observe which are true for the input we have given. ![alt text](assets/img/message_check.png)

17. Try It Yourself ✏️:
    1. How would you change the prompt to include the SQL agent for being called?
    2. What metadata is required for the scheduler agent?
    3. Publish one more query containing “schedule a 1:1 with my manager <your email> ”, which agents will be invoked now?

## Task 02: Setup the Workflow distribution 
Now that the Orchestrator Agent is up and running, it's time to activate the specialized agents that perform actual tasks.🧩 Concept Recap
Each agent is an independent component in the system. Here's a quick breakdown:<br>
🗄 SQL Agent: Retrieves employee or department-level data using employee_id or user_email from a SQL database.<br>
🔎 Vector Search Agent: Uses semantic embeddings to retrieve contextually relevant documents from a MongoDB Vector Store.<br>
📅 Scheduler Agent: Automates meeting scheduling using structured metadata like title, time, and attendees.<br>

These agents listen on their respective Kafka input topics and output results to their own response topics (e.g., mongo_agent_response, search_agent_response, scheduler_result).

So we now create three router queries which routes the message to it's repective agent inputs. 


🔹 SQL Agent Routing 
Can you add the flag condition which will help us determine routing the request to mongo_agent_input ?
```sql
CREATE TABLE mongo_agent_input AS 
SELECT 
    CAST(message AS BYTES) AS key,
    mongo_agent_query as query, 
    message_id , 
    employee_id , 
    user_email , 
    message,
    session_id , 
    `timestamp`
FROM orchestrator_metadata 
where mongo_agent='true'; 
```

🔹 Search Agent (Vector)
Can you add the flag condition which will help us determine routing the request to search_agent_input ?

```sql
CREATE TABLE search_agent_input AS 
SELECT 
    CAST(message AS BYTES) AS key,
    search_agent_query as query, 
    message_id , 
    employee_id , 
    user_email , 
    message,
    session_id , 
    `timestamp`
FROM orchestrator_metadata 
where search_agent='true';
```

🔹 Scheduler Agent
Can you add the flag condition which will help us determine routing the request to scheduler_agent_input ?

```sql
CREATE TABLE scheduler_agent_input AS 
SELECT 
    CAST(message AS BYTES) AS key,
    scheduler_title as title, 
    scheduler_description as `description` ,
    scheduler_location as `location`,
    scheduler_start as `start`,
    scheduler_end as `end`,
    message_id , 
    employee_id , 
    user_email , 
    message,
    session_id , 
    `timestamp`,
    scheduler_attendees AS attendees
FROM orchestrator_metadata
WHERE scheduler_agent = 'true';
```
Verify the data in the respective topics - **mongo_agent_input**, **search_agent_input** and **scheduler_agent_input**.If any of these topics are empty, it likely means you haven’t triggered a user query that would activate the corresponding agent.

👉 Next Step:
Create a few test queries that would intentionally route to each of these agents. For example:

"How many employees are based in North America like me?" → SQL Agent
```json
{
  "message_id": "6f0e8192-9a14-49a7-9a22-6fc324d7d4co",
  "employee_id": "E001",
  "user_email": "john.smith@company.com",
  "session_id": "sess-01",
  "message": "How many employees are based in North America like me?",
  "timestamp": 1746717000000
}
```

"Can you help me understand hybrid Compensation & performance structure ?" → Search Agent
```json
{
  "message_id": "8f0e8192-9a14-49a7-9a22-6fc324d7d4ci",
  "employee_id": "E001",
  "user_email": "john.smith@company.com",
  "session_id": "sess-01",
  "message": "How do skill premiums work with the overall compensation structure?",
  "timestamp": 1746717000000
}
```

"Schedule a skip-level meeting with my manager next week" → Scheduler Agent
*Don’t forget to add your own email address so you receive the necessary notifications during the workshop.*
```json
{
  "message_id": "9f0e8192-9a14-49a7-9a22-6fc324d7ddghe",
  "employee_id": "E001",
  "user_email": "john.smith@company.com",
  "session_id": "sess-01",
  "message": "Schedule a skip-level meeting with my manager <your_email_id> next week",
  "timestamp": 1746717000000
}
```

This will help populate the input topics and allow you to test the complete agent workflow.

## Task 03 (Optional) – Integrating Email service with Scheduler agent using AWS SNS
You can send email notifications about the meeting from the scheduler agent using AWS SNS service. The Scheduler agent pushes events to the SNS service. You can create an E-mail subscription out of the SNS topic using your email address to receive email notification.

You need to create an email subscription on AWS SNS

  - Go to AWS SNS --> Click Subscription. 
  - Fill in the details like the SNS topic arn, 
      - Set Protocol = <b>Email</b>
      - Type in your email address
  
  <p><img src="assets/img/sns_subscription.png" alt="sign-up" /></p>

Create a subscription and verify your email address via an email sent by SNS service.

Once the email is verified you'll receive emails about the new events when a scheduler agent creates one.


## Task 04: Employee Context Retrieval via Mongo Search 
We now navigate to add context to our Research Agent using Amazon Bedrock embeddings.

1. Navigate to the Integrations tab within your environment and see another connections integration. This time with the the following: 
 - Name: `mongodb-search-connection` 
 - Endpoint: `mongodb+srv://multi-agent-workplace-s.<cluster_id>.mongodb.net/workplace_knowledgebase`. 
 - You can find the endpoint in terraform output section.The end result should look like this:
  ![alt text](assets/img/mongo_integration.png)


2. Navigate back to Flink and run the following queries.Create a Flink SQL table that maps to your employee_collection in MongoDB:
  ```sql
  CREATE TABLE mongodb_text_search (
  employee_id STRING,
  full_name STRING,
  first_name STRING,
  last_name STRING,
  email STRING,
  phone STRING,
  employment_type STRING,
  hire_date STRING,
  last_promotion_date STRING,
  next_eligible_promotion STRING,
  job_title STRING,
  job_level STRING,
  manager_id STRING,
  manager_name STRING,
  status STRING,
  tenure_years DOUBLE,
  
  -- Nested object: benefits
  benefits ROW<
    health_insurance STRING,
    retirement_plan STRING,
    paid_time_off INT
  >,

  -- Nested object: compensation
  compensation ROW<
    base_salary INT,
    currency STRING,
    bonus_eligibility BOOLEAN,
    stock_options INT
  >,

  -- Nested array: performance_reviews
  performance_reviews ARRAY<ROW<
    review_period STRING,
    rating STRING,
    reviewer STRING,
    comments STRING
  >>,

  -- Nested array: projects
  projects ARRAY<ROW<
    project_id STRING,
    project_name STRING,
    role STRING,
    start_date STRING,
    end_date STRING,
    status STRING
  >>,

  -- Array of strings: skills
  skills ARRAY<STRING>,

  -- Array of strings: tags
  tags ARRAY<STRING>,

  -- Nested object: work_location
  work_location ROW<
    office STRING,
    remote_status STRING,
    country STRING,
    region STRING,
    time_zone STRING
  >
  ) WITH (
  'connector' = 'mongodb',
  'mongodb.connection' = 'mongodb-search-connection',
  'mongodb.database' = 'workplace_knowledgebase',
  'mongodb.collection' = 'employee_collection',
  'mongodb.index' = 'employee_id_index'
  );
  ```

3. Get search results.Take incoming queries from mongo_agent_input and perform a MongoDB text search on the employee_collection. The results are written to the mongo_agent_response sink:

  ```sql
    INSERT INTO mongo_agent_response SELECT CAST(message_id AS BYTES) AS `key`,        
    message_id,
    employee_id,
    CAST(`timestamp` AS STRING) as `timestamp`,
    query,
    'success' AS status,
    CAST(search_results AS STRING) AS mongo_result,  
    'web',
    session_id AS sessionId
    FROM mongo_agent_input,
    LATERAL TABLE(
      TEXT_SEARCH_AGG(mongodb_text_search, DESCRIPTOR(employee_id), query, 1)
    );
  ```

4. Verify Results: Check the `mongo_response_topic` Kafka topic to confirm that embeddings are being generated and that MongoDB search results are correctly returned.

## Task 05: Knowledge Context Retrieval via Vector Search 
We now navigate to add context to our Research Agent using Amazon Bedrock embeddings.

1. Navigate to the Integrations tab within your environment and see another connections integration. This time with the the following: 
 - Name: `bedrock-embedding-connection` 
 - Endpoint: `https://bedrock-runtime.<your_current_region>.amazonaws.com/model/amazon.titan-embed-text-v1/invoke`. 
  
  ![alt text](assets/img/connections.png)


2. Navigate back to Flink and run the following queries:

    Create Bedrock Model in Flink SQL
    ```sql
    CREATE MODEL bedrock_embed
    INPUT (text STRING)
    OUTPUT (response ARRAY<FLOAT>)
    WITH (
      'bedrock.connection'='bedrock-embed-connection',
      'bedrock.input_format'='AMAZON-TITAN-EMBED',
      'provider'='bedrock',
      'task'='embedding'
    );
    ```

3. Embed User Queries
    ```sql
    CREATE TABLE search_embeddings AS 
    SELECT CAST(message_id AS BYTES) as key,`response` as query_embedding, query ,message_id ,employee_id ,user_email,message,session_id ,`timestamp` from `search_agent_input`, 
    LATERAL TABLE(
        ML_PREDICT(
            'bedrock_embed',(
                'queryFromEmployee: ' || query 
            )
        )
    );
    ```

4. Verify embeddings being generated in `search_embeddings` topics.

5. Connect to MongoDB Atlas Vector Store

    ```sql
    CREATE TABLE mongodb_vector (
      policyId STRING,
      title STRING,
      region STRING,
      category STRING,
      lastUpdated STRING, 
      content STRING , 
    contentEmbedding ARRAY<FLOAT>
    ) WITH (
    'connector' = 'mongodb',
    'mongodb.connection' = 'mongodb-search-connection',
    'mongodb.database' = 'workplace_knowledgebase',
    'mongodb.collection' = 'knowledge_collection',
    'mongodb.index' = 'knowledge_index',
    'mongodb.numcandidates' = '100'
    );
    ```
6. Perform Vector Search to Retrieve Results

  ```sql
  CREATE TABLE `search_agent_response` AS
  SELECT
    query,
    message_id,
    employee_id,
    user_email,
    message,
    session_id,
    `timestamp`,
    CONCAT(
      'policyId: ', IF(search_results[1].`policyId` IS NOT NULL, search_results[1].`policyId`, 'UNKNOWN'), '; ',
      'title: ', IF(search_results[1].`title` IS NOT NULL, search_results[1].`title`, 'No Title'), '; ',
      'region: ', IF(search_results[1].`region` IS NOT NULL, search_results[1].`region`, 'Unspecified'), '; ',
      'category: ', IF(search_results[1].`category` IS NOT NULL, search_results[1].`category`, 'General'), '; ',
      'lastUpdated: ', IF(search_results[1].`lastUpdated` IS NOT NULL, CAST(search_results[1].`lastUpdated` AS STRING), '1970-01-01'), '; ',
      'content: ', IF(search_results[1].`content` IS NOT NULL, search_results[1].`content`, 'No content available.')
    ) AS search_result_summary
  FROM search_embeddings,
    LATERAL TABLE(
      VECTOR_SEARCH_AGG(mongodb_vector, DESCRIPTOR(contentEmbedding), search_embeddings.query_embedding,1)
    ) AS T(search_results);
  ```

## Task 05: Integrate Agents with Lambda Sink Connector
This task helps you build a fully managed Lambda Kafka Sink Connector that routes your queries to all the lambda agents(SQL, Scheduler & Search).
Goal:
Stream mongo_agent_input , search_embeddings and scheduler_agent_input Kafka topics data directly to their respective AWS Lambda Agents.

Before creating the connector, make sure the Lambda is properly configured.
- Open the AWS Console.
- Search for and open your Lambda function (e.g., scheduler_agent).
- Validate the following environment variables to the function: 

```bash
BOOTSTRAP_ENDPOINT=<your-confluent-bootstrap-endpoint>
KAFKA_API_KEY=<your-kafka-api-key>
KAFKA_API_SECRET=<your-kafka-api-secret>
SCHEMA_REGISTRY_API_KEY=<your-schema-registry-api-key>
SCHEMA_REGISTRY_API_SECRET=<your-schema-registry-api-secret>
SCHEMA_REGISTRY_ENDPOINT=https://<your-schema-registry-endpoint>
TOPIC_NAME=mongo_agent_response
```
Step-by-step Setup:
1. Go to Confluent Cloud > Connectors.

2. Select AWS Lambda Sink Connector from the available connectors.
  ![alt text](assets/img/connector_select.png)

3. Select the `scheduler_agent_input` topic. Each time a record lands in this topic, the respective Lambda function will get triggered.

    ![alt text](assets/img/topic_select.png)

4. During the authentication part, be sure you point this connector input topics to the respective lambda functions/agents.
    1. Set `AWS Lambda function configuration mode` to `single`.
  
    ![alt text](assets/img/lambdas.png)

    2. In the  `AWS Lambda Function Name ` , enter `scheduler_agent_<your_unique_identifier>. You can get the name by logging into AWS lambda console.
    3. Use the `Access Keys` as the authentication method. 
    4. Run the following command in terminal to get aws access keys and secret. 
    ```shell
    cat terraform/service_principal_keys.txt
    ```
    Enter the access_key and secret in the AWS credentials section and Click on Continue.

7. Set the Input Kafka record value format to `AVRO`. Leave all other values as default/empty.
    ![alt text](assets/img/avro.png)

7. Lastly, provide your connector a name of `AgentSinkConnector`

8. Verify the responses in respective response topics.
[alt text](assets/img/verify_response.png)


## Task 06 – Final Agent Builder Join & response input Structuring
Now that all three agents (SQL, Search, Scheduler) have emitted results, we perform a final conditional join with the orchestrator metadata. This gives us a fully enriched context for each user query.

🔹 Step 1: Join All Agent Results
This query joins orchestrator_metadata with the three agent response topics conditionally, based on which agents were triggered (mongo_agent, search_agent, scheduler_agent).
```sql
CREATE TABLE enriched_query_with_agent_responses(
event_time TIMESTAMP(3),
  WATERMARK FOR event_time AS event_time - INTERVAL '1' SECOND)
 with('changelog.mode'='append')  AS
SELECT
  o.mongo_agent,
  o.mongo_agent_query,
  o.mongo_agent_user_email,
  o.mongo_agent_employee_id,
  o.search_agent,
  o.search_agent_query,
  o.scheduler_agent,
  o.scheduler_title,
  o.scheduler_description,
  o.scheduler_location,
  o.scheduler_start,
  o.scheduler_end,
  o.scheduler_attendees,
  o.execution_sequence,
  o.`$rowtime` as event_time,
  o.message_id,
  o.user_email,
  o.session_id,
  o.employee_id,
  o.message,
  CASE 
        WHEN o.mongo_agent = 'true' 
         AND s.`$rowtime` BETWEEN o.`$rowtime` - INTERVAL '5' MINUTE AND o.`$rowtime` + INTERVAL '2' HOUR 
        THEN s.mongo_result 
        ELSE NULL 
      END AS employee_info,
  CASE 
        WHEN o.search_agent = 'true' 
         AND c.`$rowtime` BETWEEN o.`$rowtime` - INTERVAL '5' MINUTE AND o.`$rowtime` + INTERVAL '2' HOUR 
        THEN c.`search_result_summary` 
        ELSE NULL 
      END AS additional_context,
  CASE 
        WHEN o.scheduler_agent = 'true' 
         AND sch.`$rowtime` BETWEEN sch.`$rowtime` - INTERVAL '5' MINUTE AND sch.`$rowtime` + INTERVAL '2' HOUR 
        THEN sch.`title`
        ELSE NULL 
      END AS meeting_title
  -- Add scheduler result fields if needed
FROM orchestrator_metadata o , mongo_agent_response s ,search_agent_response c ,scheduler_agent_response sch
  where o.message_id = s.message_id
  AND o.mongo_agent = 'true'
  AND s.`$rowtime` BETWEEN o.`$rowtime` - INTERVAL '5' MINUTE AND o.`$rowtime` + INTERVAL '2' HOUR
  OR ( o.message_id = c.message_id
  AND o.search_agent = 'true'
  AND c.`$rowtime` BETWEEN o.`$rowtime` - INTERVAL '5' MINUTE AND o.`$rowtime` + INTERVAL '2' HOUR )
  OR ( o.message_id = sch.message_id
  AND o.scheduler_agent = 'true'
  AND sch.`$rowtime` BETWEEN o.`$rowtime` - INTERVAL '5' MINUTE AND o.`$rowtime` + INTERVAL '2' HOUR) ;
  ```
🔹 Step 2: Filter Latest Version per Message

Now that agent data is joined with metadata, we only want the most recent version per message ID, so we don’t emit multiple rows per 10-second interval.
```sql
CREATE TABLE final_response_builder AS 
SELECT mongo_agent,mongo_agent_query,search_agent,search_agent_query,scheduler_agent,scheduler_title,scheduler_description,execution_sequence,event_time,message_id,user_email,session_id,employee_id,message,employee_info,additional_context
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY window_start, window_end, message_id 
               ORDER BY event_time DESC
           ) AS row_num
    FROM TABLE(
        TUMBLE(TABLE enriched_query_with_agent_responses,
               DESCRIPTOR(event_time), 
               INTERVAL '10' SECOND)
    )
)
WHERE row_num = 1;
```
Explanation:

- We use a TUMBLE window on the joined table to group outputs every 10 seconds.

- The ROW_NUMBER() function selects the latest event per message ID within the window.

- This filters out older or duplicate outputs and prepares a clean stream for the final response.

NOTE: You can find more information about Flink Window aggregations & joins [here](https://docs.confluent.io/cloud/current/flink/reference/queries/window-tvf.html).

## Task 07 – Final Response Generation (Natural Language)
Once all agent responses are joined and filtered into a clean stream (final_response_builder), we use a Bedrock LLM to formulate a natural language answer. This is the final response a user would see in Slack, email, or a chatbot.

🔹 Step 1: Create a model instance for Final response generator

```sql
    CREATE MODEL BedrockGeneralModelFinalResponse 
    INPUT (text STRING) 
    OUTPUT (response STRING)
    WITH
    (
        'task' = 'text_generation',
        'provider' = 'bedrock',
        'bedrock.PARAMS.max_tokens' = '200000',
        'bedrock.PARAMS.temperature' = '0.1',
        'bedrock.connection' = 'bedrock-text-connection'
    );

```

🔹 Step 2: Define Prompt Template for Bedrock
We'll send a structured prompt to the LLM, containing:
- The original user message
- Agent metadata
- Results from each agent
- Execution sequence (optional but useful for reasoning)


```sql
CREATE TABLE user_friendly_agent_response
WITH ('changelog.mode' = 'append') AS
SELECT 
  message_id,user_email,session_id,employee_id,message,`response` as final_response_text FROM final_response_builder,
LATERAL TABLE(
  ML_PREDICT(
    'BedrockGeneralModelFinalResponse',
    'You are a helpful workplace assistant. Summarize the structured agent responses below into a natural and helpful reply to the user.' || '\n\n' ||

    '---' || '\n' ||
    'Original message: ' || message || '\n\n' ||

    'SQL Agent Triggered: ' || mongo_agent || '\n' ||
    'Employee/Department Level Info Result obtained from SQL agent: ' ||  IFNULL(employee_info, 'none') || '\n\n' ||

    'Search Agent Triggered: ' || search_agent || '\n' ||
    'Search Result: ' || IFNULL(additional_context, 'none') || '\n\n' ||

    'Scheduler Agent Triggered: ' || scheduler_agent || '\n' ||
    'Meeting Title: ' ||  IFNULL(scheduler_title, 'none') || '\n' ||
    'Description: ' ||  IFNULL(scheduler_description, 'none') || '\n' ||

    'Generate a complete, professional answer below:\n'
  )
 );
```
### 🔄 Testing Agent Responses & Accelerating Watermark Progression
If you're not seeing responses in the final joined topic or the watermark is lagging, feel free to add more messages to the input Kafka topic. This helps push the watermark forward, ensuring downstream Flink operators are triggered appropriately.

Below are some sample messages. You can copy and publish them directly to your `queries` topic.

"Can I extend coverage of my healthcare benefits to family members?" → SQL Agent
```json
{
  "message_id": "6f0e8192-9a14-49a7-9a22-6fc324d7d4co",
  "employee_id": "E002",
  "user_email": "john.smith@company.com",
  "session_id": "sess-01",
  "message": "Can I extend coverage of my healthcare benefits to family members?",
  "timestamp": 1746717000000
}
```

"Can you tell me when is the my next public holiday based on my country ?" → Sql & Search Agent
```json
{
  "message_id": "8f0e8192-9a14-49a7-9a22-6fc324d7d4ci",
  "employee_id": "E002",
  "user_email": "john.smith@company.com",
  "session_id": "sess-01",
  "message": "Can you tell me when is the my next public holiday based on my country ?",
  "timestamp": 1746717000000
}
```

"Schedule a meeting." → Scheduler Agent
*Don’t forget to add your own email address so you receive the necessary notifications during the workshop.*
```json
{
  "message_id": "9f0e8192-9a14-49a7-9a22-6fc324d7ddghe",
  "employee_id": "E003",
  "user_email": "john.smith@company.com",
  "session_id": "sess-01",
  "message": "Can you schedule a meeting with my manager <your_email_id> to discuss what happens to my benefits during my upcoming international assignment? Also, can you pull a summary report on this?",
  "timestamp": 1746717000000
}
```


✅ Example Output
If a user asked:
"Can you schedule a meeting with my manager at to discuss what happens to my benefits during my upcoming international assignment? Also, can you pull a summary report on this?"

✅ Example Output:
"I've scheduled a 45-minute meeting titled 'International Assignment – Benefits Discussion' with your manager at for 10 AM this Thursday. I've also pulled a summary report highlighting changes to healthcare, retirement contributions, and relocation allowances during international assignments. The report is attached for your review."

## End of Workshop.

# If you don't need your infrastructure anymore, do not forget to delete the resources!
- Log in to Confluent Cloud.

- Click on your organization name in the top left corner.

- Select the "Environments" tab and click on your cluster.

- Select the lambda Connectors we deployed and scroll down to the bottom.

- Choose "Delete".
![Delete Resources Diagram](assets/img/delete_connector.png)

- Navigate to <b>setup/teardown.sh</b> and edit the following:

    ```bash
    # setup/init.sh

    export TF_VAR_cc_cloud_api_key="<Confluent Cloud API Key>"
    export TF_VAR_cc_cloud_api_secret="<Confluent Cloud API Secret>"
    export TF_VAR_mongodbatlas_public_key="<MongoDB Public API Key>"
    export TF_VAR_mongodbatlas_private_key="<MongoDB Private API Key>"
    export AWS_DEFAULT_REGION="us-west-2" #If using a Confluent-provided AWS account, make sure this region matches the region found in the above steps (most likely it will be us-west-2)
    export AWS_ACCESS_KEY_ID="<AWS Access Key ID"
    export AWS_SECRET_ACCESS_KEY="<AWS Access Key Secret>"
    export AWS_SESSION_TOKEN="<AWS Session Token>" #Only necessary if you are using a Confluent-provided AWS account or using the temporary credentials from your personal AWS account.
    ```
-  After Setting the variables, run:

    ```bash
    chmod +x ./setup/teardown.sh
    ./setup/teardown.sh
    ```
