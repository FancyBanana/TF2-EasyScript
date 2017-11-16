class CFG:

    # if set to yes, will disable callback when pressing a key twice
    preventCallbackSpam = False

    # source files for groups
    source_groups = './source/groups/'

    # surce file for modifiers
    source_modifiers = './source/modifiers.grp'

    # source files for prefabs
    source_prefabs = './source/prefabs/'

    # directory to store temp files
    temp = './temp/'

    # final output directory
    out_dir = './output/'

    # file to store base definitions in
    oFramework = out_dir + '/easyscript.cfg'

    # file to store reset commands in
    # usefull when reapplying framework
    oResets = out_dir + '/resets.cfg'

    # file to store group definitions in
    oGroups = out_dir + '/groups.cfg'

    # file to store modifiers' definitions in
    oModifiers = out_dir + '/modifiers.cfg'

    # stitch output files toghether with some prefabs
    # create the stitch list
    list_framework = [
        source_prefabs + 'title.pre',
        source_prefabs + 'def_binds.pre',
        temp + 'def_binds.o',
        source_prefabs + 'def_funct.pre',
        temp + 'def_funct.o',
        source_prefabs + 'execs.pre',
    ]
    list_resets = [
        source_prefabs + 'reset.pre',
        temp + 'reset.o',
        source_prefabs + 'unstick.pre',
    ]
    list_groups = [source_prefabs + 'groups.pre',
                   temp + 'groups.o',
                   source_prefabs + 'built_ins.pre']

    list_modifiers = [
        temp + 'modifiers.o',
    ]

    # this will tell compiler where ti write stiched output
    stitching_map = [
        (list_framework, oFramework),
        (list_resets, oResets),
        (list_groups, oGroups),
        (list_modifiers, oModifiers)
    ]
