#!/bin/bash

# Check if a commit message is provided
if [ -z "$1" ]; then
  echo "Commit message is required"
  exit 1
fi

# Store the commit message
commit_message="$1"

# Execute Git commands
git add -A
git commit -m "$commit_message"
git push