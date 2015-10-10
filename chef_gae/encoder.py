from base64 import b64encode
from collections import OrderedDict
from datetime import datetime

from Crypto.Hash.SHA import SHA1Hash
from Crypto.PublicKey import RSA
from Crypto.Util import number

"""
cf. Chef API spec at https://docs.chef.io/api_chef_server.html
"""


def encode_headers(server_url, key, user_id, method, path, body=""):

    hashed_path = b64encode(SHA1Hash(path).digest())
    hashed_body = b64encode(SHA1Hash(body).digest())

    vk = RSA.importKey(key)

    canonical = OrderedDict()
    canonical["Method"] = method
    canonical["Hashed Path"] = hashed_path
    canonical["X-Ops-Content-Hash"] = hashed_body
    canonical["X-Ops-Timestamp"] = _process_datetime(datetime.utcnow())
    canonical["X-Ops-UserId"] = user_id

    headers = {
        "X-Ops-Server-API-Info": "1",
        "X-Chef-Version": "0.10.8",
        "X-Ops-Sign": "version=1.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Host": server_url.split("https://")[1] + ":443",
        "X-Ops-Timestamp": canonical["X-Ops-Timestamp"],
        "X-Ops-Content-Hash": canonical["X-Ops-Content-Hash"],
        "X-Ops-Userid":  canonical["X-Ops-UserId"],
        "Method": canonical["Method"],
        "Hashed Path": canonical["Hashed Path"]
    }

    msg = _emsa_pkcs1_v1_5_encode(_encode_message(canonical),
                                  number.size(vk.n) / 8)
    signature = b64encode(vk.decrypt(msg))

    _add_sig_to_headers(headers, signature)

    return headers


def _process_datetime(datetimeobj):
    return datetimeobj.isoformat().split(".")[0] + "Z"


def _add_sig_to_headers(headers, signature):
    base_header = "X-Ops-Authorization-"
    sl = 60  # chef api spec
    truncated_sigs = (signature[i:i+sl] for i in range(0, len(signature), sl))
    for j, string in enumerate(truncated_sigs):
        headers[base_header + str(j+1)] = string


def _encode_message(canonical):
    encd = "\n".join(["{}:{}".format(k, v) for k, v in canonical.iteritems()])
    return encd


def _emsa_pkcs1_v1_5_encode(m, em_len):
    padded_s = '\xff' * (em_len - len(m) - 3)
    return '\x00\x01' + padded_s + '\x00' + m
