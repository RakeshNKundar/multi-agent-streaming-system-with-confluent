

provider "aws" {
}
data "aws_region" "current" {}

resource "aws_s3_bucket" "lambda_layers" {
  bucket        = "code-bucket-${random_string.random.id}"
  force_destroy = true
}

# resource "aws_s3_object" "mongo_agent_layer_zip" {
#   bucket = aws_s3_bucket.lambda_layers.bucket
#   key    = "layers/mongo_agent_layer.zip"
#   source = "../agents/mongo_agent/artifacts/mongo_agent_layer.zip"
#   etag   = filemd5("../agents/mongo_agent/artifacts/mongo_agent_layer.zip")
# }

resource "aws_s3_object" "scheduler_agent_layer_zip" {
  bucket = aws_s3_bucket.lambda_layers.bucket
  key    = "layers/scheduler_agent_layer.zip"
  source = "../agents/scheduler_agent/artifacts/scheduler_lambda_layer.zip"
  etag   = filemd5("../agents/scheduler_agent/artifacts/scheduler_lambda_layer.zip")
}

resource "aws_s3_object" "search_agent_layer_zip" {
  bucket = aws_s3_bucket.lambda_layers.bucket
  key    = "layers/search_agent_layer.zip"
  source = "../agents/search_agent/artifacts/search_agent_layer.zip"
  etag   = filemd5("../agents/search_agent/artifacts/search_agent_layer.zip")
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role_${random_string.random.id}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# resource "aws_lambda_layer_version" "mongo_agent_layer" {
#   layer_name          = "mongo_agent_layer_${random_string.random.id}"
#   compatible_runtimes = ["python3.12"]
#   s3_bucket           = aws_s3_bucket.lambda_layers.bucket
#   s3_key              = aws_s3_object.mongo_agent_layer_zip.key
#   description         = "mongo_agent_layer 1"
# }

resource "aws_lambda_layer_version" "scheduler_agent_layer" {
  layer_name          = "scheduler_agent_layer_${random_string.random.id}"
  compatible_runtimes = ["python3.13"]
  s3_bucket           = aws_s3_bucket.lambda_layers.bucket
  s3_key              = aws_s3_object.scheduler_agent_layer_zip.key
  description         = "scheduler_agent_layer 1"
}

resource "aws_lambda_layer_version" "search_agent_layer" {
  layer_name          = "search_agent_layer_${random_string.random.id}"
  compatible_runtimes = ["python3.12"]
  s3_bucket           = aws_s3_bucket.lambda_layers.bucket
  s3_key              = aws_s3_object.search_agent_layer_zip.key
  description         = "search_agent_layer 1"
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "bedrock_access" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
}

resource "aws_iam_role_policy_attachment" "sns_access" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
}

# data "archive_file" "mongo_agent_lambda" {
#   type        = "zip"
#   source_dir  = "../agents/mongo_agent/source_code/"
#   output_path = "../agents/mongo_agent/artifacts/mongo_agent_lambda.zip"
# }


data "archive_file" "scheduler_agent_lambda" {
  type        = "zip"
  source_dir  = "../agents/scheduler_agent/source-code/"
  output_path = "../agents/scheduler_agent/artifacts/scheduler_agent_lambda.zip"
}

data "archive_file" "search_agent_lambda" {
  type        = "zip"
  source_dir  = "../agents/search_agent/source_code/"
  output_path = "../agents/search_agent/artifacts/search_agent_lambda.zip"
}

# resource "aws_lambda_function" "mongo_agent" {
#   function_name = "mongo_agent_${random_string.random.id}"
#   role          = aws_iam_role.lambda_exec_role.arn
#   handler       = "main.lambda_handler"
#   runtime       = "python3.12"
#   timeout       = 900
#   memory_size   = 10240
#   ephemeral_storage {
#     size = 10240
#   }
#   filename         = data.archive_file.mongo_agent_lambda.output_path
#   source_code_hash = filebase64sha256(data.archive_file.mongo_agent_lambda.output_path)
#   layers           = [aws_lambda_layer_version.mongo_agent_layer.arn]
#   environment {
#     variables = {
#       BOOTSTRAP_ENDPOINT         = confluent_kafka_cluster.default.bootstrap_endpoint
#       KAFKA_API_KEY              = confluent_api_key.cluster-api-key.id
#       KAFKA_API_SECRET           = confluent_api_key.cluster-api-key.secret
#       SCHEMA_REGISTRY_API_KEY    = confluent_api_key.schema-registry-api-key.id
#       SCHEMA_REGISTRY_API_SECRET = confluent_api_key.schema-registry-api-key.secret
#       SCHEMA_REGISTRY_ENDPOINT   = data.confluent_schema_registry_cluster.default.rest_endpoint
#       mongo_agent_result_topic   = "mongo_agent_response"
#     }
#   }
# }

