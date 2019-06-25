#!python

import sys
from urllib.parse import unquote

f = ''
with open(sys.argv[1], 'r') as fd:
    f = unquote(fd.read())

with open(sys.argv[1], 'w') as fd:
    fd.write(f)
