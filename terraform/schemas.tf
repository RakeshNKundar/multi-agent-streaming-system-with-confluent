resource "confluent_schema" "Queries" {
  schema_registry_cluster {
    id = data.confluent_schema_registry_cluster.default.id
  }
  rest_endpoint      = data.confluent_schema_registry_cluster.default.rest_endpoint
  subject_name       = "queries-value"
  format             = "AVRO"
  schema             = file("../schemas/queries.avsc")
  recreate_on_update = false
  hard_delete        = true
  credentials {
    key    = confluent_api_key.schema-registry-api-key.id
    secret = confluent_api_key.schema-registry-api-key.secret
  }
  lifecycle {
    prevent_destroy = false
  }
}

resource "confluent_schema" "mongo_agent_response" {
  schema_registry_cluster {
    id = data.confluent_schema_registry_cluster.default.id
  }
  rest_endpoint      = data.confluent_schema_registry_cluster.default.rest_endpoint
  subject_name       = "mongo_agent_response-value"
  format             = "AVRO"
  schema             = file("../schemas/mongo_agent_response.avsc")
  recreate_on_update = false
  hard_delete        = true
  credentials {
    key    = confluent_api_key.schema-registry-api-key.id
    secret = confluent_api_key.schema-registry-api-key.secret
  }
  lifecycle {
    prevent_destroy = false
  }
}

resource "confluent_schema" "scheduler_agent_response" {
  schema_registry_cluster {
    id = data.confluent_schema_registry_cluster.default.id
  }
  rest_endpoint      = data.confluent_schema_registry_cluster.default.rest_endpoint
  subject_name       = "scheduler_agent_response-value"
  format             = "AVRO"
  schema             = file("../schemas/scheduler_agent_response.avsc")
  recreate_on_update = false
  hard_delete        = true
  credentials {
    key    = confluent_api_key.schema-registry-api-key.id
    secret = confluent_api_key.schema-registry-api-key.secret
  }
  lifecycle {
    prevent_destroy = false
  }
}

resource "confluent_schema" "search_agent_response" {
  schema_registry_cluster {
    id = data.confluent_schema_registry_cluster.default.id
  }
  rest_endpoint      = data.confluent_schema_registry_cluster.default.rest_endpoint
  subject_name       = "search_agent_response-value"
  format             = "AVRO"
  schema             = file("../schemas/search_agent_response.avsc")
  recreate_on_update = false
  hard_delete        = true
  credentials {
    key    = confluent_api_key.schema-registry-api-key.id
    secret = confluent_api_key.schema-registry-api-key.secret
  }
  lifecycle {
    prevent_destroy = false
  }
}
