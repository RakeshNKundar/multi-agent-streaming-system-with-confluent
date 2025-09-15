resource "aws_iam_user" "service_principal" {
  name = "agent-bedrock-service-principal"
}

resource "aws_iam_user_policy_attachment" "bedrock_access" {
  user       = aws_iam_user.service_principal.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
}

resource "aws_iam_user_policy" "lambda_invoke_policy" {
  name = "LambdaInvokeAccess"
  user = aws_iam_user.service_principal.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["lambda:InvokeFunction"]
        Resource = format("arn:aws:lambda:%s:%s:function:*", data.aws_region.current.name, data.aws_caller_identity.current.account_id)
      }
    ]
  })
}

resource "aws_iam_access_key" "service_principal_keys" {
  user = aws_iam_user.service_principal.name
}

output "aws_access_key_id" {
  value = aws_iam_access_key.service_principal_keys.id
}

output "aws_secret_access_key" {
  value     = aws_iam_access_key.service_principal_keys.secret
  sensitive = true
}

resource "local_file" "service_principal_keys" {
  content  = <<EOT
AWS_ACCESS_KEY_ID=${aws_iam_access_key.service_principal_keys.id}
AWS_SECRET_ACCESS_KEY=${aws_iam_access_key.service_principal_keys.secret}
EOT
  filename = "${path.module}/service_principal_keys.txt"
}




