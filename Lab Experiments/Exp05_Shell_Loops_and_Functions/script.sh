#!/bin/bash 
factorial() { 
    local n=$1 f=1 
    while [ $n -gt 1 ]; do 
        f=$((f * n)) 
        n=$((n - 1)) 
    done 
    echo $f 
} 
  
is_prime() { 
    local n=$1 
    [ $n -lt 2 ] && return 1 
    for ((i = 2; i * i <= n; i++)); do 
        [ $((n % i)) -eq 0 ] && return 1 
    done 
    return 0 
} 
  
echo -n "Enter a number: " 
read num 
echo "Factorial of $num = $(factorial $num)" 
echo "Multiplication table of $num:" 
for i in 1 2 3 4 5; do 
    echo "$num x $i = $((num * i))" 
done 
echo -n "Prime numbers up to $num: " 
for ((k = 2; k <= num; k++)); do 
    is_prime $k && echo -n "$k " 
done 
echo
