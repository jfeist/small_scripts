#!/usr/bin/env python
if __name__ == '__main__':
    from nbconvert import NotebookExporter, preprocessors
    import sys
    if len(sys.argv)>1:
        import io
        from os.path import splitext
        from shutil import move
        nbfile = sys.argv[1]
        root, ext = splitext(nbfile)
        dirtyfile = root + '-dirty' + ext
        move(nbfile,dirtyfile)
        infi  = io.open(dirtyfile)
        outfi = io.open(nbfile,'w')
    else:
        infi  = sys.stdin
        outfi = sys.stdout

    cop = preprocessors.ClearOutputPreprocessor()
    exporter = NotebookExporter(preprocessors=[cop])
    body, _ = exporter.from_file(infi)
    outfi.write(body)
