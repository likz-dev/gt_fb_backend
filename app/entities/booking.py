class Booking:
    def __init__(self, booking_id, name, start_time, end_time, booked_by, facility_id):
        self.booking_id = booking_id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.booked_by = booked_by
        self.facility_id = facility_id
