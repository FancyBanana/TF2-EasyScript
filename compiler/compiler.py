#! python3

# If you want to modify complation process,
# then go to compiler/config.py
# This file

from glob import glob
from os import makedirs, path

# get functions
from compiler.group import *
from compiler.modifiers import *
from compiler.text import *


def compile(CFG):

    # this will hold the list of all modifiable aliases
    modifiables = []

    # creating relevant dirs

    if(not path.isdir(CFG.out_dir)):
        makedirs(CFG.out_dir)
    if(not path.isdir(CFG.temp)):
        makedirs(CFG.temp)
    # file containing modifiers' definition
    m = open(CFG.source_modifiers, 'r')

    # relevant output files where text is saved before stitching
    frs = open(CFG.temp + 'reset.o', 'w+')
    fdb = open(CFG.temp + 'def_binds.o', 'w+')
    fdf = open(CFG.temp + 'def_funct.o', 'w+')
    fmd = open(CFG.temp + 'modifiers.o', 'w+')

    # read every group, it's options and compile items
    groups = glob(CFG.source_groups + '*.grp')
    fo = open(CFG.temp + 'groups.o', 'w')
    for gpr in groups:
        f = baseNameNoExt(gpr)
        f1 = open(gpr, 'r')
        f2 = open(CFG.source_groups + f + '.opt', 'r')
        res = compileGroup(f, readGroup(f1.readlines()),
                           readOptions(f2.readlines()),
                           CFG.preventCallbackSpam)
        writeListToFile(res['text'], fo)
        writeListToFile(res['resets'], frs)
        writeListToFile(res['def_binds'], fdb)
        writeListToFile(res['def_funct'], fdf)
        modifiables += res['modifiables']
        f1.close()
        f2.close()
        fo.write("\n")
    fo.close()

    # compile modifiers
    res = None
    res = compileModifiers(readModifiers(m.readlines()), modifiables)
    writeListToFile(res['text'], fmd)
    writeListToFile(res['resets'], frs)
    writeListToFile(res['def_binds'], fdb)

    # closing file since it is useless now
    m.close()
    # closing all files since we will need to reopen them
    frs.close()
    fdb.close()
    fdf.close()
    fmd.close()

    for (l, d) in CFG.stitching_map:
        stitchFiles(l, d)

    print('End of compilation')
