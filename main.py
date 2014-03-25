import sys
from f60 import invoice
#import f60faktura

o = invoice.Invoice (sys.argv[1])
o.render()
