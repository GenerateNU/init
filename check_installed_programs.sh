#!/bin/bash

if [ $# -gt 0 ]; then
    programs=("$@")
else
    read -ra programs
fi

missing=false

for program in "${programs[@]}"; do
    if nix-env -q "$program" > /dev/null 2>&1; then
        echo "$program is installed in the current Nix profile"
    else
        echo "$program is not installed in the current Nix profile"
        missing=true
    fi
done

if $missing; then
    exit 1
else
    exit 0
fi
