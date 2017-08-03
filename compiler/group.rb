def compile_group(group_name, group_data, options)
    #is this first entry to be processed?
    #i know that i could use each_with_index, but i dont want to clutter the loop
    is_first = true;
    #entry that should be set as invnext at the start
    #entry that should be set as invprev at the start
    invnext_entry = nil;
    invprev_entry = nil;
    #groups text
    text = []
    #same as text, only goes first
    header = []
    #same as text, only goes second
    init = []
    #i maybe have OCD, because i really want some lines to be toghether
    init2 = []
    #reset assigment
    resets = []
    #default functions
    def_funct = []
    #default binds
    def_binds  =[]
    #things that are affected by modifiers
    #format [handle,defualt_value]
    modifiables = []

    gpre = {
    #this is group's callback function, called at start and reassigned at the end
        gc:     'gc_'+group_name,
    #this is groups lastinv pointers
        gl:     'gl_'+group_name,
        pgl:    '+gl_'+group_name,
        mgl:    '-gl_'+group_name,
    #invnext pointer
        pgn:    '+gn_'+group_name,
        mgn:    '-gn_'+group_name,
    #invprev pointer
        pgp:    '+gp_'+group_name,
        mgp:    '-gp_'+group_name,
    }

    #resetting some group aliases
    if options[:qswitch] == "yes" then
        resets << %Q/alias #{gpre[:pgl]} none; /
        resets << %Q/alias #{gpre[:mgl]} none; /
        resets << %Q/alias #{gpre[:gl]} none; /
    end
    resets << %Q/alias #{gpre[:gc]} none; /  if  options[:callback] == "yes"
    
    #Group's name in the header
    header << ' '
    header << %Q\////////////////////////////////////////////////////////////////\
    header << %Q\///// #{group_name}\
    header << %Q\////////////////////////////////////////////////////////////////\

    group_data.each do |entry|

        #Testing if this entry is a part of quickswitch
        qswitch_element = options.has_value?(entry[:name]);

        #precompile all prefixes for ease of use
        pre = {
            #aliases that user binds
            pu:     '+u_'+entry[:name],
            mu:     '-u_'+entry[:name],
            #aliases used by scripters
            pse:    '+se_'+entry[:name],
            mse:    '-se_'+entry[:name],
            sa:     'sa_'+entry[:name],
            sc:     'sc_'+entry[:name],
            #Framework internal aliases
            #these mirror user's end, they are used for qswitch
            pfd:    '+fd_'+entry[:name],
            mfd:    '-fd_'+entry[:name],
            #these aliases mirror scripters end, used for modifiers
            pfe:    '+fe_'+entry[:name],
            mfe:    '-fe_'+entry[:name],
            fa:     'fa_'+entry[:name],
            fc:     'fc_'+entry[:name],
            #this one holds the callback pointer for this entry
            fp:     'fp_'+entry[:name],
            #this is lastinv function for this entry
            fl:     'fl_'+entry[:name],
        }

#export everything that is affected by modifiers in separate array
        if options[:modifiers] == "yes" then
        modifiables << [pre[:pfe], pre[:pse]]
        modifiables << [pre[:mfe], pre[:mse]]
        modifiables << [pre[:fa], pre[:sa]]
        modifiables << [pre[:fc], pre[:sc]] if options[:callback] == "yes"  && !qswitch_element
        end

#some precompiled prefixes for invnext and invprev
        begin
        lpre = {}
        if options[:qswitch] == "yes"  && !qswitch_element then
            lpre = {
                    pin: '+fd_'+entry[:next],
                    min: '-fd_'+entry[:next],
                    pip: '+fd_'+entry[:prev],
                    mip: '-fd_'+entry[:prev],
                }
        end
        rescue
            abort("Error occured: Most likely you forgot to define invnext or invprev in #{group_name} at #{entry[:name]}\n I know these might not be usefull but hey, i dont want to rewrite my compiler again")
        end
#creating resets and default binds
        resets << %Q/alias #{pre[:sc]} none; /  if  options[:callback] == "yes"

#setting default functions some aliases or resetting them
        if entry[:funct] == nil then
            resets << %Q/alias #{pre[:pse]} none; /
            resets << %Q/alias #{pre[:mse]} none; /
            resets << %Q/alias #{pre[:sa]} none; /
        elsif  entry[:funct] =~ /\+.+/ then
            def_funct << %Q/alias #{pre[:pse]} "#{entry[:funct]}"; /
            def_funct << %Q/alias #{pre[:mse]} "#{m_alias(entry[:funct])}"; /
            resets << %Q/alias #{pre[:sa]} none; /
        else
            def_funct << %Q/alias #{pre[:sa]} "#{entry[:funct]}"; /
            resets << %Q/alias #{pre[:pse]} none; /
            resets << %Q/alias #{pre[:mse]} none; /
        end

