# -*- encoding: utf-8 -*-

'''
TODO
from f60faktura import pdfgen ?
wrap reportlab so can switch to other pdf render (cairo/pango)??
'''

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm, inch
from reportlab.lib.colors import white, black, yellow
#from reportlab.lib.colors import blue

from static import render as render_static_background

VERSION = '0.1alpha'

# @todo do not make global?
#width, height = A4
page_width = A4[0]


class Faktura (object):

    canvas = None
    #page = None

    def __init__ (self, filename):
        self.canvas = canvas.Canvas (filename)
        #self.canvas = canvas.Canvas (filename, render_fixed_bg=True)
        # @todo make page_size explicit (don't depend on default)

    def render (self):
        c = self.canvas
        render_static_background (c)
        c.showPage()
        c.save()
