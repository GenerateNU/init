#!/usr/bin/env sh

# base URL for raw files
GITHUB_REPO_URL="https://raw.githubusercontent.com/GenerateNU/init/main"

# Full URLs
GET_OS_URL="$GITHUB_REPO_URL/scripts/get_os.sh"
INSTALL_NIX_URL="$GITHUB_REPO_URL/scripts/install_nix.sh"
CLI_URL="$GITHUB_REPO_URL/cli/cli.py"
TEMPLATES_URL="$GITHUB_REPO_URL/cli/templates.py"
UTILS_URL="$GITHUB_REPO_URL/cli/utils.py"

# Make sure command exits if error detected
check_exit_status() {
  if [ $? -ne 0 ]; then
    rm install_nix.sh
    rm get_os.sh
    exit 1
  fi
}

# Download and run the Nix installation script
curl -L $GET_OS_URL -o get_os.sh 
curl -L $INSTALL_NIX_URL -o install_nix.sh
chmod +x get_os.sh
chmod +x install_nix.sh
./install_nix.sh
check_exit_status

# Download scripts to run cli
curl -L $UTILS_URL -o utils.py
curl -L $TEMPLATES_URL -o templates.py
curl -L $CLI_URL -o cli.py
chmod +x cli.py
./cli.py

# Clean up files
rm install-nix.sh
rm get_os.sh
rm cli.py
rm utils.py
rm templates.py
rm -rf __pycache__