from app.daos.booking_dao import BookingDAO
from app.daos.db_helper import DBHelper
from app.daos.facility_dao import FacilityDAO


class BaseHelper:
    def __init__(self):
        self.db_helper = None
        self.facility_dao = None
        self.booking_dao = None

    def get_db_helper(self):
        if not self.db_helper:
            self.db_helper = DBHelper()
        return self.db_helper

    def get_facility_dao(self):
        if not self.facility_dao:
            self.facility_dao = FacilityDAO(self.get_db_helper())
        return self.facility_dao

    def get_booking_dao(self):
        if not self.booking_dao:
            self.booking_dao = BookingDAO(self.get_db_helper())
        return self.booking_dao
