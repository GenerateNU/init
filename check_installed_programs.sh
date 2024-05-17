#!/usr/bin/env sh

green='\033[0;32m'
red='\033[0;31m'
reset='\033[0m'

if ! command -v nix > /dev/null 2>&1; then
    echo "${red}Error: 'nix' command not found. Please install Nix.${reset}"
    exit 1
fi

if [ $# -gt 0 ]; then
    programs=("$@")
else
    read -ra programs
fi

missing=false

for program in "${programs[@]}"; do
    if find /nix/store -mindepth 1 -maxdepth 1 -type d -name "*-$program-*" -print -quit | grep -q .; then
        echo "${green}$program is installed in the Nix store${reset}"
    else
        echo "${red}$program is not installed in the Nix store${reset}"
        missing=true
    fi
done

if $missing; then
    exit 1
else
    exit 0
fi
