#!/bin/bash
echo "Listing top 10 processes with high memory"
ps aux --sort -%mem | head -n 6
