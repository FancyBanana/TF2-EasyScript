#every directory is relative to the compile.rb file, which should be located in projects root
#source files location
$groups = './source/groups/'            #contains .grp and .opt files
$modifiers = './source/modifiers.grp'   #a single file containing modifiers buttons, default: modifiers.grp
$prefabs = './source/prefabs/'
#a directory to store build files
$build = './build/'
#output folder
$out_dir = './output/'
#compiler result location
$framework = $out_dir + 'framework.cfg'
$reset = $out_dir + 'resets.cfg'
$group = $out_dir + 'groups.cfg'
$modifier = $out_dir + 'modifiers.cfg'
#directory of compiler parts