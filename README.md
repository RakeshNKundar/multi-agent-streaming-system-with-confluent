# 🧠 Multi-Agent Workplace Engagement System — Workshop

Welcome to the workshop on building a **Multi-Agent System for Workplace Engagement** using **Apache Kafka**, **Apache Flink**, and **Amazon Bedrock**. In this workshop, you'll learn to orchestrate multiple intelligent agents that collaborate to handle real-world workplace queries like scheduling meetings, retrieving company data, or answering knowledge base questions.

---

## 📘 Overview

This project demonstrates how to build an LLM-powered multi-agent system for workplace engagement. It combines real-time streaming (Flink), event-driven architecture (Kafka), vector search, and Generative AI (Amazon Bedrock) to enable interactive workflows such as:

- Querying company/employee data from SQL databases
- Searching context from internal documents using embeddings
- Executing tasks like schedulin and sending emails using automation agents

Participants will walk away with hands-on experience building a production-grade GenAI application with real-time agent coordination.

---

## 🗺️ Architecture

![Architecture Diagram](assets/img/architecture.png)

This architecture includes:
- **Orchestrator Agent**: Uses Bedrock LLM to decide which agents to invoke based on incoming user queries.
- **Query Agent**: Fetches data from relational databases (PostgreSQL).
- **Research Agent**: Searches company documents using vector search and embeddings.
- **Task Agent**: Performs action-oriented tasks like scheduling via calendar APIs.
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
- **Local Software Requirements:** 
    - Python3 > 3.9
    - [Terraform CLI](https://developer.hashicorp.com/terraform/install)
    - [Confluent Cloud CLI](https://docs.confluent.io/confluent-cli/current/install.html)

- **Access:** 
    1. MongoDB Atlas Account Access - https://www.mongodb.com/
    2. AWS Account Access - Provided by workshop coordinators
    3. Confluent Cloud Account Access 

<p> <b>Note:</b> For OpenAI API Key, if you don't have any existing account, you can accept the invite from openai with subject Confluent Workshops on OpenAI received on the mail you registered for the workshop and create an openai key.</p>

- **Sign up for Confluent Cloud**
    - Navigate to [Confluent Cloud Sign Up](https://confluent.cloud/signup?utm_campaign=tm.fm-ams_cd.Q424_AMER_GenAI_RAG_Workshop&utm_medium=workshop).
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
    - Enter the promo code : POPTOUT0000EK38
        <p><img src="assets/img/promo.png" alt="promo" width="300" /></p>

---

## 🚀 Quick Start (TL;DR)

1. ### Clone the workshop Github Repo on your local
```bash
git clone https://github.com/RakeshNKundar/genai-gameday
```

```bash
cd realtime-rag-workshop
```
2. ### Create a Cloud API Key
Create cloud api key for your confluent cloud account with resource scope as Cloud resource management.
- Go to https://confluent.cloud/settings/api-keys 
- Add API Key 
- Cloud resource management 
- Download API Key 

<p><img src="assets/img/apikey.png" alt="nim" width="300" /></p>


3. ### Create a MongoDB Programmatic Access API Key
Create MongoDB Programmatic Access api key for your mongo account - https://www.mongodb.com/docs/atlas/configure-api-access-org/
* In Atlas, go to the Organization Access Manager page.
* Click the Applications tab
* Click on Create API Key with Organization Owner Permissions
* Save the API Key for further use.

<p><img src="assets/img/apikeymongo.png" alt="nim" width="300" /></p>

4. ### Setup environment variables

1. Navigate to <b>setup/init.sh</b> and edit the following:

```bash
# setup/init.sh

export TF_VAR_cc_cloud_api_key="<Confluent Cloud API Key>"
export TF_VAR_cc_cloud_api_secret="<Confluent Cloud API Secret>"
export TF_VAR_mongodbatlas_public_key="<MongoDB Public API Key>"
export TF_VAR_mongodbatlas_private_key="<MongoDB Private API Key>"

```
2. After Setting the variables, run:

```bash
chmod +x ./setup/init.sh
./setup/init.sh
```

## Task 01 – Orchestrator Agent (LLM-based Decision Making)


1. Login to your confluent cloud account to see the different resources deployed on your environment.Make a not of your environment id.

2. In a different terminal, run:
Login to confluent cloud
```bash
confluent login --save 
```
Select the environment id for the environment created on your account.
```bash
confluent env use --<YOUR_ENVIRONMENT_ID>
```
Create a FlinkSQL connection to connect to bedrock claude text model.Please replace your access keys and secrets & <env-id> before running the command.
```bash
confluent flink connection create bedrock-text-connection \
  --cloud AWS \
  --region us-east-1 \
  --environment <env-id> \
  --type bedrock \
  --endpoint https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-3-sonnet-20240229-v1:0/invoke \
  --aws-access-key <Replace with your own access key> \
  --aws-secret-key <Replace with your own access secret >
```

3. Log in to your confluent cloud env and access flink workspace(UI tool to run your flinksql queries) to run following queries:

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
Replace <message_field> value before running the command.

```sql
CREATE TABLE `orchestrator_metadata`
 AS SELECT 
    response AS output,
    JSON_VALUE(response, '$.sql_agent') AS sql_agent,
    JSON_VALUE(response, '$.sql_agent_metadata.query') AS sql_agent_query,
    JSON_VALUE(response, '$.sql_agent_metadata.user_email') AS sql_agent_user_email,
    JSON_VALUE(response, '$.sql_agent_metadata.employee_id') AS sql_agent_employee_id,

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

```json
{
  "sql_agent": true | false,
  "sql_agent_metadata": {
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

  "sequence": ["scheduler_agent", "search_agent", "sql_agent"]
}
\```
' || '\n User prompt: ' ||
            '{
   message_id: ' || message_id || ','
  'employee_id: '||  employee_id || ','
  'user_email:' || user_email || ','
  'message:'|| <message_field> || '}'
        )
    )
);
```
5. Insert a sample query in the `queries` topic to test out our flink agent. 

```json
{
  "message_id": "d7a97c0a-8e5b-4c65-90cb-7ea5934ae6d4",
  "employee_id": "E001",
  "user_email": "vdeshpande@confluent.io",
  "session_id": "sess-01",
  "message": "What is company's maternal leave policy? How much am I eligible for ?",
  "timestamp": 1746717000000
}
```

5. Verify the data in the respective topics - **queries** and **orchestrator_metadata**. 

6. Take a look at the agent flags and observe which are true for the input we have given.

7. Try It Yourself ✏️:
    1. How would you change the prompt to exclude the SQL agent from being called?
    2. What metadata is required for the scheduler agent?
    3. Publish one more query containing “schedule a 1:1 with my manager”, which agents will be invoked now?

## Task 2: Setup the Workflow distribution 
Now that the Orchestrator Agent is up and running, it's time to activate the specialized agents that perform actual tasks.🧩 Concept Recap
Each agent is an independent component in the system. Here's a quick breakdown:
🗄 SQL Agent: Retrieves employee or department-level data using employee_id or user_email from a SQL database.
🔎 Vector Search Agent: Uses semantic embeddings to retrieve contextually relevant documents from a MongoDB Vector Store.
📅 Scheduler Agent: Automates meeting scheduling using structured metadata like title, time, and attendees.

These agents listen on their respective Kafka input topics and output results to their own response topics (e.g., sql_result, context_result, scheduler_result).

So we now create three router queries which routes the message to it's repective agent inputs. 


🔹 SQL Agent Routing 
Can you add the flag condition which will help us determine routing the request to sql_agent_input ?
```sql
CREATE TABLE sql_agent_input AS 
SELECT 
    CAST(message AS BYTES) AS key,
    sql_agent_query as query, 
    message_id , 
    employee_id , 
    user_email , 
    message,
    session_id , 
    `timestamp`
FROM orchestrator_metadata 
where <Enter the condition here>; 
```

🔹 Search Agent (Vector)
```sql
CREATE TABLE search_agent_v2 AS 
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
  SPLIT(
  REGEXP_REPLACE(scheduler_attendees, '\\["|\\"]', ''), '","'
) AS attendees
FROM orchestrator_metadata
WHERE scheduler_agent = 'true';
```
Verify the data in the respective topics - **sql_agent_input**, **search_agent_v2** and **scheduler_agent_input**.If any of these topics are empty, it likely means you haven’t triggered a user query that would activate the corresponding agent.

👉 Next Step:
Create a few test queries that would intentionally route to each of these agents. For example:

"How many people are in the engineering team?" → SQL Agent
```json
{
  "message_id": "6f0e8192-9a14-49a7-9a22-6fc324d7d4co",
  "employee_id": "E001",
  "user_email": "vdeshpande@confluent.io",
  "session_id": "sess-01",
  "message": "How many people are in the engineering team?",
  "timestamp": 1746717000000
}
```

"Can you help me understand hybrid Compensation & performance structure ?" → Search Agent
```json
{
  "message_id": "8f0e8192-9a14-49a7-9a22-6fc324d7d4ci",
  "employee_id": "E001",
  "user_email": "vdeshpande@confluent.io",
  "session_id": "sess-01",
  "message": "What is company's maternal leave policy? How much am I eligible for ?",
  "timestamp": 1746717000000
}
```

"Schedule a skip-level meeting with my manager next week" → Scheduler Agent
```json
{
  "message_id": "9f0e8192-9a14-49a7-9a22-6fc324d7ddghe",
  "employee_id": "E001",
  "user_email": "vdeshpande@confluent.io",
  "session_id": "sess-01",
  "message": "What is company's maternal leave policy? How much am I eligible for ?",
  "timestamp": 1746717000000
}
```

This will help populate the input topics and allow you to test the complete agent workflow.

## Task 3: Integrate SQL Agent with Lambda Sink Connector
This task helps you build a fully managed Lambda Kafka Sink Connector that routes your queries to a SQL lambda agent.
Goal:
Stream sql_agent_input Kafka topic data directly to your AWS Lambda.
Step-by-step Setup:
1. Go to Confluent Cloud > Connectors.

2. Select AWS Lambda Sink Connector from the available connectors.

3. Fill in the relevant configuration details below and deploy the connector.
```json
{
  "name": "sql-agent-sink",
  "config": {
    "connector.class": "io.confluent.connect.http.HttpSinkConnector",
    "topics": "sql_agent_input",
    "tasks.max": "1",
    "http.api.url": "<YOUR_SQL_LAMBDA_ENDPOINT>",
    "reporter.bootstrap.servers": "<BOOTSTRAP_SERVERS>",
    "confluent.topic.bootstrap.servers": "<BOOTSTRAP_SERVERS>",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": false,
    "header.converter": "org.apache.kafka.connect.storage.SimpleHeaderConverter",
    "errors.tolerance": "all",
    "errors.log.enable": "true",
    "errors.deadletterqueue.topic.name": "sql_agent_dlq",
    "errors.deadletterqueue.context.headers.enable": "true"
  }
}

```

## Task 4: Context Retrieval via Vector Search 
We now add intelligence to our Research Agent using Amazon Bedrock embeddings + MongoDB vector search.

1. Create a FlinkSQL connection to connect to bedrock text embedding model.Please replac your own keys before running the command.
```bash
confluent flink connection create bedrock-embedding-connection \
  --cloud AWS \
  --region 	us-east-1 \
  --environment <env-id> \
  --type bedrock \
  --endpoint https://bedrock-runtime.us-east-1.amazonaws.com/model/amazon.titan-embed-text-v1/invoke \
  --aws-access-key <Replace with your own access key> \
  --aws-secret-key <Replace with your own access secret >
```

Log in to your confluent cloud env and access flink workspace(UI tool to run your flinksql queries) to run following queries:

2. Create Bedrock Model in Flink SQL
```sql
CREATE MODEL bedrock_embed
INPUT (text STRING)
OUTPUT (response ARRAY<FLOAT>)
WITH (
  'bedrock.connection'='bedrock-embedding-connection',
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
4. Connect to MongoDB Atlas Vector Store
```sql
CREATE TABLE mongodb (
  policyId STRING,
  title STRING,
  region STRING,
  category STRING,
  lastUpdated STRING, 
  content STRING , 
 contentEmbedding ARRAY<FLOAT>
) WITH (
  'connector' = 'mongodb',
  'mongodb.connection' = 'mongodb-fed-search-connection',
  'mongodb.database' = '<knowledge_base>',
  'mongodb.collection' = '<collection_name>',
  'mongodb.index' = 'vector_index',
  'mongodb.embedding_column' = 'contentEmbedding',
  'mongodb.numCandidates' = '1'
);
```
5. Perform Vector Search to Retrieve Results
```sql
CREATE TABLE context_results AS
SELECT query,message_id,employee_id,user_email,message,session_id,`timestamp`,search_results  FROM search_embeddings,
  LATERAL TABLE(VECTOR_SEARCH(mongodb, 1,DESCRIPTOR(contentEmbedding), search_embeddings.query_embedding));
```

## Task 5: Integrate Scheduler Agent with Lambda Sink Connector
This task helps you build a fully managed Lambda Kafka Sink Connector that routes your queries to a Scheduler lambda agent , similar to how we did it for a sql agent.
Goal:
Stream scheduler_agent_input Kafka topic data directly to your AWS Lambda.
Step-by-step Setup:
1. Go to Confluent Cloud > Connectors.

2. Select AWS Lambda Sink Connector from the available connectors.

3. Fill in the relevant configuration details below and deploy the connector.
```json
{
  "name": "scheduler-agent-input",
  "config": {
    "connector.class": "io.confluent.connect.http.HttpSinkConnector",
    "topics": "scheduler_agent_input",
    "tasks.max": "1",
    "http.api.url": "<YOUR_SQL_LAMBDA_ENDPOINT>",
    "reporter.bootstrap.servers": "<BOOTSTRAP_SERVERS>",
    "confluent.topic.bootstrap.servers": "<BOOTSTRAP_SERVERS>",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": false,
    "header.converter": "org.apache.kafka.connect.storage.SimpleHeaderConverter",
    "errors.tolerance": "all",
    "errors.log.enable": "true",
    "errors.deadletterqueue.topic.name": "sql_agent_dlq",
    "errors.deadletterqueue.context.headers.enable": "true"
  }
}
```

## Task 06 – Final Agent Builder Join & response input Structuring
Now that all three agents (SQL, Search, Scheduler) have emitted results, we perform a final conditional join with the orchestrator metadata. This gives us a fully enriched context for each user query.

🔹 Step 1: Join All Agent Results
This query joins orchestrator_metadata with the three agent response topics conditionally, based on which agents were triggered (sql_agent, search_agent, scheduler_agent).
```sql
CREATE TABLE enriched_query_with_agent_responses(
event_time TIMESTAMP(3),
  WATERMARK FOR event_time AS event_time - INTERVAL '1' SECOND)
 with('changelog.mode'='append')  AS
SELECT
  o.sql_agent,
  o.sql_agent_query,
  o.sql_agent_user_email,
  o.sql_agent_employee_id,
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
        WHEN o.sql_agent = 'true' 
         AND s.`$rowtime` BETWEEN o.`$rowtime` - INTERVAL '5' MINUTE AND o.`$rowtime` + INTERVAL '5' MINUTE 
        THEN s.sql_result 
        ELSE NULL 
      END AS employee_info,
  CASE 
        WHEN o.search_agent = 'true' 
         AND c.`$rowtime` BETWEEN o.`$rowtime` - INTERVAL '5' MINUTE AND o.`$rowtime` + INTERVAL '5' MINUTE 
        THEN c.search_results 
        ELSE NULL 
      END AS additional_context
  -- Add scheduler result fields if needed
FROM orchestrator_metadata o , sql_result s ,context_results c ,scheduler_agent_response sch
  where o.message_id = s.message_id
  AND o.sql_agent = 'true'
  AND s.`$rowtime` BETWEEN o.`$rowtime` - INTERVAL '5' MINUTE AND o.`$rowtime` + INTERVAL '5' MINUTE
  OR ( o.message_id = c.message_id
  AND o.search_agent = 'true'
  AND c.`$rowtime` BETWEEN o.`$rowtime` - INTERVAL '5' MINUTE AND o.`$rowtime` + INTERVAL '5' MINUTE )
  OR ( o.message_id = sch.message_id
  AND o.scheduler_agent = 'true'
  AND sch.`$rowtime` BETWEEN o.`$rowtime` - INTERVAL '5' MINUTE AND o.`$rowtime` + INTERVAL '5' MINUTE) ;

```
🔹 Step 2: Filter Latest Version per Message

Now that agent data is joined with metadata, we only want the most recent version per message ID, so we don’t emit multiple rows per 10-second interval.
```sql
CREATE TABLE final_response_builder AS 
SELECT message_id, employee_info, additional_context
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY window_start, window_end, message_id 
               ORDER BY event_time DESC
           ) AS row_num
    FROM TABLE(
        TUMBLE(TABLE final_enriched_output_with_inner_joinv2, 
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


## Task 07 – Final Response Generation (Natural Language)
Once all agent responses are joined and filtered into a clean stream (final_response_builder), we use a Bedrock LLM to formulate a natural language answer. This is the final response a user would see in Slack, email, or a chatbot.

🔹 Step 1: Define Prompt Template for Bedrock
We'll send a structured prompt to the LLM, containing:
- The original user message
- Agent metadata
- Results from each agent
- Execution sequence (optional but useful for reasoning)


```sql
CREATE TABLE user_friendly_agent_response
WITH ('changelog.mode' = 'append') AS
SELECT 
  message_id,
  ML_PREDICT(
    'BedrockFinalFormatter',
    'You are a helpful workplace assistant. Summarize the structured agent responses below into a natural and helpful reply to the user.' || '\n\n' ||

    '---' || '\n' ||
    'Original message: ' || message || '\n\n' ||

    'SQL Agent Triggered: ' || sql_agent || '\n' ||
    'Query: ' || sql_agent_query || '\n' ||
    'Employee/Department Level Info Result obtained from SQL agent: ' || employee_info || '\n\n' ||

    'Search Agent Triggered: ' || search_agent || '\n' ||
    'Search Query: ' || search_agent_query || '\n' ||
    'Search Result: ' || additional_context || '\n\n' ||

    'Scheduler Agent Triggered: ' || scheduler_agent || '\n' ||
    'Meeting Title: ' || scheduler_title || '\n' ||
    'Description: ' || scheduler_description || '\n' ||
    'Time: ' || scheduler_start || ' to ' || scheduler_end || '\n' ||
    'Attendees: ' || scheduler_attendees || '\n\n' ||

    'Execution Sequence: ' || execution_sequence || '\n\n' ||

    'Generate a complete, professional answer below:\n'
  ) AS final_response_text
FROM enriched_query_with_agent_responses;
```

✅ Example Output
If a user asked:
"Can you schedule a 30-minute meeting with Alice and show me her department's last month performance?"

And all agents responded, the final result might be:

"I've scheduled a 30-minute meeting titled 'Project Discussion' with Alice at 3 PM tomorrow. Her department's performance for last month shows a 12% increase in output. I've also attached a document detailing her recent projects."

