Siyl
====

 Sqli In Your Log. Simple SQLi deobfuscation in your logs

Siyl could, url decode, char decode and pipe clean any log file.

Usage :
Piped  : zcat mylogs.gz | Siyl -p
Direct : Siyl -i [FILE]

Switches:
 -h for Help
 -p for PipeMode or -i [FILE] for Filemode
 -j : Disable '||' joining
 -c : Disable chr(xx) decoding
 -u : Disable URL decoding

