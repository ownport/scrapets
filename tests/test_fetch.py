
import os
import copy

import pytest

from StringIO import StringIO

from scrapets.fetch import Fetcher
from scrapets.errors import PathDoesNotExist

# -------------------------------------------------------------
#
#   Parameters
#

SUCCESS_URL = 'http://example.com'
NONE_URL = 'http://none.com'

URLS = {
    'http://example.com': {
        'sha256': 'f0e6a6a97042a4f1f1c87f5f7d44315b2d852c2df5c7991cc66241bf7072d1c4',
        'pairtree': 'f0/e6/f0e6a6a97042a4f1f1c87f5f7d44315b2d852c2df5c7991cc66241bf7072d1c4',
    },
    'http://none.com': {
        'url.sha256': '824d4352291905ff7ecfaa24f5490075b0b51256f851d1171847735a5e6ab41b',
        'url.pairtree': '82/4d/824d4352291905ff7ecfaa24f5490075b0b51256f851d1171847735a5e6ab41b'
    }
}

RESULT_STATUS_200 = {
    'url': 'http://example.com',
    'url.sha256': 'f0e6a6a97042a4f1f1c87f5f7d44315b2d852c2df5c7991cc66241bf7072d1c4',
    'url.pairtree': 'f0/e6/f0e6a6a97042a4f1f1c87f5f7d44315b2d852c2df5c7991cc66241bf7072d1c4',
    'file.path': None,
    'file.sha256': '9a9b3e8cb888d070aff71af3e08626005ebb948266a7a97dbacbd054d7231046',
    'file.pairtree': '9a/9b/9a9b3e8cb888d070aff71af3e08626005ebb948266a7a97dbacbd054d7231046',
    'status.code': 200,
}

RESULT_STATUS_404 = {
    'url': 'http://none.com',
    'status.code': 404,
    'url.sha256': '824d4352291905ff7ecfaa24f5490075b0b51256f851d1171847735a5e6ab41b',
    'url.pairtree': '82/4d/824d4352291905ff7ecfaa24f5490075b0b51256f851d1171847735a5e6ab41b'
}

# -------------------------------------------------------------
#
#   Mocks
#

class MockedRequest(object):

    def __init__(self, url, headers):

        self._url = url
        self._headers = headers

    def get(self):

        return self

    def send(self, stream=False):

        if self._url == SUCCESS_URL:
            return MockedResponse(code=200, body=StringIO('MockedResponse200'))
        elif self._url == NONE_URL:
            return MockedResponse(code=404, body=StringIO('MockedResponse404'))


class MockedResponse(object):

    def __init__(self, code, body):

        self.code = code
        self.body = body

# -------------------------------------------------------------
#
#   test cases
#

def test_fetch_create(tmpdir):

    path = str(tmpdir)
    fetcher = Fetcher(path)
    assert isinstance(fetcher, Fetcher)
    assert fetcher.path == path


def test_fetch_path_does_not_exist():

    with pytest.raises(PathDoesNotExist):
        fetcher = Fetcher('the-path-does-not-exist')


def test_fetch_single_url(tmpdir, monkeypatch):

    monkeypatch.setattr("scrapets.packages.reqres.Request", lambda url, headers: MockedRequest(url, headers))
    path = str(tmpdir)

    testcase_result = copy.copy(RESULT_STATUS_200)
    testcase_result['file.path'] = os.path.join(path, URLS[SUCCESS_URL]['sha256'])

    fetcher = Fetcher(path)
    assert fetcher.fetch(SUCCESS_URL) == (testcase_result,)


def test_fetch_single_url_pairtree(tmpdir, monkeypatch):

    monkeypatch.setattr("scrapets.packages.reqres.Request", lambda url, headers: MockedRequest(url, headers))
    path = str(tmpdir)

    testcase_result = copy.copy(RESULT_STATUS_200)
    testcase_result['file.path'] = os.path.join(path, URLS[SUCCESS_URL]['pairtree'])

    fetcher = Fetcher(path)
    assert fetcher.fetch(SUCCESS_URL, pairtree=True) == (testcase_result,)


def test_fetch_multiple_urls(tmpdir, monkeypatch):

    monkeypatch.setattr("scrapets.packages.reqres.Request", lambda url, headers: MockedRequest(url, headers))
    path = str(tmpdir)
    fetcher = Fetcher(path)
    assert fetcher.path == path

    testcase_result = copy.copy(RESULT_STATUS_200)
    testcase_result['file.path'] = os.path.join(path, URLS[SUCCESS_URL]['sha256'])

    urls = [SUCCESS_URL for i in range(3)]
    for r in fetcher.fetch(urls):
        assert r == testcase_result


def test_fetch_return_error_result(tmpdir, monkeypatch):

    monkeypatch.setattr("scrapets.packages.reqres.Request", lambda url, headers: MockedRequest(url, headers))
    path = str(tmpdir)
    fetcher = Fetcher(path)
    assert fetcher.path == path
    assert fetcher.fetch(NONE_URL) == (RESULT_STATUS_404,)
