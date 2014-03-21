#!/usr/bin/python

import os, sys

from PIL import Image

#
#	Por defecto se usa el programa 'xv' para visualizar. 
#	Si no se tiene instalado se puede usar 
#	"Eye of Gnome" (por defecto presente en Ubuntu).
#	Necesario hacer un alias:
#		"sudo ln -s /usr/bin/eog /usr/bin/xv"
#


im = Image.open("pruebaIm.jpg")
im.show()
print (im.format, im.size, im.mode)