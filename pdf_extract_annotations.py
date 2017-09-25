#!/opt/local/bin/python2.7

import poppler
import sys
import urllib
import os

def indent(text, amount, ch=' '):
    padding = amount * ch
    return ''.join((i!=0)*padding+line for i,line in enumerate(text.splitlines(True)))

def main():
    input_filename = sys.argv[1]
    # http://blog.hartwork.org/?p=612
    input_url = 'file://%s' % urllib.pathname2url(os.path.abspath(input_filename))
    document = poppler.document_new_from_file(input_url, None)
    n_pages = document.get_n_pages()
    all_annots = 0

    for i in range(n_pages):
        page = document.get_page(i)
        annot_mappings = page.get_annot_mapping()
        num_annots = len(annot_mappings)
        if num_annots > 0:
            for annot_mapping in annot_mappings:
                if annot_mapping.annot.get_annot_type().value_name != 'POPPLER_ANNOT_LINK':
                    all_annots += 1
                    # print 'page: {0:3}, {1:10}, type: {2:10}, content: {3}'.format(i+1, annot_mapping.annot.get_modified(), annot_mapping.annot.get_annot_type().value_nick, annot_mapping.annot.get_contents())
                    contents = annot_mapping.annot.get_contents()
                    annottype = annot_mapping.annot.get_annot_type().value_nick
                    print indent('page %3s, %10s: %s' % (i+1, annottype, contents),22)
                    #if contents:
                    #  print 'page %3s: %s' % (i+1, contents)
                    #else:
                    #  print 'page %3s, %10s' % (i+1, annottype)

    # if all_annots > 0:
    #   print all_annots, "annotation(s) found"
    # else:
    #   print "no annotations found"

if __name__ == "__main__":
    main()
