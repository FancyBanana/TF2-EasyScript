#! python3


def compileModifiers(modifiers, modifiables):
    # since tf2 doesn't understand very long commands,
    # we will chain aliases of length 10
    link_len = 10
    # main portion of the text
    text = []
    # reset assigment
    resets = []
    # default binds
    def_binds = []

    text += [' ']
    text += ['/////////////////////////////////////////////\
              ///////////////////']
    text += ['///// Modifiers']
    text += ['/////////////////////////////////////////////\
              ///////////////////']
    text += [' ']
    text += ['alias mod_reset none;']

    # since resetting aliases to previous values
    # is common operation for all modifiers
    # it makes sense to define it only once
    al_index = 0
    fm_reset = "mod_reset; "
    fm_reset += "alias fm_reset "
    for index, entry in enumerate(modifiables):
        if (index % link_len) != 0:
            fm_reset += 'alias ' + entry[0] + ' ' + entry[1] + '; '
        else:
            fm_reset += ' fm_reset%s;"\nalias fm_reset%s "' % (al_index,
                                                               al_index)
            al_index += 1

    fm_reset += ' "'

    text += [fm_reset] + [' ']

    for modifier in modifiers:
        modifier_name = modifier['name']
        modifier_type = modifier['type']
        # precompiling prefixes
        pre = {
            # alias that contains modifier commands
            'fm': "fm_mod_"+modifier_name,
            # script facing aliases for button presses
            'pse': "+se_mod_"+modifier_name,
            'mse': "-se_mod_"+modifier_name,
            # aliases for user binds
            'pu': "+u_mod_"+modifier_name,
            'mu': "-u_mod_"+modifier_name,
            # aliases for toggle mode
            'ft': "ft_mod_"+modifier_name,
            'pft': "+ft_mod_"+modifier_name,
            'mft': "-ft_mod_"+modifier_name,
            'set': "mod_"+modifier_name+"_set",
            'reset': "mod_"+modifier_name+"_reset",
        }
        # resetting/setting values of script aliases
        resets += ['alias ' + pre['pse'] + ' none; ']
        resets += ['alias ' + pre['mse'] + ' none; ']
        resets += ['alias ' + pre['set'] + ' none; ']
        resets += ['alias ' + pre['reset'] + ' none; ']

        # default' binds for modifier keys
        def_binds += ['//bind <key> ' + pre['pu']]
        # some logic for press/toggle type of modifiers
        if modifier_type == "press":
            text += ['alias %s "%s; %s;"' %
                     (pre['pu'], pre['fm'], pre['pse'])]
            text += ['alias %s "fm_reset; %s;"' % (pre['mu'], pre['mse'])]
        elif modifier_type == "toggle":
            text += ['alias %s %s; ' % (pre['ft'], pre['pft'])]
            text += ['alias %s "%s; alias %s %s;" '
                     % (pre['pft'], pre['fm'], pre['ft'], pre['mft'])]
            text += ['alias %s "fm_reset; alias %s %s;" '
                     % (pre['mft'], pre['ft'], pre['pft'])]
            text += ['alias %s %s; ' % (pre['pu'], pre['ft'])]
            text += ['alias %s none; ' % pre['mu']]

        fm = 'alias %s "' % pre['fm']
        fm += '%s; ' % pre['set']
        fm += 'alias mod_reset %s; ' % pre['reset']
        al_index = 0

        for index, entry in enumerate(modifiables):
            if index % link_len != 0:
                fm += 'alias %s %s_%s; ' % (entry[0], entry[1], modifier_name)
            else:
                fm += ' %s%s;"\nalias %s%s "' % (pre['fm'], al_index,
                                                 pre['fm'], al_index)
                al_index += 1
            resets += ['alias %s_%s %s; ' %
                       (entry[1], modifier_name, entry[1])]

        fm += ' "'
        text += [fm] + [' ']

    def_binds += [' ']
    return {'text': text, 'resets': resets, 'def_binds': def_binds}
