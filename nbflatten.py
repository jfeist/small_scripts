#!/usr/bin/env python3
from __future__ import print_function
import sys, io
from nbformat import read
from IPython.utils.text import strip_ansi
from IPython.display import display
import json

from nbconvert.preprocessors import ClearOutputPreprocessor

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

try:
    from pygments import lexers, formatters, highlight
    lexer = lexers.get_lexer_by_name(nb.metadata.language_info.name)
    formatter = formatters.Terminal256Formatter(style='friendly')
    my_highlight = lambda x: highlight(x,lexer,formatter)
except Exception as e:
    print("Error while getting highlighter for notebook: %s:"%type(e).__name__,
          *e.args,"\n",file=sys.stderr)
    lexer, formatter = None, None
    my_highlight = lambda x: x

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
    if cell.cell_type == 'code':
        source = my_highlight(source)

    print(source)
    if not source.endswith('\n'):
        print()

    if cell.cell_type == 'code':
        if cell.outputs:
            print(banners['output'])
            for output in cell.outputs:
                if 'text' in output:
                    print(output.text)
                elif 'traceback' in output:
                    print('\n'.join(output.traceback))
                elif 'data' in output and "text/plain" in output.data:
                    print(output.data['text/plain'])
                else:
                    print('(Non-plaintext output)')
            print()
