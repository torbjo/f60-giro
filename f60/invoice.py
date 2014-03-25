# TODO
# better to override BaseDocTemplate into InvoiceDocTemplate?

#from reportlab import platypus
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import Preformatted, XPreformatted, Image
#from reportlab.platypus import Frame, FrameBreak
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, cm, inch
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import A4
#from reportlab.lib.colors import white, black, yellow, blue

from static import render as render_static_background
from fields import render as render_fields

# tmp stuff while developing
import initnormalno
from apps.invoice import models

styles = getSampleStyleSheet()


class Invoice (object):

    # DPI to render images at
    dpi = 200

    def __init__ (self, filename):
        self.get_data()
        self.doc = SimpleDocTemplate (filename, pagesize=A4)
        #self.doc = SimpleDocTemplate (filename, showBoundary=1)
        doc = self.doc
        doc.showBoundary = True
        doc.creator = 'https://github.com/torbjo/f60-giro'
        #doc.author = self.invoice.account.name
        #doc.title = 'Faktura ' + self.invoice.invoice_no()
        doc.subject = 'what to put here?'


    # tmp stuff while developing
    def get_data (self):
        self.invoice = models.Invoice.objects.get (pk=1)
        assert self.invoice.account
        # fixup data
        acc = self.invoice.account
        acc.address = acc.name + '\n' + acc.address.replace('\r', '')
        payer = self.invoice.client
        payer.address = payer.address.replace('\r', '')
        # Invoice lines:
        # Note amount is Decimal while quantity is float. so have missmatch
        # Workaround is to cast to float and throw away decimal part.
        # Correct way: Fraction(o.amount) * Fraction(o.quantity)
        # or change o.quantity to Decimal datatype in Django
        self.invoice_lines = self.invoice.invoiceline_set.all()
        for l in self.invoice_lines:
            l.sum = int('%.0f' % (float(l.amount) * l.quantity))


    def render (self):
        story = [
            self.get_header(),
            Spacer (0, 12*mm),
            self.get_invoice_lines(),
        ]
        self.doc.build (story, onFirstPage=self.on_first_page, onLaterPages=self.on_later_pages)
        #self.doc.build (story, onFirstPage=self.on_new_page, onLaterPages=self.on_new_page)
        #c = self.doc.canv
        #render_static_background (c)
        #c.save()


    def on_first_page (self, canv, doc):
        pass
        #render_static_background (canv)
        #render_fields (c, **data)

    def on_later_pages (self, canv, doc):
        raise Exception ('No support for multi-page!')



    ### Private API ###

    def get_image (self, filename):
        img = Image (filename)
        img.drawWidth  = img.imageWidth  * inch/self.dpi
        img.drawHeight = img.imageHeight * inch/self.dpi
        return img


    # @todo drop antall? only: Beskrivelse and Pris?
    def get_invoice_lines (self):
        data = [('Beskrivelse', 'Antall', 'Pris', 'Sum')]
        #data.append ([(l.text, l.quantity, str(l.amount)+',-') for l in lines]
        for l in self.invoice_lines:
            data.append ((l.text, l.quantity, '%d,-'%l.amount, '%d,-'%l.sum))
        #data.append (('', '', 'Total', '%d,-' % sum([l.sum for l in self.invoice_lines])))
        #data.append (('Sum mva-pliktig: 0,- | Sum mva-fritt: %.0f,-'%total, '', 'Total', '%d,-'%total))
        total = sum ([l.sum for l in self.invoice_lines])
        data.extend ((
            ('', '', 'Sum mva-pliktig', '0,-'),
            ('', '', 'Sum mva-fritt',   '%d,-'%total),
            ('', '', 'Total',           '%d,-'%total),
        ))
        colw = 2*cm
        width = self.doc.width - 3*colw - 12*mm   # last is extra padding
        #return Table (data, (width,)+(colw,)*3, style=TableStyle ([
        return Table (data, (width, colw, colw, colw), style=TableStyle ([
            ('FONT',  ( 0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONT',  (-2,-1), (-1,-1), 'Helvetica-Bold'),
            ('ALIGN', ( 1, 0), (-1,-1), 'RIGHT'),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, black),
            ('LINEABOVE', (0,-3), (-1,-3), 0.5, black),
            ('LINEABOVE', (0,-1), (-1,-1), 0.5, black),
            ('LINEBELOW', (0,-1), (-1,-1), 0.5, black, 0, None, None, 2, 2),
        ]))


    # @todo pass dynamic data
    def get_header (self):
        # Biller
        labels = (
            ('address',     'Addresse'),
            ('phone',       'Telefon'),
            ('email',       'E-post'),
            ('org_no',      'Foretaksregisteret'),
        )
        data = []
        for key,label in labels:
            value = getattr (self.invoice.account, key)
            if value: data.append ((label, value))

        col2_1 = Table (data, style=TableStyle ([
            ('ALIGN',  (0,0), (0,-1), 'RIGHT'),
            ('VALIGN', (0,0), (0, 0), 'TOP'),
            ('TOPPADDING', (0,0), (-1, -1), 0),
            #('BOTTOMPADDING', (0,0), (-1, -1), 0),
        ]))

        # "Fakturainfo"
        obj = self.invoice
        data = (
            ('FAKTURA',         obj.invoice_no()),
            ('Fakturadato',     obj.date),
            ('Forfallsdato',    obj.due),
        )
        col2_2 = Table (data, style=TableStyle ([
            ('ALIGN',    (0,0), (-1,-1), 'RIGHT'),
            ('FONTSIZE', (0,1), (-1,-1), 12),
            ('FONT',     (0,0), (-1, 0), 'Helvetica-Bold', 14),
            #('BOTTOMPADDING', (0,0), (-1, 0), 6),
        ]))

        # Payer
        payer = self.invoice.client
        sty = styles['BodyText']
        sty.fontSize = 13
        sty.leading = 13 * 1.33
        col1_2 = XPreformatted ('<b>%s</b>\n%s' % (payer.name, payer.address), sty)

        ## Layout
        col1 = [
            self.get_image('logo.png'),
            Spacer (0, 12*mm),
            col1_2,
            #XPreformatted ('<b>%s</b>\n%s' % (payer.name, payer.address), sty)
        ]
        col2 = (col2_1, Spacer (0, 5*mm), col2_2)

        w = self.doc.width
        return Table ([(col1, col2)], colWidths=(0.6*w, 0.4*w), style=TableStyle ([
            ('VALIGN', (0,0), (0, 0), 'TOP'),
            ('ALIGN',  (1,0), (1,-1), 'RIGHT'),
#            ('GRID', (0,0), (-1,-1), 0.25, black),
        ]))
