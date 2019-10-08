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
from flask import Flask
from flask import request
from flask import jsonify
from dciauth.signature import Signature
from dciauth.request import AuthRequest
from dciauth.v2.signature import is_valid
from dciauth.v2.headers import parse_headers


app = Flask(__name__)


@app.route("/api/v1/jobs", methods=["GET", "POST"])
def get_jobs():
    algorithm = request.headers["Authorization"].split(" ")[0]
    if algorithm == "DCI-HMAC-SHA256":
        auth_request = AuthRequest(
            method=request.method,
            endpoint=request.path,
            payload=request.get_json(silent=True),
            headers=request.headers,
            params=request.args.to_dict(flat=True),
        )
        signature = Signature(request=auth_request)
        if not signature.is_valid("secret"):
            raise Exception("Authentication failed: signature invalid")
        if signature.is_expired():
            raise Exception("Authentication failed: signature expired")
    if algorithm == "DCI2-HMAC-SHA256":
        valid, error_message = is_valid(
            {
                "method": request.method,
                "endpoint": request.path,
                "payload": request.get_json(silent=True),
                "params": request.args.to_dict(flat=True),
            },
            {"secret_key": "secret"},
            parse_headers(request.headers),
        )
        if not valid:
            raise Exception("Authentication failed: %s" % error_message)
    return jsonify({"jobs": []})


if __name__ == "__main__":
    app.run()
