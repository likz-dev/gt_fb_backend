import unittest
import pytest

from mock import MagicMock
from app.views.helpers.facility_helper import FacilityHelper


def mock_db_helper():
    db_helper = MagicMock()
    return db_helper


def mock_facility_dao():
    return MagicMock(return_value=[
        {'id': 1, 'name': 'Marina', 'level': 12, 'pax': 2},
        {'id': 2, 'name': 'Jurong', 'level': 12, 'pax': 4},
        {'id': 3, 'name': 'Somerset', 'level': 12, 'pax': 4},
        {'id': 4, 'name': 'Clementi', 'level': 12, 'pax': 4},
        {'id': 5, 'name': 'Newton', 'level': 12, 'pax': 8}])


def mock_booking_dao():
    return MagicMock(return_value=[
        {'facilityId': 3, 'text': 'booking 7', 'start': '2021/03/10 14:00', 'end': '2021/03/10 18:00',
         'booked_by': 'likz', 'isMe': False},
        {'facilityId': 2, 'text': 'booking 4', 'start': '2021/03/10 16:00', 'end': '2021/03/10 17:00',
         'booked_by': 'likz', 'isMe': False},
        {'facilityId': 1, 'text': 'booking 6', 'start': '2021/03/10 16:00', 'end': '2021/03/10 17:00',
         'booked_by': 'likz', 'isMe': False},
        {'facilityId': 1, 'text': 'booking 2', 'start': '2021/03/10 20:00', 'end': '2021/03/10 23:00',
         'booked_by': 'likz', 'isMe': False},
        {'facilityId': 2, 'text': 'booking 5', 'start': '2021/03/10 09:00', 'end': '2021/03/10 12:00',
         'booked_by': 'likz', 'isMe': False},
        {'facilityId': 1, 'text': 'booking 9', 'start': '2021/03/11 20:00', 'end': '2021/03/11 23:00',
         'booked_by': 'likz', 'isMe': False},
        {'facilityId': 1, 'text': 'booking 3', 'start': '2021/03/11 20:00', 'end': '2021/03/11 23:00',
         'booked_by': 'likz', 'isMe': False},
        {'facilityId': 3, 'text': 'booking 8', 'start': '2021/03/10 20:00', 'end': '2021/03/10 23:00',
         'booked_by': 'likz', 'isMe': False}]
    )


@pytest.mark.freeze_time('2021-03-10 00:00:00')
class TestFacilityHelper(unittest.TestCase):
    def test_get_all_facilities_and_bookings(self):
        db_helper = MagicMock()

        facility_helper = FacilityHelper()

        facility_helper.get_db_helper = db_helper
        facility_helper.get_facility_dao().get_facilities = mock_facility_dao()
        facility_helper.get_booking_dao().get_all_valid_bookings = mock_booking_dao()

        response = facility_helper.get_all_facilities_and_bookings()

        facility_helper.get_facility_dao().get_facilities.assert_called_once()
        facility_helper.get_booking_dao().get_all_valid_bookings.assert_called_once()

        assert response == {'endDate': '2021/03/16',
                            'facilities': {'Clementi': {'facilityId': 4,
                                                        'level': 12,
                                                        'pax': 4,
                                                        'schedule': []},
                                           'Jurong': {'facilityId': 2,
                                                      'level': 12,
                                                      'pax': 4,
                                                      'schedule': [{'booked_by': 'likz',
                                                                    'end': '2021/03/10 17:00',
                                                                    'facilityId': 2,
                                                                    'isMe': False,
                                                                    'start': '2021/03/10 16:00',
                                                                    'text': 'booking 4'},
                                                                   {'booked_by': 'likz',
                                                                    'end': '2021/03/10 12:00',
                                                                    'facilityId': 2,
                                                                    'isMe': False,
                                                                    'start': '2021/03/10 09:00',
                                                                    'text': 'booking 5'}]},
                                           'Marina': {'facilityId': 1,
                                                      'level': 12,
                                                      'pax': 2,
                                                      'schedule': [{'booked_by': 'likz',
                                                                    'end': '2021/03/10 17:00',
                                                                    'facilityId': 1,
                                                                    'isMe': False,
                                                                    'start': '2021/03/10 16:00',
                                                                    'text': 'booking 6'},
                                                                   {'booked_by': 'likz',
                                                                    'end': '2021/03/10 23:00',
                                                                    'facilityId': 1,
                                                                    'isMe': False,
                                                                    'start': '2021/03/10 20:00',
                                                                    'text': 'booking 2'},
                                                                   {'booked_by': 'likz',
                                                                    'end': '2021/03/11 23:00',
                                                                    'facilityId': 1,
                                                                    'isMe': False,
                                                                    'start': '2021/03/11 20:00',
                                                                    'text': 'booking 9'},
                                                                   {'booked_by': 'likz',
                                                                    'end': '2021/03/11 23:00',
                                                                    'facilityId': 1,
                                                                    'isMe': False,
                                                                    'start': '2021/03/11 20:00',
                                                                    'text': 'booking 3'}]},
                                           'Newton': {'facilityId': 5,
                                                      'level': 12,
                                                      'pax': 8,
                                                      'schedule': []},
                                           'Somerset': {'facilityId': 3,
                                                        'level': 12,
                                                        'pax': 4,
                                                        'schedule': [{'booked_by': 'likz',
                                                                      'end': '2021/03/10 18:00',
                                                                      'facilityId': 3,
                                                                      'isMe': False,
                                                                      'start': '2021/03/10 14:00',
                                                                      'text': 'booking 7'},
                                                                     {'booked_by': 'likz',
                                                                      'end': '2021/03/10 23:00',
                                                                      'facilityId': 3,
                                                                      'isMe': False,
                                                                      'start': '2021/03/10 20:00',
                                                                      'text': 'booking 8'}]}},
                            'startDate': '2021/03/10'}
