import json

import mock


@mock.patch('app.views.helpers.booking_helper.BookingHelper.create_booking')
def test_index(mocked_create_booking, app, client):
    mocked_create_booking.return_value = 1
    res = client.post('/book', json={
        'booking_name': 'booking1',
        'start_time': '2021/03/12 10:00',
        'end_time': '2021/03/12 12:00',
        'facility_id': 1,
        'booked_by': 'likz'
    })

    mocked_create_booking.assert_called_once()
    assert res.status_code == 200
    expected = 1
    assert json.loads(res.get_data(as_text=True)) == expected
