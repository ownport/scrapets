import __init__

import os
import sys

from packages import click
from fetch import DEFAULT_USER_AGENT

CONTEXT_SETTINGS = dict(auto_envvar_prefix='SCRAPETS')


@click.group(context_settings=CONTEXT_SETTINGS)
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
@click.pass_context
def fetch(ctx, **opts):
    """ Fetch operations
    """

    if not opts['url'] and not opts['urls']:
        print(ctx.get_help())
        sys.exit(1)

    import fetch

    fetcher = fetch.Fetcher(opts['path'], user_agent=opts['user_agent'])

    if opts['url']:
        print map(lambda u: fetcher.fetch(u.strip()), opts['url'])
    if opts['urls']:
        print map(lambda u: fetcher.fetch(u.strip()), opts['urls'].readlines())
