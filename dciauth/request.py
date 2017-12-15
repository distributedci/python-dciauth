import json
from collections import OrderedDict

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class AuthRequest(object):
    def __init__(self, method='GET', endpoint='/', payload=None, headers=None, params=None):
        self.algorithm = 'DCI-HMAC-SHA256'
        self.method = method.upper()
        self.endpoint = endpoint
        self.payload = payload or {}
        self.headers = headers or {}
        authorization_header = self.headers.get('Authorization', '')
        info = self._get_info_from_authorization_header(authorization_header)
        self.client_type = info.get('client_type')
        self.client_id = info.get('client_id')
        self.signature = info.get('signature')
        self.headers = self._order_dict(self._filter_headers(self.headers, authorization_header))
        self.signed_headers = self._calc_signed_headers(self.headers)
        self.params = params or {}
        self.query_string = urlencode(self._order_dict(self.params))
        if payload:
            self.payload_string = json.dumps(self._order_dict(self.payload))
        else:
            self.payload_string = ''

    @staticmethod
    def find_between(s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    def _get_info_from_authorization_header(self, authorization_header):
        info = {}
        if authorization_header:
            credentials = self.find_between(authorization_header, 'Credential=', ',').split('/')
            info['client_type'] = credentials[0]
            info['client_id'] = credentials[1]
            info['signature'] = self.find_between(authorization_header, 'Signature=', ',')
        return info

    @staticmethod
    def _order_dict(dictionary):
        return OrderedDict(sorted(dictionary.items(), key=lambda k: k[0]))

    @staticmethod
    def _calc_signed_headers(headers):
        return ';'.join(headers.keys())

    def _filter_headers(self, headers, authorization_header):
        if not authorization_header:
            return headers
        signed_headers = self.find_between(authorization_header, 'SignedHeaders=', ',').split(';')
        filtered_headers = {}
        for key, value in headers.items():
            if key in signed_headers:
                filtered_headers[key] = value
        return filtered_headers

    def add_header(self, key, value):
        self.headers[key] = value
        self.signed_headers = self._calc_signed_headers(self.headers)

    def get_signed_headers(self, client_type, client_id, signature):
        auth_string_format = "{dci_algorithm} Credential={client_type}/{client_id}, SignedHeaders={signed_headers}, Signature={signature},"
        headers = self.headers.copy()
        headers['Authorization'] = auth_string_format.format(
            dci_algorithm=self.algorithm,
            client_type=client_type,
            client_id=client_id,
            signed_headers=self.signed_headers,
            signature=signature)
        return headers