# resource "aws_cloudwatch_log_group" "lambda_log_group_mongo_agent" {
#   name              = "/aws/lambda/${aws_lambda_function.mongo_agent.function_name}"
#   retention_in_days = 14
# }

resource "aws_sns_topic" "gameday_sns_topic" {
  name = "gameday-sns-topic-new_${random_string.random.id}"
}

resource "aws_lambda_function" "scheduler_agent" {
  function_name = "scheduler_agent_${random_string.random.id}"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.13"
  filename      = data.archive_file.scheduler_agent_lambda.output_path
  timeout       = 900
  memory_size   = 10240
  ephemeral_storage {
    size = 10240
  }
  source_code_hash = filebase64sha256(data.archive_file.scheduler_agent_lambda.output_path)
  layers           = [aws_lambda_layer_version.scheduler_agent_layer.arn]
  environment {
    variables = {
      BOOTSTRAP_ENDPOINT           = confluent_kafka_cluster.default.bootstrap_endpoint
      KAFKA_API_KEY                = confluent_api_key.cluster-api-key.id
      KAFKA_API_SECRET             = confluent_api_key.cluster-api-key.secret
      SCHEMA_REGISTRY_API_KEY      = confluent_api_key.schema-registry-api-key.id
      SCHEMA_REGISTRY_API_SECRET   = confluent_api_key.schema-registry-api-key.secret
      SCHEMA_REGISTRY_ENDPOINT     = data.confluent_schema_registry_cluster.default.rest_endpoint
      scheduler_agent_result_topic = "scheduler_agent_response"
      SNS_ARN                      = aws_sns_topic.gameday_sns_topic.arn
    }
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group_scheduler_agent" {
  name              = "/aws/lambda/${aws_lambda_function.scheduler_agent.function_name}"
  retention_in_days = 14
}

resource "aws_lambda_function" "search_agent" {
  function_name = "search_agent_${random_string.random.id}"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  filename      = data.archive_file.search_agent_lambda.output_path
  timeout       = 900
  memory_size   = 10240
  ephemeral_storage {
    size = 10240
  }
  source_code_hash = filebase64sha256(data.archive_file.scheduler_agent_lambda.output_path)
  layers           = [aws_lambda_layer_version.search_agent_layer.arn]
  environment {
    variables = {
      MONGO_HOST                 = replace(mongodbatlas_cluster.default.connection_strings.0.standard_srv, "mongodb+srv://", "")
      MONGO_USER                 = mongodbatlas_database_user.default.username
      MONGO_PASSWORD             = mongodbatlas_database_user.default.password
      MONGO_URI_RAW              = mongodbatlas_cluster.default.srv_address
      DB_NAME                    = "workplace_knowledgebase"
      COLLECTION_NAME            = "knowledge_collection"
      BOOTSTRAP_ENDPOINT         = confluent_kafka_cluster.default.bootstrap_endpoint
      KAFKA_API_KEY              = confluent_api_key.cluster-api-key.id
      KAFKA_API_SECRET           = confluent_api_key.cluster-api-key.secret
      SCHEMA_REGISTRY_API_KEY    = confluent_api_key.schema-registry-api-key.id
      SCHEMA_REGISTRY_API_SECRET = confluent_api_key.schema-registry-api-key.secret
      SCHEMA_REGISTRY_ENDPOINT   = data.confluent_schema_registry_cluster.default.rest_endpoint
      search_agent_result_topic  = "search_agent_response"
    }
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group_search_agent" {
  name              = "/aws/lambda/${aws_lambda_function.search_agent.function_name}"
  retention_in_days = 14
}
