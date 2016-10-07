import __init__

import os
import sys
import json

from packages import click

from storage import utils
from fetch import DEFAULT_USER_AGENT

CONTEXT_SETTINGS = dict(auto_envvar_prefix='SCRAPETS')

def show_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('scrapets, version %s' % __init__.__version__)
    ctx.exit()


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
        print(ctx.get_help())
        sys.exit(1)

    import fetch

    metadata_index = dict()
    if opts['index']:
        try:
            for rec in opts['index'].readlines():
                rec = json.loads(rec)
                sha256url = rec.pop('url.sha256')
                metadata_index[sha256url] = rec
        except ValueError:
            pass

    if opts['url']:
        urls = opts['url']
    elif opts['urls']:
        urls = opts['urls'].readlines()

    urls = [u.strip() for u in urls if utils.sha256str(u.strip()) not in metadata_index.keys()]

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
@click.option('--file', type=click.File('rb'), help='the path to the file for processing')
@click.option('--directory', type=click.Path(exists=True), help='the path to the directory for processing')
@click.option('--filter', help='regular experssion for url filtering ')
@click.pass_context
def linkextract(ctx, **opts):
    ''' link extractor
    '''
    if not opts['file'] and not opts['directory']:
        print(ctx.get_help())
        sys.exit(1)

    import re
    import extract

    URLFILTER = None
    if opts['filter']:
        URLFILTER = re.compile(opts['filter'])

    if opts['file']:
        le = extract.LinkExtractor()
        le.feed(opts['file'].read().decode('utf-8'))
        for link in filter(lambda u: URLFILTER.search(u) if URLFILTER else True, le.links):
            print link

    elif opts['directory']:
        le = extract.LinkExtractor()
        for root, dirs, files in os.walk(opts['directory']):
            for _file in files:
                try:
                    path = os.path.join(root, _file)
                    le.feed(open(path).read().decode('utf-8'))
                    for link in filter(lambda u: URLFILTER.search(u) if URLFILTER else True, le.links):
                        print link
                except Exception, err:
                    print >> sys.stderr, "[ERROR] Cannot process the file, %s" % (path,)

@cli.command()
@click.option('--action', type=click.Choice(['select', 'remove']), help='content processing action')
# @click.option('--xpath', help='xpath for the action')
@click.option('--selector', help='Selector for the action')
@click.option('--file', type=click.File('rb'), help='the path to the file for processing')
@click.option('--directory', type=click.Path(exists=True), help='the path to the directory for processing')
@click.pass_context
def content(ctx, **opts):
    ''' content processing
    '''
    if not opts['file'] and not opts['directory']:
        print(ctx.get_help())
        sys.exit(1)

    import content

    if opts['file']:
        cntnt = content.CCSSelectParser(opts['file'].read())
        if opts['action'] == 'select':
            print cntnt.select(opts['selector'])
        elif opts['action'] == 'remove':
            print cntnt.remove(opts['selector'])

    elif opts['directory']:
        for root, dirs, files in os.walk(opts['directory']):
            for _file in files:
                try:
                    path = os.path.join(root, _file)
                    cntnt = content.Content(open(path).read())
                except Exception, err:
                    print >> sys.stderr, "[ERROR] Cannot process the file, %s" % (path,)
