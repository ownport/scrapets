
import sys
import json
import codecs

#
#   click utils
#

def show_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('scrapets, version %s' % __init__.__version__)
    ctx.exit()


def show_help(ctx):
    print(ctx.get_help())
    sys.exit(1)


#
#   File system utils
#

def walk(path):

    if os.path.isfile(path):
        yield path
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for _file in files:
                yield os.path.join(root, _file)

#
#   Metadata processing
#

def import_metadata(db, source, keyname):
    ''' import metadata from JSONline file
    '''
    print "[INFO] Import from %s" % source
    with codecs.open(source, 'r', 'utf-8') as _in:
        for line in _in:
            if not line.strip():
                continue
            try:
                _rec = json.loads(line)
            except:
                continue
            if not _rec.get(keyname):
                continue
            db[_rec.pop(key_name)] = _rec


def export_metadata(db, target, keyname):
    ''' export metadata to JSONline file
    '''
    print "[INFO] Export to %s" % target
    with codecs.open(target, 'w', 'utf-8') as _out:
        for k, v in db.items():
            _rec = { keyname: k }
            _rec.update(v)
            _out.write("%s\n" % json.dumps(_rec))


def join_metadata(left_rows, left_key, right_rows, right_key):
    ''' join metadata rows key names
    '''
    print "[INFO] Join %s:%s with %s:%s" % (left_rows, left_key, right_rows, right_key)
