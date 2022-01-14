#!/usr/bin/env python

import os, sys

# workaround for a problem with Qt5 wrongly checking macOS 11 version
if not os.getenv("SYSTEM_VERSION_COMPAT") == "0":
    os.environ["SYSTEM_VERSION_COMPAT"] = "0"
    import subprocess
    proc = subprocess.run(sys.argv)
    sys.exit(proc.returncode)

# start of actual script
from popplerqt5 import Poppler
from PyQt5.QtCore import QRectF, QPointF
from textwrap import fill

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[34m'
    OKCYAN = '\033[36m'
    OKGREEN = '\033[32m'
    WARNING = '\033[33m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def indent(text, amount, ch=' '):
    padding = amount * ch
    return ''.join((i!=0)*padding+line for i,line in enumerate(text.splitlines(True)))

printind22 = lambda text: print(indent(text,22))

pageshift = int(os.getenv("PDF_PAGESHIFT",0))

def main():
    input_filename = sys.argv[1]
    document = Poppler.Document.load(input_filename)
    n_annots = 0

    for i in range(len(document)):
        page = document.page(i)
        scaleP = lambda P: QPointF(P.x() * page.pageSize().width(), P.y() * page.pageSize().height())
        scaleQ = lambda Q: QRectF(scaleP(Q.points[0]),scaleP(Q.points[2]))

        for annot in page.annotations():
            if not isinstance(annot,Poppler.LinkAnnotation):
                n_annots += 1
                contents = annot.contents()
                annottype = type(annot).__name__.replace("Annotation","")
                printind22(f'{bcolors.OKBLUE}page {i+1+pageshift:3d}, {annottype:>10s}{bcolors.ENDC}: {fill(contents,100)}')
                if isinstance(annot,Poppler.HighlightAnnotation):
                    quads = annot.highlightQuads()
                    txt = " ".join([page.text(scaleQ(quad)).strip() for quad in quads])
                    printind22(f'    {bcolors.OKGREEN}highlighted text:{bcolors.ENDC} {fill(txt,100)}')
                print()

    # if n_annots > 0:
    #   print n_annots, "annotation(s) found"
    # else:
    #   print "no annotations found"

if __name__ == "__main__":
    main()
