
resource "confluent_service_account" "default" {
  display_name = "workplace_assistant_sa_${random_string.random.id}"
  description  = "Service Account for workplace assistant pipeline"
}

resource "confluent_environment" "default" {
  display_name = "confluent_agentic_workshop_${random_string.random.id}"

  lifecycle {
    prevent_destroy = false
  }
}

resource "confluent_kafka_cluster" "default" {
  display_name = "workplace_assistant_${random_string.random.id}"
  availability = "SINGLE_ZONE"
  cloud        = "AWS"
  region       = data.aws_region.current.name
  standard {}

  environment {
    id = confluent_environment.default.id
  }

  lifecycle {
    prevent_destroy = false
  }
}

resource "confluent_role_binding" "cluster-admin" {
  principal   = "User:${confluent_service_account.default.id}"
  role_name   = "CloudClusterAdmin"
  crn_pattern = confluent_kafka_cluster.default.rbac_crn
}

resource "confluent_role_binding" "env-admin" {
  principal   = "User:${confluent_service_account.default.id}"
  role_name   = "EnvironmentAdmin"
  crn_pattern = confluent_environment.default.resource_name
}

resource "confluent_role_binding" "topic-write" {
  principal   = "User:${confluent_service_account.default.id}"
  role_name   = "DeveloperWrite"
  crn_pattern = "${confluent_kafka_cluster.default.rbac_crn}/kafka=${confluent_kafka_cluster.default.id}/topic=*"
}

resource "confluent_role_binding" "topic-read" {
  principal   = "User:${confluent_service_account.default.id}"
  role_name   = "DeveloperRead"
  crn_pattern = "${confluent_kafka_cluster.default.rbac_crn}/kafka=${confluent_kafka_cluster.default.id}/topic=*"
}


resource "confluent_api_key" "cluster-api-key" {
  display_name = "workplace-assistant-kafka-api-key-${random_string.random.id}"
  description  = "Kafka API Key that is owned by default service account"
  owner {
    id          = confluent_service_account.default.id
    api_version = confluent_service_account.default.api_version
    kind        = confluent_service_account.default.kind
  }

  managed_resource {
    id          = confluent_kafka_cluster.default.id
    api_version = confluent_kafka_cluster.default.api_version
    kind        = confluent_kafka_cluster.default.kind

    environment {
      id = confluent_environment.default.id
    }
  }

  lifecycle {
    prevent_destroy = false
  }
}
