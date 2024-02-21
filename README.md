# What?
Deploy full VEDA stack easily.

# How to deploy?
## Steps
1. Create an Environment in the repository. See [Requirements](#requirements) on details of creating the environment.
2. Add necessary env vars in the Environment
3. Go to Actions. Select "CI/CD" workflow. Select "Run workflow", choose the environment from step 1. Click "Run workflow."

# Requirements
## Environment
Each environment needs a minimum of

### Secrets
`DEPLOYMENT_ROLE_ARN` - oidc role with permissions to deploy

### Variables
`DEPLOYMENT_ENV_SECRET_NAME` - the AWS secrets manager secret name with the required env vars. See AWS Secrets Requirements for what env vars are needed.
`PROJECT_PREFIX` (TBD)
`STAGE` (TBD)

### Variables (Optional)
Indexes for each project to use to deploy. Can be branch name, release tag, commit hash, etc. Anything that works with `git checkout`

`VEDA_AUTH_GIT_INDEX`
`VEDA_BACKEND_GIT_INDEX`
`VEDA_DATA_AIRFLOW_GIT_INDEX`
`VEDA_FEATURES_API_GIT_INDEX`

#### AWS Secrets Requirements
```bash
AWS_ACCOUNT_ID=******
AWS_REGION=******
VPC_ID=******
SUBNET_TAGNAME=******
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