#!/usr/bin/env python

import os, sys

# workaround for a problem with Qt5 wrongly checking macOS 11 version
if not os.getenv("SYSTEM_VERSION_COMPAT") == "0":
    os.environ["SYSTEM_VERSION_COMPAT"] = "0"
    import subprocess
    subprocess.run(sys.argv)
else:
    from popplerqt5 import Poppler

    def indent(text, amount, ch=' '):
        padding = amount * ch
        return ''.join((i!=0)*padding+line for i,line in enumerate(text.splitlines(True)))

    def main():
        input_filename = sys.argv[1]
        document = Poppler.Document.load(input_filename)
        n_annots = 0

        for i in range(len(document)):
            page = document.page(i)
            for annot in page.annotations():
                if not isinstance(annot,Poppler.LinkAnnotation):
                    n_annots += 1
                    contents = annot.contents()
                    annottype = type(annot).__name__.replace("Annotation","")
                    print(indent('page %3s, %10s: %s' % (i+1, annottype, contents), 22))

        # if n_annots > 0:
        #   print n_annots, "annotation(s) found"
        # else:
        #   print "no annotations found"

    if __name__ == "__main__":
        main()
