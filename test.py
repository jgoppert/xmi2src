#!/usr/bin/python

from lxml import etree
from StringIO import StringIO

schema = etree.XMLSchema(etree.XML(open('classes.xsd').read()))
parser = etree.XMLParser(dtd_validation=False, schema=schema)
root = etree.fromstring(open('test.xml').read(),parser)
