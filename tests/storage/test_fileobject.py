
import os
import pytest

from scrapets.storage.fileobject import FileObject

def test_fileobject_init(tmpdir):

    path = str(tmpdir.join('fileobject-init'))
    fo = FileObject(path)
    assert isinstance(fo, FileObject)
    assert fo.path == path


def test_fileobject_write_str(tmpdir):

    path = str(tmpdir.join('fileobject-write-str'))
    fo = FileObject(path)
    fo.write('fileobject-write-str')
    assert fo.path == path


def test_fileobject_write_read_str(tmpdir):

    path = str(tmpdir.join('fileobject-write-read-str'))
    fo = FileObject(path)
    fo.write('fileobject-write-read-str')
    assert fo.path == path
    assert fo.read() == 'fileobject-write-read-str'


def test_fileobject_write_file(tmpdir):

    from cStringIO import StringIO
    path = str(tmpdir.join('fileobject-write-file'))
    fo = FileObject(path)
    fo.write(StringIO('fileobject-write-file'))
    assert fo.path == path


def test_fileobject_meta(tmpdir):

    path = str(tmpdir.join('fileobject-meta'))
    fo = FileObject(path)
    fo.write('fileobject-meta-content')
    assert fo.path == path
    assert fo.meta == {
                        'filename.path': path,
                        'filename.name': 'fileobject-meta',
                        'filename.sha256': 'd2088266c0fc064b249d1b9959c80d986cc72b377066ad80e7211837d57e6c09',
                        'filename.pairtree': 'd2/08/d2088266c0fc064b249d1b9959c80d986cc72b377066ad80e7211837d57e6c09',
                        'content.sha256': 'e7de0e8d1d59a0f01d7de63a9ed1948f93554bdf63d8f544655b5a89c2e2af1c',
                        'content.pairtree': 'e7/de/e7de0e8d1d59a0f01d7de63a9ed1948f93554bdf63d8f544655b5a89c2e2af1c',
                        'content.size': 23,
    }

def test_fileobject_write_none(tmpdir):

    path = str(tmpdir.join('fileobject-write-none'))
    fo = FileObject(path)
    with pytest.raises(RuntimeError):
        fo.write(None)


def test_fileobject_rename(tmpdir):

    path = tmpdir.join('fileobject-rename')
    fo = FileObject(str(path))
    fo.write('fileobject-rename')
    assert fo.path == path

    new_path = os.path.join(path.dirname, 'fileobject-rename-new')
    fo.rename(new_path)
    assert fo.read() == 'fileobject-rename'


def test_fileobject_tmppath_no_file(tmpdir):

    path = tmpdir.join('fileobject-tmppath-no-file')
    fo = FileObject(str(path))
    assert fo.path == path

    fo.mktemp()
    assert fo.path.endswith('fileobject-tmppath-no-file.part')
    assert not os.path.exists(fo.path)

    fo.rmtemp()
    assert fo.path.endswith('fileobject-tmppath-no-file')
    assert not os.path.exists(fo.path)


def test_fileobject_tmppath_with_file(tmpdir):

    path = tmpdir.join('fileobject-tmppath-with-file')
    fo = FileObject(str(path))
    assert fo.path == path

    fo.write('fileobject-tmppath-with-file')
    assert fo.read() == 'fileobject-tmppath-with-file'

    fo.mktemp()
    assert fo.path.endswith('fileobject-tmppath-with-file.part')
    assert os.path.exists(fo.path)

    fo.rmtemp()
    assert fo.path.endswith('fileobject-tmppath-with-file')
    assert os.path.exists(fo.path)


def test_fileobject_tmppath_two_files_with_same_name(tmpdir):

    path1 = tmpdir.join('fileobject-tmppath-twofiles')
    fo1 = FileObject(str(path1))
    fo1.write('fileobject-tmppath-twofiles-1')
    assert fo1.read() == 'fileobject-tmppath-twofiles-1'

    path2 = tmpdir.join('fileobject-tmppath-twofiles')
    fo2 = FileObject(str(path2))
    fo2.write('fileobject-tmppath-twofiles-2')
    assert fo2.read() == 'fileobject-tmppath-twofiles-2'
