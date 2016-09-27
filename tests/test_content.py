
import pytest

from scrapets import content

CONTENT = '''
<html>
<head><title>Test content</title></head>
<body>
    <p>Test content</p>
    <a href="link1">Link1</a>
    <a href="link2">Link2</a>
    <a href="link3">Link3</a>
</body>
</html>
'''

def test_content_create():

    cntnt = content.Content(CONTENT)
    assert isinstance(cntnt, content.Content)


def test_content_select():

    cntnt = content.Content(CONTENT)
    assert cntnt.select('.//head') == ['<head><title>Test content</title></head>',]
    assert cntnt.select('.//a[@href="link1"]') == ['<a href="link1">Link1</a>',]


def test_content_remove():

    cntnt = content.Content(CONTENT)
    cntnt = cntnt.remove('.//head')
    assert isinstance(cntnt, content.Content)
    cntnt = cntnt.remove('.//p')
    cntnt = cntnt.remove('.//body')
    assert str(cntnt) == '<html>\n</html>'


def test_content_remove_several_elements():

    cntnt = content.Content(CONTENT)
    cntnt = cntnt.remove('.//a')
    cntnt = cntnt.remove('.//body')
    cntnt = cntnt.remove('.//head')    
    assert str(cntnt) == '<html>\n</html>'
