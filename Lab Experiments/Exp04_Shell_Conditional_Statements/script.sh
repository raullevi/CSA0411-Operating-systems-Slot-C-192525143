#!/bin/bash 
echo -n "Enter the mark (0-100): " 
read mark 
if [ $mark -ge 90 ]; then 
    echo "Grade: S" 
elif [ $mark -ge 75 ]; then 
    echo "Grade: A" 
elif [ $mark -ge 50 ]; then 
    echo "Grade: B" 
else 
    echo "Grade: Fail" 
fi 
  
echo -n "Enter a number: " 
read n 
if [ $((n % 2)) -eq 0 ]; then 
    echo "$n is Even" 
else 
    echo "$n is Odd" 
fi 
  
echo -n "Enter day number (1-7): " 
read d 
case $d in 
    1) echo "Sunday" ;; 
    2) echo "Monday" ;; 
    3) echo "Tuesday" ;; 
    4) echo "Wednesday" ;; 
    5) echo "Thursday" ;; 
    6) echo "Friday" ;; 
    7) echo "Saturday" ;; 
    *) echo "Invalid day number" ;; 
esac
