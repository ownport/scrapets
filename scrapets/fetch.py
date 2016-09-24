
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


    def fetch(self, url, pairtree=False, meta='short'):
        ''' fetch url and store as file

        pairtree = False, the path to filename is sha256 hashsum from url, no subdirectories
        pairtree = True, the path to filename is the result from sha256 checksum from url

        meta = short, returns url, url.sha256, file.path, status.code
        meta = details, returns url, url.sha256, url.pairtree, file.path, file.sha256, file.pairtree, status.code
        '''
        filepath = utils.pairtree(utils.sha256str(url)) if pairtree else utils.sha256str(url)
        filepath = os.path.join(self._path, filepath)
        request = reqres.Request(url=url, headers={'User-Agent': self._user_agent})
        resp = request.get().send(stream=True)

        sha256url = utils.sha256str(url)

        result = { 'url': url, 'url.sha256': sha256url, 'status.code': None, }

        if resp.code == 200:
            fo = FileObject(filepath)
            fo.write(resp.body)

            filemeta = fo.meta
            result['file.path'] = filepath
            if meta == 'detail':
                result['file.sha256'] = filemeta['content.sha256']
                result['file.pairtree'] = filemeta['content.pairtree']

        if meta == 'detail':
            result['url.pairtree'] = utils.pairtree(sha256url)
        result['status.code'] = resp.code

        return result
