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
import os
import requests

from dciauth.signature import Signature
from dciauth.request import AuthRequest

auth_request = AuthRequest(endpoint='/api/v1/jobs')
headers = Signature(request=auth_request).generate_headers('remoteci', 'client_id', 'secret')
r = requests.get('http://127.0.0.1:5000/api/v1/jobs', headers=headers)
assert r.status_code == 200

auth_request = AuthRequest(endpoint='/api/v1/jobs', params={"limit": 100})
headers = Signature(request=auth_request).generate_headers('remoteci', 'client_id', 'secret')
r = requests.get('http://127.0.0.1:5000/api/v1/jobs', params={"limit": 100}, headers=headers)
assert r.status_code == 200

payload = {"bar": "I'm ❤ bar"}
auth_request = AuthRequest(method="POST", endpoint='/api/v1/jobs', payload=payload,
                           headers={'content-type': 'application/json'})
headers = Signature(request=auth_request).generate_headers('remoteci', 'client_id', 'secret')
r = requests.post('http://127.0.0.1:5000/api/v1/jobs', headers=headers, json=payload)
assert r.status_code == 200

auth_request = AuthRequest(method="POST", endpoint='/api/v1/jobs', headers={'content-type': 'application/json'})
headers = Signature(request=auth_request).generate_headers('remoteci', 'client_id', 'secret')
file_path = os.path.join(os.path.dirname(__file__), 'test.txt')
files = {'file': open(file_path, 'rb')}
r = requests.post('http://127.0.0.1:5000/api/v1/jobs', headers=headers, files=files)
assert r.status_code == 200
