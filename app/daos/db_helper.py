import psycopg2
import psycopg2.extras
from psycopg2._psycopg import Error

class DBHelper:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect('db_credentials')
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except (Exception, Error) as error:
            print('Error while connecting to PostgreSQL', error)
            self.connection = None
            self.cursor = None

    def execute(self, query, params=None):
        try:
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
