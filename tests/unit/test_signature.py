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
import datetime
from dciauth.request import AuthRequest
from dciauth.signature import Signature


def test_can_create_signature():
    request = AuthRequest()
    signature = Signature(request=request)
    assert signature.request.method == 'GET'


def test_signature_calc_dci_datetime_and_date_with_good_format():
    request = AuthRequest()
    now = datetime.datetime(2017, 12, 15, 11, 19, 29)
    signature = Signature(request=request, now=now)
    assert signature.dci_date == '20171215'
    assert signature.dci_datetime == '20171215T111929Z'


def test_2_signatures_now_is_different_if_not_defined():
    signature = Signature(request=AuthRequest())
    signature2 = Signature(request=AuthRequest())
    assert signature.now.strftime('%Y%m%dT%H%M%S.%fZ') != signature2.now.strftime('%Y%m%dT%H%M%S.%fZ')


def test_create_canonical_request():
    request = AuthRequest(endpoint='/api/v1/jobs')
    now = datetime.datetime(2017, 12, 15, 11, 19, 29)
    signature = Signature(request=request, now=now)
    canonical_request = signature._create_canonical_request()
    expected_canonical_request = """GET
/api/v1/jobs



e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"""
    assert expected_canonical_request == canonical_request


def test_create_canonical_request_with_params():
    request = AuthRequest(
        method='GET',
        endpoint='/api/v1/jobs',
        params={'embed': 'teams', 'limit': '50'},
        headers={'dci-datetime': '20171215T111929Z'}
    )
    now = datetime.datetime(2017, 12, 15, 11, 19, 29)
    signature = Signature(request=request, now=now)
    canonical_request = signature._create_canonical_request()
    expected_canonical_request = """GET
/api/v1/jobs
embed=teams&limit=50
dci-datetime:20171215T111929Z

dci-datetime
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"""
    assert expected_canonical_request == canonical_request


def test_create_canonical_request_post():
    request = AuthRequest(
        method='POST',
        endpoint='/api/v1/users',
        payload={'name': 'u'},
        headers={'content-type': 'application/json', 'dci-datetime': '20171215T111929Z'}
    )
    now = datetime.datetime(2017, 12, 15, 11, 19, 29)
    signature = Signature(request=request, now=now)
    canonical_request = signature._create_canonical_request()
    expected_canonical_request = """POST
/api/v1/users

content-type:application/json
dci-datetime:20171215T111929Z

content-type;dci-datetime
0a8ed5c97edb6664928d54d4c5adbb92a9992fe5b78c9a10016824fee1cdb230"""
    assert expected_canonical_request == canonical_request


def test_create_string_to_sign():
    request = AuthRequest(endpoint='/api/v1/jobs', headers={'dci-datetime': '20171215T111929Z'})
    now = datetime.datetime(2017, 12, 15, 11, 19, 29)
    signature = Signature(request=request, now=now)
    string_to_sign = signature._create_string_to_sign()
    expected_string_to_sign = """DCI-HMAC-SHA256
20171215T111929Z
20171215
6cff96f139f2517692f4dfc7e3396b947112908750b1d894e087a59649a4b3a7"""
    assert expected_string_to_sign == string_to_sign


def test_sign():
    request = AuthRequest(endpoint='/api/v1/jobs', headers={'dci-datetime': '20171215T111929Z'})
    now = datetime.datetime(2017, 12, 15, 11, 19, 29)
    signature = Signature(request=request, now=now)
    expected_signature = 'bfbe2596b3e4dfbc08ff7523d26afc883125e08a522674be063cc44a152ce2b6'
    assert expected_signature == signature._sign('secret')


def test_generate_headers():
    request = AuthRequest(endpoint='/api/v1/jobs')
    now = datetime.datetime(2017, 12, 15, 11, 19, 29)
    signature = Signature(request=request, now=now)
    headers = signature.generate_headers(client_type='remoteci', client_id='abcdef', secret='secret')
    expected_headers = {
        'Authorization': 'DCI-HMAC-SHA256 Credential=remoteci/abcdef, SignedHeaders=dci-datetime, Signature=bfbe2596b3e4dfbc08ff7523d26afc883125e08a522674be063cc44a152ce2b6,',
        'dci-datetime': '20171215T111929Z'
    }
    for key in expected_headers.keys():
        assert expected_headers[key] == headers[key]


def test_generate_headers_post():
    request = AuthRequest(
        method='POST',
        endpoint='/api/v1/users',
        payload={'name': 'u'},
        headers={'content-type': 'application/json'}
    )
    now = datetime.datetime(2017, 12, 15, 11, 19, 29)
    signature = Signature(request=request, now=now)
    headers = signature.generate_headers(client_type='feeder', client_id='abcdef', secret='secret')
    expected_headers = {
        'Authorization': 'DCI-HMAC-SHA256 Credential=feeder/abcdef, SignedHeaders=content-type;dci-datetime, Signature=d6448fc3a067570527cee42370611736c861853dbc09ff74e9bc0abf14d5f65e,',
        'dci-datetime': '20171215T111929Z'
    }
    for key in expected_headers.keys():
        assert expected_headers[key] == headers[key]
