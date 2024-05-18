#!/usr/bin/env sh

# Ensure at least one command was provided.
if [ $# -lt 1 ]; then
  printf "\033[31;1merror\033[0m: no commands provided\n"
  exit 1
fi

# Search for each command.
missing=false
for command in "$@"; do
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