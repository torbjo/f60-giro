# -*- encoding: utf-8 -*-
# @todo ammount: what if str and not tuple?
#       due: accept datetime.data or datetime.datatime also?
# @todo change fonts per field


'''
Render the dynamic parts (the fields) of a F60-1 GIRO.

PARTS:

Part1: Upper yellow row ("Kvittering")
Part2: Main part
Part3: Yellow row
Part4: Number row

FIELDS:

Part number + field (a-z)

1a  account     Innbetalt til konto
1b  amount      Beløp

2a  info        Betalingsinformasjon
2b  due         Betalingsfrist
2c  payer       Betalt av
2d  payee       Betalt til

4a  kid         Kundeidentifikasjon (KID)
4b  amount[0]   Kroner
4c  amount[1]   Øre
4d              <kontrollsiffer>
4e  account     Til konto

Note: amount = (kroner, øre)
Note: 1a & e4: same text but different font
Note: 1b = printf('%d,%.2d', amount[0], amount[1])
      1b = printf('%.2f', amount[0] + amount[1]/100.0) # fix s/./,/
Note: <kontrollsiffer> is auto-calculated

account -> accountno?
info -> payment_info / description?
'''

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm, inch
from reportlab.lib.colors import white, black, yellow


# Position and size of all fields. Uses the postscript/pdf coordinate
# system. All units are in mm. (x,y) is upper right corner of field.
# @todo add width & height
field_layout = {
#   'id': (x,y , width,height)
    '1a': ( 15, 105 , -1, -1),
    '1b': ( 84, 106 , -1, -1),      # right-align (or center)
    '2a': ( 15,  90 , -1, -1),      # bigger font?
    '2b': (167,  95 , -1, -1),      # center
    '2c': ( 17,  59 , -1, -1),
    '2d': (115,  59 , -1, -1),
    '4a': ( 14,  21 , -1, -1),
    '4b': ( 85,  21 , -1, -1),      # ralign
    '4c': (106,  21 , -1, -1),
    '4d': (118,  21 , -1, -1),      # center
    '4e': (131,  21 , -1, -1),
}


# Map from field name to field id.
name_to_field = {
    'account':  '1a',
    'amount':   '1b',       # takes tuple of (4b,4c)
    'info':     '2a',
    'due':      '2b',
    'payer':    '2c',
    'payee':    '2d',
    'kid':      '4a',
}



## Public API

def render (canvas,
            account     = '',
            amount      = ('', ''),
            info        = '',
            due         = '',
            payer       = '',
            payee       = '',
            kid         = ''):
    data = {
        name_to_field['account']: account,
        name_to_field['amount']:  ','.join(amount),
        name_to_field['info']:    info,
        name_to_field['due']:     due,
        name_to_field['payer']:   payer,
        name_to_field['payee']:   payee,
        name_to_field['kid']:     kid,
    }
    data['4b'] = amount[0]
    data['4c'] = amount[1]
    #data['4d'] = ''             # @todo "kontrollsiffer"
    data['4e'] = data['1a']     # account
    _render (canvas, data)



## Internal API

def _render (canvas, data):
    c = canvas
    c.saveState()
    c.setFillColor (black)
    c.setFont ('Helvetica', 11)
    for key,val in data.iteritems():
        x,y,w,h = field_layout[key]
        text (c, x, y, val)
    canvas.restoreState()


def text (c, x, y, string):
    ''' Render multi-line text '''
    txt = c.beginText (x*mm, y*mm)
    txt.textLines (string)
    c.drawText (txt)
