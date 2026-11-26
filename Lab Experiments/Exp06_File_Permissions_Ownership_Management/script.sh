#!/usr/bin/env bash
# IMPLEMENTATION OF FILE PERMISSIONS AND OWNERSHIP MANAGEMENT IN LINUX
set -euo pipefail

touch report.txt 
mkdir project 
ls -l 
chmod u+x,g-r,o-r report.txt 
ls -l report.txt 
chmod 754 report.txt 
ls -l report.txt 
chmod 640 report.txt 
ls -l report.txt 
groupadd -f labgroup 
id -u student1 >/dev/null 2>&1 || useradd student1 
chown student1 report.txt 
chgrp labgroup report.txt 
ls -l report.txt 
chown -R student1:labgroup project 
ls -ld project 
stat -c "%n  %A  %a  %U  %G" report.txt
