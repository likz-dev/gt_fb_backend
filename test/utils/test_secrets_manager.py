import unittest

import boto3
from moto import mock_secretsmanager

from app.utils.secrets_manager import SecretsManager


class TestSecretsManager(unittest.TestCase):
    @mock_secretsmanager
    def test_get_value(self):
        conn = boto3.client("secretsmanager", region_name="us-east-2")

        conn.create_secret(
            Name="secret-name", SecretString='{"key": "secret-password"}'
        )

        secrets_manager = SecretsManager()
        secret = secrets_manager.get_value('secret-name')

        assert secret.get('key') == 'secret-password'

        secrets_manager = SecretsManager()
        secret = secrets_manager.get_value('non-exist')

        assert secret is None
