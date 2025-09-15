
output "gameday_sns_topic_arn" {
  value = aws_sns_topic.gameday_sns_topic.arn
}

# output "mongo_agent_lambda" {
#   value = aws_lambda_function.mongo_agent.arn
# }

output "scheduler_agent_lambda" {
  value = aws_lambda_function.scheduler_agent.arn
}

output "mongo_agent_response_topic" {
  value = confluent_kafka_topic.mongo_agent_response.id
}

output "scheduler_agent_response_topic" {
  value = confluent_kafka_topic.scheduler_agent_response.id
}

output "kafka_api_key" {
  value = confluent_api_key.cluster-api-key.id
}

output "kafka_api_secret" {
  value     = confluent_api_key.cluster-api-key.secret
  sensitive = true
}

output "bootstrap_endpoint" {
  value = confluent_kafka_cluster.default.bootstrap_endpoint
}
output "schema_registry_api_key" {
  value = confluent_api_key.schema-registry-api-key.id
}

output "schema_registry_api_secret" {
  value     = confluent_api_key.schema-registry-api-key.secret
  sensitive = true
}

output "schema_registry_endpoint" {
  value = data.confluent_schema_registry_cluster.default.rest_endpoint
}

output "flink_api_key" {
  value = confluent_api_key.flink-default.id
}

output "flink_api_secret" {
  value     = confluent_api_key.flink-default.secret
  sensitive = true
}

output "deployed_region" {
  value = data.aws_region.current.name
}

output "mongo_uri" {
  value = mongodbatlas_cluster.default.srv_address
}
