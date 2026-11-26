#!/bin/bash 
CPU_LIMIT=80 
MEM_LIMIT=80 
  
cpu_usage() { 
    read -r _ u1 n1 s1 i1 _ < /proc/stat 
    sleep 1 
    read -r _ u2 n2 s2 i2 _ < /proc/stat 
    busy=$(( (u2 + n2 + s2) - (u1 + n1 + s1) )) 
    total=$(( busy + (i2 - i1) )) 
    [ $total -eq 0 ] && total=1 
    echo $(( 100 * busy / total )) 
} 
  
for check in 1 2 3; do 
    cpu=$(cpu_usage) 
    mem=$(free | awk '/Mem:/ {printf "%d", $3 * 100 / $2}') 
    echo "Check $check: CPU = ${cpu}%  Memory = ${mem}%" 
    if [ $cpu -gt $CPU_LIMIT ]; then echo "  WARNING: High CPU usage"; else echo "  CPU 
usage OK"; fi 
    if [ $mem -gt $MEM_LIMIT ]; then echo "  WARNING: High memory usage"; else echo "  
Memory usage OK"; fi 
done
