#!/usr/bin/env python3
# coding: utf-8

import re
import sys
import os
import bibtexparser
import pickle
from colorama import Fore, Style

warn_str = Fore.YELLOW + Style.BRIGHT + "WARNING:" + Style.RESET_ALL

for flag in 'etal', 'arxiv':
    locals()[flag] = False
    if '--'+flag in sys.argv:
        locals()[flag] = True
        sys.argv.remove('--'+flag)
        #print(flag,"set to true")
        assert '--'+flag not in sys.argv, 'do not repeat --'+flag

refbib = None
for arg in sys.argv[1:]:
    if arg.startswith('--refbib='):
        sys.argv.remove(arg)
        assert refbib is None, 'do not repeat --refbib'
        refbib = arg.split('=',1)[1]

outdir = os.path.dirname(sys.argv[1])

# get citations in tex files
citlines = []
for fi in sys.argv[1:]:
    with open(fi+'.aux','r') as f:
        citlines.extend([x.replace(r'\citation{','').replace('}\n','') for x in f if r'\citation' in x])
cites = set(re.split('[, ]+',", ".join(citlines)))

def mycustom(record):
    record.pop('abstract',None)
    record.pop('file',None)
    if 'title' in record:
        record['title'] = '{'+record['title']+'}'
    if etal and 'author' in record:
        auths = record['author'].split(' and ')
        if len(auths)>5:
            record['author'] = auths[0] + ' and others'
    if 'eprint' in record:
        if arxiv:
            record['journal'] = 'arXiv:'+record['eprint']
        elif 'journal' not in record and 'booktitle' not in record:
            # for revtex42
            record['ENTRYTYPE'] = 'unpublished'
    if 'keywords' in record:
        keywords = record['keywords'].split(',')
        record['keywords'] = ','.join(sorted(keywords,key=lambda s: s.casefold()))
    return record

# load pickled bibtex database
with open('/Users/feist/Documents/work/tex/bibliography/library_clean.pickle','rb') as f:
    bib_database = pickle.load(f)

# only take references used in paper and apply the transformations we want
db = bib_database.entries_dict
bib_database.entries = [mycustom(db[key]) for key in cites if key in db]
bib_database._entries_dict = {}

if refbib:
    with open(refbib) as f:
        refbibdb = bibtexparser.load(f)
    # this will merge the two bibtex files, with refbibdb having precedence
    for entry in bib_database.entries:
        if entry["ID"] not in refbibdb.entries_dict:
            refbibdb.entries.append(entry)
        else:
            print(warn_str, f"entry already in reference bibliograph {refbib}:", entry["ID"])
    bib_database = refbibdb

missing_entries = cites - set(bib_database.entries_dict.keys())
missing_entries -=  {'apsrev41Control', 'REVTEX41Control', 'apsrev42Control', 'REVTEX42Control', 'achemso-control'}
if missing_entries:
    print(warn_str, "missing entries in make_latex_references.py:", *sorted(missing_entries))

# write to file
with open(os.path.join(outdir,'references.bib'),'w') as f:
    bibtexparser.dump(bib_database,f)
