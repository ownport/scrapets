from setuptools import setup
from scrapets import __version__

setup(
    name='scrapets',
    version=__version__,
    py_modules=['scrapets'],
    entry_points='''
        [console_scripts]
        scrapets=scrapets.main:cli
    ''',
)
