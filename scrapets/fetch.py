
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


    def fetch(self, source):
        ''' fetch source
        '''
        result = ()
        if isinstance(source, (str,unicode)):
            result = self._fetch_by_url(source)
        elif isinstance(source, (list, tuple)):
            result = self._fetch_by_urls(source)
        return result


    def _fetch_by_url(self, url):

        filename = os.path.join(self._path, utils.sha256str(url))
        request = reqres.Request(url=url, headers={'User-Agent': self._user_agent})
        resp = request.get().send(stream=True)
        if resp.code == 200:
            fo = FileObject(filename)
            fo.write(resp.body)
            return ({
                    'url': url,
                    'url/sha256': utils.sha256str(url),
                    'url/pairtree': utils.pairtree(utils.sha256str(url)),
                    'file/sha256': utils.sha256file(filename),
                    'file/pairtree': utils.pairtree(utils.sha256file(filename))
                },)
        else:
            return ()


    def _fetch_by_urls(self, urls):

        for url in [url.strip() for url in urls if url]:
            yield self._fetch_by_url(url)[0]
