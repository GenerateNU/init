#! /usr/bin/env sh

# Installs the Nix toolchain using the Determinate Systems installer.
install_nix() {
  yes | curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
}

# Ensure root permissions.
if [ "$(id -u)" -ne 0 ]; then
    printf "\033[31;1merror\033[0m: root permissions required\n"
    exit 1
fi

# Install the Nix toolchain on supported systems.
case "$(./"$(dirname "$0")"/get_os.sh 2> /dev/null)" in
  "LINUX")
    printf "\033[36;1minfo\033[0m: detected Linux\n"
    ;;
  "WSL")
    printf "\033[36;1minfo\033[0m: detected WSL\n"
    ;;
  "MACOS")
    printf "\033[36;1minfo\033[0m: detected macOS\n"
    ;;
  *)
    printf "\033[31;1merror\033[0m: unsupported OS\n"
    exit 1
    ;;
esac

if install_nix; then
  printf "\033[32;1msuccess\033[0m: installed Nix\033[0m\n"
  exit 0
else
  printf "\033[31;1merror\033[0m: failed to install Nix\n"
  exit 1
fi
