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
    rm install_nix.sh
    rm get_os.sh
    exit 1
  fi
}

# Download and run the Nix installation script.
cd /tmp
curl -L $GET_OS_URL -o get_os.sh
curl -L $INSTALL_NIX_URL -o install_nix.sh
chmod +x get_os.sh
chmod +x install_nix.sh
./install_nix.sh
check_exit_status

# Download scripts to run CLI.
curl -L $MAIN_URL -o __main__.py
curl -L $CLI_URL -o cli.py
curl -L $OPTIONS_URL -o options.py
curl -L $TEMPLATES_URL -o templates.py
curl -L $TREE_URL -o tree.py
curl -L $UTILS_URL -o utils.py
chmod +x __main__.py
./__main__.py

# Clean up files.
rm install-nix.sh
rm get_os.sh

rm __main__.py
rm cli.py
rm options.py
rm templates.py
rm tree.py
rm utils.py

rm -rf __pycache__