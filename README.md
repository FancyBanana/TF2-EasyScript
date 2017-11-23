# TF2 EasyScript
A scripting framework by /u/FanciestBanana  
A thank you for people contributing to this project: /u/Tvde1  

## Update 1.2 broke compatibility with previous version. Please read changelog. Older 1.1 version is still available. Sorry of inconvenience.

#### For quick programming guide scroll to the bottom.

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

 * ### Scripter's best friend!
   Most confusing and annoying necessities are taken care of!
   TF2-EasyScript has hooks for different button press events, callbacks for when pressing next button in a button group as well as built-in null-canceling movement script.   
   Lastinv, invnext, invprev, and spectator commands are already implemented.

 * ### Aliases for commands you didn't know existed!
   Call for an uber with single key press or instantly deploy a sentry. Or you can even use that taunt in the last slot that you hate to reach for...
 
 * ### Sharing scripts is never more complicated than drag'n'drop!
   Since all your script call TF2-EasyScript, it eliminates any need for changing your key binds

## How to install:  
1. Go to:  
     * [Releases](https://github.com/FancyBanana/TF2-EasyScript/releases) page on `GitHub`
and grab a `.zip` with latest release of TF2-EasyScript

1. Navigate to your TF2 cfg folder.  
    -  Example: `C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\cfg`

1. Copy the contents of the archive into TF2 cfg folder  

1. If you hadn't already, create `autoexec.cfg`. This file will be executed  
        at every launch.  

1. In `autoexec.cfg` write on first line `exec easyscript.cfg`    
        This will execute easyscript script at every launch.  

1. In `easyscript.cfg` navigate to `Default bindings` section.  
        There you will find a bunch of bindings that resemble default ones   
        If you want to change binds, this is the place to do it.

1.  (Advanced) If you happen to have `<class>.cfg` scripts they should call `exec easyscript.cfg` in the first line. This will reset all aliases to defaults as well unstick all keys. This framework is designed to clean up everything for you :).  

## How to use

##### For in-depth explanation on how to use TF2-EasyScript, please see `Wiki` section. (Coming soon)

#### Vocabulary
        function - a native command that when written in console executes some action
        alias - a user-defined command that may call function(s) and/or other alias(es)
        binding - act of connecting a key press to function or alias
        a binding - the connection of a button to a function or alias

It also should be noted that when a function or an alias with `+` prefix is bound to a key a function or an alias of the same name with prefix `-` is called on the release of the key, ex:

        bind w +forward

        pressing w down -> +forward is called
        releasing w     -> -forward is called

TF2-EasyScript consists of 4 files, but everything useful in conveniently located in `easyscript.cfg`, other 3 are purely technical.  

`easyscript.cfg` contains all key bindings, active and stubs for unused ones, and also aliases for voice commands, building stuff, destroying stuff, using eurika teleport, joining a class, joining a team, disguise for every combination of team/class, and lastly default functions for framework aliases that mirror buttons and shift modifiers.  
There's also a nifty script for showing console text on top of your HUD.

The main principle behind this framework is that every default function (and more) is mirrored, so instead of:  

        bind w +forward

we have 

        bind w +u_forward
        alias +se_forward +forward
        alias -se_forward -forward

There's quite a bit more code, but it allows for extreme flexibility.  
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
        -se_<function_name>  //keyup event alias

   that are used to call alias in user scripts. Please notice that all these are the same aliases name with different prefixes.

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
                           ("alias gc_attack sc_attack")

                           3. +se_attack called (+attack)

        releasing MOUSE1-> 1. -se_attack called (-attack)

Comment: attack key group has callback functionality, that's why you can define `sc_attack`, `sc_attack2` and `sc_attack3` to be called for consecutive key presses.

another example  
### Calling medic on `E`

what you write

        bind  E +u_callmed
        alias +se_callmed v_medic (v_medic is one of many 
                                  short-hand aliases in TF2-EasyScript)

and what happens when you press key

        pressing  E-> 1. +se_callmed (v_medic)

        releasing E-> 1. -se_callmed (nothing)

