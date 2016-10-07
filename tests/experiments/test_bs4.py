
import pytest

from scrapets.packages.bs4 import BeautifulSoup as BS
from scrapets.packages.bs4.builder._htmlparser import HTMLParserTreeBuilder

CONTENT = '''
<html>
<head>
    <title></title>
</head>
<body>
    <p>
        <a href="link1">Link1</a>
        <a href="link2">Link2</a>
        <a href="link3">Link3</a>
    </p>
</body>
</html>
'''

def test_bs_head():

    soup = BS(CONTENT, builder=HTMLParserTreeBuilder())
    head = unicode(soup.head).replace('\n', '')
    assert head == '<head><title></title></head>'


def test_bs_head():

    soup = BS(CONTENT, builder=HTMLParserTreeBuilder())
    head = unicode(soup.title).replace('\n', '')
    assert head == '<title></title>'


def test_bs_findall():

    soup = BS(CONTENT, builder=HTMLParserTreeBuilder())
    assert [tag.attrs['href'] for tag in soup.find_all('a')] == ['link1', 'link2', 'link3']
    assert [tag.text for tag in soup.find_all('a')] == ['Link1', 'Link2', 'Link3']

def test_bs_select():

    soup = BS(CONTENT, builder=HTMLParserTreeBuilder())
    assert [unicode(r) for r in soup.select('a[href=link1]')] == ['<a href="link1">Link1</a>',]
