import unittest

from mock import MagicMock
from app.entities.booking import Booking
from app.views.helpers.booking_helper import BookingHelper


class TestBookingHelper(unittest.TestCase):
    def test_insert_booking(self):
        booking_helper = BookingHelper()

        booking_helper.get_db_helper = MagicMock()
        booking_helper.get_booking_dao().insert_booking = MagicMock(return_value=1)

        booking = Booking(None, 'test booking', '2021/03/12 10:00', '2021/03/12 10:00', 'test_user', 1)
        response = booking_helper.create_booking(booking)

        assert response == {'success': 1}
