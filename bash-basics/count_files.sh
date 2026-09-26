#!/bin/bash

count=$(find . -type f | wc -l)
echo "This folder contains $count files"

