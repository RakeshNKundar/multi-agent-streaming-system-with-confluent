

resource "confluent_flink_connection" "bedrock-text-connection" {

  organization {
    id = data.confluent_organization.default.id
  }

  environment {
    id = confluent_environment.default.id
  }
  compute_pool {
    id = confluent_flink_compute_pool.default.id
  }
  principal {
    id = confluent_service_account.default.id
  }
  rest_endpoint = data.confluent_flink_region.default.rest_endpoint
  credentials {
    key    = confluent_api_key.flink-default.id
    secret = confluent_api_key.flink-default.secret
  }
  display_name = "bedrock-text-connection"
  type         = "BEDROCK"
  endpoint     = format("https://bedrock-runtime.%s.amazonaws.com/model/anthropic.claude-3-5-haiku-20241022-v1:0/invoke", data.aws_region.current.name)


  aws_access_key = aws_iam_access_key.service_principal_keys.id
  aws_secret_key = aws_iam_access_key.service_principal_keys.secret
}




resource "confluent_flink_connection" "bedrock-embed-connection" {

  organization {
    id = data.confluent_organization.default.id
  }
  environment {
    id = confluent_environment.default.id
  }
  compute_pool {
    id = confluent_flink_compute_pool.default.id
  }
  principal {
    id = confluent_service_account.default.id
  }
  rest_endpoint = data.confluent_flink_region.default.rest_endpoint
  credentials {
    key    = confluent_api_key.flink-default.id
    secret = confluent_api_key.flink-default.secret
  }
  display_name = "bedrock-embed-connection"
  type         = "BEDROCK"
  endpoint     = format("https://bedrock-runtime.%s.amazonaws.com/model/amazon.titan-embed-text-v1/invoke", data.aws_region.current.name)


  aws_access_key = aws_iam_access_key.service_principal_keys.id
  aws_secret_key = aws_iam_access_key.service_principal_keys.secret
}



resource "confluent_flink_connection" "mongodb-search-connection" {

  organization {
    id = data.confluent_organization.default.id
  }
  environment {
    id = confluent_environment.default.id
  }
  compute_pool {
    id = confluent_flink_compute_pool.default.id
  }
  principal {
    id = confluent_service_account.default.id
  }
  rest_endpoint = data.confluent_flink_region.default.rest_endpoint
  credentials {
    key    = confluent_api_key.flink-default.id
    secret = confluent_api_key.flink-default.secret
  }
  display_name = "mongodb-search-connection"
  type         = "MONGODB"
  endpoint     = mongodbatlas_cluster.default.srv_address

  username = local.mongo_workshop_database_user
  password = local.mongo_workshop_database_pass

}

