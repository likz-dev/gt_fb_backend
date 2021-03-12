from app.views.helpers.base_helper import BaseHelper


class BookingHelper(BaseHelper):
    def create_booking(self, booking):
        response = self.get_booking_dao().insert_booking(booking)
        return {'success': response}

# h = FacilityHelper()
# print(h.get_all_facilities_and_bookings())
