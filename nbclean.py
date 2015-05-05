#!/usr/bin/env python
def clean_nb(nb):
    try:
        del nb.metadata['signature']
    except KeyError:
        pass

    for cell in nb.cells:
        if 'outputs' in cell:
            cell['outputs'] = []
        if "execution_count" in cell:
            cell["execution_count"] = None
    return nb

if __name__ == '__main__':
    import io, sys
    from IPython import nbformat
    from os.path import splitext
    from shutil import move
    if len(sys.argv)>1:
        nbfile = sys.argv[1]
        root, ext = splitext(nbfile)
        dirtyfile = root + '-dirty' + ext
        move(nbfile,dirtyfile)
        infi  = io.open(dirtyfile)
        outfi = io.open(nbfile,'w')
    else:
        infi  = sys.stdin
        outfi = sys.stdout

    nb = nbformat.read(infi,4)
    nb = clean_nb(nb)
    nbformat.write(nb, outfi)
