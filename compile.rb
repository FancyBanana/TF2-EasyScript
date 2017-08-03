#! ruby
#get the configuration
require './cfg.rb';
#get functions
Dir['./compiler/*'].each do |file|
    require file
end

#this will hold the list of all modifiable aliases
modifiables = []

#file containing modifiers' definition
m = File.new($modifiers,'r+')

#relevant output files where text is saved before stitching
frs = File.new($build+'reset.o','w+')
fdb = File.new($build+'def_binds.o','w+')
fdf = File.new($build+'def_funct.o','w+')
fmd = File.new($build+'modifiers.o','w+')

#read every group, it's options and compile itew
groups = Dir[$groups+'*.grp']
groups.each {|grp|
    f = File.basename(grp,'.grp');
    f1 = File.new($groups+f+'.grp','r+')
    f2 = File.new($groups+f+'.opt','r+')
    fo = File.new($build+'groups/'+f+'.o','w+')
    res = compile_group(f,read_group(f1),read_options(f2))
    res[:text].each{|line| fo << line << "\n"}
    res[:resets].each{|line| frs << line << "\n"}
    res[:def_binds].each{|line| fdb << line << "\n"}
    res[:def_funct].each{|line| fdf << line << "\n"}
    modifiables += res[:modifiables]
    f1.close
    f2.close
    fo.close
}

#compile modifiers
res = nil
res = compile_modifiers(read_modifiers(m),modifiables)
res[:text].each{|line| fmd << line << "\n"}
res[:resets].each{|line| frs << line << "\n"}
res[:def_binds].each{|line| fdb << line << "\n"}

#closing file since it is useless now
m.close
#closing all files since we will need to reopen them
frs.close
fdb.close
fdf.close
fmd.close

#stitch output files toghether with some prefabs
#create the stitch list
l_framework = [
    $prefabs+'title.pre',
    $prefabs+'def_binds.pre',
    $build+'def_binds.o',
    $prefabs+'def_funct.pre',
    $build+'def_funct.o',
    $prefabs+'execs.pre',
]
l_resets = [
    $prefabs+'reset.pre',
    $build+'reset.o',
    $prefabs+'unstick.pre',
]
l_groups = [
    $prefabs+'groups.pre',
    Dir[$build+'groups/*'],
    $prefabs+'built_ins.pre'
]
l_modifiers = [
    $build+'modifiers.o',
]
l_groups = l_groups.flatten

#build framework.cfg
stitch_files(l_framework, $framework);

#build resets
stitch_files(l_resets, $reset);

#build groups
stitch_files(l_groups, $group);

#build modifiers
stitch_files(l_modifiers, $modifier);

puts 'End of compilation'