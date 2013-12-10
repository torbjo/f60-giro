import sys
from f60 import invoice
#import f60faktura

print invoice.VERSION

o = invoice.Faktura (sys.argv[1])
o.render()
