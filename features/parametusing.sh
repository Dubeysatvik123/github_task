#!/bin/bash

echo "Script: $0"
echo "First : $1"
echo "Second : $2"
echo "Third : $3"

echo "Number of parameters passed: $#"
echo "All parameters (\$@): $@"
echo "All parameters (\$*): $*"


if [ $# -lt 2 ]; then
  echo "Usage: $0 param1 param2 [param3 ...]"
  exit 1
fi


sum=$(( $1 + $2 ))
echo "Sum of first two parameters: $sum"

