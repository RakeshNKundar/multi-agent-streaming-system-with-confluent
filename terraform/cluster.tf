resource "confluent_service_account" "default" {
  display_name = "workplace_assistant_sa"
  description  = "Service Account for workplace assistant pipeline"
}

resource "confluent_environment" "default" {
  display_name = "confluent_agentic_workshop"

  lifecycle {
    prevent_destroy = false
  }
}

resource "confluent_kafka_cluster" "default" {
  display_name = "workplace_assistant"
  availability = "SINGLE_ZONE"
  cloud        = "AWS"
  region       = "us-east-1"
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
  display_name = "workplace-assistant-kafka-api-key"
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
