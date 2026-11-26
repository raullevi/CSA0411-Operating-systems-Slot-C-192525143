#!/bin/bash 
# System information and resource monitoring report 
echo "========== SYSTEM INFORMATION ==========" 
echo "Host name      : $(hostname)" 
echo "Logged-in user : $(whoami)" 
echo "Kernel version : $(uname -r)" 
echo "Date and time  : $(date '+%d-%m-%Y %H:%M:%S')" 
echo "Uptime         : $(uptime -p)" 
echo "CPU cores      : $(nproc)" 
echo 
echo "========== MEMORY USAGE (MB) ==========" 
free -m 
echo 
echo "========== DISK USAGE ==========" 
df -h / | awk '{print $1, $2, $3, $4, $5}' 
echo 
echo "========== PROCESS COUNT ==========" 
echo "Running processes : $(ps -e --no-headers | wc -l)"
