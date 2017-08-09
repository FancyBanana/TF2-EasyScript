## 1.0  

 * First release.
 * Compiler written in ruby.

## 1.1

 * Added mode shifting

## 1.1.1 

 * Renamed to TF2-EasyScript
 * Added a proper readme and a small tutorial

## 1.2

 * Removed 'sa_' aliases because of redundancy.
   * The reason behind this change is to sinplify the usage. 'sa_' and '+se_' where called in the same place, essentially making them redundant. The role of 'sa_' was to provide the 'key pressed and released' type of functionality, but there is no reason to not to use '+se_' since they are functionally identical.   
   * This makes scripts for previous version incompatible. Sorry for inconvinience.
   * Every function aiased to sa_<func_name> is now aliased to +se_<func_name>

## 1.2.1

 * Bugfix: Fixed funky behaviour when usign invlast, invnext and invprev.