#!/usr/bin/env sh

# Ensure 'nix' command is installed. You can't install Nix packages without Nix!
if ! ./"$(dirname "$0")"/detect_commands.sh "nix" 1> /dev/null 2>&1; then
  printf "\033[31;1merror\033[0m: 'nix' command not detected. Please install Nix\n"
  exit 1
fi

# Read in a list of programs to detect.
if [ $# -gt 0 ]; then
  programs=("$@")
else
  read -ra programs
fi

# Search for each program in the Nix store.
missing=false
for program in "${programs[@]}"; do
  if find /nix/store -mindepth 1 -maxdepth 1 -type d -name "*-$program-*" -print -quit | grep -q . 1> /dev/null 2>&1; then
    printf "\033[32;1m%s detected\033[0m\n" "$program"
  else
    printf "\033[31;1m%s not detected\033[0m\n" "$program"
    missing=true
  fi
done

# Fail if any programs are missing.
if $missing; then
  exit 1
else
  exit 0
fi