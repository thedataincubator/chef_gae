from datetime import datetime

from mock import patch
# Pychef
import chef.auth
from chef.rsa import Key

# Our chef
from chef_gae.encoder import encode_headers, _process_datetime
from chef_gae.tests.sample_data import RSA_KEY, USER_NAME, ORG_NAME, SERVER_URL

timestamp = datetime.utcnow()


@patch('chef_gae.encoder._process_datetime',
       return_value=_process_datetime(timestamp))
def test_encode_headers(patched_datetime):
    k = Key(RSA_KEY)
    http_method = 'GET'
    path = "/organizations/" + \
           ORG_NAME + \
           "/nodes"
    body = ""
    user_id = USER_NAME
    host = SERVER_URL.split("https://")[1] + ":443"

    official_headers = chef.auth.sign_request(k, http_method,
                                              path, body, host,
                                              timestamp, user_id)

    our_headers = encode_headers(SERVER_URL, RSA_KEY, user_id,
                                 http_method, path, body)

    # these are set later by Chef API, we care about RSA functionality
    our_headers.pop("X-Chef-Version")
    our_headers.pop("X-Ops-Server-API-Info")
    our_headers.pop("Method")
    our_headers.pop("Accept")
    our_headers.pop("Host")
    our_headers.pop("Hashed Path")
    our_headers.pop("Content-Type")

    for header in our_headers:
        lowered = header.lower()
        assert official_headers[lowered] == our_headers[header]
