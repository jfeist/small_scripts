#!/usr/bin/env python
if __name__ == '__main__':
    import io, sys
    import nbformat
    useformat = nbformat.current_nbformat
    for nbfile in sys.argv[1:]:
        nb = nbformat.read(nbfile,useformat)
        nbformat.write(nb, nbfile)
