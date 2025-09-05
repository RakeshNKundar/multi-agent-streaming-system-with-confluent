# data "mongodbatlas_project" "default" {
#   name = "confluent_agentic_workshop"
# }

variable "mongodb_atlas_org_id" {
  description = "MongoDB Atlas Organization ID"
  type        = string
}

resource "mongodbatlas_project" "default" {
  name   = "confluent_agentic_workshop" # <- your project name
  org_id = var.mongodb_atlas_org_id     # <- your MongoDB Atlas organization ID
}


resource "mongodbatlas_project_ip_access_list" "allow_all_ips" {
  project_id = resource.mongodbatlas_project.default.id
  cidr_block = "0.0.0.0/0"
  comment    = "Allow all IPs for development"
}


locals {
  mongo_workshop_database            = "workplace_knowledgebase"
  mongo_workshop_database_user       = "confluent"
  mongo_workshop_database_pass       = "mongo"
  mongo_workshop_database_collection = "knowledge_collection"
  mongo_workshop_employee_collection = "employee_collection"
  mongo_workshop_database_index      = "knowledge_index"
}

resource "mongodbatlas_database_user" "default" {
  username           = local.mongo_workshop_database_user
  password           = local.mongo_workshop_database_pass
  project_id         = resource.mongodbatlas_project.default.id
  auth_database_name = "admin"

  roles {
    role_name     = "readWrite"
    database_name = "admin"
  }

  roles {
    role_name     = "readWrite"
    database_name = local.mongo_workshop_database
  }

  roles {
    role_name     = "atlasAdmin"
    database_name = "admin"
  }

  labels {
    key   = "owner"
    value = "workshop"
  }
  labels {
    key   = "purpose"
    value = "learning"
  }
}

resource "mongodbatlas_cluster" "default" {
  project_id                  = resource.mongodbatlas_project.default.id
  name                        = "multi-agent-workplace-system"
  provider_name               = "TENANT"
  backing_provider_name       = "AWS"
  provider_region_name        = data.aws_region.current.name == "us-east-1" ? "US_EAST_1" : "US_WEST_2"
  provider_instance_size_name = "M0"
}

resource "null_resource" "seed_mongodb_knowledge" {
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
    command = <<EOT
      mongoimport \
        --uri="${mongodbatlas_cluster.default.connection_strings.0.standard_srv}" \
        --username="${local.mongo_workshop_database_user}" \
        --password="${local.mongo_workshop_database_pass}" \
        --authenticationDatabase=admin \
        --db="${local.mongo_workshop_database}" \
        --collection="${local.mongo_workshop_database_collection}" \
        --file=seed/data.json \
        --jsonArray \
        --tlsInsecure
    EOT
  }

  depends_on = [mongodbatlas_cluster.default]
}

resource "null_resource" "seed_mongodb_employee" {
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
    command = <<EOT
      mongoimport \
        --uri="${mongodbatlas_cluster.default.connection_strings.0.standard_srv}" \
        --username="${local.mongo_workshop_database_user}" \
        --password="${local.mongo_workshop_database_pass}" \
        --authenticationDatabase=admin \
        --db="${local.mongo_workshop_database}" \
        --collection="${local.mongo_workshop_employee_collection}" \
        --file=seed/employee.json \
        --jsonArray \
        --tlsInsecure
    EOT
  }

  depends_on = [mongodbatlas_cluster.default]
}







resource "mongodbatlas_search_index" "default" {
  project_id      = resource.mongodbatlas_project.default.id
  name            = local.mongo_workshop_database_index
  cluster_name    = mongodbatlas_cluster.default.name
  collection_name = local.mongo_workshop_database_collection
  database        = local.mongo_workshop_database
  type            = "vectorSearch"
  fields          = <<-EOF
    [{
        "type": "vector",
        "path": "contentEmbedding",
        "numDimensions": 1536,
        "similarity": "cosine"
    }]
    EOF
  depends_on      = [null_resource.seed_mongodb_knowledge]
}


resource "mongodbatlas_search_index" "employee_id_index" {
  project_id      = mongodbatlas_project.default.id
  name            = " "
  cluster_name    = mongodbatlas_cluster.default.name
  collection_name = local.mongo_workshop_employee_collection
  database        = local.mongo_workshop_database
  type            = "search"

  mappings_dynamic = true

  # mappings_fields = <<-EOF
  # {
  #   "employee_id": {
  #     "type": "string",
  #     "analyzer": "keyword"
  #   }
  # }
  # EOF

  depends_on = [null_resource.seed_mongodb_employee]
}




