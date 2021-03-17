from app.views.helpers.base_helper import BaseHelper


class BookingHelper(BaseHelper):
    def create_booking(self, booking):
        response = self.get_booking_dao().insert_booking(booking)
        return {'success': response}

    def get_all_user_booking(self, booked_by):
        response = self.get_booking_dao().get_all_user_valid_bookings(booked_by)
        return {'bookings': response}

    def delete_user_booking(self, booking_id):
        response = self.get_booking_dao().delete_user_booking(booking_id)
        return {'success': response}

# h = FacilityHelper()
# print(h.get_all_facilities_and_bookings())
