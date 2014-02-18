# -*- encoding: utf-8 -*-

'''
Render the static/fixed background of a F60-1 GIRO.

Use this when printing on a blank sheet of paper. Do *not* use when
printing on a preprinted "GIRO F60-1".

These are the individual parts, listed from top to bottom:

  Part1: «Kvittering»       (yellow)
  Part2: The main part      (white)
  Part3: Yellow row         (yellow; no surprise there)
  Part4: KID, Kroner, ...   (white)


MISSING:
- Yellow line in "Underskrift ved girering"
- Two of the frame corners should have wider stroke.
- Yello corner after "Blankettnummer"

@todo only export render()
@todo make fonts configurable? (at least don't hardcode!)

  font1: fixed fields (Helvetica-Bold 8)
         "Kvitering"    12
         "GIRO"         14
  font2: Helvetica      10      "<  >" around amount controll digit
'''

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm, inch
from reportlab.lib.colors import white, black, yellow

page_width  = A4[0]
#page_height = A4[1]


## Public API

def render (canvas):
    ''' Render the static/fixed background of a F60-1 GIRO '''
    canvas.saveState()
    _render_part1 (canvas)
    _render_part2 (canvas)
    _render_part3 (canvas)
    _render_part4 (canvas)
    canvas.restoreState()



## Internal API

## Helper functions
# All cordinates are in millimeters (mm).
# Origin is the lower-left corner.
# @todo c -> page (ctx?)
# @todo move to utility.py / helpers.py ?
#from utils import box, ribbon, text, frame

def box (c, x, y, width, height):
    ''' Render box at (x,y) with size (width, height) '''
    c.rect (x*mm, y*mm, width*mm, height*mm, stroke=False, fill=True)


def ribbon (c, y, height):
    ''' Render a box with same width as the page '''
    # @todo can get page-width from c?
    box (c, 0, y, page_width, height)


def text (c, x, y, string):
    ''' Render lines of text '''
    assert (string[-1] != os.linesep)
    if not string.count (os.linesep):
        c.drawString (x*mm, y*mm, string)
    else:   # multi-line text
        txt = c.beginText (x*mm, y*mm)
        txt.textLines (string)
        c.drawText (txt)


# @todo better to draw these as path? q: can change line width?
def frame (c, x, y, width, height):
    ''' Render the four 2x2mm corners around a rectangle '''
    w, h = (width, height)
    #wm, hm = (width*mm, height*mm) ?
    c.saveState()
    c.translate (x*mm, y*mm)
    c.lines ([(w*mm,h*mm , (w-2)*mm,h*mm), (w*mm,h*mm , w*mm, (h-2)*mm)])
    c.lines ([
        (0,0 , 2*mm,0), (0,0 , 0, 2*mm),
        (0,h*mm , 2*mm,h*mm), (0,h*mm , 0,(h-2)*mm),
        (w*mm,0 , (w-2)*mm,0), (w*mm,0 , w*mm,2*mm),
    ])
    c.restoreState()




# Part1: Kvittering.
def _render_part1 (c):
    c.setFillColor (yellow)
    ribbon (c, 101.5, 21)
    ribbon (c,  34,    8.5)
    ribbon (c,  15,    2)     # 14+2/3 ?

    # "Punch whole" in the yellow ribbon by painting white boxes
    # on top. @todo make them transparent?
    c.setFillColor (white)
    box (c,  80, 103, 36, 9)    # Beløp
    box (c, 126, 103, 40, 9)    # Betalerens kontonummer
    box (c, 170, 103, 31, 9)    # Blankettnummer

    # Add text
    c.setFillColor (black)
    c.setFont ('Helvetica-Bold', 12)
    text (c,  15, 116, 'Kvitering')
    c.setFont ('Helvetica-Bold', 8)
    text (c,  15, 111, 'Innbetalt til konto')
    #c.setFont ('Helvetica-Bold', 8)
    text (c,  80+2, 103+9+2, 'Beløp')
    text (c, 127+2, 103+9+2, 'Betalerens kontonummer')
    text (c, 170+2, 103+9+2, 'Blankettnummer')



# Part2: The main part  (white)
# @todo two of the frame corners shall have wider stroke width
def _render_part2 (c):
    c.setFont ('Helvetica-Bold', 14)
    text (c, 111, 95, 'GIRO')
    c.setFont ('Helvetica-Bold', 8)
    text (c,  15, 97, 'Betalingsinformasjon')
    text (c,  15, 66, 'Betalt av')
    text (c, 114, 89, 'Underskrift ved girering') # @todo small yellow line
    text (c, 114, 66, 'Betalt til')
#        text (c, 152, 96.3,   'Betalings-')   # @todo use multi line text?
#        text (c, 152, 93, 'frist')
    text (c, 150, 95+1.5, 'Betalings-\nfrist')

    c.setStrokeColor (black)
    #c.setLineWidth (0.33)
    # "Betalt av" & "Betalt til" frames are 86mm x 22mm
    # "Underskrift ved girering" fram are 86mm x 19mm
    # box1: y => [44, 66]
    #       x => [12, 86.3]
    frame (c,  12,44 , 86,22)       # Betalt av
    frame (c, 111,44 , 86,22)       # Betalt til
    frame (c, 111,70.5 , 86,18)     # Underskrift ved girering
    frame (c, 166.33,93 , 30.5,6)   # Betalingsfrist



# Part3: Yellow row
# Note: reportlab does not provide a way to measure the size
# of multiline text boxes. So no way to vertically center; therefor
# must hardcode text values. Bug if font changes
def _render_part3 (c):
    c.setFillColor (black)
    c.setFont ('Helvetica', 8)
    text (c,  31  , 36.5+2, 'Belast\nkonto')        # +2 = manuall vcenter
    text (c, 178.5, 36.5+2, 'Kvittering\ntilbake')

    # Eleven white boxes: pos=(42mm,36mm), size=(5mm,6mm), hspace=1mm
    c.setFillColor (white)
    for n in range(11):
        box (c, 42 + n*6, 35 , 5,6)
    box (c, 192, 35 , 5,6)  # last white checkbox (Kvittering tilbake)



# Part4: Bottom: KID, Kroner, Øre, Til konto, Blankettnummer
def _render_part4 (c):
    # vertical lines: two black and one yellow
    c.setLineWidth (0.3333*mm)
    c.setStrokeColor (black)
    c.lines ([(8*mm, 17*mm, 8*mm, 32*mm), (79*mm, 17*mm, 79*mm, 32*mm)])
    c.setStrokeColor (yellow)
    c.line (104.5*mm, 17*mm , 104.5*mm, 32*mm)

    c.setFont ('Helvetica-Bold', 8)
    c.setFillColor (black)
    c.setStrokeColor (black)
    text (c,   9.33, 30, 'Kundeindentifikasjon (KID)')
    text (c,  80.33, 30, 'Kroner')
    text (c, 106   , 30, 'Øre')
    text (c, 131   , 30, 'Til konto')
    text (c, 172   , 30, 'Blankettnummer')
    # @todo yellow corner bottom-right of «blankettnummer»

    # fixed text
    c.setFont ('Helvetica', 10)
    y = 5.0/6.0 * inch / mm
    #y = 21.166*mm   # acount line
    text (c,   1, y, "H")       # @todo x-height to low.
    text (c, 113, y, "<")
    text (c, 123, y, ">")

    # trademark :)
    c.setFont ('Helvetica-Bold', 6)
    c.saveState()
    c.translate (2.3*mm, 44*mm)
    c.rotate (90)
    text (c, 0,0, 'GIRO F60-1  Got weed?')
    c.restoreState()
