#!/usr/bin/env -S just --justfile
# this shebang allows the justfile to be executed with `./justfile`.

# list available recipes
default:
    @just --list

# run static checks
check: check_shell check_nix

# format code
fmt: fmt_just fmt_nix

# shellcheck all shell scripts in the `scripts/` directory
check_shell:
    @find scripts -type f -name '*.sh' | xargs shellcheck

# check Nix flake
check_nix:
    @nix flake check --all-systems 2> /dev/null

# format justfile
fmt_just:
    @just --unstable --fmt 2> /dev/null

# format Nix code
fmt_nix:
    @nix fmt 2> /dev/null

# install the Nix package manager globally
install_nix:
    @./scripts/install_nix.sh

# ensure all PROGRAMS are installed via Nix
detect_installed_programs +PROGRAMS:
    -@./scripts/detect_installed_programs.sh {{ PROGRAMS }}
