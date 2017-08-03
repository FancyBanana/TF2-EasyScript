def compile_modifiers(modifiers, modifiables)
    #since tf2 doesn't understand very long commands, we will chain aliases of length
    link_len = 10
    #main portion of the text
    text = []
    #reset assigment
    resets = []
    #default binds
    def_binds  =[]

    text << ' '
    text << %Q\////////////////////////////////////////////////////////////////\
    text << %Q\///// Modifiers\
    text << %Q\////////////////////////////////////////////////////////////////\
    text << ' '

    #since resetting aliases to previous values is common operation for all modifiers
    #it makes sense to define it only once
    al_index = 0
    fm_reset = %Q`alias fm_reset "`
        modifiables.each_with_index{ |entry, index|
            if (index % link_len) != 0 then
                fm_reset << %Q`alias #{entry[0]} #{entry[1]}; `
            else 
                fm_reset << %Q` fm_reset#{al_index};"\nalias fm_reset#{al_index} "`
                al_index += 1
            end
        }
    fm_reset << %Q` "`

    text << fm_reset << ' '

    modifiers.each{ |var|
    modifier = var[:name]
    type = var[:type]
        #precompiling prefixes
        pre = {
            #alias that contains modifier commands
            fm: "fm_mod_"+modifier,
            #script facing aliases for button presses
            sa: "sa_mod_"+modifier,
            pse: "+se_mod_"+modifier,
            mse: "-se_mod_"+modifier,
            #aliases for user binds
            pu: "+u_mod_"+modifier,
            mu: "-u_mod_"+modifier,
            #aliases for toggle mode
            ft: "ft_mod_"+modifier,
            pft: "+ft_mod_"+modifier,
            mft: "-ft_mod_"+modifier,
        }
        #resetting/setting values of script aliases
        resets << %Q`alias #{pre[:sa]} none; `
        resets << %Q`alias #{pre[:pse]} none; `
        resets << %Q`alias #{pre[:mse]} none; `

        

        #'default' binds for modifier keys
        def_binds << %Q`//bind <key> #{pre[:pu]}; `
        #some logic for press/toggle type of modifiers
        case type 
        when  "press" 
            text << %Q`alias #{pre[:pu]} "#{pre[:fm]}; #{pre[:pse]}; #{pre[:sa]};" `
            text << %Q`alias #{pre[:mu]} "fm_reset; #{pre[:mse]};" `
        when "toggle"
            text << %Q`alias #{pre[:ft]} #{pre[:pft]}; `
            text << %Q`alias #{pre[:pft]} "#{pre[:fm]}; alias #{pre[:ft]} #{pre[:mft]};" `
            text << %Q`alias #{pre[:mft]} "fm_reset; alias #{pre[:ft]} #{pre[:pft]};" `
            text << %Q`alias #{pre[:pu]} #{pre[:ft]}; `
            text << %Q`alias #{pre[:mu]} none; `
        end


            fm = %Q`alias #{pre[:fm]} "`
            al_index = 0
            modifiables.each_with_index{ |entry, index|
                if (index % link_len) != 0 then
                    fm << %Q`alias #{entry[0]} #{entry[1]}_#{modifier}; `
                else 
                    fm << %Q` #{pre[:fm]}#{al_index};"\nalias #{pre[:fm]}#{al_index} "`
                    al_index += 1
                end
                resets << %Q`alias #{entry[1]}_#{modifier} #{entry[1]}; `
            }
            fm << %Q` "`

            text << fm << ' '
        
    }
    def_binds << ' '
    return {text: text, resets: resets, def_binds: def_binds}
end
