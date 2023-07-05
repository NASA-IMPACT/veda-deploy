# veda-deploy
Deploy full stack 

# Steps
1- Define the necessary environment variables in AWS secret manager (make note of the name of the secret manager)
```bash
AWS_ACCOUNT_ID=******
AWS_REGION=******
VPC_ID=******
STAGE=******
SUBNET_TAGNAME=******
PROJECT_PREFIX=******
PERMISSIONS_BOUNDARY_POLICY_NAME=******
COGNITO_GROUPS=******
VEDA_DB_PGSTAC_VERSION=******
VEDA_DB_SCHEMA_VERSION=******
PREFIX=******
STATE_BUCKET_NAME=******
STATE_BUCKET_KEY=*****
STATE_DYNAMO_TABLE=*****
VEDA_STAC_PATH_PREFIX=*****
VEDA_RASTER_PATH_PREFIX=*****
```

2- Define github secrets and variables
Define `DEPLOYMENT_ROLE_ARN` as a github secret and
```bash 
DEPLOYMENT_ENV_SECRET_NAME=*** (This is the AWS secret manager you define the deployment env variables)
PROJECT_PREFIX=*** (match the project prefix defined in AWS secret manager)
STAGE=*** (matches the stage defined in AWS secret manager)
```
in github variables 
