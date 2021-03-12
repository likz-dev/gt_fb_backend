from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from app.views.booking_view import BookingView
from app.views.facility_view import FacilityView

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)


@app.route('/')
def home():
    return {'status': 'ok'}


# [GET] Get all facilities and bookings
api.add_resource(FacilityView, '/facility/all')
# [POST] Create booking
api.add_resource(BookingView, '/book')

if __name__ == '__main__':
    app.run(debug=True)
