from setuptools import setup
from testsuites import __version__

setup(
    name='scraplets',
    version=__version__,
    py_modules=['scraplets'],
    entry_points='''
        [console_scripts]
        scraplets=scraplets.main:run
    ''',
)
