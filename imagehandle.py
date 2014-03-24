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
im2 = Image.new(im.mode,(800,575),"red")
print im.mode, im.size, im2.mode, im2.size

x, y = im.size
im2.paste(im,(0,0))

im2.show()

print "Done"