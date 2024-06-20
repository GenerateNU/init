#! /usr/bin/env sh

# Determine if user has root permissions.
if [ "$(id -u)" -eq 0 ]; then
    exit 0
else
    exit 1
fi