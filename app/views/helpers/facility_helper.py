from datetime import datetime, timedelta

from app.views.helpers.base_helper import BaseHelper


class FacilityHelper(BaseHelper):
    def get_all_facilities_and_bookings(self):
        # Retrieve required records
        all_facilities = self.get_facility_dao().get_facilities()
        all_bookings = self.get_booking_dao().get_all_valid_bookings()

        # Close DB connection
        self.get_db_helper().close()

        # Create response structure
        start_date = datetime.date(datetime.now())
        end_date = start_date + timedelta(days=6)
        facilities_bookings = {
            'startDate': start_date.strftime("%Y/%m/%d"),
            'endDate': end_date.strftime("%Y/%m/%d"),
            'facilities': {}
        }

        # Populate facilities information
        for facility in all_facilities:
            facility_bookings = list(filter(lambda b: b.get('facilityId') == facility.get('id'), all_bookings))
            facilities_bookings.get('facilities')[facility.get('name')] = {
                'facilityId': facility.get('id'),
                'level': facility.get('level'),
                'pax': facility.get('pax'),
                'schedule': facility_bookings
            }

        return facilities_bookings

# h = FacilityHelper()
# print(h.get_all_facilities_and_bookings())
