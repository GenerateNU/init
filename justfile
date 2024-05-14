#!/usr/bin/env -S just --justfile
# this shebang allows the justfile to be executed with `./justfile`.

# list available recipes
default:
  @just --list

# run static checks
check: shellcheck

# check all shell scripts in the `scripts/` directory
shellcheck:
  find scripts -type f | xargs shellcheck

# install the Nix package manager globally
install_nix:
  ./scripts/install_nix.sh

# ensure all PROGRAMS are installed via Nix
check_installed_programs +PROGRAMS:
  ./scripts/check_installed_programs.sh {{PROGRAMS}}