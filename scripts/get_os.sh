#!/usr/bin/env sh

# Hacky way to determine if a Linux system is actually Windows Subsystem for Linux.
is_wsl() {
  test -f "/proc/sys/fs/binfmt_misc/WSLInterop"
}

# Print the name of the current operating system.
case "$(uname -s 2> /dev/null)" in
  "Linux")
    if is_wsl; then
      printf "WSL\n"
      exit 0
    else
      printf "LINUX\n"
      exit 0
    fi
    ;;
  "Darwin")
    printf "MACOS\n"
    exit 0
    ;;
  *)
    printf "UNKNOWN\n"
    exit 1
    ;;
esac