
import xml.etree.ElementTree as ET

from packages.bs4 import BeautifulSoup as BS4
from packages.bs4.builder._htmlparser import HTMLParserTreeBuilder

from packages import yaml


def parse_selector(value):

    if not value:
        return None, None

    if value.find('::') >= 0:
        selector, func = value.split('::', 1)
        func = eval(func)
    else:
        selector = value
        func = None

    return selector, func



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


    def select(self, criteria, func=None):
        ''' select content by criteria

        func - if not None, perform func call for all selections
        html - if True, for each selection will be applied unicode()
        merge - if True, return all selections as single BeautifulSoup instance
        '''
        result = [r for r in self._soup.select(criteria)]

        if func:
            result = map(lambda r: func(r), result)

        result = map(lambda r: unicode(r), result)
        self._soup = BS4('\n'.join(result), builder=HTMLParserTreeBuilder())

        return self



    def remove(self, criteria):
        ''' remove content by criteria
        '''
        for res in self._soup.select(criteria):
            res.decompose()
        return self


    def transform(self, rules):
        ''' transform content according to rules
        '''
        _rules = yaml.load(rules)
        if not 'rules' in _rules:
            raise RuntimeError('Rules section is missed in rules file')

        for rule in _rules['rules']:
            if 'select' in rule:
                self.select(*parse_selector(rule['select']['selector']))
                continue
            if 'remove' in rule:
                self.remove(rule['remove']['selector'])
                continue

        return self


    def fields(self, rules):
        ''' extract info from the content and return key/values
        '''
        _rules = yaml.load(rules)
        if not 'fields' in _rules:
            raise RuntimeError('Fields section is missed in rules file')

        _orig_soup = self._soup
        result = dict()
        for rule in _rules['fields']:
            criteria, func = parse_selector(rule['selector'])
            result[rule['name']] = unicode(self.select(criteria, func))
            self._soup = _orig_soup
        return result
