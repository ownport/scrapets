import __init__

import os
import sys
import json

from packages import click
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
@click.option('--urls',
                type=click.File('rb'),
                help='fetch files by the list of urls')
@click.option('--path',
                default=os.getcwd(),
                type=click.Path(exists=True),
                help='the target directory, default: %s' % os.getcwd())
@click.option('--user-agent',
                default=DEFAULT_USER_AGENT,
                help='User agent, default: %s' % DEFAULT_USER_AGENT)
@click.option('--pairtree/--no-pairtree',
                default=False,
                help='create pairtree structure in the target directory, default: turn off')
@click.option('--meta',
                default='short',
                help='format or metadata. Possible values: short, detail. Default: short')
@click.pass_context
def fetch(ctx, **opts):
    """ Fetch operations
    """
    if not opts['url'] and not opts['urls']:
        print(ctx.get_help())
        sys.exit(1)

    import fetch

    if opts['url']:
        urls = opts['url']
    elif opts['urls']:
        urls = opts['urls'].readlines()

    fetcher = fetch.Fetcher(opts['path'], user_agent=opts['user_agent'])
    for res in map(lambda u: fetcher.fetch(u.strip(), pairtree=opts['pairtree'], meta=opts['meta']), urls):
        print json.dumps(res)
