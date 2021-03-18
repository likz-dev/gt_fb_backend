import json

import mock


@mock.patch('app.views.helpers.booking_helper.BookingHelper.create_booking')
@mock.patch('app.views.helpers.authentication.authenticate', return_value=True)
def test_post(_, mocked_create_booking, app, client):
    mocked_create_booking.return_value = 1
    res = client.post('/booking', json={
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


@mock.patch('app.views.helpers.booking_helper.BookingHelper.create_booking')
def test_post_unauthenticated(mocked_create_booking, app, client):
    mocked_create_booking.return_value = False
    res = client.post('/booking', json={
        'booking_name': 'booking1',
        'start_time': '2021/03/12 10:00',
        'end_time': '2021/03/12 12:00',
        'facility_id': 1,
        'booked_by': 'likz'
    })

    assert res.status_code == 500


@mock.patch('app.views.helpers.booking_helper.BookingHelper.get_all_user_booking')
@mock.patch('app.views.helpers.authentication.authenticate', return_value=True)
def test_get(_, mocked_get_all_user_booking, app, client):
    mocked_get_all_user_booking.return_value = [{'booking_id': 1, 'booked_by': 'test_user'},
                                                {'booking_id': 2, 'booked_by': 'test_user'}]
    res = client.get('/booking', query_string={'booked_by': 'test_user'})

    mocked_get_all_user_booking.assert_called_with('test_user')
    assert res.status_code == 200
    assert json.loads(res.get_data(as_text=True)) == [{'booking_id': 1, 'booked_by': 'test_user'},
                                                      {'booking_id': 2, 'booked_by': 'test_user'}]


@mock.patch('app.views.helpers.booking_helper.BookingHelper.get_all_user_booking')
def test_get_unauthenticated(mocked_get_all_user_booking, app, client):
    mocked_get_all_user_booking.return_value = [{'booking_id': 1, 'booked_by': 'test_user'},
                                                {'booking_id': 2, 'booked_by': 'test_user'}]
    res = client.delete('/booking', query_string={'booked_by': 'test_user'})

    assert res.status_code == 500


@mock.patch('app.views.helpers.booking_helper.BookingHelper.delete_user_booking')
@mock.patch('app.views.helpers.authentication.authenticate', return_value=True)
def test_delete(_, mocked_delete_user_booking, app, client):
    mocked_delete_user_booking.return_value = True
    res = client.delete('/booking', json={'booking_id': 1})

    mocked_delete_user_booking.assert_called_with('1')
    assert res.status_code == 200
    assert json.loads(res.get_data(as_text=True)) is True


@mock.patch('app.views.helpers.booking_helper.BookingHelper.delete_user_booking')
def test_delete_unauthenticated(mocked_delete_user_booking, app, client):
    mocked_delete_user_booking.return_value = 1
    res = client.delete('/booking', json={'booking_id': 1})

    assert res.status_code == 500