Pretty simple, right? How about something more complex:
### Mod shifting `E` to call for Uber

Here we will be using predefined `pa` (full name is `mod_pa`) modifier.  
There are 2 types of modifiers: `press` and `toggle`.  
`a` is a `press` modifier (**p**a), first by alphabetical order (p**a**). There are a total of 4 predefined modifiers:  
 * (`mod_`)`pa`
 * (`mod_`)`pb`
 * (`mod_`)`ta`
 * (`mod_`)`tb`

 when any modifier is active, every script alias "gains a suffix", that corresponds to modifier name ex:

        +se_callmed becomes +se_callmed_pa

you can add more (why would you need more?) by modifying source files and building the framework from source.

assuming the last example we need to write

        bind `MOUSE4` +u_mod_pa  //binding shift mode alias 

        alias +se_callmed_pa v_activateuber 

                        (again, this handy short-hand alias
                        for a voice command can be found in
                        `easyscript.cfg`)

And that's all! Now anytime you press `MOUSE4`+`E` you can annoy your medic to give you uber XD

And for the last topic:
### Callbacks

It's rather hard for me to describe what a callback is, so I will base my explanation on an example.

Let's say you play spy, your `fov_desired` is `90` by default but you want it to switch to `75` for your ambassador. So you need to switch to `75` when choosing `slot1`, and back to `90` when choosing anything else. The problem starts with *anything else* part. Normally you would need to include `fov_desired 90` into slots 2 to 10 to set fov to normal, but with TF2-EasyScript you need to do it only once for `slot1` callback, `sc_slot1`.

Assuming you are using default binds (`bind 1 +u_slot1`,etc...)  
We need to locate the default function for `+u_slot1`, which should be a combination of any of 4 script aliases. In this case it's 

        alias +se_slot1 "slot1"; (you can easily find this in easyscript.cfg)

We will override this to include desired functionality.

Now, for convenience we will create a spy.cfg, which will be automatically called when you change your class to spy.

Inside we write:

        exec easyscript.cfg //obligatory, will reset aliases and cleanup

        alias +se_slot1 "slot1; fov_desired 75" //now selecting slot1 will set your fov to 75

        alias sc_slot1 "fov_desired 90;"  //this will reset fov to normal when deselecting slot1


And this is it! Amazingly simple, isn't it? Normally it will take a lot more code to implement, and maintaining the code becomes more difficult the more you write (believe me, without bloody compiler this framework is huge pain in the bottom).

So now we will examine what happens when we press `2` then `1` then `3`:

        pressing 2  ->  1. call gc_slot (starting value
                           is sc_slot1; "fov_desired 90;")

                        2. setting gc_slot to sc_slot2 
                           (default: "none")

                        3. +se_slot2 ("slot2")

        releasing 2 ->  1. -se_slot2 ("none")
                        
        pressing  1 ->  1. call gc_slot ( sc_slot2 : "none")

                        2. setting gc_slot to sc_slot1
                           (we defined sc_slot1: "fov_desired 90")

                        3. +se_slot1 ("slot1; fov_desired 75;")
                        
        releasing 1 ->  1. -se_slot1 ("none")

        pressing  3 ->  1. call gc_slot (sc_slot1:"fov_desired 90")
                          //yay, just but switching away from slot 1 
                          //we reset our fov

                        2. setting gc_slot to sc_slot3 ("none")

                        3. +se_slot3("none")

        releasing 3 ->  1. -se_slot3("none")

Comment: When using mode shifting, the same callback alias `gc_<group_name>` will be used across mode shift, meaning that switching from `slot1_pa` to `slot1` will call `sc_slot1_pa`. This behavior maybe subject to change. If you have a request, feel free to write me.

So now you have basic understanding of how to work with TF2-EasyScript, what now? Now you play, write scripts, download scripts and just enjoy your new controls. Invert medigun attack function, make quickbuild script for engineer or randomized disguise for spy. You have all the freedom and one of the most powerful api and your disposal. Go nuts!
