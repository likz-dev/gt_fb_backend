from app.daos.base_dao import BaseDAO, SCHEMA_NAME

TABLE_NAME = 'facility'

FIELD_ID = 'id'
FIELD_NAME = 'name'
FIELD_LEVEL = 'level'
FIELD_PAX = 'pax'


class FacilityDAO(BaseDAO):
    def get_facilities(self):
        query = f'SELECT * FROM {SCHEMA_NAME}.{TABLE_NAME}'
        try:
            return self.db_helper.execute(query)
        except Exception as error:
            print(error)
            print(f'Error while executing query: {query}')
            return False

# helper = DBHelper()
# dao = FacilityDAO(helper)
# print(dao.get_facilities())
