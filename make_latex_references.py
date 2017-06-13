#!/usr/bin/env python
# coding: utf-8

import bibtexparser
import re
import sys

etal = False
if '--etal' in sys.argv:
    etal=True
    sys.argv.remove('--etal')
    #print("etal set to true")
    assert '--etal' not in sys.argv, 'do not repeat --etal'

# get citations in tex files
citlines = []
for fi in sys.argv[1:]:
    with open(fi+'.aux','r') as f:
        citlines.extend([x.replace(r'\citation{','').replace('}\n','') for x in f if (r'\citation' in x)])
cites = set(re.split('[, ]+',", ".join(citlines)))

def mycustom(record):
    if 'title' in record:
        record['title'] = '{'+record['title']+'}'
    if etal and 'author' in record:
        auths = record['author'].split(' and ')
        if len(auths)>5:
            record['author'] = auths[0] + ' and others'
    return record
parser = bibtexparser.bparser.BibTexParser()
parser.customization = mycustom
bib_database = bibtexparser.load(open('/Users/feist/Documents/work/tex/mendeley/library_clean.bib','r'), parser=parser)

# only take references used in paper
bib_database.entries = [bib_database.entries_dict[key] for key in cites if key in bib_database.entries_dict]
# so that entries_dict will be regenerated
bib_database._entries_dict = {}

missing_entries = cites - set(bib_database.entries_dict.keys())
missing_entries -=  {'apsrev41Control', 'REVTEX41Control'}
if missing_entries:
    print("missing entries in make_latex_references.py:",*(k for k in missing_entries))

# write back to file
bibtexparser.dump(bib_database,open('references.bib','w'))