#setting default binds
        if entry[:bind] != nil then
            def_binds << %Q\bind #{entry[:bind]} #{pre[:pu]};  \
        else
            def_binds << %Q`//bind <key> #{pre[:pu]}; `
        end

#setting up some aliases for quickswitch
        if is_first then
            is_first = false;
            if  options[:qswitch] == "yes" then
                invnext_entry = entry[:next]
                invprev_entry = entry[:prev]
            end
        end
        if options[:qswitch] == "yes" && invnext_entry == entry[:name] then
            init << %Q\alias #{gpre[:pgn]} #{pre[:pfd]}; \
            init << %Q\alias #{gpre[:mgn]} #{pre[:mfd]}; \
        init << ' '
        end
        if options[:qswitch] == "yes" &&  invprev_entry == entry[:name] then
            init << %Q\alias #{gpre[:pgp]} #{pre[:pfd]}; \
            init << %Q\alias #{gpre[:mgp]} #{pre[:mfd]}; \
        init << ' '
        end

        #a function to setup quickswitch
        if options[:qswitch] == "yes"  && !qswitch_element then
            fl_funct = %Q\alias #{pre[:fl]} "\
            fl_funct << %Q\alias #{gpre[:pgl]}  #{pre[:pfd]}; \
            fl_funct << %Q\alias #{gpre[:mgl]}  #{pre[:mfd]}; \
            fl_funct << %Q\alias #{gpre[:pgn]}  #{lpre[:pin]}; \
            fl_funct << %Q\alias #{gpre[:mgn]}  #{lpre[:min]}; \
            fl_funct << %Q\alias #{gpre[:pgp]}  #{lpre[:pip]}; \
            fl_funct << %Q\alias #{gpre[:mgp]}  #{lpre[:mip]}; "\

            init2 << fl_funct
        end

        #defaul script aliases for framework vars
        header << %Q/alias #{pre[:pfe]} #{pre[:pse]}; /
        header << %Q/alias #{pre[:mfe]} #{pre[:mse]}; /
        header << %Q/alias #{pre[:fa]} #{pre[:sa]}; /
        header << %Q/alias #{pre[:fc]} #{pre[:sc]}; /  if  options[:callback] == "yes"
        header << %Q/alias #{pre[:pu]} #{pre[:pfd]}; /
        header << %Q/alias #{pre[:mu]} #{pre[:mfd]}; /
        header << ' '



#Default button press alias
        palias = %Q/alias #{pre[:pfd]} "/
        palias << %Q/#{gpre[:gc]}; / if  options[:callback] == "yes" && !qswitch_element
        palias << %Q/#{gpre[:pgl]}; / if options[:lastinv] == entry[:name]
        palias << %Q/#{gpre[:pgn]}; / if options[:invnext] == entry[:name]
        palias << %Q/#{gpre[:pgp]}; / if options[:invprev] == entry[:name]
        palias << %Q/alias #{gpre[:gc]} #{pre[:fc]}; / if options[:callback] == "yes"  && !qswitch_element
        palias << %Q/#{gpre[:gl]}; alias #{gpre[:gl]} #{pre[:fl]}; / if options[:qswitch] == "yes"  && !qswitch_element
        palias << %Q/#{pre[:pfe]}; #{pre[:fa]}; /
        palias << %Q/#{entry[:secondary]} /
        palias << %Q/"/
        text << palias
#Default button release alias
        malias = %Q/alias #{pre[:mfd]} "/
        malias << %Q/#{gpre[:mgl]}; / if options[:lastinv] == entry[:name]
        malias << %Q/#{gpre[:mgn]}; / if options[:invnext] == entry[:name]
        malias << %Q/#{gpre[:mgp]}; / if options[:invprev] == entry[:name]
        malias << %Q/#{pre[:mfe]}; /
        malias << %Q/#{m_alias(entry[:secondary].split(';').collect{|cmd| cmd+';'}).join('')} / if entry[:secondary]
        malias << %Q/"/
        text << malias

#a newline to separate each entry
        text << ' '
    end
    header << init << ' ' << init2 << ' '<< text;
    header = header.flatten;
    def_binds << ' '
    def_funct << ' '
    return {text: header, resets: resets,def_binds: def_binds, def_funct: def_funct, modifiables: modifiables}
end