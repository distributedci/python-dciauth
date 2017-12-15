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


def test_auth_request_get_query_string():
    query_string = AuthRequest(params={'a': 1, 'b': 2}).get_query_string()
    assert query_string == 'a=1&b=2'


def test_auth_request_get_query_string_empty_params():
    query_string = AuthRequest().get_query_string()
    assert query_string == ''


def test_auth_request_get_query_string_order_params_by_key():
    query_string = AuthRequest(params={'b': 2, 'a': 1}).get_query_string()
    assert query_string == 'a=1&b=2'


def test_auth_request_get_payload_string():
    payload_string = AuthRequest(payload={'a': 1, 'b': 2}).get_payload_string()
    assert payload_string == '{"a": 1, "b": 2}'


def test_auth_request_get_payload_string_empty_payload():
    payload_string = AuthRequest().get_payload_string()
    assert payload_string == ''


def test_auth_request_get_payload_string_order_params_by_key():
    payload_string = AuthRequest(payload={'b': 2, 'a': 1}).get_payload_string()
    assert payload_string == '{"a": 1, "b": 2}'


def test_auth_request_get_headers_string_based_on_filtered_headers():
    request = AuthRequest(headers={'a': 1, 'b': 2})
    request.filtered_headers = request.headers
    headers_string = request.get_headers_string()
    assert headers_string == 'a:1\nb:2\n'


def test_auth_request_get_headers_string_empty_headers():
    request = AuthRequest()
    assert request.get_headers_string() == ''


def test_auth_request_get_headers_string_order_by_key():
    request = AuthRequest(headers={'b': 2, 'a': 1, 'c': 3})
    request.filtered_headers = request.headers
    headers_string = request.get_headers_string()
    assert headers_string == 'a:1\nb:2\nc:3\n'


def test_auth_request_method_is_uppercase():
    request = AuthRequest(method='delete')
    assert request.method == 'DELETE'


def test_request_get_signed_headers_based_on_filtered_headers():
    request = AuthRequest(headers={'not_wanted': 'filtered', 'content-type': 'application/json'})
    request.filtered_headers = {'content-type': 'application/json'}
    signed_headers = request.get_signed_headers_string()
    assert signed_headers == 'content-type'


def test_request_get_signed_headers_string_are_lowercase():
    request = AuthRequest(headers={'Content-Type': 'application/json'})
    request.filtered_headers = {'Content-Type': 'application/json'}
    signed_headers = request.get_signed_headers_string()
    assert signed_headers == 'content-type'


def test_request_get_signed_headers_empty_headers():
    signed_headers = AuthRequest().get_signed_headers_string()
    assert signed_headers == ''


def test_request_get_signed_headers_string_after_new_header_added():
    request = AuthRequest(headers={'content-type': 'application/json'})
    request.add_header('dci-datetime', '20171215T111929Z')
    signed_headers = request.get_signed_headers_string()
    assert request.headers['dci-datetime'] == '20171215T111929Z'
    assert signed_headers == 'content-type;dci-datetime'


def test_build_headers():
    request = AuthRequest(headers={'content-type': 'application/json'})
    request.add_header('dci-datetime', '20171215T111929Z')
    headers = request.build_headers(client_type='remoteci', client_id='abc', signature='123')
    expected_headers = {
        'Authorization': 'DCI-HMAC-SHA256 Credential=remoteci/abc, SignedHeaders=content-type;dci-datetime, Signature=123,',
        'dci-datetime': '20171215T111929Z',
        'content-type': 'application/json'
    }
    for key in expected_headers.keys():
        assert expected_headers[key] == headers[key]


def test_request_get_client_info():
    headers = AuthRequest().build_headers(client_type='remoteci', client_id='abc', signature='123')
    print(headers)
    client_info = AuthRequest(headers=headers).get_client_info()
    assert client_info['client_type'] == 'remoteci'
    assert client_info['client_id'] == 'abc'
    assert client_info['signature'] == '123'


def test_filter_headers_with_signed_headers_value():
    request = AuthRequest(headers={
        'Authorization': 'DCI-HMAC-SHA256 Credential=remoteci/abc, SignedHeaders=content-type;dci-datetime, Signature=123,',
        'dci-datetime': '20171215T111929Z',
        'content-type': 'application/json',
        'new-header': '',
    })
    filtered_headers = request.filtered_headers
    assert len(filtered_headers) == 2
    assert filtered_headers['dci-datetime'] == '20171215T111929Z'
    assert filtered_headers['content-type'] == 'application/json'


def test_filter_headers_case_insensitive():
    request = AuthRequest(headers={
        'Authorization': 'DCI-HMAC-SHA256 Credential=remoteci/abc, SignedHeaders=content-type;dci-datetime, Signature=123,',
        'Dci-Datetime': '20171215T111929Z',
        'Content-Type': 'application/json'
    })
    filtered_headers = request.filtered_headers
    assert len(filtered_headers) == 2
    assert filtered_headers['dci-datetime'] == '20171215T111929Z'
    assert filtered_headers['content-type'] == 'application/json'
