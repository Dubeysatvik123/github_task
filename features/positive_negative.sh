#!/bin/bash 
read -p "Enter any number" n
if [[ $n -gt 0 ]]; then
    echo "The number $n is positive."
elif [[ $n -lt 0 ]]; then
    echo "The number $n is negative."
else
    echo "The number is zero."
fi
