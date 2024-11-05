#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import json
import os
import requests

from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

from dciauth.signature import HmacAuthBase
from dciauth.v2.headers import generate_headers


# #################### TEST HMAC V2 #################################

headers = generate_headers(
    {"host": "127.0.0.1:65432", "endpoint": "/api/v1/jobs"},
    {"access_key": "remoteci/client_id", "secret_key": "secret"},
)
headers.update({"Content-Type": "application/json"})
r = requests.get("http://127.0.0.1:65432/api/v1/jobs", headers=headers)
assert r.status_code == 200

params = {"limit": 100}
headers = generate_headers(
    {"host": "127.0.0.1:65432", "endpoint": "/api/v1/jobs", "params": params},
    {"access_key": "remoteci/client_id", "secret_key": "secret"},
)
headers.update({"Content-Type": "application/json"})
r = requests.get("http://127.0.0.1:65432/api/v1/jobs", params=params, headers=headers)
assert r.status_code == 200

data = json.dumps({"bar": "I'm ❤ bar"})
headers = generate_headers(
    {
        "method": "POST",
        "host": "127.0.0.1:65432",
        "endpoint": "/api/v1/jobs",
        "data": data,
    },
    {"access_key": "remoteci/client_id", "secret_key": "secret"},
)

headers.update({"Content-Type": "application/json"})
r = requests.post("http://127.0.0.1:65432/api/v1/jobs", data=data, headers=headers)
assert r.status_code == 200

payload = {"bar": "I'm ❤ bar"}
headers = generate_headers(
    {
        "method": "POST",
        "host": "127.0.0.1:65432",
        "endpoint": "/api/v1/jobs",
        "payload": payload,
    },
    {"access_key": "remoteci/client_id", "secret_key": "secret"},
)
r = requests.post("http://127.0.0.1:65432/api/v1/jobs", headers=headers, json=payload)
assert r.status_code == 200

headers = generate_headers(
    {"method": "POST", "host": "127.0.0.1:65432", "endpoint": "/api/v1/jobs"},
    {"access_key": "remoteci/client_id", "secret_key": "secret"},
)
file_path = os.path.join(os.path.dirname(__file__), "test.xml")
files = {"file": ("test.xml", open(file_path, "rb"), "application/junit")}
r = requests.post("http://127.0.0.1:65432/api/v1/jobs", headers=headers, files=files)
assert r.status_code == 200

file_path = os.path.join(os.path.dirname(__file__), "run.sh.tgz")
headers = generate_headers(
    {
        "method": "POST",
        "host": "127.0.0.1:65432",
        "endpoint": "/api/v1/jobs",
        "data": open(file_path, "rb").read(),
    },
    {"access_key": "remoteci/client_id", "secret_key": "secret"},
)
r = requests.post(
    "http://127.0.0.1:65432/api/v1/jobs", headers=headers, data=open(file_path, "rb")
)
assert r.status_code == 200

# nrt dciclient url.path used in dciclient generated headers is already encoded
headers = generate_headers(
    {
        "method": "GET",
        "endpoint": "/api/v1/files/AppStream/ppc64le/os/Packages/passt-0%5E20230222.g4ddbcb9-1.el9.ppc64le.rpm",
        "params": {},
        "host": "127.0.0.1:65432",
        "data": "",
    },
    {"access_key": "remoteci/client_id", "secret_key": "secret"},
)
headers.update({"Content-Type": "application/json"})
r = requests.get(
    "http://127.0.0.1:65432/api/v1/files/AppStream/ppc64le/os/Packages/passt-0^20230222.g4ddbcb9-1.el9.ppc64le.rpm",
    headers=headers,
)
assert r.status_code == 200


# #################### TEST HMAC #################################

auth = HmacAuthBase(
    access_key="remoteci/client_id",
    secret_key="secret",
    region="BHS3",
    service="api",
    service_key="dci2_request",
    algorithm="DCI2-HMAC-SHA256",
)
response = requests.get("http://127.0.0.1:65432/api/v1/jobs", auth=auth)
assert response.status_code == 200

# #################### TEST AWS #################################


class Credentials:
    token = None

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key


# nrt space in params not escaped correctly

params = {
    "query": "((components.type=ocp) and (components.version=~4.14.30*))",
    "offset": "1",
    "limit": "2",
    "sort": "-created_at",
}
request = AWSRequest(
    "GET",
    "/api/v1/jobs",
    params=params,
    headers={"Host": "127.0.0.1"},
)
SigV4Auth(Credentials("remoteci/access_key", "secret"), "api", "BHS3").add_auth(request)

response = requests.get(
    "http://127.0.0.1:65432/api/v1/jobs",
    params=params,
    headers=request.headers,
)
assert response.status_code == 200
