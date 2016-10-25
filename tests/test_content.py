import pytest

from scrapets.content import Content

BASE_URL="http://example.com"

CONTENT = '''
<html>
<head><title>Test content title</title></head>
<body>
    <p>Test content header</p>
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


PROFILE = '''
profile: Test profile

rules:
- name: remove title
  select:
    method: css
    expr: body > p
- remove:
    method: css
    expr: 'a'
- remove:
    method: css
    expr: 'p:nth-child(2)'

fields:
- name: title
  xpath: .//title/text()
- name: header
  xpath: .//body/p[1]/text()
'''

EMPTY_PROFILE = '''
profile: Empty
'''


def test_content_create():

    content = Content(BASE_URL, "<p>Test content</p>")
    assert isinstance(content, Content)

    with pytest.raises(RuntimeError) as err:
        content = Content(None, "<p>Test content</p>")

    with pytest.raises(RuntimeError) as err:
        content = Content([BASE_URL,], None)

    with pytest.raises(RuntimeError) as err:
        content = Content(BASE_URL, None)

    with pytest.raises(RuntimeError) as err:
        content = Content(BASE_URL, [CONTENT,])


def test_content_make_links_absolute():

    content = Content(BASE_URL, '<a href="link">Test link</a>')
    content.make_links_absolute()
    assert content.extract() == u'<a href="%s/link">Test link</a>' % BASE_URL


def test_content_select_xpath():

    content = Content(BASE_URL, CONTENT)
    assert content.select('//title/text()', method='xpath').extract() == ['Test content title']
    assert content.select('//a/@href', method='xpath').extract() == ['link1', 'link2', 'link3', 'link4', 'link5', 'link6']
    assert content.select('//p/a/@href', method='xpath').extract() == ['link4', 'link5', 'link6']
    assert content.select('//p/a', method='xpath').extract() == ['<a href="link4">Link4</a>', '<a href="link5">Link5</a>', '<a href="link6">Link6</a>']


def test_content_select_css():

    content = Content(BASE_URL, CONTENT)
    assert content.select('title', method='css').extract() == ['<title>Test content title</title>']
    assert content.select('html title', method='css').extract() == ['<title>Test content title</title>']

def test_content_remove_xpath():

    content = Content(BASE_URL, CONTENT)
    content = content.remove('head', method='xpath')
    assert isinstance(content, Content)

    content = content.remove('p', method='xpath')
    content = content.remove('body', method='xpath')
    assert content.extract().replace('\n', '') == u'<html></html>'


def test_content_remove_css():

    content = Content(BASE_URL, CONTENT)
    content = content.remove('head', method='css')
    assert isinstance(content, Content)

    content = content.remove('p', method='css')
    content = content.remove('body', method='css')
    assert content.extract().replace('\n', '') == u'<html></html>'


def test_content_transform():

    content = Content(BASE_URL, CONTENT)
    assert content.transform(PROFILE).extract().replace('\n', '') == '<div><p>Test content header</p></div>'

def test_content_fields():

    content = Content(BASE_URL, CONTENT)
    assert content.fields(PROFILE) == {
        'title': ['Test content title'],
        'header': ['Test content header'],
    }


def test_content_empty_profile():

    content = Content(BASE_URL, CONTENT)

    with pytest.raises(RuntimeError) as err:
        content.transform("").extract() == ''

    with pytest.raises(RuntimeError) as err:
        content.transform(EMPTY_PROFILE).extract() == ''

    with pytest.raises(RuntimeError) as err:
        content.fields(EMPTY_PROFILE) == {}
