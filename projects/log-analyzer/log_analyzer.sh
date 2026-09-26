#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <logfile>" >&2
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: '$1' does not exist or is not a regular file" >&2
    exit 1
fi

total_lines=$(grep -cv '^[[:space:]]*$' "$1")
total_info=$(grep -c 'INFO' "$1")
total_warning=$(grep -c 'WARNING' "$1")
total_error=$(grep -c 'ERROR' "$1")

echo "Log report: $1"
echo "------------------------------"
echo "Total lines : $total_lines"
echo "INFO        : $total_info"
echo "WARNING     : $total_warning"
echo "ERROR       : $total_error"
