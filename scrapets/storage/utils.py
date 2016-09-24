
import os
import hashlib

def sha256file(path):
    ''' returns the sha256 file hashsum
    '''
    if not os.path.exists(path):
        return None

    sha256hash = hashlib.sha256()
    with open(path, 'rb') as obj:
        map(lambda b: sha256hash.update(b), obj.read(64000))
    return sha256hash.hexdigest()


def sha256str(string):
    ''' returns sha256 hashsum for the string
    '''
    return hashlib.sha256(string).hexdigest()


def pairtree(path):

    new_path = os.path.join(path[0:2], path[2:4])
    return os.path.join(new_path, path)
