import argparse
import json
import re

import boto3

_ARG_REGEX = r'--(.*)=(.*)'


def update_secret_with_inputs():
    parser = argparse.ArgumentParser(
        description="""
        **WARNING** This is destructive, if an input is provided that's name already exists in
        the AWS Secret, it will be overridden.

        ---

        Takes in N inputs in the form --input-name=value and inserts them into the provided
        AWS SecretsManager secret. If a prefix is provided, it will be appended to the input name

        This assumes that the SecretString value is a stringified JSON object

        For example, with no prefix, an input of --my-secret-item=hello will be inserted as:

        MY_SECRET_ITEM=hello

        Whereas with a prefix of MY_PREFIX, an input of --my-secret-item=hello will be inserted as:

        MY_PREFIX_MY_SECRET_ITEM=hello
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--prefix", default="", required=False, help="Optional prefix to append to inputs names")
    parser.add_argument("--secret-id", required=True, help="The ARN or Name of the AWS SecretsManager secret to update")

    known_args, unknown_args = parser.parse_known_args()

    if not (secret_id := known_args.secret_id):
        raise Exception("An AWS SecretsManager secret id is required")

    values_to_add_to_secret = {}

    for arg in unknown_args:
        if match := re.match(_ARG_REGEX, arg):
            secret_entry_name = known_args.prefix.upper() + match.group(1).upper().replace("-", '_')
            secret_entry_value = match.group(2)
            values_to_add_to_secret[secret_entry_name] = secret_entry_value

    secrets_manager_client = boto3.client("secretsmanager")
    secret = secrets_manager_client.get_secret_value(SecretId=secret_id)
    secret_value = json.loads(secret["SecretString"])

    for k, v in values_to_add_to_secret.items():
        secret_value[k] = v

    secrets_manager_client.put_secret_value(SecretId=secret_id, SecretString=json.dumps(secret_value))


if __name__ == "__main__":
    update_secret_with_inputs()
