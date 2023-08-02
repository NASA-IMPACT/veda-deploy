import json
import sys
import re
import boto3

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Provide command line args in the form of: python update_secrets.py cdk-outputs.json aws_secret_name"
        )
        exit()

    cdk_output = sys.argv[1]
    secret_name = sys.argv[2]

    mapping = {
        "pgstacsecretname": "STAC_DB_SECRET_NAME",
        "securitygroupid": "STAC_DB_SECURITY_GROUP_ID",
        "rasterapi": "RASTER_URL",
        "stacapi": "STAC_URL",
        "vpcid": "STAC_DB_VPC_ID",
        "userpoolid": "USERPOOL_ID",
        "sdkclientid": "CLIENT_ID",
        "workflowssecretoutput": "COGNITO_APP_SECRET",
    }

    new_secrets = dict()
    secrets = json.load(open(cdk_output))

    for stack_name, secrets in secrets.items():
        for k, v in secrets.items():
            for mapping_key in mapping.keys():
                if re.compile(mapping_key).match(k):
                    new_secrets[mapping[mapping_key]] = v

    client = boto3.client("secretsmanager")

    existing_secret = json.loads(
        client.get_secret_value(SecretId=secret_name).get("SecretString")
    )

    updated_secret = {**existing_secret, **new_secrets}

    client.put_secret_value(SecretId=secret_name, SecretString=json.dumps(updated_secret))
