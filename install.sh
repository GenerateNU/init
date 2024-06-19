#! /usr/bin/env sh

# base URL for raw files
REPO_URL="https://raw.githubusercontent.com/GenerateNU/init/main"

# Full URLs
GET_OS_URL="$REPO_URL/scripts/get_os.sh"
HAS_ROOT_PERMISSIONS_URL="$REPO_URL/scripts/has_root_permissions.sh"
INSTALL_NIX_URL="$REPO_URL/scripts/install_nix.sh"
CLI_URL="$REPO_URL/cli/cli.py"
TEMPLATES_URL="$REPO_URL/cli/templates.py"
UTILS_URL="$REPO_URL/cli/utils.py"

# Make sure command exits if error detected
check_exit_status() {
  if [ $? -ne 0 ]; then
    rm /tmp/install_nix.sh
    rm /tmp/get_os.sh
    exit 1
  fi
}

# Download and run the Nix installation script
curl -L $GET_OS_URL -o /tmp/get_os.sh
curl -L $HAS_ROOT_PERMISSIONS_URL -o /tmp/has_root_permissions.sh
curl -L $INSTALL_NIX_URL -o /tmp/install_nix.sh
chmod +x /tmp/get_os.sh
chmod +x /tmp/has_root_permissions.sh
chmod +x /tmp/install_nix.sh
./tmp/install_nix.sh
check_exit_status

# Download scripts to run cli
curl -L $UTILS_URL -o /tmp/utils.py
curl -L $TEMPLATES_URL -o /tmp/templates.py
curl -L $CLI_URL -o /tmp/cli.py
chmod +x /tmp/cli.py
./tmp/cli.py

# Clean up files
rm /tmp/install-nix.sh
rm /tmp/get_os.sh
rm /tmp/has_root_permissions.sh
rm /tmp/cli.py
rm /tmp/utils.py
rm /tmp/templates.py
rm -rf __pycache__