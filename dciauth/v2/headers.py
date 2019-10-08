#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Red Hat, Inc.
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
import hashlib
import hmac
import json
from collections import OrderedDict

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"
DATESTAMP_FORMAT = "%Y%m%d"


def _order_dict(dictionary):
    return OrderedDict(sorted(dictionary.items(), key=lambda k: k[0]))


def _sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _get_signature_key(
    algorithm, key, datestamp, region_name, service_name, request_type
):
    key_date = _sign(
        (algorithm.replace("-HMAC-SHA256", "") + key).encode("utf-8"), datestamp
    )
    key_region = _sign(key_date, region_name)
    key_service = _sign(key_region, service_name)
    key_signing = _sign(key_service, request_type)
    return key_signing


def _get_headers_string(request, content_type, host, timestamp):
    signed_headers = request.get("signed_headers")
    canonical_headers = request.get("canonical_headers")
    if signed_headers and canonical_headers:
        canonical_headers = (
            "\n".join(
                ["%s:%s" % (h, canonical_headers[h]) for h in signed_headers.split(";")]
            )
            + "\n"
        )

    else:
        signed_headers = "content-type;host;x-dci-date"
        canonical_headers = "content-type:%s\nhost:%s\nx-dci-date:%s\n" % (
            content_type,
            host,
            timestamp,
        )
    return signed_headers, canonical_headers


def generate_headers(request, credentials):
    access_key = credentials.get("access_key")
    secret_key = credentials.get("secret_key")
    if not access_key or not secret_key:
        return {}

    method = request.get("method", "GET")
    service = request.get("service", "api")
    host = request.get("host", "api.distributed-ci.io")
    region = request.get("region", "BHS3")
    endpoint = request.get("endpoint", "/")
    params = request.get("params", {})
    payload = request.get("payload", {})
    content_type = request.get("content-type", "application/json")
    now = request.get("now", datetime.datetime.utcnow())
    timestamp = request.get("timestamp", now.strftime(TIMESTAMP_FORMAT))
    datestamp = request.get("datestamp", now.strftime(DATESTAMP_FORMAT))
    algorithm = request.get("algorithm", "DCI2-HMAC-SHA256")
    request_type = request.get("request_type", "dci2_request")

    signed_headers, canonical_headers = _get_headers_string(
        request, content_type, host, timestamp
    )

    if method == "GET":
        request_parameters = urlencode(_order_dict(params))
        canonical_querystring = request_parameters
        payload_hash = hashlib.sha256(("").encode("utf-8")).hexdigest()
    else:
        request_parameters = json.dumps(_order_dict(payload)) if payload else ""
        canonical_querystring = ""
        payload_hash = hashlib.sha256(request_parameters.encode("utf-8")).hexdigest()

    canonical_request = (
        method
        + "\n"
        + endpoint
        + "\n"
        + canonical_querystring
        + "\n"
        + canonical_headers
        + "\n"
        + signed_headers
        + "\n"
        + payload_hash
    )

    credential_scope = datestamp + "/" + region + "/" + service + "/" + request_type
    string_to_sign = (
        algorithm
        + "\n"
        + timestamp
        + "\n"
        + credential_scope
        + "\n"
        + hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    )
    signing_key = _get_signature_key(
        algorithm, secret_key, datestamp, region, service, request_type
    )

    signature = hmac.new(
        signing_key, (string_to_sign).encode("utf-8"), hashlib.sha256
    ).hexdigest()

    authorization_header = (
        algorithm
        + " "
        + "Credential="
        + access_key
        + "/"
        + credential_scope
        + ", "
        + "SignedHeaders="
        + signed_headers
        + ", "
        + "Signature="
        + signature
    )
    headers = {
        "X-DCI-Date": timestamp,
        "Authorization": authorization_header,
        "Content-Type": content_type,
    }

    return headers
