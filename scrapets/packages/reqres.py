#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import urllib
import urllib2
import urlparse

__version__ = '1.1.1'

class HTTPException(Exception):

    def __init__(self, code, msg, headers, body):
        super(HTTPException, self).__init__()
        self.code = code
        self.msg = msg
        self.headers = headers
        self.body = body


class Response(object):

    def __init__(self, code, headers={}, body=None, error_msg=None):

        self.code = code
        self.headers = headers
        self.body = body
        self.error_msg = error_msg

    def json_body(self):

        return json.loads(self.body)


class Request(object):

    def __init__(self, url, headers={}, timeout=60):

        self._url = url
        if isinstance(url, unicode):
            self._url.encode('utf-8')
        self._opener = urllib2.build_opener(urllib2.HTTPHandler)
        self._headers = headers
        self._request = None
        self._timeout = timeout

    @property
    def headers(self):
        ''' return request headers
        '''
        return self._headers


    def _add_headers(self):

        if not self._request:
            raise RuntimeError('Request was not initiated, %s' % self._request)
        for k,v in self._headers.items():
            self._request.add_header(k,v)


    def _make_request(self, method, data=None):

        self._request = urllib2.Request(self._url, data=data)
        self._add_headers()
        self._request.get_method = lambda: method
        return self


    def get(self):
        ''' HTTP GET method
        '''
        return self._make_request('GET')


    def post(self, data=None):
        ''' HTTP POST method
        '''
        return self._make_request('POST', data=data)


    def put(self, data=None):
        ''' HTTP PUT method
        '''
        return self._make_request('PUT', data=data)


    def patch(self, data=None):
        ''' HTTP PATCH method
        '''
        return self._make_request('PATCH', data=data)


    def send(self, stream=False):
        ''' return response of HTTP request

        if stream=True, the body of HTTP response will be as file object
        '''
        result = None
        try:
            response = self._opener.open(self._request, timeout=self._timeout)
            if stream:
                result = Response(200, body=response, headers=dict(response.info().items()))
            else:
                result = Response(200, body=response.read(), headers=dict(response.info().items()))
        except urllib2.HTTPError, err:
            result = Response(code=err.getcode(), error_msg=err.msg,
                                headers=dict(err.hdrs.items()), body='\n'.join(err.readlines()))
        return result

#
#   Utils
#

def get_basic_auth_headers(username, password):

    import base64
    auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    return {"Authorization": "Basic %s" % auth}
