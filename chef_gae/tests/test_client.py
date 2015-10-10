import json

import responses

import chef_gae
from chef_gae.tests.sample_data import SERVER_URL, ORG_NAME, RSA_KEY, USER_NAME


@responses.activate
def test_client_request():

    node1_url = "{}/organizations/{}/nodes/node1".format(SERVER_URL, ORG_NAME)
    resp_json = '{"node1": "' + node1_url + '"}'

    responses.add(responses.GET,
                  "{}/organizations/{}/nodes".format(SERVER_URL, ORG_NAME),
                  body=resp_json,
                  content_type='application/json')

    cli = chef_gae.Chef(SERVER_URL, RSA_KEY, USER_NAME, ORG_NAME)
    resp = cli.get_endpoint("GET", "/nodes")
    assert json.dumps(resp) == resp_json
