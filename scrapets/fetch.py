
import os

from errors import PathDoesNotExist

from storage import utils
from storage.fileobject import FileObject

from packages import reqres

DEFAULT_USER_AGENT='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'


class Fetcher():

    def __init__(self, path, user_agent=DEFAULT_USER_AGENT):

        self._user_agent = user_agent
        if not path or not os.path.exists(path):
            raise PathDoesNotExist("The path does not exist, %s" % path)
        self._path = path

    @property
    def path(self):

        return self._path


    def fetch(self, url, pairtree=False):
        ''' fetch url to file

        pairtree = False, the path to filename is sha256 hashsum from url, no subdirectories
        pairtree = True, the path to filename is the result from sha256 checksum from url
        '''
        result = ()
        if isinstance(url, (str,unicode)):
            result = self._fetch_by_url(url, pairtree)
        elif isinstance(url, (list, tuple)):
            result = self._fetch_by_urls(url, pairtree)
        return result


    def _fetch_by_url(self, url, pairtree=False):
        ''' fetch url and store as file

        pairtree = False, the path to filename is sha256 hashsum from url, no subdirectories
        pairtree = True, the path to filename is the result from sha256 checksum from url
        '''
        filepath = utils.pairtree(utils.sha256str(url)) if pairtree else utils.sha256str(url)
        filepath = os.path.join(self._path, filepath)
        request = reqres.Request(url=url, headers={'User-Agent': self._user_agent})
        resp = request.get().send(stream=True)

        sha256url = utils.sha256str(url)

        if resp.code == 200:
            fo = FileObject(filepath)
            fo.write(resp.body)

            sha256file = utils.sha256file(filepath)
            return ({
                    'url': url,
                    'url.sha256': sha256url,
                    'url.pairtree': utils.pairtree(sha256url),
                    'file.path': filepath,
                    'file.sha256': sha256file,
                    'file.pairtree': utils.pairtree(sha256file),
                    'status.code': resp.code,
                },)
        else:
            return ({
                    'url': url,
                    'status.code': resp.code,
                    'url.sha256': sha256url,
                    'url.pairtree': utils.pairtree(sha256url),
            },)


    def _fetch_by_urls(self, urls, pairtree=False):

        for url in [url.strip() for url in urls if url]:
            yield self._fetch_by_url(url, pairtree)[0]
