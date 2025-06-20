data "confluent_organization" "default" {}

data "confluent_flink_region" "default" {
  cloud  = "AWS"
  region = data.aws_region.current.name
}

resource "confluent_role_binding" "environment-admin" {
  principal   = "User:${confluent_service_account.default.id}"
  role_name   = "EnvironmentAdmin"
  crn_pattern = confluent_environment.default.resource_name
}

resource "confluent_flink_compute_pool" "default" {
  display_name = "multi-agent-workplace-system_pool_${random_string.random.id}"
  cloud        = "AWS"
  region       = data.aws_region.current.name
  max_cfu      = 50
  environment {
    id = confluent_environment.default.id
  }
}

resource "confluent_api_key" "flink-default" {
  display_name = "multi-agent-workplace-system-flink-api-key-${random_string.random.id}"
  description  = "Flink API Key that is owned by default service account"
  owner {
    id          = confluent_service_account.default.id
    api_version = confluent_service_account.default.api_version
    kind        = confluent_service_account.default.kind
  }

  managed_resource {
    id          = data.confluent_flink_region.default.id
    api_version = data.confluent_flink_region.default.api_version
    kind        = data.confluent_flink_region.default.kind

    environment {
      id = confluent_environment.default.id
    }
  }

  lifecycle {
    prevent_destroy = false
  }

  depends_on = [confluent_role_binding.environment-admin]
}
