
#
# File Object component
#

import os
import utils

class FileObject(object):

    def __init__(self, path):
        self._path = path


    @property
    def path(self):
        ''' returns the path to the fileobject
        '''
        return self._path


    @property
    def meta(self):
        ''' return dict of meta information
        '''
        filename = os.path.basename(self._path)
        filename_sha256 = utils.sha256str(filename)
        content_sha256 = utils.sha256file(self._path)
        return {
            'file.path': self._path,
            'file.name': filename,
            'file.name.sha256': filename_sha256,
            'file.name.pairtree': utils.pairtree(filename_sha256),
            'content.sha256': content_sha256,
            'content.pairtree': utils.pairtree(content_sha256),
            'content.size': os.stat(self._path).st_size,
        }


    def read(self, mode='rb'):
        ''' read data from file
        '''
        result = None
        with open(self._path, mode) as fo:
            result = fo.read()
        return result


    def write(self, data, mode='w'):
        ''' write data into fileobject
        '''
        # data as string or unicode
        if isinstance(data, (str, unicode)):
            with open(self._path, mode) as fo:
                fo.write(data)
            return

        # data as file object with read() method
        read_method = getattr(data, 'read', None)
        if read_method and callable(read_method):
            self.mktemp()
            with open(self._path, mode) as fo:
                while True:
                    chunk = data.read(64000)
                    if not chunk:
                        break
                    fo.write(chunk)
            self.rmtemp()
            return
        else:
            raise RuntimeError('Unknown data format: [%s] %s' % (type(data), data))


    def rename(self, newpath):
        ''' rename current path to new one
        '''
        self.mkdirs()
        os.rename(self._path, newpath)
        self._path = newpath


    def mktemp(self):
        """ make the path as temporary
        """
        oldpath = newpath = self._path
        if not oldpath.endswith('.part'):
            newpath = oldpath + ".part"

        if os.path.exists(oldpath):
            self.rename(newpath)

        self._path = newpath
        self.mkdirs()
        return self._path


    def rmtemp(self):
        ''' remove .part by the end of the path
        '''
        oldpath = newpath = self._path
        if oldpath.endswith('.part'):
            newpath = oldpath[:-len('.part')]

        if os.path.exists(oldpath):
            self.rename(newpath)

        self._path = newpath
        self.mkdirs()
        return self._path


    def mkdirs(self, path=None):
        ''' make directories is not exists
        '''
        path = self._path if not path else path
        dirname = os.path.dirname(path)
        if os.path.exists(dirname):
            return
        os.makedirs(dirname)
