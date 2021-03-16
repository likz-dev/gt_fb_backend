import json
import ssl
import urllib
from functools import wraps
from urllib.request import urlopen

from jose import jwt
from flask import request

from app.utils.secrets_manager import SecretsManager, SECRET_NAME_AUTH0, SECRET_STRING_AUTH0_CLIENT_ID, \
    SECRET_STRING_AUTH0_CLIENT_SECRET, SECRET_STRING_AUTH0_API_BASE_URL

ALGORITHMS = ["RS256"]

secrets_manager = SecretsManager()
auth0_secrets = secrets_manager.get_value(SECRET_NAME_AUTH0)
auth_client_id = auth0_secrets.get(SECRET_STRING_AUTH0_CLIENT_ID)
auth_client_secret = auth0_secrets.get(SECRET_STRING_AUTH0_CLIENT_SECRET)
auth_client_api_base_url = auth0_secrets.get(SECRET_STRING_AUTH0_API_BASE_URL)


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_authorization_header():
    return request.headers.get("Authorization", None)


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = get_authorization_header()
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                             "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must start with"
                             " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must be"
                             " Bearer token"}, 401)

    token = parts[1]
    return token


def get_well_known_jwks():
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen(f'{auth_client_api_base_url}/.well-known/jwks.json')
    return response.read().decode('utf-8')

def authenticate():
    token = get_token_auth_header()
    jsonurl = get_well_known_jwks()
    jwks = json.loads(jsonurl)
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=auth_client_id,
                issuer=f'{auth_client_api_base_url}/'
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                             "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                             "description":
                                 "incorrect claims,"
                                 "please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                             "description":
                                 "Unable to parse authentication"
                                 " token."}, 401)

        # _request_ctx_stack.top.current_user = payload
        return True
    raise AuthError({"code": "invalid_header",
                     "description": "Unable to find appropriate key"}, 401)


def requires_auth(f):
    """Determines if the Access Token is valid
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if authenticate():
            return f(*args, **kwargs)

    return decorated
