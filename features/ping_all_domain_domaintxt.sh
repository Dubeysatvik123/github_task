#!/bin/bash
echo "Ping the domains"
read -p "Enter the file name" file
if [[ ! -f "$file" ]]; then
	echo "file not exists"
fi
for i in $(cat "$file"); do
  
    if [[ -z "$i" ]]; then
        continue
    fi

    echo "Pinging $i..."
    ping -c 1 "$i" &> /dev/null

    if [[ $? -eq 0 ]]; then
        echo "$i is reachable "
    else
        echo "$i is not reachable "
    fi
done
echo "All done!"
