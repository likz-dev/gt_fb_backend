SCHEMA_NAME = 'gt'


class BaseDAO:
    def __init__(self, db_helper):
        self.db_helper = db_helper
        if not db_helper.connection:
            db_helper.connect()

