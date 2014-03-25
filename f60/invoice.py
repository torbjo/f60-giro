# TODO
# better to override BaseDocTemplate into InvoiceDocTemplate?
# Or use F60GiroDocTemplate to get static background?
# make SimpleDocTemplate changeable so can use F60GiroDocTemplate
# Use font with better unicode support

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

styles = getSampleStyleSheet()



def render (filename, biller, invoice):
    ''' Helper for one-shot mode '''
    Invoice (biller).render (filename, invoice)



# @todo better name. PDFInvoice?
class Invoice (object):

    # DPI to render images at
    dpi = 200

    def __init__ (self, biller):
        self.biller = biller


    def render (self, filename, invoice):
        self.doc = doc = SimpleDocTemplate (filename, pagesize=A4)
        doc.creator = 'https://github.com/torbjo/f60-giro'
        doc.author = self.biller['name']    # @todo add email if set
        doc.title = 'Faktura ' + invoice['invoice_no']
        #doc.subject = 'what to put here?'
        story = [
            self.make_header (invoice),
            Spacer (0, 12*mm),
            self.make_invoice_lines (invoice),
        ]
        # @todo filter out None so make_* can drop objects
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

    # Note: All make-methods returns one or more flowables.

    def make_image (self, filename):
        img = Image (filename)
        img.drawWidth  = img.imageWidth  * inch/self.dpi
        img.drawHeight = img.imageHeight * inch/self.dpi
        return img


    # @todo drop antall? only: Beskrivelse and Pris?
    def make_invoice_lines (self, invoice):
        data = [('Beskrivelse', 'Antall', 'Pris', 'Sum')]
        lines = invoice['lines']
        if len(lines[0]) == 3:
            lines = [l+(l[1]*l[2],) for l in lines] # add sum column
        #data.extend (lines)
        for l in lines:
            data.append ((l[0], l[1], '%d,-'%l[2], '%d,-'%l[3]))
        #data.append (('', '', 'Total', '%d,-' % sum([l.sum for l in self.invoice_lines])))
        #data.append (('Sum mva-pliktig: 0,- | Sum mva-fritt: %.0f,-'%total, '', 'Total', '%d,-'%total))
        total = invoice.get('total')
        total = total if total else '%d,-'%sum ([l[-1] for l in lines])
        data.extend ((
            ('', '', 'Sum mva-pliktig', '0,-'),
            ('', '', 'Sum mva-fritt',   total),
            ('', '', 'Total',           total),
        ))
        colw = 2*cm     # @todo do not hardcode
        width = self.doc.width - 3*colw - 12*mm   # last is extra padding
        #return Table (data, (width,)+(colw,)*3, style=TableStyle ([
        #return Table (data, (width, colw, colw, colw), style=TableStyle ([
        return Table (data, (width+12*mm, colw, colw, colw), style=TableStyle ([
            ('FONT',  ( 0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONT',  (-2,-1), (-1,-1), 'Helvetica-Bold'),
            ('ALIGN', ( 1, 0), (-1,-1), 'RIGHT'),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, black),
            ('LINEABOVE', (0,-3), (-1,-3), 0.5, black),
            ('LINEABOVE', (1,-1), (-1,-1), 0.5, black),
            ('LINEBELOW', (1,-1), (-1,-1), 0.5, black, 0, None, None, 2, 2),
            #('LINEABOVE', (0,-1), (-1,-1), 0.5, black),
            #('LINEBELOW', (0,-1), (-1,-1), 0.5, black, 0, None, None, 2, 2),
        ]))


    # @todo pull out stuff that don't change per page (biller)
    # @todo use self.data instead of passing invoice around?
    def make_header (self, invoice):
        # Biller
        labels = (
            #('address',     'Addresse'),
            ('phone',       'Telefon'),
            ('email',       'E-post'),
            ('org_no',      'Foretaksregisteret'),
        )
        #data = []
        biller = self.biller
        data = [('Addresse', biller['name'] + '\n' + biller['address'])]
        for key,label in labels:
            if biller.get(key): data.append ((label, biller.get(key)))
            #value = getattr (self.biller, key)
            #value = self.biller.get(key)
            #if value: data.append ((label, value))

        _biller = Table (data, style=TableStyle ([
            ('ALIGN',  (0,0), (0,-1), 'RIGHT'),
            ('VALIGN', (0,0), (0, 0), 'TOP'),
            ('TOPPADDING', (0,0), (-1, -1), 0),
            #('BOTTOMPADDING', (0,0), (-1, -1), 0),
        ]))

        # "Fakturainfo"
        data = (
            ('FAKTURA',         invoice['invoice_no']),
            ('Fakturadato',     invoice['date']),
            ('Forfallsdato',    invoice['due']),
        )
        _payinfo = Table (data, style=TableStyle ([
            ('ALIGN',    (0,0), (-1,-1), 'RIGHT'),
            ('FONTSIZE', (0,1), (-1,-1), 12),
            ('FONT',     (0,0), (-1, 0), 'Helvetica-Bold', 14),
            #('BOTTOMPADDING', (0,0), (-1, 0), 6),
        ]))

        # Payer
        payer = invoice['payer']
        sty = styles['BodyText']
        sty.fontSize = 13
        sty.leading = 13 * 1.33
        _payer = XPreformatted ('<b>%s</b>\n%s' % (payer['name'], payer['address']), sty)

        ## Layout. Pack into a 2x1 table
        #col1 = (self.make_image('logo.png'), Spacer (0, 12*mm), _payer)
        logo = self.biller.get('logo')
        if logo:
            col1 = (self.make_image(logo), Spacer (0, 12*mm), _payer)
        else:
            col1 = (Spacer (0, 6*mm), _payer)
        col2 = (_biller, Spacer (0, 5*mm), _payinfo)
        w = self.doc.width
        return Table ([(col1, col2)], colWidths=(0.6*w, 0.4*w), style=TableStyle ([
            ('VALIGN', (0,0), (0, 0), 'TOP'),
            ('ALIGN',  (1,0), (1,-1), 'RIGHT'),
#            ('GRID', (0,0), (-1,-1), 0.25, black),
        ]))
