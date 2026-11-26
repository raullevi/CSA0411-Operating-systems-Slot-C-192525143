#!/usr/bin/env bash
# IMPLEMENTATION OF COMMAND PIPELINES, INPUT REDIRECTION, AND OUTPUT REDIRECTION
set -euo pipefail

echo "Arun 78" > marks.txt 
echo "Bala 92" >> marks.txt 
echo "Kavi 65" >> marks.txt 
echo "Divya 88" >> marks.txt 
cat marks.txt 
wc -l < marks.txt 
sort -k2 -n -r < marks.txt 
sort -k2 -n -r marks.txt | head -2 
grep "a" marks.txt | wc -l 
cut -d' ' -f1 marks.txt | sort > names.txt 
cat names.txt 
ls nofile.txt 2> error.log 
cat error.log
