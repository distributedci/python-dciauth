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
from datetime import datetime

from dciauth.v2.headers import generate_headers


def test_empty_credential_returns_empty_header():
    request = {"endpoint": "/api/v1/identity"}
    credential = {}
    assert generate_headers(request, credential) == {}


def test_credential_field_in_autorization_header():
    request = {
        "service": "api2",
        "region": "BHS4",
        "algorithm": "DCI3-HMAC-SHA256",
        "request_type": "dci3_request",
        "now": datetime(2017, 12, 15, 11, 19, 29),
    }
    credential = {
        "access_key": "feeder/464cc0a3-d638-a69e-4081-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    authorization_header = generate_headers(request, credential)["Authorization"]
    assert "DCI3-HMAC-SHA256" in authorization_header
    assert (
        "Credential=feeder/464cc0a3-d638-a69e-4081-4c80261f3ba5/20171215/BHS4/api2/dci3_request"
        in authorization_header
    )


def test_generate_headers_default_values():
    request = {
        "endpoint": "/api/v1/users",
        "params": {"limit": 100, "embed": "teams"},
        "now": datetime(2017, 12, 15, 11, 19, 29),
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    assert generate_headers(request, credential) == {
        "X-DCI-Date": "20171215T111929Z",
        "Content-Type": "application/json",
        "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=content-type;host;x-dci-date, Signature=6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
    }


def test_generate_headers_post():
    request = {
        "method": "POST",
        "endpoint": "/api/v1/users",
        "payload": {"name": "foo"},
        "now": datetime(2017, 12, 15, 11, 19, 29),
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    assert generate_headers(request, credential) == {
        "X-DCI-Date": "20171215T111929Z",
        "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=content-type;host;x-dci-date, Signature=3212f321bdf66c72d12ead089d17a01ed5ce8858976dff688fd60785216bf624",
        "Content-Type": "application/json",
    }


def test_generate_headers_with_claimed_stamps():
    request = {
        "method": "POST",
        "endpoint": "/api/v1/users",
        "payload": {"name": "foo"},
        "timestamp": "20171215T111929Z",
        "datestamp": "20171215",
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    assert generate_headers(request, credential) == {
        "X-DCI-Date": "20171215T111929Z",
        "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=content-type;host;x-dci-date, Signature=3212f321bdf66c72d12ead089d17a01ed5ce8858976dff688fd60785216bf624",
        "Content-Type": "application/json",
    }
