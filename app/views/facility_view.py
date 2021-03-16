from flask_restful import Resource

from app.views.helpers.facility_helper import FacilityHelper
from app.views.helpers.authentication import requires_auth


class FacilityView(Resource):
    """
    A class used to manage facilities and booking information API calls
    ...

    Methods
    -------
    get()
        Get all the facilities and booking.py information
    """

    def __init__(self):
        self.helper = FacilityHelper()

    @requires_auth
    def get(self):
        """Get all the facilities and booking information

        Returns
        -------
        dict
            dict object with facilities and booking.py information
        """
        return self.helper.get_all_facilities_and_bookings()
