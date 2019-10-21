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
from dciauth.v2.signature import is_valid
from dciauth.v2.headers import parse_headers


def test_signature_is_valid():
    request = {
        "now": datetime(2017, 12, 15, 11, 19, 30),
        "endpoint": "/api/v1/users",
        "params": {"limit": 100, "embed": "teams"},
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    headers = parse_headers(
        {
            "Host": "api.distributed-ci.io",
            "X-DCI-Date": "20171215T111929Z",
            "Content-Type": "application/json",
            "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=content-type;host;x-dci-date, Signature=6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
        }
    )
    assert is_valid(request, credential, headers)[0]


def test_signature_is_valid_with_post_request():
    request = {
        "now": datetime(2017, 12, 15, 11, 19, 30),
        "method": "POST",
        "endpoint": "/api/v1/users",
        "data": '{"name": "foo"}',
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    headers = parse_headers(
        {
            "X-DCI-Date": "20171215T111929Z",
            "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=content-type;host;x-dci-date, Signature=3212f321bdf66c72d12ead089d17a01ed5ce8858976dff688fd60785216bf624",
            "Content-Type": "application/json",
            "host": "api.distributed-ci.io",
        }
    )
    assert is_valid(request, credential, headers)[0]


def test_signature_is_valid_with_put_request():
    request = {
        "now": datetime(2017, 12, 15, 11, 19, 30),
        "method": "PUT",
        "endpoint": "/api/v1/users",
        "data": '{"name": "foo"}',
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    headers = parse_headers(
        {
            "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=content-type;host;x-dci-date, Signature=53422ab72a75871f8ecc75b1228c71664a4ab22cd02fb5c8577c4f856d6e8e87",
            "Content-Type": "application/json",
            "X-DCI-Date": "20171215T111929Z",
            "host": "api.distributed-ci.io",
        }
    )
    assert is_valid(request, credential, headers)[0]


def test_signature_is_valid_with_delete_request():
    request = {
        "now": datetime(2017, 12, 15, 11, 19, 30),
        "method": "DELETE",
        "endpoint": "/api/v1/users/ef837f60-87f4-4432-a249-b4977ec5bb45",
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    headers = parse_headers(
        {
            "Content-Type": "application/json",
            "X-DCI-Date": "20171215T111929Z",
            "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=content-type;host;x-dci-date, Signature=295b646610163e8914765053998848cb2ed8c5db63af44b847f21ced345f43a3",
            "host": "api.distributed-ci.io",
        }
    )
    assert is_valid(request, credential, headers)[0]


def test_signature_aws4_is_valid():
    request = {"now": datetime(2019, 10, 8, 12, 16, 59), "endpoint": "/api/v1/identity"}
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    headers = parse_headers(
        {
            "Authorization": "AWS4-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20191008/BHS3/api/aws4_request, SignedHeaders=host;x-amz-date, Signature=ed58acc0005ad7522c942f731aa4d8570f1f7b3500da9efb7cfe8f74732f4082",
            "X-Amz-Date": "20191008T121659Z",
            "User-Agent": "PostmanRuntime/7.17.1",
            "Connection": "keep-alive",
            "Postman-Token": "6d95b7c6-cdd8-4e71-9ccc-ed2b9533924e",
            "Host": "127.0.0.1:5000",
            "Cache-Control": "no-cache",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
        }
    )
    assert is_valid(request, credential, headers)[0]


def test_signature_aws4_post_request_is_valid():
    request = {
        "method": "POST",
        "now": datetime(2019, 10, 21, 10, 56, 28),
        "endpoint": "/api/v1/jobs",
        "host": "api.distributed-ci.io",
        "data": """{
    "components": [
        "d4bcd2e2-98df-4962-b224-8d50eedaba1b"
    ],
    "topic_id": "c4171062-e2b4-4b60-9a5f-3e2fb32b4f68"
}"""
    }
    credential = {
        "access_key": "remoteci/79626298-a124-4e22-b5be-ec1a5e46fb41",
        "secret_key": "XFe4YmxzehlZMGQsL3svsbIrhKBBPHiRWdw22uclpAsX8a6sSixQrZkdxxqdVBDZ",
    }
    headers = parse_headers(
        {
            "Authorization": "AWS4-HMAC-SHA256 Credential=remoteci/79626298-a124-4e22-b5be-ec1a5e46fb41/20191021/BHS3/api/aws4_request, SignedHeaders=content-type;host;x-amz-content-sha256;x-amz-date, Signature=5ab513f88534f6cd454d9604dbbac45339b0ad1b1bbfb36996956eef7981be3f",
            "X-Amz-Date": "20191021T105628Z",
            "X-Amz-Content-Sha256": "929e03af12349f2b9f30f892ddc5ca1d8c9f4b68a358a464428c1088268ea765",
            "Content-Type": "application/json",
            "Host": "api.distributed-ci.io",
            "User-Agent": "PostmanRuntime/7.17.1",
            "Connection": "keep-alive",
            "Postman-Token": "d055dc78-4b0e-4d38-bc21-2c138e7fe316",
            "Cache-Control": "no-cache",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
        }
    )
    assert is_valid(request, credential, headers)[0]


def test_signature_is_invalid_if_no_authorization():
    request = {"endpoint": "/api/v1/users/ef837f60-87f4-4432-a249-b4977ec5bb45"}
    headers = parse_headers({"Host": "api.distributed-ci.io"})
    valid, error_message = is_valid(request, {}, headers)
    assert valid is False
    assert "headers are malformated" in error_message


def test_signature_is_invalid_because_endpoint_changed():
    request = {"now": datetime(2017, 12, 15, 11, 19, 30), "endpoint": "/api/v1/users"}
    credential = {"access_key": "remoteci/ak", "secret_key": "sk"}
    headers = parse_headers(
        {
            "Content-Type": "application/json",
            "X-DCI-Date": "20171215T111929Z",
            "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/ak/20171215/BHS3/api/dci2_request, SignedHeaders=content-type;host;x-dci-date, Signature=22970220e6592b55e382f53c1349a608e911f3e090297a900b7ca7650b786c9d",
            "Host": "api.distributed-ci.io",
        }
    )
    assert is_valid(request, credential, headers)[0]
    request = {"now": datetime(2017, 12, 15, 11, 19, 30), "endpoint": "/api/v1/admin"}
    valid, error_message = is_valid(request, credential, headers)
    assert valid is False
    assert "signature is invalid" in error_message


def test_signature_is_expired():
    fifteen_min_and_one_sec_after = datetime(2017, 12, 15, 11, 34, 30)
    request = {
        "endpoint": "/api/v1/users",
        "params": {"limit": 100, "embed": "teams"},
        "now": fifteen_min_and_one_sec_after,
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    headers = parse_headers(
        {
            "Host": "api.distributed-ci.io",
            "X-DCI-Date": "20171215T111929Z",
            "Content-Type": "application/json",
            "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=content-type;host;x-dci-date, Signature=6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
        }
    )
    valid, error_message = is_valid(request, credential, headers)
    assert valid is False
    assert "signature is expired" in error_message


def test_signature_aws_is_expired():
    fifteen_min_and_one_sec_after = datetime(2019, 10, 8, 12, 32, 0)
    request = {"now": fifteen_min_and_one_sec_after, "endpoint": "/api/v1/identity"}
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    headers = parse_headers(
        {
            "Authorization": "AWS4-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20191008/BHS3/api/aws4_request, SignedHeaders=host;x-amz-date, Signature=ed58acc0005ad7522c942f731aa4d8570f1f7b3500da9efb7cfe8f74732f4082",
            "X-Amz-Date": "20191008T121659Z",
            "User-Agent": "PostmanRuntime/7.17.1",
            "Connection": "keep-alive",
            "Postman-Token": "6d95b7c6-cdd8-4e71-9ccc-ed2b9533924e",
            "Host": "127.0.0.1:5000",
            "Cache-Control": "no-cache",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
        }
    )
    valid, error_message = is_valid(request, credential, headers)
    assert valid is False
    assert "signature is expired" in error_message


def test_signature_is_not_expired():
    fifteen_min = datetime(2017, 12, 15, 11, 34, 29)
    request = {
        "endpoint": "/api/v1/users",
        "params": {"limit": 100, "embed": "teams"},
        "now": fifteen_min,
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    headers = parse_headers(
        {
            "Host": "api.distributed-ci.io",
            "X-DCI-Date": "20171215T111929Z",
            "Content-Type": "application/json",
            "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=content-type;host;x-dci-date, Signature=6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
        }
    )
    assert is_valid(request, credential, headers)[0]


def test_signature_aws_is_not_expired():
    fifteen_min = datetime(2019, 10, 8, 12, 31, 59)
    request = {"now": fifteen_min, "endpoint": "/api/v1/identity"}
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    headers = parse_headers(
        {
            "Authorization": "AWS4-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20191008/BHS3/api/aws4_request, SignedHeaders=host;x-amz-date, Signature=ed58acc0005ad7522c942f731aa4d8570f1f7b3500da9efb7cfe8f74732f4082",
            "X-Amz-Date": "20191008T121659Z",
            "User-Agent": "PostmanRuntime/7.17.1",
            "Connection": "keep-alive",
            "Postman-Token": "6d95b7c6-cdd8-4e71-9ccc-ed2b9533924e",
            "Host": "127.0.0.1:5000",
            "Cache-Control": "no-cache",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
        }
    )
    assert is_valid(request, credential, headers)[0]
