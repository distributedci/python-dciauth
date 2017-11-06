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
import requests

from dciauth import signature

secret = "Y4efRHLzw2bC2deAZNZvxeeVvI46Cx8XaLYm47Dc019S6bHKejSBVJiGAfHbZLIN"

method = "GET"
content_type = 'application/json'
url = "/api/v1/jobs"
params = {'limit': 100, 'offset': 1}
payload = {}
headers = signature.generate_headers_with_secret(
    secret,
    method,
    content_type,
    url,
    params,
    payload)
r = requests.get('http://127.0.0.1:5000%s' % url, params=params, headers=headers)
print(headers)
print(r.status_code)
print(r.text)
print(r.url)

params = {"foo": "I ❤ bar"}
headers = signature.generate_headers_with_secret(
    secret,
    method,
    content_type,
    url,
    params,
    payload)
r = requests.get('http://127.0.0.1:5000%s' % url, params=params, headers=headers)
print(headers)
print(r.status_code)
print(r.url)

method = "POST"
content_type = 'application/json'
url = "/api/v1/jobs"
payload = {"bar": "I'm ❤ bar"}
params = {"heart": "❤"}
headers = signature.generate_headers_with_secret(
    secret,
    method,
    content_type,
    url,
    params,
    payload)
r = requests.post('http://127.0.0.1:5000%s' % url, params=params, headers=headers, json=payload)
print(headers)
print(r.status_code)
print(r.url)

method = "POST"
content_type = 'application/json'
url = "/api/v1/jobs"
payload = {}
params = {}
headers = signature.generate_headers_with_secret(
    secret,
    method,
    content_type,
    url,
    params,
    payload)
files = {'file': open('test.txt', 'rb')}
r = requests.post('http://127.0.0.1:5000%s' % url, headers=headers, files=files)
print(headers)
print(r.status_code)
print(r.url)
