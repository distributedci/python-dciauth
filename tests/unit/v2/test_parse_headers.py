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
from dciauth.v2.headers import parse_headers


def test_parse_header():
    assert parse_headers(
        {
            "X-DCI-Date": "20171215T111929Z",
            "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
            "Host": "api.distributed-ci.io",
        }
    ) == {
        "signed_headers": "host;x-dci-date",
        "service": "api",
        "datestamp": "20171215",
        "canonical_headers": {
            "x-dci-date": "20171215T111929Z",
            "host": "api.distributed-ci.io",
        },
        "client_id": "464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "client_type": "remoteci",
        "region": "BHS3",
        "host": "api.distributed-ci.io",
        "algorithm": "DCI2-HMAC-SHA256",
        "timestamp": "20171215T111929Z",
        "request_type": "dci2_request",
        "signature": "6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
    }


def test_parse_header_ignore_case():
    assert parse_headers(
        {
            "X-DCI-Date": "20171215T111929Z",
            "auThorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
            "HOST": "api.distributed-ci.io",
        }
    ) == {
        "signed_headers": "host;x-dci-date",
        "service": "api",
        "datestamp": "20171215",
        "canonical_headers": {
            "x-dci-date": "20171215T111929Z",
            "host": "api.distributed-ci.io",
        },
        "client_id": "464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "client_type": "remoteci",
        "region": "BHS3",
        "host": "api.distributed-ci.io",
        "algorithm": "DCI2-HMAC-SHA256",
        "timestamp": "20171215T111929Z",
        "request_type": "dci2_request",
        "signature": "6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
    }


def test_parse_header_return_none_if_access_key_len_not_equal_to_5():
    assert (
        parse_headers(
            {
                "X-DCI-Date": "20171215T111929Z",
                "Authorization": "DCI2-HMAC-SHA256 Credential=464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
                "Host": "api.distributed-ci.io",
            }
        )
        is None
    )


def test_parse_header_return_none_if_no_timestamp_header():
    assert (
        parse_headers(
            {
                "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
                "Host": "api.distributed-ci.io",
            }
        )
        is None
    )


def test_parse_header_return_none_if_timestamp_header_unknown():
    assert (
        parse_headers(
            {
                "X-Foo-Date": "20171215T111929Z",
                "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
                "Host": "api.distributed-ci.io",
            }
        )
        is None
    )
    assert (
        parse_headers(
            {
                "X-Amz-Date": "20171215T111929Z",
                "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-amz-date, Signature=6fd8a24d8eb52e7a1b62f26f48f5a865a56cf08e492b56e16066e2cd4ce3e02e",
                "Host": "api.distributed-ci.io",
            }
        )["timestamp"]
        == "20171215T111929Z"
    )
