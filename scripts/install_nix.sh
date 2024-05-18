#!/usr/bin/env sh

# Installs the Nix toolchain.
install_nix() {
  yes | curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
}

# Install the Nix toolchain on supported systems.
case "$(./"$(dirname "$0")"/get_os.sh 2> /dev/null)" in
  "LINUX")
    printf "Detected OS: Linux\n"
    ;;
  "WSL")
    printf "Detected OS: WSL\n"
    ;;
  "MACOS")
    printf "Detected OS: macOS\n"
    ;;
  *)
    printf "\033[31;1merror\033[0m: unsupported OS\n"
    exit 1
    ;;
esac

if install_nix; then
  printf "\033[32;1mNix installation successful\033[0m\n"
  exit 0
else
  printf "\033[31;1mNix installation failed\033[0m\n"
  exit 1
fi
