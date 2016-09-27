
import xml.etree.ElementTree as ET


class Content(object):

    def __init__(self, content):

        if not content:
            raise RuntimeError('The content cannot be Null')

        if not isinstance(content, (str, unicode)):
            raise RuntimeError('The contant shall be string or unicode')

        self._content = content

    def __str__(self):
        return self._content


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
