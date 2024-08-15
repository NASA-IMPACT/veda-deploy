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
Git Ref for each project to use to deploy. Can be branch name, release tag or commit hash. Anything that works with `git checkout`.

`VEDA_AUTH_GIT_REF`
`VEDA_BACKEND_GIT_REF`
`VEDA_DATA_AIRFLOW_GIT_REF`
`VEDA_FEATURES_API_GIT_REF`

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


#### AWS Secrets Requirements For SM2A
```bash
AIRFLOW_UID=******
PREFIX=******
VPC_ID=******
STATE_BUCKET_NAME=******
STATE_BUCKET_KEY=******
STATE_DYNAMO_TABLE=******
PRIVATE_SUBNETS_TAGNAME=******
PUBLIC_SUBNETS_TAGNAME=******
AIRFLOW_FERNET_KEY=******
AIRFLOW_DB_NAME=******
AIRFLOW_DB_USERNAME=******
AIRFLOW_DB_PASSWORD=******
PERMISSION_BOUNDARIES_ARN=******
DOMAIN_NAME=******
STAGE=******
TF_VAR_gh_app_client_id=******
TF_VAR_gh_app_client_secret=******
TF_VAR_gh_team_name=******
TF_VAR_subdomain=******
```
##### Github variables
Add these variables to Github environment variables 
```bash
DEPLOY_SM2A=true
SM2A_ENVS_DEPLOYMENT_SECRET_NAME=<SM2A deploymnet secrets>
VEDA_SM2A_DATA_AIRFLOW_GIT_REF=<target branch name or tag default to main>
```
