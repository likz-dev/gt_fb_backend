import unittest
from datetime import date

import pytest
from freezegun import freeze_time
from mock import MagicMock
from app.entities.booking import Booking
from app.daos.booking_dao import BookingDAO


def do_insert_booking(db_helper):
    dao = BookingDAO(db_helper)

    booking = Booking(None, 'test booking', '2021/03/12 10:00', '2021/03/12 10:00', 'test_user', 1)
    response = dao.insert_booking(booking)

    query = f'''
INSERT INTO gt.booking (start_time, end_time, booked_by, facility_id, name)
VALUES (%s, %s, %s, %s, %s)
RETURNING booking_id
'''

    params = ('2021/03/12 10:00', '2021/03/12 10:00', 'test_user', 1, 'test booking')

    db_helper.connect.assert_called_once()
    db_helper.execute.assert_called_with(query, params=params)

    return response


def do_get_all_valid_bookings(db_helper):
    dao = BookingDAO(db_helper)

    response = dao.get_all_valid_bookings()

    query = f'''
SELECT * FROM gt.booking
WHERE start_time > '2021-03-10'
'''

    db_helper.connect.assert_called_once()
    db_helper.execute.assert_called_with(query)

    return response


class TestBookingDAO(unittest.TestCase):
    def test_insert_booking_valid(self):
        db_helper = MagicMock()
        db_helper.connection = None
        db_helper.execute = MagicMock(return_value=1)

        response = do_insert_booking(db_helper)

        assert response == 1

    def test_insert_booking_invalid(self):
        db_helper = MagicMock()
        db_helper.connection = None
        db_helper.execute = MagicMock(side_effect=Exception('sample error'))

        response = do_insert_booking(db_helper)

        assert response is False

    @freeze_time('2021-03-10 00:00:00')
    def test_get_all_valid_bookings_valid(self):
        db_helper = MagicMock()
        db_helper.connection = None
        db_helper.execute = MagicMock(return_value=[{
            'facility_id': '1',
            'name': 'booking_2',
            'start_time': date(2021, 3, 12),
            'end_time': date(2021, 4, 12),
            'booked_by': 'test_user',
        }])

        response = do_get_all_valid_bookings(db_helper)

        assert response == [{'bookedBy': 'test_user',
                             'end': '2021/04/12 00:00',
                             'facilityId': '1',
                             'isMe': False,
                             'start': '2021/03/12 00:00',
                             'text': 'booking_2'}]

    @freeze_time('2021-03-10 00:00:00')
    def test_get_all_valid_bookings_invalid(self):
        db_helper = MagicMock()
        db_helper.connection = None
        db_helper.execute = MagicMock(side_effect=Exception('sample_error'))

        response = do_get_all_valid_bookings(db_helper)

        assert response is False
