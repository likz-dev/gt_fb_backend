import json

import mock


@mock.patch('app.views.helpers.facility_helper.FacilityHelper.get_all_facilities_and_bookings')
@mock.patch('app.views.helpers.authentication.authenticate', return_value=True)
def test_facility_all(_, mocked_get_all_facilities_and_bookings, app, client):
    mocked_get_all_facilities_and_bookings.return_value = ['fac1', 'fac2']
    res = client.get('/facility/all')
    assert res.status_code == 200
    expected = ['fac1', 'fac2']
    assert json.loads(res.get_data(as_text=True)) == expected


@mock.patch('app.views.helpers.facility_helper.FacilityHelper.get_all_facilities_and_bookings')
def test_facility_all_unauthenticated(mocked_get_all_facilities_and_bookings, app, client):
    res = client.get('/facility/all')

    assert res.status_code == 500
