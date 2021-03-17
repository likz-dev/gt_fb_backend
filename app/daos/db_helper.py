import psycopg2
import psycopg2.extras
from psycopg2._psycopg import Error

from app.utils.secrets_manager import SecretsManager, SECRET_NAME_DATABASE, SECRET_STRING_DATABASE_USERNAME, \
    SECRET_STRING_DATABASE_PASSWORD, SECRET_STRING_DATABASE_NAME, SECRET_STRING_DATABASE_HOST


class DBHelper:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            secrets_manager = SecretsManager()
            db_credentials = secrets_manager.get_value(SECRET_NAME_DATABASE)
            host = db_credentials.get(SECRET_STRING_DATABASE_HOST)
            name = db_credentials.get(SECRET_STRING_DATABASE_NAME)
            username = db_credentials.get(SECRET_STRING_DATABASE_USERNAME)
            password = db_credentials.get(SECRET_STRING_DATABASE_PASSWORD)

            self.connection = psycopg2.connect(f'host={host} dbname={name} user={username} password={password}')
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except (Exception, Error) as error:
            print('Error while connecting to PostgreSQL', error)
            self.connection = None
            self.cursor = None

    def execute(self, query, params=None):
        try:
            print(self.cursor.mogrify(query, params))
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as error:
            raise error

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
        except Exception as _:
            self.cursor = None
            self.connection = None
