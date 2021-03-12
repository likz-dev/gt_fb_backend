import unittest

from mock import MagicMock
from app.daos.facility_dao import FacilityDAO


class TestFacilityDAO(unittest.TestCase):
    def test_get_facilities(self):
        db_helper = MagicMock()
        db_helper.connection = None
        db_helper.execute = MagicMock(return_value=['fac1', 'fac2'])

        dao = FacilityDAO(db_helper)

        response = dao.get_facilities()

        query = f'SELECT * FROM gt.facility'

        db_helper.connect.assert_called_once()
        db_helper.execute.assert_called_with(query)

        assert response == ['fac1', 'fac2']

