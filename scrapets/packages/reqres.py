#!/usr/bin/env python

import sys
import json
import urllib
import urllib2
import urlparse

class HTTPException(Exception):
    def __init__(self, code, msg, headers, body):
        super(HTTPException, self).__init__()
        self.code = code
        self.msg = msg
        self.headers = headers
        self.body = body


class HTTPResponse(object):

    def __init__(self, code, headers={}, body=None, error_msg=None):

        self.code = code
        self.headers = headers
        self.body = body
        self.error_msg = error_msg

    def json_body(self):

        return json.loads(self.body)


class HttpRequest(object):

    def __init__(self, url, headers={}, timeout=60):

        self._url = url
        self._opener = urllib2.build_opener(urllib2.HTTPHandler)
        self._headers = headers
        self._request = None
        self._timeout = timeout

    def _add_headers(self):

        for k,v in self._headers.items():
            self._request.add_header(k,v)

    def make_request(self, method, data=None):

        self._request = urllib2.Request(self._url, data=data)
        self._add_headers()
        self._request.get_method = lambda: method
        return self


    def get(self):

        return self.make_request('GET')


    def post(self, data=None):

        return self.make_request('POST', data=data)


    def put(self, data=None):

        return self.make_request('PUT', data=data)


    def patch(self, data=None):

        return self.make_request('PATCH', data=data)


    def send(self):
        ''' return response of HTTP request
        '''
        try:
            response = self._opener.open(self._request, timeout=self._timeout)
            return HTTPResponse(200, body=response.read(), headers=dict(response.info().items()))
        except urllib2.HTTPError, err:
            return HTTPResponse(code=err.getcode(), error_msg=err.msg,
                                headers=dict(err.headers.items()), body='\n'.join(err.readlines()))


#
#   Utils
#

def get_basic_auth_headers(username, password):

    import base64
    auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    return {"Authorization": "Basic %s" % auth}
