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
from dciauth.v2.signature import is_valid
from dciauth.v2.headers import parse_headers


app = Flask(__name__)


@app.route("/api/v1/jobs", methods=["GET", "POST"])
def get_jobs():
    algorithm = request.headers["Authorization"].split(" ")[0]
    if algorithm in ["DCI-HMAC-SHA256", "DCI2-HMAC-SHA256", "AWS4-HMAC-SHA256"]:
        valid, error_message = is_valid(
            {
                "method": request.method,
                "endpoint": request.path,
                "data": request.data,
                "params": request.args.to_dict(flat=True),
            },
            {"secret_key": "secret"},
            parse_headers(request.headers),
        )
        if valid:
            return jsonify({"jobs": []})
        else:
            raise Exception("Authentication failed: %s" % error_message)
    raise Exception("Authentication failed")


@app.route("/api/v1/files/<path:filepath>", methods=["GET"])
def get_file(filepath):
    algorithm = request.headers["Authorization"].split(" ")[0]
    if algorithm in ["DCI-HMAC-SHA256", "DCI2-HMAC-SHA256", "AWS4-HMAC-SHA256"]:
        valid, error_message = is_valid(
            {
                "method": request.method,
                "endpoint": request.path,
                "data": request.data,
                "params": request.args.to_dict(flat=True),
            },
            {"secret_key": "secret"},
            parse_headers(request.headers),
        )
        if valid:
            return jsonify({"jobs": []})
        else:
            raise Exception("Authentication failed: %s" % error_message)
    raise Exception("Authentication failed")


if __name__ == "__main__":
    app.run(port=65432)
