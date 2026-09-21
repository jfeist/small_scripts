#!/usr/bin/env python3
# coding: utf-8

import re
import sys
import os
import bibtexparser
from bibtexparser.model import DuplicateBlockKeyBlock, ParsingFailedBlock
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

# the bibtexparser v2 Entry mimics a dict (including the pseudo-keys ENTRYTYPE and
# ID), so this works on v2 entries just as it did on the v1 dicts
def mycustom(record):
    record.pop('abstract',None)
    record.pop('file',None)
    record.pop('annotation',None)
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

# load pickled bibtex database (a bibtexparser v2 Library, written by clean_library.py)
with open('/Users/feist/Documents/work/tex/bibliography/library_clean.pickle','rb') as f:
    bib_database = pickle.load(f)

# only take references used in paper and apply the transformations we want.
# Library.entries is a read-only property in v2, so build a new library instead of
# assigning to it (which also makes the v1 `_entries_dict` cache reset obsolete)
db = bib_database.entries_dict
bib_database = bibtexparser.Library([mycustom(db[key]) for key in sorted(cites) if key in db])

if refbib:
    refbibdb = bibtexparser.parse_file(refbib)
    # entries whose key was seen before are not added to "entries" but wrapped in a
    # DuplicateBlockKeyBlock, so the first occurrence of a key is the one that is kept
    # (v1 kept the last one). Warn about the ones that are dropped below.
    duplicates = {b.key for b in refbibdb.failed_blocks if isinstance(b,DuplicateBlockKeyBlock)}
    if duplicates:
        print(warn_str, f"duplicate entries in reference bibliography {refbib}:", *sorted(duplicates))
    # this will merge the two bibtex files, with refbibdb having precedence
    extra_entries = [entry.key for entry in refbibdb.entries if entry.key not in cites]
    if extra_entries:
        print(warn_str, "entries in reference bibliography not cited in tex files:", *sorted(extra_entries))
    new_entries = []
    for entry in bib_database.entries:
        if entry.key not in refbibdb.entries_dict:
            new_entries.append(entry)
        else:
            print(warn_str, f"entry already in reference bibliography {refbib}:", entry.key)
    # again, build a new library instead of appending to the read-only entries list.
    # Any @string/@preamble/@comment blocks of the reference bibliography are kept,
    # while the blocks that failed to parse (duplicates etc) are dropped.
    bib_database = bibtexparser.Library(
        [b for b in refbibdb.blocks if not isinstance(b,ParsingFailedBlock)] + new_entries)

missing_entries = cites - set(bib_database.entries_dict.keys())
missing_entries -=  {'apsrev41Control', 'REVTEX41Control', 'apsrev42Control', 'REVTEX42Control', 'achemso-control'}
if missing_entries:
    print(warn_str, "missing entries in make_latex_references.py:", *sorted(missing_entries))

# write to file
bibtexparser.write_file(os.path.join(outdir,'references.bib'), bib_database)
