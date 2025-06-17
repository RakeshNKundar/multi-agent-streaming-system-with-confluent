# setup/init.sh

export TF_VAR_cc_cloud_api_key="<Confluent Cloud API Key>"
export TF_VAR_cc_cloud_api_secret="<Confluent Cloud API Secret>"
export TF_VAR_mongodbatlas_public_key="<MongoDB Public API Key>"
export TF_VAR_mongodbatlas_private_key="<MongoDB Private API Key>"
export TF_VAR_mongodb_atlas_org_id="<MongoDB Organization ID>"
export AWS_DEFAULT_REGION="us-west-2" #If using a Confluent-provided AWS account, make sure this region matches the region found in the above steps (most likely it will be us-west-2)
export AWS_ACCESS_KEY_ID="<AWS Access Key ID"
export AWS_SECRET_ACCESS_KEY="<AWS Access Key Secret>"
export AWS_SESSION_TOKEN="<AWS Session Token>" #Only necessary if you are using a Confluent-provided AWS account or using the temporary credentials from your personal AWS account.


cd terraform
terraform init
terraform apply --auto-approve