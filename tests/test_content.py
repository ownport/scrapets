
import pytest

from scrapets import content
from scrapets.packages import bs4

CONTENT = '''
<html>
<head><title>Test content</title></head>
<body>
    <p>Test content</p>
    <a href="link1">Link1</a>
    <a href="link2">Link2</a>
    <a href="link3">Link3</a>
    <p>
        <a href="link4">Link4</a>
        <a href="link5">Link5</a>
        <a href="link6">Link6</a>
    </p>
</body>
</html>
'''

#
#   XPathParser
#

def test_xpathparser_create():

    cntnt = content.XPathParser(CONTENT)
    assert isinstance(cntnt, content.XPathParser)


def test_xpathparser_select():

    cntnt = content.XPathParser(CONTENT)
    assert cntnt.select('.//head') == ['<head><title>Test content</title></head>',]
    assert cntnt.select('.//a[@href="link1"]') == ['<a href="link1">Link1</a>',]


def test_xpathparser_remove():

    cntnt = content.XPathParser(CONTENT)
    cntnt = cntnt.remove('.//head')
    assert isinstance(cntnt, content.XPathParser)
    cntnt = cntnt.remove('.//p')
    cntnt = cntnt.remove('.//body')
    assert str(cntnt) == '<html>\n</html>'


def test_xpathparser_remove_several_elements():

    cntnt = content.XPathParser(CONTENT)
    cntnt = cntnt.remove('.//a')
    cntnt = cntnt.remove('.//body')
    cntnt = cntnt.remove('.//head')
    assert str(cntnt) == '<html>\n</html>'

#
#   CCSSelectParser
#

def test_ccsselectparser_create():

    cntnt = content.CCSSelectParser(CONTENT)
    assert isinstance(cntnt, content.CCSSelectParser)


def test_ccsselectparser_select():

    cntnt = content.CCSSelectParser(CONTENT)
    assert cntnt.select('head') == ['<head><title>Test content</title></head>',]
    assert cntnt.select('a[href=link1]') == ['<a href="link1">Link1</a>',]
    assert cntnt.select('a[href="link1"]') == ['<a href="link1">Link1</a>',]
    assert cntnt.select('a') == [
            '<a href="link1">Link1</a>', '<a href="link2">Link2</a>', '<a href="link3">Link3</a>',
            '<a href="link4">Link4</a>', '<a href="link5">Link5</a>', '<a href="link6">Link6</a>',
    ]
    assert cntnt.select('p a[href="link5"]') == ['<a href="link5">Link5</a>',]
    assert cntnt.select('p > a[href="link5"]') == ['<a href="link5">Link5</a>',]


def test_ccsselectparser_select_attrs():

    cntnt = content.CCSSelectParser(CONTENT)
    assert cntnt.select('a', lambda a: a.get('href')) == ['link1', 'link2', 'link3', 'link4', 'link5', 'link6']
    assert cntnt.select('p', lambda p: p.string) == ['Test content', None]
    assert cntnt.select('title', lambda t: t.string) == ['Test content']

def test_ccsselectparser_select_not_html():

    cntnt = content.CCSSelectParser(CONTENT)
    assert map(lambda e: type(e), cntnt.select('title', html=False)) == [bs4.element.Tag,]


def test_ccsselectparser_remove():

    cntnt = content.CCSSelectParser(CONTENT)
    cntnt = cntnt.remove('head')
    assert isinstance(cntnt, content.CCSSelectParser)
    cntnt = cntnt.remove('p')
    cntnt = cntnt.remove('body')
    assert str(cntnt).replace('\n', '') == '<html></html>'
    assert unicode(cntnt).replace(u'\n', u'') == u'<html></html>'
