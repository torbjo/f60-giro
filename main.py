import sys
from f60 import invoice
#import f60faktura

print invoice.VERSION

#o = invoice.Invoice (sys.argv[1])
o = invoice.Faktura (sys.argv[1])
o.render()
