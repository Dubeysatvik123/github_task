#!/bin/bash
echo "Number of lines are in your file."
read -p " enter the filename: " file

if [[ -f "$file" ]]; then
	echo "No. of lines in  '$file' has $(wc -l < "$file") lines."
else
    echo " '$file'Not exists"
fi

