resource "confluent_kafka_topic" "queries" {
  kafka_cluster {
    id = confluent_kafka_cluster.default.id
  }
  topic_name       = "queries"
  rest_endpoint    = confluent_kafka_cluster.default.rest_endpoint
  partitions_count = 1
  credentials {
    key    = confluent_api_key.cluster-api-key.id
    secret = confluent_api_key.cluster-api-key.secret
  }

  lifecycle {
    prevent_destroy = false
  }
}

resource "confluent_kafka_topic" "sql_agent_response" {
  kafka_cluster {
    id = confluent_kafka_cluster.default.id
  }
  topic_name       = "sql_agent_response"
  rest_endpoint    = confluent_kafka_cluster.default.rest_endpoint
  partitions_count = 1
  credentials {
    key    = confluent_api_key.cluster-api-key.id
    secret = confluent_api_key.cluster-api-key.secret
  }

  lifecycle {
    prevent_destroy = false
  }
}



resource "confluent_kafka_topic" "scheduler_agent_response" {
  kafka_cluster {
    id = confluent_kafka_cluster.default.id
  }
  topic_name       = "scheduler_agent_response"
  rest_endpoint    = confluent_kafka_cluster.default.rest_endpoint
  partitions_count = 1
  credentials {
    key    = confluent_api_key.cluster-api-key.id
    secret = confluent_api_key.cluster-api-key.secret
  }

  lifecycle {
    prevent_destroy = false
  }
}
resource "confluent_kafka_topic" "search_agent_response" {
  kafka_cluster {
    id = confluent_kafka_cluster.default.id
  }
  topic_name       = "search_agent_response"
  rest_endpoint    = confluent_kafka_cluster.default.rest_endpoint
  partitions_count = 1
  credentials {
    key    = confluent_api_key.cluster-api-key.id
    secret = confluent_api_key.cluster-api-key.secret
  }

  lifecycle {
    prevent_destroy = false
  }
}