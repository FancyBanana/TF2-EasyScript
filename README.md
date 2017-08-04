# TF2 EasyScript
A scripting framework by /u/FanciestBanana  
A thank you for people contribuiting to this project: /u/Tvde1  

### For quick programming guide scroll to the bottom.

## Description

A script so ambitious it has it's own compiler!
This framework is meant to be a starting point for scripters as well as 
a base for sharing scripts. It serves as a middleman between user input and scripts, also serving as a solid foundation for your scripts.

# Features
 * ### Every single functionality in TF2 is taken care of!  
   Every single key press can be and should be treated by EasyScript.

 * ### Change key binds without changing your script!
   
 * ### Mode shift everything!
   Mode shifting for ***every single*** (you heard it) ___key in the game___.  

 * ### Scripters best friend!
   Most confusing and annoying necessities are taken care of!
   TF2-EasyScript has hooks for different button press events, callbacks for when pressing next button in a button group as well as built-in null-canceling movement script.   
   Lastinv, invnext, invprev are already implemented.

 * ### Aliases for commands you didn't know existed!
   Call for an uber with single key press or instantly deply a sentry. Or you can even use that taunt in the last slot that you hate to reach for...
 
 * ### Sharing scripts is never more complicated than drag'n'drop!
   Since all your script call TF2-EasyScript, it elimenates any need 

