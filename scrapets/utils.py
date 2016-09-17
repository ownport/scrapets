
import hashlib

DEFAULT_USER_AGENT='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'


def sha256file(filename):
    ''' returns the sha256 file hashsum
    '''
    sha256hash = hashlib.sha256()

    with open(filename, 'rb') as source:
        while True:
            buff = source.read(4096)
            if not buff:
                break
            sha256hash.update(buff)
    return sha256hash.hexdigest()


def sha256str(string):
    ''' returns sha256 hashsum for the string
    '''
    return hashlib.sha256(string).hexdigest()


def pairtree(path):

    new_path = os.path.join(path[0:2], path[2:4])
    return os.path.join(new_path, path)
