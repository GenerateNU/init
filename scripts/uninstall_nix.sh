#! /usr/bin/env sh

# Uninstalls the Nix toolchain using the Determinate Systems installer.
uninstall_nix() {
  yes | /nix/nix-installer uninstall
}

# Ensure root permissions.
if ! ./"$(dirname "$0")"/has_root_permissions.sh; then
    printf "\033[31;1merror\033[0m: root permissions required\n"
    exit 1
fi

if uninstall_nix; then
  printf "\033[32;1msuccess\033[0m: uninstalled Nix\033[0m\n"
  exit 0
else
  printf "\033[31;1merror\033[0m: failed to uninstall Nix\n"
  exit 1
fi