## How to install:  
1. Go to:  
     * [Releases](https://github.com/FancyBanana/TF2-EasyScript/releases) page on `GitHub`  
     * [Tags](https://gitlab.com/vharabar/TF2-EasyScript/tags) page on `GitLab`  
and grab a `.zip` with latest release of TF2-EasyScript

1. Navigate to your TF2 cfg folder.  
    -  Example: `C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\cfg`

1. Copy the contents of `/output/*` into TF2 cfg folder  

1. If you hadn't already, create `autoexec.cfg`. This file will be executed  
        at every launch.  

1. In `autoexec.cfg` write on first line `exec easyscript.cfg`    
        This will execute easyscript script at every launch.  

1. In `easyscript.cfg` navigate to `Default bindings` section.  
        There you will find a bunch of bindings that ressemble default ones   
        If you want to change binds, this is the place to do it.

1.  (Advanced) If you happen to have `<class>.cfg` scripts they should call `exec easyscript.cfg` in the first line. This will reset all aliases to defaults as well unstick all keys. This framework is designed to clean up everything for you :).  

## How to use

##### For in-depth explanation on how to use TF2-EasyScript, please see `Wiki` section. (Coming oon)

#### Vocabulary
        function - a native command that when written in console executes some action
        alias - a user-defined command that may call function(s) and/or other alias(es)
        binding - act of connecting a key press to function or alias
        a binding - the connection of a button to a function or alias

It also should be noted that when a function or an alias with `+` prefix is bound to a key a function or an alias of the same name with prefix `-` is called on the release of the key, ex:

        bind w +forward

        pressing w down -> +forward is called
        releasing w     -> -forward is called

TF2-EasyScript consists of 4 files, but everything usefull in conviently located in `easyscript.cfg`, other 3 ae purely technical.  

`easyscript.cfg` contains all key bindings, active and stubs for unused ones, and also aliases for voice commands, building stuff, destroying stuff, usign eurika teleport, joining a class, joining a team, disguse for every combination of team/class, and lastly default functions for framework aliases that mirror buttons and shift modifiers.  
There's also a nifty script for showing console text on top of your hud.

The main principle behind this framework is that every default function (and more) is mirrored, so instead of:  

        bind w +forward

we have 

        bind w +u_forward
        alias +se_forward +forward
        alias -se_forward -forward

There's quite a bit more code, but it allows for exterme flexibility.  
Here's a bit more detailed:  
 * there are user aliases:  

        +u_<function_name>  //key press
        -u_<function_name>  //key release
   
   that are bound to keys:

        bind <key> +u_<function_name>

   so now whenever we press a `key` the `+u` alias is called, and when we release the `key` the `-u` alias is called

 * there are also scripting aliases:

         sc_<function_name>  //callback alias(explained later)
        +se_<function_name>  //keydown event alias
         sa_<function_name>  //key press event alias
        -se_<function_name>  //keyup event alias

   that are used to call alias in user scripts. Please notice that all these are the same function name with different prefixes.

Here are couple of simple examples with key press events detailed:

### `attack` on `MOUSE1`
don't worry about `gc_attack` and `sc_attack`  

what you write:

        bind MOUSE1 +u_attack
        alias +se_attack +attack
        alias -se_attack -attack
   
and how it is executed:

        pressing MOUSE1 -> 1. gc_attack  called 
                           (previous alias for gc_attack, 
                           for example "alias gc_attack sc_attack2")

                           2. setting gc_attack to sc_attack
                           ("alias gc_attack sc_attakc")

                           3. +se_attack called (+attack)

                           4. sa_attack  called (nothing)

        releasing MOUSE1-> 1. -se_atack called (-attack)

Comment: attack key group has callback functionality, that's why you can define `sc_attack`, `sc_attack2` and `sc_attack3` to be called for consecutive key presses.

another example  
### Calling medic on `E`

what you write

        bind E +u_callmed
        alais sa_callmed v_medic (v_medic is one of many 
                                  short-hand aliases in TF2-EasyScript)

and what happens when you press key

        pressing  E-> 1. +se_callmed (nothing)
                      2. sa_callmed (v_medic)

        releasing E-> 1. -se_callmed (nothing)

Pretty simple, right? How about something more complex:
### Mod shifting `E` to call for Uber

Here we will be using predefind `pa` (full name is `mod_pa`) modified.  
There are 2 types of modifiers: `press` and `toggle`.  
`a` is a `press` modfifier (**p**a), first by aphabetical order (**a**). There are a total of 4 predefined modifires:  
 * (`mod_`)`pa`
 * (`mod_`)`pb`
 * (`mod_`)`ta`
 * (`mod_`)`tb`

 when any modifier is active, every script alias "gains a suffix", that correspods to modifier name ex:

        sa_callmed becomes sa_callmed_pa

you can add more (why would you need more?) by modifiying source files and building the framework from source.

assuming the last example we need to write

        bind `MOUSE4` +u_mod_pa  //binding shift mode alias 

        alias sa_callmed_pa v_activateuber 

                        (again, this handy short-hand alias
                        for a voice command can be found in
                        `easyscript.cfg`)

And that's all! Not anytime you press `MOUSE4`+E you can annoy your medic to give you uber XD

And for the last topic:
### Callbacks

It's rather hard for me to describe what a callback is, so i will base my explanation on na example.

Let's say you play spy, your `fov_desired` is `90` by default but you want it to switch to `75` for your ambassador. So you need to switch to `75` when choosing `slot1`, and and back to `90` when choosing anything else. The problem starts with *anythign else* part. Normally you would need to include `fov_desired 90` into slots 2 to 10 to set fov to normal, but with TF2-EasyScript you need to do it only once for `slot1` callback, `sc_slot1`.

Assuming you are using default binds (`bind 1 +u_slot`,etc...)  
We need to locate the default function for `+u_slot1`, which should be a combination of any of 4 script aliases. In this case it's 

        alias sa_slot1 "slot1"; (you can easil find this in easyscript.cfg)

We will override this to inlude desired functionality.

Now, for convinience we will create a spy.cfg, which will be automatically called when you change your class to spy.

Inside we write:

        exec easyscript.cfg //obligatory, will reset aliases and cleanup

        alias sa_slot1 "slot1; fov_desired 75" //now selecting slot1 will set your fov to 75

        alias sc_slot1 "fov_desired 90;"  //this will reset fov to normal when deselecting slot1


And this is it! Amazingly simple, isn't it? Normaly it will take a lot more code to implement, and maintainig the code becomes more difficult the more you write (believe me, without bloody compiler this framework is huge pain in the bottom).

So now we will examine what happens when we press `2` then `1` then `3`:

        pressing 2  ->  1. call gc_slot (starting value
                           is sc_slot1; "fov_desired 90;")

                        2. settign gc_slot to sc_slot2 
                           (default: "none")

                        3. +se_slot2('none')

                        4. sa_slot2 ("slot2")

        releasing 2 ->  1. -se_slot2 ("none")
                        
        pressing  1 ->  1. call gc_slot ( sc_slot2 : "none")

                        2. setting gc_slot to sc_slot1
                           (we defined sc_slot1: "fov_desired 90")

                        3. +se_slot1("none")

                        4. sa_slot1 ("slot1; fov_desired 75;")
                        
        releasing 1 ->  1. -se_slot1 ("none")

        pressign  3 ->  1. call gc_slot (sc_slot1:"fov_desired 90")
                          //yay, just bu switching away from slot 1 
                          //we reset our fov

                        2. settign gc_slot to sc_slot3 ("none")

                        3. +se_slot3("none")

                        4. sa_slot3 ("none")

        releasing 3 ->  1. -se_slot3("none")

Comment: When using mode shifting, the same callback alias `gc_<group_name>` will be used acros mode shift, meaning that switching from `slot1_pa` to `slot1` will call `sc_slot1_pa`. This behaviour maybe subject to change. If you have a request, feel free to write me.

So now you have basic understaning of how to work with TF2-EasyScript, what now? Now you play, write scripts, download scripts and just enjoy your new controlls. Invert medigun attack function, make quickbuild script for engi or randomized disguise for spy. You have all the freedom and one of the most powerfull api and your disposal. Go nuts!