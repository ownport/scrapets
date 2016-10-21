
import xml.etree.ElementTree as ET

from packages.bs4 import BeautifulSoup as BS4
from packages.bs4.builder._htmlparser import HTMLParserTreeBuilder


class BaseParser(object):

    def __init__(self, content):

        if not content:
            raise RuntimeError('The content cannot be Null')

        if not isinstance(content, (str, unicode)):
            raise RuntimeError('The contant shall be string or unicode')

        self._content = content


    def __str__(self):
        return self._content



class XPathParser(BaseParser):

    def select(self, criteria):
        ''' select content by xpath criteria
        '''
        root = ET.fromstring(self._content)
        return [ET.tostring(e, encoding="utf-8", method="html").strip() for e in root.findall(criteria)]


    def remove(self, criteria):
        ''' remove content by xpath criteria
        '''
        root = ET.fromstring(self._content)
        founded_elements = [e for e in root.findall(criteria)]
        for r_elem in root.iter():
            res = [r_elem.remove(fe) for fe in founded_elements if fe in list(r_elem)]
        self._content = ET.tostring(root, encoding="utf-8", method="html")
        return self


class CCSSelectParser(BaseParser):

    def __init__(self, content):

        super(CCSSelectParser, self).__init__(content)
        self._soup = BS4(self._content, builder=HTMLParserTreeBuilder())


    def __str__(self):

        return str(self._soup)


    def __unicode__(self):

        return unicode(self._soup)


    def select(self, criteria, func=None, html=True):
        ''' select content by criteria
        '''
        print criteria, html, func
        if html and not func:
            return [unicode(res) for res in self._soup.select(criteria)]

        if not html and not func:
            return [res for res in self._soup.select(criteria)]

        if func:
            return [func(res) for res in self._soup.select(criteria)]


    def remove(self, criteria):
        ''' remove content by criteria
        '''
        for res in self._soup.select(criteria):
            res.decompose()
        return self
