# encoding: utf8

import sys
import datetime

# Note: All fields must either be strings or convertible to strings.

biller = dict (
    # Required
    name =      'NORMAL',
    address =   'Hjelmsgate 3\n0355 Oslo',
    # Optional
    phone =     '(+47) 99 32 59 61',
    email =     'post@normal.no',
    org_no =    'NO 982 770 122',
    logo =      'logo.png',
)

invoice = dict (
    invoice_no = '12345678',
    date =      datetime.date.today(),
    due =       datetime.date.today() + datetime.timedelta(days=20),

    payer = dict (
        name =      'Ima Sucker',
        address =   'Drammensveien 1\n0010 Oslo',
    ),

    # Note: The sum-column and total price is automatically
    # calculated unless specified.
    # Important: price calculations are truncated to integers!
    lines = (
        # Text                      Quantity         Price      [Sum]
        ('Insult-consulting',           22.5,         750),
        ('Misc hardware',                  1,       22500),
        # @todo wrap long lines
        #(u'Removed some «kuk» from the computer. How is long lines handled? Is this long enough?', 1, 145000),
        # @todo?
        #('Insult-consulting, 22.5t',                           16875),
        # add unit? other examples than t/timer and stk.
    ),
    # @todo howto handle split on ',' in giro-part?
    #total = u'150 000,-'    # calculated from lines.quantity * lines.price
    # @todo extra text
)


# Optional
# @todo move account to biller?
giro = dict (
    account =       '0535 38 57497',
#    kid =           '246810121416',
    # The rest of these fileds are auto-populated from 'invoice'
#    amount =        ('12000', '00'),
#    info =          'Fakturanummer 1359',
#    due =           '2014-12-31',
#    payer =         'Ima Sucker\nDrammensveien 1\n0001 Oslo',
#    payee =         'NORMAL',

    # Use pre-printed giro, or use blank paper (add the giro background).
    add_static_background = True,
)
invoice['giro'] = giro



#import f60
#f60.invoice.render (sys.argv[1], biller, invoice)
from f60.invoice import render as render_invoice


## Example 1) Render to file passing filename:
render_invoice (sys.argv[1], biller, invoice)
exit(0)


## Example 2) Render to StringIO buffer (or other file-like object):
#fp = open (sys.argv[1], 'wb')
from cStringIO import StringIO
fp = StringIO()
render_invoice (fp, biller, invoice)
data = fp.getvalue()
# or stream the data back from StringIO buffer:
#size = fp.tell()
#fp.seek(0)
#while True:
#    buf = fp.read(8192)
#    if not buf: break
#    print len(buf)
#fp.close()



# @todo support
#from f60.invoice import Invoice
#inv = Invoice (biller)
#inv.render ('page1.pdf', invoice)
#inv.render ('page2.pdf', invoice)


# @todo multi-page document
#obj = Invoice ('out.pdf')
#obj.add_page (biller, invoice1)
#obj.add_page (biller, invoice2)
#obj.close()    # does the rendering
