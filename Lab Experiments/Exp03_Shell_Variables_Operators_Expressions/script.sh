#!/bin/bash 
echo -n "Enter first number : " 
read a 
echo -n "Enter second number: " 
read b 
echo "---- Arithmetic Operators ----" 
echo "Sum        = $((a + b))" 
echo "Difference = $((a - b))" 
echo "Product    = $((a * b))" 
echo "Quotient   = $((a / b))" 
echo "Remainder  = $((a % b))" 
echo "---- Relational Operators ----" 
[ $a -gt $b ] && echo "$a is greater than $b" 
[ $a -lt $b ] && echo "$a is less than $b" 
[ $a -eq $b ] && echo "$a is equal to $b" 
echo "---- Expression ----" 
result=$(( (a + b) * 2 - a / b )) 
echo "(a + b) * 2 - a / b = $result"
