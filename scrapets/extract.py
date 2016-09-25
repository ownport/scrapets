# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser

# -------------------------------------------------------
#
#   LinkExtractor: extract links from html page
#

class BaseExtractor(HTMLParser):

    def __init__(self):

        HTMLParser.__init__(self)
        self._links = []

    @property
    def links(self):

        return self._links


class LinkExtractor(BaseExtractor):

    def handle_starttag(self, tag, attrs):

        if tag == 'a':
            links = [v for k,v in attrs if k == 'href' and v not in self._links]
            self._links.extend(links)


class ImageLinkExtractor(BaseExtractor):

    def handle_starttag(self, tag, attrs):

        if tag == 'img':
            links = [v for k,v in attrs if k == 'src' and v not in self._links]
            self._links.extend(links)
