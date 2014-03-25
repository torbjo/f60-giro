# encoding: utf8

import sys
import datetime
from f60.invoice import Invoice
#from f60 import invoice    # then can not use invoice as local variable

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
    #total = u'150 000,-'    # calculated from lines.quantity * lines.price
    # @todo extra text
)


inv = Invoice (biller)
inv.render (sys.argv[1], invoice)
