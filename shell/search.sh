#!/bin/bash

# Check if a keyword is provided
if [ -z "$1" ]; then
  echo "Usage: $0 target_keyword"
  exit 1
fi

target_keyword="$1"

# Use grep to recursively search for the keyword in the current directory
grep -r --color=auto --include='*' "$target_keyword" .
