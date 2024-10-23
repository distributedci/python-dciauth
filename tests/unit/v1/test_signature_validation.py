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

from dciauth.v1.request import AuthRequest
from dciauth.v1.signature import Signature


def test_signature_is_valid():
    request = AuthRequest(
        endpoint="/api/v1/jobs",
        headers={
            "Authorization": "DCI-HMAC-SHA256 Credential=remoteci/abcdef, SignedHeaders=dci-datetime, Signature=bfbe2596b3e4dfbc08ff7523d26afc883125e08a522674be063cc44a152ce2b6,",
            "dci-datetime": "20171215T111929Z",
        },
    )
    now = datetime.datetime(2017, 12, 15, 11, 19, 29)
    signature = Signature(request=request, now=now)
    assert signature.is_valid("secret")


def test_signature_is_valid_even_after_5sec():
    request = AuthRequest(
        endpoint="/api/v1/jobs",
        headers={
            "Authorization": "DCI-HMAC-SHA256 Credential=remoteci/abcdef, SignedHeaders=dci-datetime, Signature=bfbe2596b3e4dfbc08ff7523d26afc883125e08a522674be063cc44a152ce2b6,",
            "dci-datetime": "20171215T111929Z",
        },
    )
    now = datetime.datetime(2017, 12, 15, 11, 19, 34)
    signature = Signature(request=request, now=now)
    assert signature.is_valid("secret")


def test_signature_is_invalid_because_endpoint_changed():
    request = AuthRequest(
        endpoint="/api/v1/bad_endpoint",
        headers={
            "Authorization": "DCI-HMAC-SHA256 Credential=remoteci/abcdef, SignedHeaders=dci-datetime, Signature=bfbe2596b3e4dfbc08ff7523d26afc883125e08a522674be063cc44a152ce2b6,",
            "dci-datetime": "20171215T111929Z",
        },
    )
    now = datetime.datetime(2017, 12, 15, 11, 19, 29)
    signature = Signature(request=request, now=now)
    assert signature.is_valid("secret") is False


def test_signature_is_expired():
    request = AuthRequest(
        headers={
            "Authorization": "DCI-HMAC-SHA256 Credential=remoteci/abcdef, SignedHeaders=dci-datetime, Signature=bfbe2596b3e4dfbc08ff7523d26afc883125e08a522674be063cc44a152ce2b6,",
            "dci-datetime": "20171215T111929Z",
        }
    )
    now = datetime.datetime(2017, 12, 14, 11, 19, 28)
    signature = Signature(request=request, now=now)
    assert signature.is_expired()


def test_signature_is_not_expired():
    request = AuthRequest(
        headers={
            "Authorization": "DCI-HMAC-SHA256 Credential=remoteci/abcdef, SignedHeaders=dci-datetime, Signature=bfbe2596b3e4dfbc08ff7523d26afc883125e08a522674be063cc44a152ce2b6,",
            "dci-datetime": "20171215T111929Z",
        }
    )
    height_hour_after = datetime.datetime(2017, 12, 15, 18, 19, 28)
    signature = Signature(request=request, now=height_hour_after)
    assert signature.is_expired() is False
