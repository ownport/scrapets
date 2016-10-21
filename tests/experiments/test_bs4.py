
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

ARTICLE = '''
<article class="post" id="post-001">
    <div class="thumbnail">
        <a href="http://links.com/1/" rel="bookmark">
            <img alt="thumbnail1.jpeg" class="thumbnail-image" height="100" src="http://images.com/123.jpeg" width="100"/>
        </a>
    </div>
    <div class="entry">
        <header class="entry-header">
            <h2 class="entry-title">
                <a href="http://entries.com/entry1" rel="bookmark">Entry</a>
            </h2>
            <div class="entry-meta">
                <span class="author vcard">
                    <h5 class="entry-author">By:
                        <a href="http://authors.com/author/John/" rel="tag">John</a>
                    </h5>
                </span>
            </div>
        </header>
        <div class="entry-summary">
            <p>Summary</p>
        </div>
    </div>
</article>
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
