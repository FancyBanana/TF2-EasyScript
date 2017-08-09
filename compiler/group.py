#! python3

from compiler.cfg import *
from compiler.util import *
from compiler.text import *
import re


def compileGroup(group_name, group_data, options):
    is_first = True         # first loop is special
    invnext_entry = None    # initialze invprev and invnext
    invprev_entry = None
    # groups text
    text = []
    # same as text, only goes first
    header = []
    # same as text, only goes second
    init = []
    # i may have OCD, because i really want some lines to be toghether
    init2 = []
    # reset assigment
    resets = []
    # default functions
    def_funct = []
    # default binds
    def_binds = []
    # things that are affected by modifiers
    # format [handle,defualt_value]
    modifiables = []
    # resetting some group aliases
    gpre = {
        'gc':     'gc_'+group_name,
        'gl':     'gl_'+group_name,
        'pgl':    '+gl_'+group_name,
        'mgl':    '-gl_'+group_name,
        'pgn':    '+gn_'+group_name,
        'mgn':    '-gn_'+group_name,
        'pgp':    '+gp_'+group_name,
        'mgp':    '-gp_'+group_name,
    }

    if options['qswitch']:
        resets += ["alias " + gpre['pgl'] + " none; "]
        resets += ["alias " + gpre['mgl'] + " none; "]
        resets += ["alias " + gpre['gl'] + " none; "]


# Group's name in the header


