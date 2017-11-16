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
import sys
from freezegun import freeze_time
from dciauth import signature


def test_hash_payload():
    payload = {"foo": "bar"}
    expected_hash = "426fc04f04bf8fdb5831dc37bbb6dcf70f63a37e05a68c6ea5f63e85ae579376"
    assert signature._hash_payload(payload) == expected_hash


def test_hash_payload_unicode():
    payload = {"foo": "I ❤ bar"}
    expected_hash = "74816a5237d72280aa327ed345267b4c31ee9f7dad0686e14940918c34a5533a"
    assert signature._hash_payload(payload) == expected_hash


def test_hash_payload_for_get_request_is_empty_string():
    payload = None
    expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert signature._hash_payload(payload) == expected_hash


def test_hash_payload_order_is_not_important():
    assert signature._hash_payload({'a': 1, 'b': 2}) == signature._hash_payload({'b': 2, 'a': 1})


@freeze_time("20171103T162727Z")
def test_not_a_replay_request():
    one_minute_ago = '20171103T162627Z'
    headers = {
        'DCI-Datetime': one_minute_ago
    }
    assert signature.is_expired(headers) is False


@freeze_time("20171103T162727Z")
def test_five_minutes_after_is_a_replay_request():
    more_thant_five_minute_ago = '20171103T162226Z'
    headers = {
        'DCI-Datetime': more_thant_five_minute_ago
    }
    assert signature.is_expired(headers)


def test_signature_equals():
    assert signature.equals(
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )


def test_signature_not_equals():
    assert signature.equals(
        "74816a5237d72280aa327ed345267b4c31ee9f7dad0686e14940918c34a5533a",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    ) is False


def test_string_without_buffer_interface():
    if sys.version_info[0] == 2:
        assert signature.equals(
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            unicode('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
        )


def test_create_string_to_sign():
    method = "GET"
    content_type = "application/json"
    timestamp = "20171103T162727Z"
    url = "/api/v1/jobs"
    query_string = "limit=100&offset=1"
    hashed_payload = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    string_to_sign = signature._create_string_to_sign(
        method,
        content_type,
        timestamp,
        url,
        query_string,
        hashed_payload,
    )

    assert string_to_sign == '''GET
application/json
20171103T162727Z
/api/v1/jobs
limit=100&offset=1
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'''


def test_calculate_signature():
    secret = "Y4efRHLzw2bC2deAZNZvxeeVvI46Cx8XaLYm47Dc019S6bHKejSBVJiGAfHbZLIN"
    method = "GET"
    headers = {
        'DCI-Datetime': '20171103T162727Z',
        'Content-type': 'application/json'
    }
    url = "/api/v1/jobs"
    params = {'limit': 100, 'offset': 1}
    payload = {}
    expected_signature = "811f7ceb089872cd264fc5859cffcd6ddfbe8ce851f0743199ad4c96470c6b6b"
    assert signature.calculate_signature(
        secret,
        method,
        headers,
        url,
        params,
        payload) == expected_signature


def test_calculate_signature_params_order_is_not_important():
    secret = "Y4efRHLzw2bC2deAZNZvxeeVvI46Cx8XaLYm47Dc019S6bHKejSBVJiGAfHbZLIN"
    method = "GET"
    headers = {
        'DCI-Datetime': '20171103T162727Z',
        'Content-type': 'application/json'
    }
    url = "/api/v1/jobs"
    params = {'offset': 1, 'limit': 100}
    payload = {}
    expected_signature = "811f7ceb089872cd264fc5859cffcd6ddfbe8ce851f0743199ad4c96470c6b6b"
    assert signature.calculate_signature(
        secret,
        method,
        headers,
        url,
        params,
        payload) == expected_signature


def test_get_signature_from_headers():
    headers = {
        'Authorization': 'DCI-HMAC-SHA256 811f7ceb089872cd264fc5859cffcd6ddfbe8ce851f0743199ad4c96470c6b6b'
    }
    expected_signature = "811f7ceb089872cd264fc5859cffcd6ddfbe8ce851f0743199ad4c96470c6b6b"
    assert signature.get_signature_from_headers(headers) == expected_signature


def test_get_signature_from_headers_return_empty_string_if_no_auth():
    assert signature.get_signature_from_headers({}) == ''


def test_get_signature_from_headers_return_empty_string_if_auth_not_dci_hmac():
    headers = {
        'Authorization': 'Basic QWxhZGRpbjpPcGVuU2VzYW1l'
    }
    assert signature.get_signature_from_headers(headers) == ''


def test_get_ordered_query_string():
    params = {'limit': 100, 'offset': 1}
    expected_query_string = "limit=100&offset=1"
    query_string = signature._get_sorted_query_string(params)
    assert expected_query_string == query_string


@freeze_time("20171103T162727Z")
def test_generate_headers_with_secret():
    secret = "Y4efRHLzw2bC2deAZNZvxeeVvI46Cx8XaLYm47Dc019S6bHKejSBVJiGAfHbZLIN"
    method = "GET"
    content_type = 'application/json'
    url = "/api/v1/jobs"
    params = {'limit': 100, 'offset': 1}
    payload = {}
    expected_headers = {
        'Authorization': 'DCI-HMAC-SHA256 811f7ceb089872cd264fc5859cffcd6ddfbe8ce851f0743199ad4c96470c6b6b',
        'Content-Type': 'application/json',
        'DCI-Datetime': '20171103T162727Z'
    }
    headers = signature.generate_headers_with_secret(
        secret,
        method,
        content_type,
        url,
        params,
        payload)
    for key in expected_headers.keys():
        assert expected_headers[key] == headers[key]


def test_calculate_signature_payload_order_is_not_important():
    secret = "Y4efRHLzw2bC2deAZNZvxeeVvI46Cx8XaLYm47Dc019S6bHKejSBVJiGAfHbZLIN"
    method = "POST"
    headers = {
        'DCI-Datetime': '20171103T162727Z',
        'Content-type': 'application/json'
    }
    url = "/api/v1/jobs"
    s1 = signature.calculate_signature(
        secret,
        method,
        headers,
        url,
        {},
        {'a': 1, 'b': 2})
    s2 = signature.calculate_signature(
        secret,
        method,
        headers,
        url,
        {},
        {'b': 2, 'a': 1})
    assert signature.equals(s1, s2)
