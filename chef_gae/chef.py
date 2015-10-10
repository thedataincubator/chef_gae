import json

import requests

from .encoder import encode_headers


class Chef(object):

    def __init__(self, server_url, rsa_key, chef_username, org_name):
        """
        A thin wrapper for the Chef Server API.

        :param server_url - the https URL of your chef server.
        :param rsa_key - the RSA private key of an authorized client.
        :param chef_username - the username of the authorized client.
        :param org_name - the base organization name.
        """

        self.rsa_key = rsa_key.strip()
        self.org_name = org_name
        self.chef_username = chef_username

        self.server_url = server_url
        if not self.server_url.startswith("https"):
            raise ValueError("You must provide an https URL.")

        # we want https://chef.abc.com, not https://chef.abc.com/
        if self.server_url[-1] == "/":
            self.server_url = server_url[:-1]

    def get_endpoint(self, method, endpoint, data=None):
        """Hits an endpoint, returns a dictionary of attributes as defined in
        the chef API docs.

        :param method - the HTTP method you'd like to use.
        :param endpoint - the endpoint you'd like to hit, starting with a /
        :param data - if the endpoint requires data (ie POST or PUT request),
                      this should be a dictionary of JSON-serializable things,
                      with the appropriate args.

        :returns a python dictionary or list.
        """

        if endpoint[0] != "/":
            raise ValueError("Endpoint needs leading / eg /nodes, not nodes")

        final_endpoint = "/organizations/" + \
                         self.org_name + \
                         endpoint\

        if method == 'GET':
            data_str = ''
        else:
            data_str = json.dumps(data)

        headers = encode_headers(self.server_url,
                                 self.rsa_key,
                                 self.chef_username,
                                 method,
                                 final_endpoint,
                                 data_str)

        requests_method = getattr(requests, method.lower())
        return requests_method(self.server_url + final_endpoint,
                               headers=headers,
                               data=data_str,
                               verify=False).json()
