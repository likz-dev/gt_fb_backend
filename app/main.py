from flask import Flask, redirect, jsonify
from flask_restful import Api
from flask_cors import CORS

from app.views.booking_view import BookingView
from app.views.facility_view import FacilityView
from app.utils.secrets_manager import SecretsManager, SECRET_NAME_FLASK, SECRET_STRING_FLASK_SECRET_KEY
from authlib.integrations.flask_client import OAuth

# Get SecretsManager
from app.views.helpers.authentication import AuthError, auth_client_id, auth_client_secret, \
    auth_client_api_base_url

secrets_manager = SecretsManager()
flask_secrets = secrets_manager.get_value(SECRET_NAME_FLASK)

# Setup Flask application
app = Flask(__name__)
app.secret_key = flask_secrets.get(SECRET_STRING_FLASK_SECRET_KEY)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

# Setup Auth0
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=auth_client_id,
    client_secret=auth_client_secret,
    api_base_url=auth_client_api_base_url,
    access_token_url=f'{auth_client_api_base_url}/oauth/token',
    authorize_url=f'{auth_client_api_base_url}/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.route('/callback')
def callback_handling():
    print('/callback')
    # Handles response from token endpoint
    token = auth0.authorize_access_token()
    id_token = token.get('id_token')
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    email = userinfo['email']

    return redirect(f'http://gt-fb-frontend.s3-website-us-east-1.amazonaws.com/booking/?email={email}&token={id_token}')


@app.route('/login')
def login():
    print('/login')
    return auth0.authorize_redirect(redirect_uri='http://gt-pi-loadb-uvdhlamggmba-1268143812.us-east-1.elb.amazonaws.com/callback')


@app.route('/')
def home():
    return {'status': 'ok'}


# [GET] Get all facilities and bookings
api.add_resource(FacilityView, '/facility/all')
# [POST] Create booking
# [GET] Get all user bookings
# [DELETE] Delete booking
api.add_resource(BookingView, '/booking')

if __name__ == '__main__':
    app.run(debug=True)
