#! python3

import re
from compiler.util import *


def stitchFiles(file_list, destination):
    fout = open(destination, "w")
    for f in file_list:
        fin = open(f, 'r')
        fout.writelines(fin.readlines())
        fout.write("\n")


def cleanLine(arg):
    m1 = re.sub(r"#.*$", '', arg)
    m1 = re.sub(r"^\s*", '', m1)
    m1 = re.sub(r"\s*$", '', m1)
    return m1


def prepLine(arg):
    m1 = cleanLine(arg)
    m2 = re.match(r"\S+", m1)
    if(m2 is None):
        return None
    parts = m1.split(r":")
    res = []
    for part in parts:
        clean = cleanLine(part)
        if len(clean) > 0:
            cropped = clean
        else:
            cropped = None
        res.append(cropped)
    return res


def rSign(text):
    if(re.match(r"\+", text)):
        return re.sub(r"\+", "-", text)
    elif(re.match(r"\-", text)):
        return re.sub(r"\-", "+", text)
    else:
        return text


def mAlias(var):
    if type(var) is str:
        return rSign(var)
    elif type(var) is list:
        res = []
        for i in var:
            res.append(rSign(i))
        return res


def readGroup(lines):
    res = []
    names = ['name', 'funct', 'bind', 'secondary', 'next', 'prev']
    for line in lines:
        l = []
        r = {}
        for i in range(0, len(names)):
            l.append(None)
        prepped = prepLine(line)
        if(prepped is None):
            continue
        arraySubst(prepped, l)
        for i in range(0, len(names)):
            r[names[i]] = l[i]
        res.append(r)
    return res


def readOptions(lines):
    optList = {'modifiers': False, 'callback': False, 'qswitch': False,
               'lastinv': None, 'invnext': None, 'invprev': None}
    opts = optList.keys()
    for line in lines:
        prepped = prepLine(line)
        if(prepped is None):
            continue
        for opt in opts:
            if(re.match(opt, prepped[0], re.I)):
                optList[opt] = qtfy(prepped[1])
                break
    return optList


def readModifiers(lines):
    res = []
    for line in lines:
        prepped = prepLine(line)
        if(not prepped):
            continue
        res.append({'name': prepped[0], 'type': prepped[1]})
    return res
