import __init__

import os
import sys
import json
import codecs

from packages import click

from storage import utils
from fetch import DEFAULT_USER_AGENT

CONTEXT_SETTINGS = dict(auto_envvar_prefix='SCRAPETS')

def show_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('scrapets, version %s' % __init__.__version__)
    ctx.exit()


def show_help(ctx):
    print(ctx.get_help())
    sys.exit(1)


def walk(path):

    if os.path.isfile(path):
        yield path
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for _file in files:
                yield os.path.join(root, _file)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--version', is_flag=True, callback=show_version,
                expose_value=False, is_eager=True, help='Show version')
def cli():
    """A scrapets command line interface."""
    pass


@cli.command()
@click.argument('url', nargs=-1)
@click.option('--urls', type=click.File('rb'), help='fetch files by the list of urls')
@click.option('--index', type=click.File('rw+'), help='index file for storing metadata')
@click.option('--path', default=os.getcwd(), type=click.Path(exists=True), help='the target directory, default: %s' % os.getcwd())
@click.option('--user-agent', default=DEFAULT_USER_AGENT, help='User agent, default: %s' % DEFAULT_USER_AGENT)
@click.option('--pairtree/--no-pairtree', default=False, help='create pairtree structure in the target directory, default: turn off')
@click.option('--meta', default='short', help='format or metadata. Possible values: short, detail. Default: short')
@click.pass_context
def fetch(ctx, **opts):
    """ fetch operations
    """
    if not opts['url'] and not opts['urls']:
        show_help(ctx)

    import fetch

    metadata_index = dict()
    if opts['index']:
        try:
            for rec in opts['index'].readlines():
                rec = json.loads(rec)
                if rec[u'status.code'] != 200:
                    continue
                sha256url = rec.pop('url.sha256')
                metadata_index[sha256url] = rec
        except ValueError:
            pass

    if opts['url']:
        urls = opts['url']
    elif opts['urls']:
        urls = opts['urls'].readlines()

    urls = [u.strip() for u in urls \
            if utils.sha256str(u.strip()) not in metadata_index.keys() and u.strip()]

    fetcher = fetch.Fetcher(opts['path'], user_agent=opts['user_agent'])
    for url in urls:
        res = fetcher.fetch(url.strip(), pairtree=opts['pairtree'], meta=opts['meta'])
        json_res = json.dumps(res)
        print json_res
        if opts['index']:
            opts['index'].write("%s\n" % json_res)
        sha256url = res.pop('url.sha256')
        metadata_index[sha256url] = res


@cli.command()
@click.option('--path', type=click.Path(exists=True), help='the path to the file or directory for processing')
@click.option('--filter', help='regular experssion for url filtering ')
@click.pass_context
def linkextract(ctx, **opts):
    ''' link extractor
    '''
    if not opts['path']:
        show_help(ctx)

    import re
    import extract

    URLFILTER = None
    if opts['filter']:
        URLFILTER = re.compile(opts['filter'])

    le = extract.LinkExtractor()
    for path in walk(opts['path']):
        try:
            le.feed(open(path).read().decode('utf-8'))
            for link in filter(lambda u: URLFILTER.search(u) if URLFILTER else True, le.links):
                print link
        except Exception, err:
            print >> sys.stderr, "[ERROR] Cannot process the file, %s" % (path,)


@cli.command()
@click.option('--action', type=click.Choice(['select', 'remove']), help='content processing action')
# @click.option('--xpath', help='xpath for the action')
@click.option('--expr', help='XPath/CSS expression for the action.' + \
                            'The format: <method>:<expr>, where method = xpath | css. ' + \
                            'Example: xpath:./title/text()')
@click.option('--profile', help='The profile for actions "transform" and "fields", yaml file')
@click.option('--path', type=click.Path(exists=True), help='the path to the file or directory for processing')
@click.pass_context
def content(ctx, **opts):
    ''' content processing
    '''
    def process(action, path, expr=None, profile=None):

        _content = content.Content('content', codecs.open(path, 'r', 'utf-8').read())

        if expr:
            method, expr = expr.split(':', 1)
            if method not in ('xpath', 'css'):
                show_help(ctx)

            if action == 'select':
                print json.dumps(_content.select(expr, method).extract())
            elif action == 'remove':
                print json.dumps(_content.remove(expr, method).extract())

        if profile:
            result = _content.process(profile)
            if isinstance(result, content.Content):
                print json.dumps(result.extract())
            elif isinstance(result, dict):
                print json.dumps(result)
            else:
                raise RuntimeError('Unknown result type, %s' % type(result))

    if not opts['path']:
        show_help(ctx)
    if opts['action'] in ('select', 'remove') and not opts['expr']:
        show_help(ctx)

    import content

    _profile = None
    if opts['profile'] and os.path.exists(opts['profile']):
        _profile = codecs.open(opts['profile'], 'r', 'utf-8').read()

    for path in walk(opts['path']):
        process(opts['action'], path, expr=opts['expr'], profile=_profile)
        try:
            pass
        except Exception, err:
            print >> sys.stderr, "[ERROR] Cannot process the file, %s. Error: %s" % (path, err)


@cli.command()
@click.option('--path', help='the path to the metadata file')
@click.option('--import-from', type=click.Path(exists=True), help='the path to the JSONline file for import')
@click.option('--export-to', type=click.Path(), help='the path to the JSONline file for export')
@click.option('--key-name', type=str, help='the key name, mandatory for import/export')
@click.pass_context
def metadata(ctx, **opts):
    ''' metadata processing
    '''
    from packages.sqlitedict import SqliteDict
    with SqliteDict(opts['path'], autocommit=True) as _data:

        if opts['import_from'] and os.path.exists(opts['import_from']) and opts['key_name']:
            print "[INFO] Import from %s" % opts['import_from']
            with codecs.open(opts['import_from'], 'r', 'utf-8') as _in:
                for line in _in:
                    if not line.strip():
                        continue
                    try:
                        _rec = json.loads(line)
                    except:
                        continue
                    if not _rec.get(opts['key_name']):
                        continue
                    _data[_rec.pop(opts['key_name'])] = _rec
            return

        if opts['export_to'] and opts['key_name']:
            print "[INFO] Export to %s" % opts['export_to']
            with codecs.open(opts['export_to'], 'w', 'utf-8') as _out:
                for k, v in _data.items():
                    _rec = { opts['key_name']: k }
                    _rec.update(v)
                    _out.write("%s\n" % json.dumps(_rec))
            return

    show_help(ctx)
