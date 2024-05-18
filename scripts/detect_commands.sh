#!/usr/bin/env sh

# Read in a list of commands to detect.
if [ $# -gt 0 ]; then
  commands=("$@")
else
  read -ra commands
fi

# Search for each command.
missing=false
for command in "${commands[@]}"; do
  if command -v "$command" 1> /dev/null 2>&1; then
    printf "\033[32;1m%s detected\033[0m\n" "$command"
  else
    printf "\033[31;1m%s not detected\033[0m\n" "$command"
    missing=true
  fi
done

# Fail if any commands are missing.
if $missing; then
  exit 1
else
  exit 0
fi