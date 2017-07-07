#!/usr/bin/env python
# coding: utf-8

import re
import sys
import os
import bibtexparser

for flag in 'etal', 'arxiv':
    locals()[flag] = False
    if '--'+flag in sys.argv:
        locals()[flag] = True
        sys.argv.remove('--'+flag)
        #print(flag,"set to true")
        assert '--'+flag not in sys.argv, 'do not repeat --'+flag

outdir = os.path.dirname(sys.argv[1])

# get citations in tex files
citlines = []
for fi in sys.argv[1:]:
    with open(fi+'.aux','r') as f:
        citlines.extend([x.replace(r'\citation{','').replace('}\n','') for x in f if r'\citation' in x])
cites = set(re.split('[, ]+',", ".join(citlines)))

def mycustom(record):
    if 'title' in record:
        record['title'] = '{'+record['title']+'}'
    if etal and 'author' in record:
        auths = record['author'].split(' and ')
        if len(auths)>5:
            record['author'] = auths[0] + ' and others'
    if arxiv and 'eprint' in record:
        record['journal'] = 'arXiv:'+record['eprint']
    return record
parser = bibtexparser.bparser.BibTexParser()
parser.customization = mycustom
bib_database = bibtexparser.load(open('/Users/feist/Documents/work/tex/mendeley/library_clean.bib','r'), parser=parser)

# only take references used in paper
bib_database.entries = [bib_database.entries_dict[key] for key in cites if key in bib_database.entries_dict]
# so that entries_dict will be regenerated
bib_database._entries_dict = {}

missing_entries = cites - set(bib_database.entries_dict.keys())
missing_entries -=  {'apsrev41Control', 'REVTEX41Control', 'achemso-control'}
if missing_entries:
    print("missing entries in make_latex_references.py:",*(k for k in missing_entries))

# write back to file
with open(os.path.join(outdir,'references.bib'),'w') as f:
    bibtexparser.dump(bib_database,f)
