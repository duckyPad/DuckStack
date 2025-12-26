#!/bin/bash

# If no arguments are provided, ask for a comment
if [[ $# -eq 0 ]]; then
    read -p "Enter a commit message: " commit_msg
    if [[ -z "$commit_msg" ]]; then
        echo "error: commit message cannot be empty"
        exit 1
    fi
else
    commit_msg="$*"
fi

# Cleanup temp and cache files
find . -type f -name "*.b#*" -exec rm -f {} \;
find . -type f -name "*.s#*" -exec rm -f {} \;
find . -type f -name "*.l#*" -exec rm -f {} \;
find . -type f -name "*.lck" -exec rm -f {} \;
find . -type f -name "*.csv#*" -exec rm -f {} \;
find . -type f -name "*.DS_Store*" -exec rm -f {} \;
find . -name "__pycache__" -exec rm -rf {} \;

find . -type f -name "main.exe" -exec rm -f {} \;
find . -type f -name "main" -exec rm -f {} \;
find . -type f -name "*.dsb" -exec rm -f {} \;
find . -type f -name "ppds.*" -exec rm -f {} \;
find . -type f -name "pyds.*" -exec rm -f {} \;

# Get current branch
current_branch=$(git rev-parse --abbrev-ref HEAD)

# Stage, commit, and push
git add --all
git commit -m "$commit_msg"
git push origin "$current_branch"