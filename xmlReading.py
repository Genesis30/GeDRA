#!/usr/bin/env python

import xml.etree.ElementTree as et

tree = et.parse('model.xml')
root = tree.getroot()

for part in root:
	print part.tag
	print '-------'
	for element in part:
		print element.tag, element.attrib
		for charac in element:
			print charac.tag
		print '**** \n'

print et.tostring(root, encoding="us-ascii", method="xml")