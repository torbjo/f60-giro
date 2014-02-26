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
from fields import render as render_fields

VERSION = '0.1alpha'

# @todo do not make global?
#width, height = A4
#page_width = A4[0]

# low-level render interface
from fields import _render as _render_fields

# Data to render the names of all fields
data = dict (
    account =   'account',
    amount =    ('amount[0]', 'amount[1]'),
    info =      'info',
    due =       'due',
    payer =     'payer',
    payee =     'payee',
    kid =       'kid',
)

# Data to render the ids of all fields
_data = dict([(x,x) for x in '1a','1b','2a','2b','2c','2d','4a','4b','4c','4d','4e'])



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
        #render_fields (c)
        #render_fields (c, **data)
        _render_fields (c, _data)
        c.showPage()
        c.save()
