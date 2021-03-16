from flask_restful import Resource, reqparse

from app.entities.booking import Booking
from app.views.helpers.booking_helper import BookingHelper
from app.views.helpers.authentication import requires_auth

parser = reqparse.RequestParser()
parser.add_argument('booking_name', type=str)
parser.add_argument('start_time', type=str)
parser.add_argument('end_time', type=str)
parser.add_argument('facility_id', type=int)
parser.add_argument('booked_by', type=str)


class BookingView(Resource):
    """
    A class used to manage booking information API calls
    ...

    Methods
    -------
    get()
        Get all the facilities and booking.py information
    """

    def __init__(self):
        self.helper = BookingHelper()

    @requires_auth
    def post(self):
        args = parser.parse_args()
        booking_name = args.get('booking_name')
        start_time = args.get('start_time')
        end_time = args.get('end_time')
        facility_id = args.get('facility_id')
        booked_by = args.get('booked_by')
        booking = Booking(None, booking_name, start_time, end_time, booked_by, facility_id)
        return self.helper.create_booking(booking)
