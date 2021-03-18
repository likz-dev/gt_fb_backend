from flask import request
from flask_restful import Resource, reqparse

from app.entities.booking import Booking
from app.views.helpers.booking_helper import BookingHelper
from app.views.helpers.authentication import requires_auth

parser = reqparse.RequestParser()
parser.add_argument('booking_id', type=str)
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
    post()
        Creates a new booking
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
        print(f'booked_by {booked_by}')
        booking = Booking(None, booking_name, start_time, end_time, booked_by, facility_id)
        print(booking)
        return self.helper.create_booking(booking)

    @requires_auth
    def get(self):
        args = request.args
        booked_by = args['booked_by']
        print(f'booked_by {booked_by}')
        return self.helper.get_all_user_booking(booked_by)

    @requires_auth
    def delete(self):
        args = parser.parse_args()
        booking_id = args.get('booking_id')
        print(f'booking_id {booking_id}')
        return self.helper.delete_user_booking(booking_id)
