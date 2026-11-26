#!/bin/bash 
while true; do 
    echo "===== SYSTEM ADMIN MENU =====" 
    echo "1. Show date and time" 
    echo "2. Show disk usage" 
    echo "3. Show memory usage" 
    echo "4. Show logged-in user" 
    echo "5. Show process count" 
    echo "6. Exit" 
    echo -n "Enter your choice: " 
    read ch 
    case $ch in 
        1) date ;; 
        2) df -h / | tail -1 ;; 
        3) free -m | grep Mem ;; 
        4) whoami ;; 
        5) echo "Running processes: $(ps -e --no-headers | wc -l)" ;; 
        6) echo "Exiting..."; break ;; 
        *) echo "Invalid choice" ;; 
    esac 
    echo 
done
