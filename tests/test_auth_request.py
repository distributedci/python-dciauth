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

from dciauth.request import AuthRequest


def test_can_create_auth_request():
    request = AuthRequest()
    assert request.algorithm == 'DCI-HMAC-SHA256'
    assert request.method == 'GET'
    assert request.endpoint == '/'
    assert request.payload == {}
    assert request.headers == {}
    assert request.params == {}


def test_can_create_auth_request_with_constructor():
    request = AuthRequest(
        method='POST',
        endpoint='/api/v1/users',
        payload={'name': 'u'},
        headers={'content-type': 'application/json'},
        params={'limit': 100},
    )
    assert request.method == 'POST'
    assert request.endpoint == '/api/v1/users'
    assert request.payload == {'name': 'u'}
    assert request.headers == {'content-type': 'application/json'}
    assert request.params == {'limit': 100}


def test_auth_request_query_string():
    assert AuthRequest(params={'a': 1, 'b': 2}).query_string == 'a=1&b=2'


def test_auth_request_query_string_empty_params():
    assert AuthRequest().query_string == ''


def test_auth_request_query_string_order_params_by_key():
    assert AuthRequest(params={'b': 2, 'a': 1}).query_string == 'a=1&b=2'


def test_auth_request_payload_string():
    assert AuthRequest(payload={'a': 1, 'b': 2}).payload_string == '{"a": 1, "b": 2}'


def test_auth_request_payload_string_empty_payload():
    assert AuthRequest().payload_string == ''


def test_auth_request_payload_string_order_params_by_key():
    assert AuthRequest(payload={'b': 2, 'a': 1}).payload_string == '{"a": 1, "b": 2}'


def test_auth_request_order_headers_by_key():
    request = AuthRequest(headers={'b': 2, 'a': 1, 'c': 3})
    assert json.dumps(request.headers) == '{"a": 1, "b": 2, "c": 3}'


def test_auth_request_method_is_uppercase():
    request = AuthRequest(method='delete')
    assert request.method == 'DELETE'


def test_request_signed_headers():
    request = AuthRequest(headers={'content-type': 'application/json'})
    assert request.signed_headers == 'content-type'


def test_request_add_header():
    request = AuthRequest(headers={'content-type': 'application/json'})
    request.add_header('dci-datetime', '20171215T111929Z')
    assert request.headers['dci-datetime'] == '20171215T111929Z'
    assert request.signed_headers == 'content-type;dci-datetime'


def test_get_signed_headers():
    request = AuthRequest(headers={'content-type': 'application/json'})
    request.add_header('dci-datetime', '20171215T111929Z')
    headers = request.get_signed_headers(client_type='remoteci', client_id='abc', signature='123')
    expected_headers = {
        'Authorization': 'DCI-HMAC-SHA256 Credential=remoteci/abc, SignedHeaders=content-type;dci-datetime, Signature=123,',
        'dci-datetime': '20171215T111929Z',
        'content-type': 'application/json'
    }
    for key in expected_headers.keys():
        assert expected_headers[key] == headers[key]


def test_request_get_client_info():
    headers = AuthRequest().get_signed_headers(client_type='remoteci', client_id='abc', signature='123')
    request = AuthRequest(headers=headers)
    assert request.client_type == 'remoteci'
    assert request.client_id == 'abc'
    assert request.signature == '123'


def test_filter_headers_with_signed_headers_value():
    request = AuthRequest(headers={
        'Authorization': 'DCI-HMAC-SHA256 Credential=remoteci/abc, SignedHeaders=content-type;dci-datetime, Signature=123,',
        'dci-datetime': '20171215T111929Z',
        'content-type': 'application/json',
        'new-header': '',
    })
    expected_headers = {
        'dci-datetime': '20171215T111929Z',
        'content-type': 'application/json'
    }
    for key in request.headers.keys():
        assert expected_headers[key] == request.headers[key]
    assert request.signed_headers == 'content-type;dci-datetime'
