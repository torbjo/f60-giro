# -*- encoding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm, inch
from reportlab.lib.colors import white, black, yellow
from reportlab.lib.colors import blue

# from f60faktura import pdfgen ?

VERSION = '0.1alpha'

# @todo page_width, page_height?
# do not make global; name conflicts
width, height = A4


## Helper functions
# All cordinates are in centimeters (cm).
# All cordinates are relative to lower-left corner.

def box (c, x, y, width, height):
    ''' Render box at (x,y) with size (width, height) '''
    c.rect (x*mm, y*mm, width*mm, height*mm, stroke=False, fill=True)

def ribbon (c, y, height):
    ''' Render a box with same width as the page '''
    box (c, 0, y, width, height)

def text (c, x, y, string):
    c.drawString (x*mm, y*mm, string)

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
    # @todo better to draw these as path

"""
        c.lines ([(86*mm,22*mm , 84*mm,22*mm), (86*mm,22*mm , 86*mm, 20*mm)])
        c.lines ([
            (0,0 , 2*mm,0), (0,0 , 0, 2*mm),
            (0,22*mm , 2*mm,22*mm), (0,22*mm , 0,20*mm),
            (86*mm,0 , 84*mm,0), (86*mm,0 , 86*mm,2*mm),
        ])
"""


class Faktura (object):

    canvas = None

    def __init__ (self, filename):
        self.canvas = canvas.Canvas (filename)
        #self.canvas = canvas.Canvas (filename, render_fixed_bg=True)

    def render (self):
        self._render_background()
        c = self.canvas
        c.showPage()
        c.save()

    # @todo pull out fixed bg rendering to own class?
    # _render_fixed_bg
    # render the fixed f60 background. use this when printing on blank
    # paper. do *not* use when printing on preprinted "GIRO F60-1"
    def _render_background (self):
        self._render_bg_part1()
        self._render_bg_part2()
        self._render_bg_part3()
        self._render_bg_part4()


    # These are the individual parts, listed from top to bottom:
    # Part1: Kvitering.     (yellow)
    # Part2: The main part  (white)
    # Part3: Yellow line
    # Part4: Bottom line: KID, amount, account number   (white)

    # Part1: Kvitering.
    def _render_bg_part1 (self):
        c = self.canvas

        c.setFillColor (yellow)
        ribbon (c, 101, 21)
        ribbon (c,  33,  9)
        ribbon (c,  14,  2)

        # "Punch whole" in the yellow ribbon by painting white boxes
        # on top. @todo make them transparent?
        c.setFillColor (white)
        box (c,  80, 103, 36, 9)    # Beløp
        box (c, 126, 103, 40, 9)    # Betalerens kontonummer
        box (c, 170, 103, 31, 9)    # Blankettnummer

        # Add text
        c.setFillColor (black)
        c.setFont ('Helvetica-Bold', 13)
        text (c,  15, 116, 'Kvitering')
        c.setFont ('Helvetica', 10)
        text (c,  15, 111, 'Innbetalt til konto')

        #c.setFont ('Helvetica-Bold', 8)
        c.setFont ('Helvetica', 8)
        text (c,  80+2, 103+9+2, 'Beløp')
        text (c, 127+2, 103+9+2, 'Betalerens kontonummer')
        text (c, 170+2, 103+9+2, 'Blankettnummer')


    # Part2: The main part  (white)
    # @todo two of the frame corners shall have wider stroke width
    def _render_bg_part2 (self):
        c = self.canvas
        c.setFont ('Helvetica-Bold', 14)
        text (c, 111, 95, 'GIRO')
        c.setFont ('Helvetica', 8)
        text (c,  15, 97, 'Betalingsinformasjon')
        text (c,  15, 66, 'Betalt av')
        text (c, 114, 89, 'Underskrift ved girering') # @todo small yellow line
        text (c, 114, 66, 'Betalt til')
        text (c, 152, 96.3,   'Betalings-')   # @todo use multi line text?
        text (c, 152, 93, 'frist')

        c.setStrokeColor (black)
        #c.setLineWidth (0.33)
        # "Betalt av" & "Betalt til" frames are 86mm x 22mm
        # "Underskrift ved girering" fram are 86mm x 19mm
        # box1: y => [44, 66]
        #       x => [12, 86.3]
        frame (c,  12,44 , 86,22)       # Betalt av
        frame (c, 111,44 , 86,22)       # Betalt til
        frame (c, 111,70.5 , 86,18)     # Underskrift ved girering
        frame (c, 166.33,93 , 30.5,6)      # Underskrift ved girering


    # Part3: Yellow line
    # Note: reportlab does not provide a way to measure the size
    # of multiline text boxes. So no way to vertically center; therefor
    # must hardcode text values. Bug if font changes
    def _render_bg_part3 (self):
        c = self.canvas
        c.setFont ('Helvetica', 8)
        #txt = c.beginText (31*mm, 36*mm )
        #print txt.getY()

        c.setFillColor (black)
        txt = c.beginText (31*mm, 36*mm + 2*mm )    # hardcoded vcenter
        txt.textLines ('Belast\nkonto')
        c.drawText (txt)
        txt = c.beginText (178.5*mm, 36*mm + 2*mm ) # hardcoded vcenter
        txt.textLines ('Kvitering\ntilbake')
        c.drawText (txt)

        c.setFillColor (white)
        # Eleven white boxes: pos=(42mm,36mm), size=(5mm,6mm), hspace=1mm
        for n in range(11):
            box (c, 42 + n*6, 34.5 , 5,6)
        # Last white checkbox (Kvitering tilbake)
        box (c, 192, 34.5 , 5,6)


    # Part4: Bottom line: KID, amount, account number   (white)
    def _render_bg_part4 (self):
        pass




"""
    ## Helpers

        # Skillelinjer for KID
        c.setStrokeColor (black)
        c.setLineWidth (0.3333*mm)
        c.lines ([(9*mm, 16*mm, 9*mm, 30*mm), (80*mm, 16*mm, 80*mm, 30*mm)])
        # @todo H

        underkant = 5.0/6.0 * inch


## Create background



# Blankettnummer
# needed?
c.setFont ('Courier', 10)
c.drawString (173*mm, 105*mm, '6071840440')
c.drawString (173*mm, underkant, '6071840440')

# Lag klammer for kontrollsiffer til sum
c.setFont ('Helvetica', 10)
c.drawString (115*mm, underkant, "<")
c.drawString (125*mm, underkant, ">")

# Lag tekst som beskriver feltene (nederste rad)
c.setFont("Helvetica-Bold", 6)


#c.line (0, underkant, width, underkant)
"""