# Group's name in the header
    header += [' ']
    header += ['////////////////////////////////\
////////////////////////////////']
    header += ['///// ' + group_name]
    header += ['////////////////////////////////\
 ////////////////////////////////']

    pre = {}
    for entry in group_data:
        # Testing if this entry is a part of quickswitch
        is_qswitch_element = (entry['name'] in options)

        # precompile all prefixes for ease of use
        pre = {
            # aliases that user binds
            'pu':     '+u_'+entry['name'],
            'mu':     '-u_'+entry['name'],
            # aliases used by scripters
            'pse':    '+se_'+entry['name'],
            'mse':    '-se_'+entry['name'],
            'sc':     'sc_'+entry['name'],
            # Framework internal aliases
            # these mirror user's end, they are used for qswitch
            'pfd':    '+fd_'+entry['name'],
            'mfd':    '-fd_'+entry['name'],
            # these aliases mirror scripters end, used for modifiers
            'pfe':    '+fe_'+entry['name'],
            'mfe':    '-fe_'+entry['name'],
            'fc':     'fc_'+entry['name'],
            # this one holds the callback pointer for this entry
            'fp':     'fp_'+entry['name'],
            # this is lastinv function for this entry
            'fl':     'fl_'+entry['name'],
            # alias to setup lastinv
            'gl':     'gl_'+entry['name'],
        }

        # export everything that is affected by modifiers in separate array
        if options['modifiers']:
            modifiables += [[pre['pfe'], pre['pse']]]
            modifiables += [[pre['mfe'], pre['mse']]]
            if options['callback'] and not is_qswitch_element:
                modifiables += [[pre['fc'], pre['sc']]]

        # some precompiled prefixes for invnext and invprev
        lpre = {}
        if options['qswitch'] and not is_qswitch_element:
            lpre = {
                    'pin': '+fd_'+entry['next'] if entry['next'] else ' ',
                    'min': '-fd_'+entry['next'] if entry['next'] else ' ',
                    'pip': '+fd_'+entry['prev'] if entry['next'] else ' ',
                    'mip': '-fd_'+entry['prev'] if entry['next'] else ' ', }
        # creating resets and default binds
        if options['callback']:
            resets += ['alias ' + pre['sc'] + ' none;']

        # setting default functions some aliases or resetting them
        if not entry['funct']:
            resets += ['alias ' + pre['pse'] + ' none;']
            resets += ['alias ' + pre['mse'] + ' none;']
        elif re.match(r"\+.+", entry['funct']):
            def_funct += ['alias ' + pre['pse'] + ' "' + entry['funct'] + '";']
            def_funct += ['alias ' + pre['mse'] + ' "' +
                          mAlias(entry['funct']) + '";']
        else:
            def_funct += ['alias ' + pre['pse'] + ' "' + entry['funct'] + '";']
            resets += ['alias ' + pre['mse'] + ' none;']

        # setting default binds
        if entry['bind']:
            def_binds += ['bind ' + entry['bind'] + ' ' + pre['pu']]
        else:
            def_binds += ['//bind <key> ' + pre['pu']]

        # setting up some aliases for quickswitch
        if is_first:
            is_first = False
            if options['qswitch']:
                invnext_entry = entry['next']
                invprev_entry = entry['prev']

        if options['qswitch'] and invnext_entry == entry['name']:
            init += ['alias ' + gpre['pgn'] + ' ' + pre['pfd']]
            init += ['alias ' + gpre['mgn'] + ' ' + pre['mfd']]
            init += [' ']

        # a function to setup quickswitch
        if options['qswitch'] and not is_qswitch_element:
            # setting up lastinv after buton press

            gl_funct = 'alias ' + pre['gl'] + ' "'\
                + ' alias ' + gpre['pgl'] + ' ' + pre['pfd'] + '; ' \
                + ' alias ' + gpre['mgl'] + ' ' + pre['mfd'] + ';"'
            init2 += [gl_funct]

            fl_funct = 'alias ' + pre['fl'] + ' "'\
                + ' alias ' + gpre['gl'] + ' ' + pre['gl'] + '; '\
                + ' alias ' + gpre['pgn'] + ' ' + lpre['pin'] + '; ' \
                + ' alias ' + gpre['mgn'] + ' ' + lpre['min'] + '; ' \
                + ' alias ' + gpre['pgp'] + ' ' + lpre['pip'] + '; ' \
                + ' alias ' + gpre['mgp'] + ' ' + lpre['mip'] + ';"'
            init2 += [fl_funct]

        # defaul script aliases for framework vars
        header += ['alias ' + pre['pfe'] + ' ' + pre['pse']]
        header += ['alias ' + pre['mfe'] + ' ' + pre['mse']]
        if options['callback']:
            header += ['alias ' + pre['fc'] + ' ' + pre['sc']]
        header += ['alias ' + pre['pu'] + ' ' + pre['pfd']]
        header += ['alias ' + pre['mu'] + ' ' + pre['mfd']]
        header += [' ']

        # Default button press alias
        palias = 'alias ' + pre['pfd'] + ' "'
        if CFG.preventCallbackSpam:
            palias += "alias %s none; " % pre['fc']
        if options['callback'] and not is_qswitch_element:
            palias += gpre['gc'] + '; '
        if CFG.preventCallbackSpam:
            palias += "alias %s %s; " % (pre['fc'], pre['sc'])
        if options['lastinv'] == entry['name']:
            palias += gpre['pgl'] + '; '
        if options['invnext'] == entry['name']:
            palias += gpre['pgn'] + '; '
        if options['invprev'] == entry['name']:
            palias += gpre['pgp'] + '; '
        if options['callback'] and not is_qswitch_element:
            palias += 'alias ' + gpre['gc'] + ' ' + pre['fc'] + '; '
        if options['qswitch'] and not is_qswitch_element:
            palias += gpre['gl'] + '; ' + pre['fl'] + '; '
        palias += pre['pfe'] + '; '
        if(entry['secondary']):
            palias += entry['secondary'] + ''
        palias += '"'
        text += [palias]

        # Default button release alias
        malias = 'alias ' + pre['mfd'] + ' "'
        if options['lastinv'] == entry['name']:
            malias += gpre['mgl'] + '; '
        if options['invnext'] == entry['name']:
            malias += gpre['mgn'] + '; '
        if options['invprev'] == entry['name']:
            malias += gpre['mgp'] + '; '
        malias += pre['mfe'] + '; '
        if entry['secondary'] and re.match(r"\+", entry['secondary']):
            tmp = mAlias(entry['secondary'].split(';'))
            tmp = [i + '; ' for i in tmp]
            tmp = ''.join(tmp)
            malias += tmp

        text += [malias + '" ']

    # a newline to separate each entry
    final = []
    final += header + init + init2 + text
    def_binds += [' ']
    def_funct += [' ']
    return {'text': final, 'resets': resets, 'def_binds': def_binds,
            'def_funct': def_funct, 'modifiables': modifiables}
