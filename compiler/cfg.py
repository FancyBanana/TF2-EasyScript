#! python3


class CFG:
    groups = './source/groups/'                 # source files for groups
    modifiers = './source/modifiers.grp'       # surce file for modifiers
    prefabs = './source/prefabs/'               # source files for prefabs
    build = './build/'                           # directory to store temp files
    out_dir = './output/'                        # final output directory
    # file to store base definitions in
    oFramework = out_dir+'/framework.cfg'
    # file to store reset commands in
    # usefull when reapplying framework
    oResets = out_dir+'/resets.cfg'
    # file to store group definitions in
    oGroups = out_dir+'/groups.cfg'
    # file to store modifiers' definitions in
    oModifiers = out_dir+'/modifiers.cfg'
