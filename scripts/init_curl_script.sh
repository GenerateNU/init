#!/usr/bin/env sh

# Define the base URL for the GitHub repository
GITHUB_REPO_URL="https://raw.githubusercontent.com/GenerateNU/init/main"
GITHUB_NEW_URL="https://raw.githubusercontent.com/GenerateNU/init/create-executable"

# Define the script URLs
GET_OS_URL="$GITHUB_REPO_URL/scripts/get_os.sh"
INSTALL_NIX_URL="$GITHUB_REPO_URL/scripts/install_nix.sh"
CLI_URL="$GITHUB_NEW_URL/cli/cli.py"
TEMPLATES_URL="$GITHUB_NEW_URL/cli/templates.py"
UTILS_URL="$GITHUB_NEW_URL/cli/utils.py"


# Download and run the Nix installation script
# curl -L $GET_OS_URL -o get_os.sh
# curl -L $INSTALL_NIX_URL -o install-nix.sh
# chmod +x get_os.sh
# chmod +x install-nix.sh
# ./install-nix.sh
# rm install-nix.sh
# rm get_os.sh

# Download and run the Python script
curl -L $UTILS_URL -o utils.py
curl -L $TEMPLATES_URL -o templates.py
curl -L $CLI_URL -o cli.py
chmod +x cli.py
./cli.py
wait $!
rm cli.py
rm utils.py
rm templates.py
rm -rf __pycache__