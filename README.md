# What?
Deploy full VEDA stack easily.

# How to deploy?
## Steps
1. Create a new Github Environment in the repository. See [Requirements](#requirements) on details of creating the environment.
2. Add necessary env vars in the Environment
3. Go to Actions. Select "Dispatch" workflow. Select "Run workflow", choose the environment from step 1. Select the components to dispatch and then "Run workflow."
4. (Optional) To add a new component in veda-deploy see [Add New Components](#add-new-components).

# Requirements
## Environment
Each Github Environment needs a minimum of:

### Secrets
`DEPLOYMENT_ROLE_ARN` - oidc role with permissions to deploy

### Variables
`DEPLOYMENT_ENV_SECRET_NAME` - the AWS secrets manager secret name with the required component env vars. See [AWS Secrets Requirements](#aws-secrets-requirements) for what env vars are needed.

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

`SM2A_ENVS_DEPLOYMENT_SECRET_NAME` - the AWS secrets manager secret name with env vars specific to a SM2A deployment. [AWS Secrets Requirements for SM2A](#aws-secrets-requirements-for-sm2a) for what env vars are needed.

#### AWS Secrets Requirements for SM2A
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

Git Ref for each project to use to deploy. Can be branch name, release tag or commit hash. Anything that works with `git checkout`.

```bash
VEDA_AUTH_GIT_REF=<target branch name or tag default to main>
VEDA_BACKEND_GIT_REF=<target branch name or tag default to main>
VEDA_DATA_AIRFLOW_GIT_REF=<target branch name or tag default to main>
VEDA_FEATURES_API_GIT_REF=<target branch name or tag default to main>
VEDA_SM2A_DATA_AIRFLOW_GIT_REF=<target branch name or tag default to main>
```

`DEPLOY_SM2A=true` - whether to deploy SM2A

# Add New Components
> [!IMPORTANT]
> This section is intended to expand an existing configured environment, see [How to Deploy](#how-to-deploy) to start from scratch. Please read the full overview before starting; some steps overlap.

## Overview
- [Add deployment action to component github repository](#add-deployment-action-to-component-github-repository)

- [Store `.env` configuration in AWS Secrets Manager](#store-env-configuration-in-aws-secrets-manager)


- [Add component submodule to veda-deploy](#add-component-submodule-to-veda-deploy)

- [Extend composite dispatched deployment action with an optional component job that uses the component submodule and environment secret](#extend-composite-dispatched-deployment-action)

- [Add new component release version and environment secret name to veda-deploy environment(s)](#add-new-component-release-version-and-environment-secret-name-to-veda-deploy-environments)

- [Configure domain and custom routes](#configure-domain-and-custom-routes)

## Add deployment action to component github repository
Dispatches from veda-deploy are composed of deployment actions imported from github submodules. The management of all configuration, testing, and deployment concerns is managed within the component's github repository (not in veda-deploy).

Create a new `cdk-deploy/action.yml` in the component project's repository. On a dispatch the configured release version of the project will be checked out and executed on the veda-deploy github runner. 

To keep the components modular, each action should include all necessary steps for deployment including Python and Node setup steps. While veda-deploy uses the same runner to deploy all components, it should not be assumed that the runner already has all needed installations and environment configuration from other components (unless a dependency is configured for the job using needs: {upstream-job-name}).

> [!TIP]
> Most deployments require [custom environment configuration](#store-env-configuration-in-aws-secrets-manager) that can be retrieved from the AWS Secrets Manager for the deployment. See [veda-backend/scripts/get-env.sh](https://github.com/NASA-IMPACT/veda-backend/blob/develop/scripts/get-env.sh) for an example environmennt configuration utility.

### Examples
- Veda-auth [cdk-deploy/action.yml](https://github.com/NASA-IMPACT/veda-auth/blob/main/.github/actions/cdk-deploy/action.yml) provides a simple example of adding configuration from an AWS Secrets Manager secret and running `cdk deploy` for an imported submodule.
- Veda-backend [cdk-deploy/action.yml](https://github.com/NASA-IMPACT/veda-backend/blob/develop/.github/actions/cdk-deploy/action.yml) contains logic to run tests before deploying components.
- This [CICD workflow in veda-backend](https://github.com/NASA-IMPACT/veda-backend/blob/develop/.github/workflows/cicd.yml) demonstrates importing the cdk-deploy/action on a merge event to test the deployment in a dev enviornment.

## Store `.env` configuration in AWS Secrets Manager
Custom configurations like RDS instance size as well as AWS environment specific configuration like VPC ID and a Permission Boundary Policy Name should be added to a key-value secret that will be loaded into the GitHub runner environment by your action. This secret should be stored in the target AWS account where the component will be deployed.

> [!NOTE]
> 1. For higher security environments, a permissions boundary policy needs to be identified. 
> 2. The qualifier of the CDK Toolkit bootstrapped for the target environment must be provided if not using the default toolkit.

### Sample environment variables
```
VPC_ID=******
PERMISSIONS_BOUNDARY_POLICY_NAME=******
STAGE=******
BOOTSTRAP_QUALIFIER=******
```

## Add component submodule to veda-deploy
Add your component submodule to [.gitmodules](https://github.com/NASA-IMPACT/veda-deploy/blob/dev/.gitmodules). Submodules are checked out on the GitHub runner when your component is deployed.

```
[submodule "my-project"]
	path = my-project
	url = git@github.com:NASA-IMPACT/my-project.git
```

## Extend composite dispatched deployment action

1. Add a [dispatch flag in .github/workflows/dispatch.yml](https://github.com/NASA-IMPACT/veda-deploy/blob/dev/.github/workflows/dispatch.yml#L66) for the component you are adding. As in `DEPLOY_MY_COMPONENT: ${{ github.event.inputs.DEPLOY_MY_COMPONENT }}`
2. Update the [dispatch message](https://github.com/NASA-IMPACT/veda-deploy/blob/dev/.github/workflows/dispatch.yml#L46) to include your component. Eventually this will get too long and will need some thought but it is currently helpful to filter the actions and identify specific dispatches.
3. Transfer the above dispatch information to the [.github/workflows/deploy.yml workflow_call](https://github.com/NASA-IMPACT/veda-deploy/blob/dev/.github/workflows/deploy.yml#L10). The deploy action is called after the environment is set by the dispatch and for production environments is only executed after the dispatch has been approved by a maintainer.
4. Add a new [named job to deploy.yml](https://github.com/NASA-IMPACT/veda-deploy/blob/dev/.github/workflows/deploy.yml#L218) that checks the condition the deployment condition for the component and, when true, checks out the deployment action from the component's GitHub repository and passes in any relevant information like the configuration environment secret name.

## Add new component release version and environment secret name to veda-deploy environment(s)
Adding new deployment environments requires admin permissions for this veda-deploy repository. New environments are added by entering project settings and selecting `Environments` from the code and automation menu. The environment naming convention is `<aws-account>-<stage>`, i.e. `smce-staging`. As more environments are added this convention will need to be updated.

In the Environment variables for the instance you are dispatching your component to, add a new variable with the GitHub reference to the release you want to deploy. It is best practice to refer to a release tag but a branch name or commit hash can also be used.

`MY_COMPONENT_GIT_REF=v1.0`

## Configure domain and custom routes
VEDA platform components include options for custom subdomains and custom root paths. Coordinate how your custom resource should be configured with the team maintaining the target environment you are deploying to.