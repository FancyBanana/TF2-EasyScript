#! python3

from os.path import basename, splitext


def qtfy(txt):
    if txt == 'no':
        return False
    if txt == 'yes':
        return True
    return txt


def arraySubst(src, dest):
    count = range(len(src))
    for i in count:
        dest[i] = src[i]
    return dest


def baseNameNoExt(filename):
    return splitext(basename(filename))[0]
