import json

import boto3
from botocore.exceptions import ClientError

SECRET_NAME_DATABASE = 'RDSCredentials'
SECRET_NAME_AUTH0 = 'Auth0Secrets'
SECRET_NAME_FLASK = 'FlaskSecrets'

SECRET_STRING_DATABASE_HOST = 'db_host'
SECRET_STRING_DATABASE_NAME = 'db_name'
SECRET_STRING_DATABASE_USERNAME = 'db_username'
SECRET_STRING_DATABASE_PASSWORD = 'db_password'
SECRET_STRING_AUTH0_CLIENT_ID = 'client_id'
SECRET_STRING_AUTH0_CLIENT_SECRET = 'client_secret'
SECRET_STRING_AUTH0_API_BASE_URL = 'api_base_url'
SECRET_STRING_FLASK_SECRET_KEY = 'secret_key'


class SecretsManager:
    """Encapsulates Secrets Manager functions."""

    def __init__(self):
        self.secretsmanager_client = boto3.client('secretsmanager')

    def get_value(self, name):
        """
        Gets the value of a secret.

        :param name: The name of the secret to retrieve
        :return: The value of the secret. When the secret is a string, the value is
                 contained in the `SecretString` field. When the secret is bytes,
                 it is contained in the `SecretBinary` field.
        """
        if name is None:
            raise ValueError

        try:
            kwargs = {'SecretId': name}
            response = self.secretsmanager_client.get_secret_value(**kwargs)
        except ClientError:
            return None
        else:
            return json.loads(response.get('SecretString'))
