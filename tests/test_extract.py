
import pytest

from scrapets import extract

PAGE = '''
<html>
<body>
    <a href="alink1">Link1</a>
    <a href="alink1">Link1</a>
    <img src="img_link1">
    <img src="img_link1">
    <a href="alink2">Link2</a>
    <img src="img_link2">
    <a href="alink3">Link3</a>
    <img src="img_link3">
</body>
</html>
'''

PAGE_LINKS = ["alink1", "alink2", "alink3"]
PAGE_IMAGE_LINKS = ["img_link1", "img_link2", "img_link3"]


def test_linkextract_create():

    le = extract.LinkExtractor()
    assert isinstance(le, extract.LinkExtractor)


def test_linkextract_links():

    le = extract.LinkExtractor()
    le.feed(PAGE)
    assert le.links == PAGE_LINKS


def test_linkextract_image_links():

    le = extract.ImageLinkExtractor()
    le.feed(PAGE)
    assert le.links == PAGE_IMAGE_LINKS
