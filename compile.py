#! python3

from glob import glob
from os import makedirs

# get the configuration
from compiler.cfg import *
# get functions
from compiler.group import *
from compiler.modifiers import *
from compiler.text import *

# this will hold the list of all modifiable aliases
modifiables = []

# creating relevant dirs
try:
    makedirs(CFG.build+'groups/')
    makedirs(CFG.out_dir)
except Exception:
    pass
# file containing modifiers' definition
m = open(CFG.modifiers, 'r')

# relevant output files where text is saved before stitching
frs = open(CFG.build+'reset.o', 'w+')
fdb = open(CFG.build+'def_binds.o', 'w+')
fdf = open(CFG.build+'def_funct.o', 'w+')
fmd = open(CFG.build+'modifiers.o', 'w+')

# read every group, it's options and compile itew
groups = glob(CFG.groups+'*.grp')
for gpr in groups:
    f = justName(gpr)
    f1 = open(gpr, 'r')
    f2 = open(CFG.groups+f+'.opt', 'r')
    fo = open(CFG.build+'groups/'+f+'.o', 'w')
    res = compileGroup(f, readGroup(f1.readlines()),
                       readOptions(f2.readlines()))
    for line in res['text']:
        fo.write(line+"\n")
    for line in res['resets']:
        frs.write(line+"\n")
    for line in res['def_binds']:
        fdb.write(line+"\n")
    for line in res['def_funct']:
        fdf.write(line+"\n")
    modifiables += res['modifiables']
    f1.close()
    f2.close()
    fo.close()


# compile modifiers
res = None
res = compileModifiers(readModifiers(m.readlines()), modifiables)
for line in res['text']:
    fmd.write(line+"\n")
for line in res['resets']:
    frs.write(line+"\n")
for line in res['def_binds']:
    fdb.write(line+"\n")

# closing file since it is useless now
m.close()
# closing all files since we will need to reopen them
frs.close()
fdb.close()
fdf.close()
fmd.close()

# stitch output files toghether with some prefabs
# create the stitch list
l_framework = [
    CFG.prefabs+'title.pre',
    CFG.prefabs+'def_binds.pre',
    CFG.build+'def_binds.o',
    CFG.prefabs+'def_funct.pre',
    CFG.build+'def_funct.o',
    CFG.prefabs+'execs.pre',
]
l_resets = [
    CFG.prefabs+'reset.pre',
    CFG.build+'reset.o',
    CFG.prefabs+'unstick.pre',
]
l_groups = [CFG.prefabs+'groups.pre']
l_groups += glob(CFG.build+'groups/*')
l_groups += [CFG.prefabs+'built_ins.pre']

l_modifiers = [
    CFG.build+'modifiers.o',
]


# build framework.cfg
stitchFiles(l_framework, CFG.oFramework)

# build resets
stitchFiles(l_resets, CFG.oResets)

# build groups
stitchFiles(l_groups, CFG.oGroups)

# build modifiers
stitchFiles(l_modifiers, CFG.oModifiers)

print('End of compilation')