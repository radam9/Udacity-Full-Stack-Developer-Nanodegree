import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = "dev-2bzp453o.eu.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "barista"

"""
AuthError Exception
A standardized way to communicate auth failure modes
"""


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Function to obtain the Access token from the Authorization Header


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    # Raise 401 error if authorization not found
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            },
            401,
        )
    # split the authorization at "space"
    parts = auth.split()
    # Raise 401 error if first part of authorization header doesnt equal Bearer
    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with 'Bearer'.",
            },
            401,
        )
    # Raise 401 error if authorization header is token is missing
    elif len(parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found"}, 401
        )
    # Raise 401 error if authorization token is in wrong format
    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be Bearer token",
            },
            401,
        )
    # return token
    token = parts[1]
    return token


# Function to check that a user has a certain permission.
def check_permissions(permission, payload):
    # Raise 401 error if the user doesn't have the provided persmission.
    if permission not in payload.get("permissions", []):
        raise AuthError(
            {"code": "unauthorized", "description": "Permission not found."}, 401,
        )
    # return True otherwise.
    return True


# Function to verify and decode the JWT token
def verify_decode_jwt(token):
    # Get public key from Auth0
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    # Extract header data from the token
    unverified_header = jwt.get_unverified_header(token)
    # Initialize RSA Key
    rsa_key = dict()
    # Raize 401 error if token header doesn't contain: kid
    if "kid" not in unverified_header:
        raise AuthError(
            {"code": "invalid_header", "description": "Authorization malformed."}, 401,
        )

    for key in jwks["keys"]:
        # Create the RSA Key of a match exists
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            # Validate the token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )
            return payload
        # Check for JWT errors
        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "Token expired."}, 401
            )
        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Incorrect claims. Please, check the audience and issuer.",
                },
                401,
            )
        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                400,
            )
    # Raise 400 error if Key not found
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the appropriate key.",
        },
        400,
    )


# Decorator function to add authorization
def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Extract token from authorization header
            token = get_token_auth_header()
            # Decode and Validate token
            payload = verify_decode_jwt(token)
            # Verify that user has the given permissions
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
