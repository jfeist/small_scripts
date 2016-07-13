#!/usr/bin/env python
# coding: utf-8

import bibtexparser
import re
import sys

# get citations in tex files
citlines = []
for fi in sys.argv[1:]:
    with open(fi+'.aux','r') as f:
        citlines.extend([x.replace(r'\citation{','').replace('}\n','') for x in f if (r'\citation' in x)])
cites = set(re.split('[, ]+',", ".join(citlines)))

def mycustom(record):
    if 'title' in record:
        record['title'] = '{'+record['title']+'}'
    return record
parser = bibtexparser.bparser.BibTexParser()
parser.customization = mycustom
bib_database = bibtexparser.load(open('/Users/feist/Documents/work/tex/mendeley/library_clean.bib','r'), parser=parser)

# only take references used in paper, and ignore missing ones (bibtex will tell me about those)
bib_database.entries = [bib_database.entries_dict[key] for key in cites if key in bib_database.entries_dict]
# so that entries_dict will be regenerated
bib_database._entries_dict = {}

# write back to file
bibtexparser.dump(bib_database,open('references.bib','w'))
