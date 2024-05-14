#!/usr/bin/env sh

install_nix_mac() {
    echo "Installing Nix for macOS"
    set -o pipefail
    yes | curl -sL https://nixos.org/nix/install | sh -s > /dev/null 2>&1
    return $?
}

install_nix_linux() {
    echo "Installing Nix for Linux"
    set -o pipefail
    yes | curl -sL https://nixos.org/nix/install | sh -s -- --daemon > /dev/null 2>&1
    return $?
}

install_nix_wsl() {
    echo "Installing Nix for WSL"
    set -o pipefail
    yes | curl -sL https://nixos.org/nix/install | sh -s -- --daemon > /dev/null 2>&1
    return $?
}

is_wsl() {
    test -f /proc/sys/fs/binfmt_misc/WSLInterop
}

case "$(uname -s)" in
    Linux*)
        if is_wsl; then
            echo "Detected WSL"
            install_nix_wsl
        else
            echo "Detected Linux"
            install_nix_linux
        fi
        ;;
    Darwin*)
        echo "Detected macOS"
        install_nix_mac
        ;;
    *)
        echo "Unsupported OS"
        exit 1
        ;;
esac

if [ $? -eq 0 ]; then
    echo "Installation successful"
    exit 0
else
    echo "Installation failed"
    exit 1
fi
