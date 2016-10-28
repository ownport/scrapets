# -*- coding: utf-8 -*-

from lxml import html

from packages import yaml

from packages import parsel


def join_by(sep, lst):
    return sep.join(lst)

def strip(v):
    return v.strip()

def foreach(lst, func):
    return map(lambda x: func(x), lst)


class Content(object):

    def __init__(self, url, content):

        if not url:
            raise RuntimeError('The url cannot be null')

        if not isinstance(url, (str, unicode)):
            raise RuntimeError('The url shall be string or unicode')

        self._url = url

        if not content:
            raise RuntimeError('The content cannot be Null')

        if not isinstance(content, (str, unicode)):
            raise RuntimeError('The content shall be string or unicode')

        if not isinstance(content, unicode):
            content = unicode(content)

        self._content = content


    def extract(self):

        return self._content


    def make_links_absolute(self):
        ''' make links absolute in the content
        '''
        _content = html.fromstring(self._content)
        _content.make_links_absolute(self._url)
        self._content = html.tostring(_content)
        return self._content


    def select(self, expr, method='xpath'):
        ''' select content by xpath

        method can be xpath or css
        '''
        selector = parsel.Selector(self._content)

        result = None
        if method == 'xpath':
            result = selector.xpath(expr)

        if method == 'css':
            result = selector.css(expr)

        return result


    def remove(self, expr, method='xpath'):
        ''' remove content by xpath expression
        '''
        _content = html.fromstring(self._content)

        if method == 'xpath':
            selected = _content.xpath(expr)

        if method == 'css':
            selected = _content.cssselect(expr)

        if not selected:
            return self

        for tag in selected:
            tag.getparent().remove(tag)

        return Content(self._url, html.tostring(_content))


    def _load_profile(self, profile):
        ''' load profile from yaml file
        '''
        _profile = yaml.load(profile)
        if not _profile:
            raise RuntimeError('Empty profile')
        return _profile


    def transform(self, profile):
        ''' transform content according to rules in the profile
        '''
        _profile = self._load_profile(profile)
        if not 'rules' in _profile:
            return self

        _content = Content(self._url, self.extract())
        for rule in _profile['rules']:
            if 'select' in rule:
                selections = _content.select(rule['select']['expr'], method=rule['select']['method'])
                _content = Content(self._url, '\n'.join(map(lambda s: s.extract(), selections)))
                continue
            if 'remove' in rule:
                _content = _content.remove(rule['remove']['expr'], method=rule['remove']['method'])
                continue

        return _content


    def fields(self, profile):
        ''' select fields from the content according to rules in the profile
        '''
        _profile = self._load_profile(profile)
        if not 'fields' in _profile:
            return self

        from packages.parsel.utils import flatten, iflatten

        fields = dict()
        for field in _profile['fields']:
            if field.get('name') and field.get('xpath'):
                fields[field['name']] = self.select(field['xpath'], method='xpath').extract()
                if field.get('method'):
                    try:
                        _ = self.select(field['xpath'], method='xpath')
                        fields[field['name']] = eval(field['method'])
                    except AttributeError:
                        pass

        return fields


    def process(self, profile):

        _content = self.transform(profile)
        return _content.fields(profile)
