#!/bin/bash

if [ $# -eq 0 ]; then
	echo "Put an argument cuh"
	exit 1
fi
echo "Hello my name is $1"
