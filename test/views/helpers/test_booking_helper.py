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

    def test_get_all_user_booking(self):
        booking_helper = BookingHelper()

        booking_helper.get_db_helper = MagicMock()
        booking_helper.get_booking_dao().get_all_user_valid_bookings = MagicMock(
            return_value=[{'booking_id': 1, 'booked_by': 'test_user'}, {'booking_id': 2, 'booked_by': 'test_user'}])

        response = booking_helper.get_all_user_booking('test_user')

        assert response == {
            'bookings': [{'booking_id': 1, 'booked_by': 'test_user'}, {'booking_id': 2, 'booked_by': 'test_user'}]}

    def test_delete_user_booking(self):
        booking_helper = BookingHelper()

        booking_helper.get_db_helper = MagicMock()
        booking_helper.get_booking_dao().delete_user_booking = MagicMock(return_value=True)

        response = booking_helper.delete_user_booking(1)

        assert response == {'success': True}
