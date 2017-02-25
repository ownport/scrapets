import __init__

import os
import sys
import json
import codecs


import fetch
import utils
import storage


from packages import click
from packages.sqlitedict import SqliteDict


CONTEXT_SETTINGS = dict(auto_envvar_prefix='SCRAPETS')


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--version', is_flag=True, callback=utils.show_version,
                expose_value=False, is_eager=True, help='Show version')
def cli():
    """A scrapets command line interface."""
    pass


@cli.command()
@click.argument('url', nargs=-1)
@click.option('--urls', type=click.File('rb'), help='fetch files by the list of urls')
@click.option('--index', type=click.File('rw+'), help='index file for storing metadata')
@click.option('--path', default=os.getcwd(), type=click.Path(exists=True), help='the target directory, default: %s' % os.getcwd())
@click.option('--user-agent', default=fetch.DEFAULT_USER_AGENT, help='User agent, default: %s' % fetch.DEFAULT_USER_AGENT)
@click.option('--pairtree/--no-pairtree', default=False, help='create pairtree structure in the target directory, default: turned off')
@click.option('--meta', default='short', help='format or metadata. Possible values: short, detail. Default: short')
@click.pass_context
def fetch(ctx, **opts):
    """ fetch operations
    """
    if not opts['url'] and not opts['urls']:
        utils.show_help(ctx)

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
            if storage.utils.sha256str(u.strip()) not in metadata_index.keys() and u.strip()]

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
        utils.how_help(ctx)

    import re
    import extract

    URLFILTER = None
    if opts['filter']:
        URLFILTER = re.compile(opts['filter'])

    le = extract.LinkExtractor()
    for path in utils.walk(opts['path']):
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
                utils.show_help(ctx)

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
        utils.show_help(ctx)
    if opts['action'] in ('select', 'remove') and not opts['expr']:
        utils.show_help(ctx)

    import content

    _profile = None
    if opts['profile'] and os.path.exists(opts['profile']):
        _profile = codecs.open(opts['profile'], 'r', 'utf-8').read()

    for path in utils.walk(opts['path']):
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
    with SqliteDict(opts['path'], autocommit=True) as _data:

        if opts['import_from'] and os.path.exists(opts['import_from']) and opts['key_name']:
            utils.import_metadata(_data, opts['import_from'], opts['key_name'])
            return

        if opts['export_to'] and opts['key_name']:
            utils.export_metadata(_data, opts['export_to'], opts['key_name'])
            return

    utils.show_help(ctx)


@cli.command()
@click.option('--left-rows', type=click.Path(exists=True), help='the path to the left JSONline file')
@click.option('--left-key', type=str, help='the key name for left rows')
@click.option('--right-rows', type=click.Path(exists=True), help='the path to the right JSONline file')
@click.option('--right-key', type=str, help='the key name for right rows')
@click.pass_context
def join(ctx, **opts):
    ''' join JSONline files by keys
    '''
    if not opts['left_rows'] or not opts['left_key'] or not opts['right_rows'] or not opts['right_key']:
        utils.show_help(ctx)
