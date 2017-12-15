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
import hashlib
import hmac


class Signature(object):
    DCI_ALGORITHM = 'DCI-HMAC-SHA256'
    DCI_DATE_FORMAT = '%Y%m%d'
    DCI_DATETIME_FORMAT = DCI_DATE_FORMAT + 'T%H%M%SZ'
    DCI_DATETIME_HEADER = 'dci-datetime'

    def __init__(self, request, now=None):
        self.request = request
        self.now = now or datetime.datetime.utcnow()
        self.dci_date = self.now.strftime(self.DCI_DATE_FORMAT)
        self.dci_datetime = self.now.strftime(self.DCI_DATETIME_FORMAT)

    def generate_headers(self, client_type, client_id, secret):
        self.request.add_header(self.DCI_DATETIME_HEADER, self.dci_datetime)
        signature = self._sign(secret)
        return self.request.build_headers(client_type, client_id, signature)

    def is_valid(self, secret):
        signature = self._sign(secret)
        client_signature = self.request.get_client_info()['signature']
        return self._equals(signature, client_signature)

    def is_expired(self):
        timestamp = self.request.headers.get(self.DCI_DATETIME_HEADER, '')
        if timestamp:
            timestamp = datetime.datetime.strptime(timestamp, self.DCI_DATETIME_FORMAT)
            return abs(self.now - timestamp) > datetime.timedelta(days=1)
        return False

    def _create_canonical_request(self):
        payload_hash = hashlib.sha256(self.request.get_payload_string().encode('utf-8')).hexdigest()
        return """{method}
{endpoint}
{query_string}
{headers_string}
{signed_headers}
{payload_hash}""".format(method=self.request.method,
                         endpoint=self.request.endpoint,
                         query_string=self.request.get_query_string(),
                         headers_string=self.request.get_headers_string(),
                         signed_headers=self.request.get_signed_headers_string(),
                         payload_hash=payload_hash)

    def _create_string_to_sign(self):
        canonical_request = self._create_canonical_request()
        canonical_request_hash = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        return """{dci_algorithm}
{dci_datetime}
{dci_date}
{canonical_request_hash}""".format(dci_algorithm=self.DCI_ALGORITHM,
                                   dci_datetime=self.dci_datetime,
                                   dci_date=self.dci_date,
                                   canonical_request_hash=canonical_request_hash)

    def _sign(self, secret):
        string_to_sign = self._create_string_to_sign()
        signing_key = hmac.new(
            secret.encode('utf-8'),
            self.dci_date.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    @staticmethod
    def _equals(client_signature, header_signature):
        return hmac.compare_digest(
            client_signature.encode('utf-8'),
            header_signature.encode('utf-8')
        )
