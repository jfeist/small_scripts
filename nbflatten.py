#!/usr/bin/env python
from __future__ import print_function
import sys, io
from IPython.nbformat import read
from IPython.utils.text import strip_ansi
from IPython.display import display
import json

from IPython.nbconvert.preprocessors import ClearOutputPreprocessor

fname = sys.argv[1]
with io.open(fname, encoding='utf-8') as f:
    nb = read(f,4)
#cop = ClearOutputPreprocessor(enabled=True)
#nb, _ = cop(nb,{})

banners = {
'initial':  'Non-cell info ---------------',
'heading':  'Heading %d ------------------',
'markdown': 'Markdown cell ---------------',
'code':     'Code cell -------------------',
'raw':      'Raw cell --------------------',
'output':   'Output ----------------------',
}

cells = nb.cells
del nb['cells']
print(banners['initial'])
# show everything but the actual cells as "raw" JSON
# use sort_keys to ensure the same order always
print(json.dumps(nb,indent=1,sort_keys=True))
print()

for cell in cells:
    if cell.cell_type == 'heading':
        print(banners['heading'] % cell.level)
    else:
        print(banners[cell.cell_type])

    source = cell.source

    print(source)
    if not source.endswith('\n'):
        print()

    if cell.cell_type == 'code':
        if cell.outputs:
            print(banners['output'])
            for output in cell.outputs:
                if 'text' in output:
                    print(strip_ansi(output.text))
                elif 'traceback' in output:
                    print(strip_ansi('\n'.join(output.traceback)))
                else:
                    print("(Non-plaintext output)")
            print()
