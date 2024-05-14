#!/bin/bash

if [ $# -gt 0 ]; then
    programs=("$@")
else
    read -ra programs
fi

for program in "${programs[@]}"; do
    IFS='@' read -r name version <<< "$program"

    if [ -n "$version" ]; then
        if command -v "$name" >/dev/null && "$name" --version | grep -qF "$version"; then
            echo "$name $version is installed"
        else
            echo "$name $version is not installed"
            exit 1
        fi
    else
        if command -v "$name" >/dev/null; then
            echo "$name is installed"
        else
            echo "$name is not installed"
            exit 1
        fi
    fi
done

exit 0