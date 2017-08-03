# FanciestBanana's  ultimate script framework
For quick programming guide scroll to the bottom.

## Description

This framework is meant to be a starting point for scripters as well as 
a base for sharing scripts.It follows Model-View-Controller, 
where model is a script/command, view is users input and 
framework itself plays the role of controller

## Contribution
You are welcome to contribute to this project.  
Either create an issue or submit a commit.  
You can also discuss this script at Reddit.  

## How to use:  

#### Users:  
1. Navigate to your TF2 cfg folder.  
    -  Example: `C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\cfg`
2. Copy the contents of `/output/*` into TF2 cfg folder  
3. If you hadn't already, create `autoexec.cfg`. This file will be executed  
        at every launch.  
4. In `autoexec.cfg` write on first line `exec framework.cfg`.  
        This will execute framework script at every launch.  
5. In `framework.cfg` navigate to `Default bindings` section.  
        There you will find a bunch of bindings that ressemble default ones.  
        If you want to change binds, this is the place to do it.  
6.  (Advanced) If you happen to have `<class>.cfg` scripts that will use this framework,  
        then it should be executed first. This script should be followed by  
        `common.cfg` that would contain scripts for all classes, and then by text for  
        this specific class.  

#### Scripters  
This is a long one, so take a seat and drink your tea.  

This framework is a barrier between user and scripts. One side has easily identifiable binds,  
other side has script handles that are called on every button press.  
All the names are similar to default ones, with prefixes:  

* `u_`, user bindings, these are used to bind buttons to them.  
    Please note that every button is binded to `+u_` alias, even slot ones.
* `f*_` prefix is used internally and should not be used by anyone.
* `s*_` prefix is used by you, dear scripter and I hope it will help you.  

You are going to use 4 prefixes:  

1. `+se_`, which stands for "button press scipt event", this one is  
            triggered whenever user presses a corresponding button.  
2. `-se_`, just like previous one, this one is triggered at button release.
3. `sa_`, stands for "script action". If your script doesn't need 
            to use press/release event, this one should be used.
4. `sc_`, this is "script callback function". Functions in this script are  
                separated in groups (lateral movement, vertical movement, slots, contextual, functional),
                and each of these groups has a callback pointer.  
                Every time you press a button in one of these groups, a callback set  
                set by previous button will be called.
                Example:
```
press +u_slot1 |  no callback  | callback = sc_slot1
press +u_slot2 | call sc_slot1 | callback = sc_slot2
press +u_slot1 | call sc_slot2 | callback = sc_slot1
press +u_slot4 | call sc_slot1 | callback = sc_slot4
```
This is extremely usefull when, for example, you set `fov_desired 75`  
for ambassador and for the rest you want to switch it back to `90`.


And one more thing, no need to bother with quickswitch and spectator commands, they are already included in framework.

#### 1.1 Update
In this update i've added a bunch of usefull aliases that you may use in your script.  
They are found in the `Default aliases` section.  

I've also added universal modifiers to the recipy, for example:

        +u_mod_pa

will replace every `sa_alias` with `sa_alias_pa`.
There are 3 types of modifiers:
* `p` modifiers, they modify the values as long as they are pressed  
* `t` are toggle modifiers, first press activates them, second press deactivates
* `s` are sticky modifiers, they are deactivated after any key they affect was pressed
Implemented modifiers are:
- pa
- pb
- ta
- tb
- sa
- sb

#### 1.1.1 Update
Buit in Null-canceling movement script, because it is usefull without altering any functionality

# Quick programming guide.  
In `<class>.cfg`:
Call this script at the beginning, then write your code.

All handles have default names with prefixes `+se_`, `-se_`, `sa_`, `sc_`. (see above for explanaton)  

Assigning movement:  
```
alias +se_forward +forward;
alias -se_forward -forward;
```

Weapon specific fov with easy reset:

```
    alias sa_slot1 "fov_desired 75; slot1"
    alias sc_slot1 "fov_desired 90" //will be called when switching AWAY FROM slot1
```

### list of implemented aliases
For the list of implemended aliases please look in `framework.cfg`,  
because this list is too long for me to update here