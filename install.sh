#! /usr/bin/env sh

# Base URL for raw files.
REPO_URL="https://raw.githubusercontent.com/GenerateNU/init/main"

# Full URLs.
GET_OS_URL="$REPO_URL/scripts/get_os.sh"
INSTALL_NIX_URL="$REPO_URL/scripts/install_nix.sh"
MAIN_URL="$REPO_URL/src/__main__.py"
CLI_URL="$REPO_URL/src/cli.py"
OPTIONS_URL="$REPO_URL/src/options.py"
TEMPLATES_URL="$REPO_URL/src/templates.py"
TREE_URL="$REPO_URL/src/tree.py"
UTILS_URL="$REPO_URL/src/utils.py"

# Make sure command exits if error detected.
check_exit_status() {
  if [ $? -ne 0 ]; then
    rm /tmp/install_nix.sh
    rm /tmp/get_os.sh
    exit 1
  fi
}

# Download and run the Nix installation script.
curl -L $GET_OS_URL -o /tmp/get_os.sh
curl -L $INSTALL_NIX_URL -o /tmp/install_nix.sh
chmod +x /tmp/get_os.sh
chmod +x /tmp/install_nix.sh
./tmp/install_nix.sh
check_exit_status

# Download scripts to run CLI.
curl -L $MAIN_URL -o /tmp/__main__.py
curl -L $CLI_URL -o /tmp/cli.py
curl -L $OPTIONS_URL -o /tmp/options.py
curl -L $TEMPLATES_URL -o /tmp/templates.py
curl -L $TREE_URL -o /tmp/tree.py
curl -L $UTILS_URL -o /tmp/utils.py
chmod +x /tmp/__main__.py
./tmp/__main__.py

# Clean up files.
rm /tmp/install-nix.sh
rm /tmp/get_os.sh

rm /tmp/__main__.py
rm /tmp/cli.py
rm /tmp/options.py
rm /tmp/templates.py
rm /tmp/tree.py
rm /tmp/utils.py

rm -rf __pycache__