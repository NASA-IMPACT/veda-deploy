import boto3
import json
from argparse import ArgumentParser

def get_cf_outs_as_env(stack_name, out_file):
    cf_client = boto3.client('cloudformation')
    response = cf_client.describe_stacks(StackName=stack_name)
    outputs = response["Stacks"][0]["Outputs"]
    with open(out_file, "a") as _env:
        for output in outputs:
            out_key = output["OutputKey"]
            out_value = output["OutputValue"]
            _env.write(f"{out_key}={out_value}\n")


def get_secrets_as_env(secret_id, out_file):
    sm_client = boto3.client('secretsmanager')
    response = sm_client.get_secret_value(
        SecretId=secret_id
    )
    secrets = json.loads(response['SecretString'])
    with open(out_file, "a") as _env:
        for out_key in secrets:
            out_value = secrets[out_key]
            _env.write(f"{out_key}={out_value}\n")


def generate_env_file(secret_id, stack_name=None, out_file=".env"):
    if stack_name:
        get_cf_outs_as_env(stack_name=stack_name, out_file=out_file)
    get_secrets_as_env(secret_id=secret_id, out_file=out_file)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Generate_env_file",
        description="Generate dot env file for deployment",
        epilog="Contact Marouane for extra help",
    )
    parser.add_argument(
        "--secret-id",
        dest="secret_id",
        help="AWS secret id",
        required=True,
    )
    parser.add_argument(
        "--stack-name",
        dest="stack_name",
        help="Cloudformation Stack name",
        default=None,
    )

    args = parser.parse_args()

    secret_id, stack_name = (
        args.secret_id,
        args.stack_name
    )
    generate_env_file(stack_name=stack_name, secret_id=secret_id, out_file=".env")

