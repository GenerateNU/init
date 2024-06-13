#!/bin/bash

SCRIPTS_DIR="$(dirname "$0")"
chmod +x "$SCRIPTS_DIR"/simulate_cli.exp
./"$SCRIPTS_DIR"/simulate_cli.exp $REPO_NAME

if [ ! -d "$REPO_NAME" ]; then
  echo "E2E test failed. $REPO_NAME directory does not exist"
  exit 1
fi

cd "$REPO_NAME"

EXPECTED_OBJECTS=(
  # root files
  "flake.nix"
  "LICENSE"
  ".gitignore"
  "README.md"

  # .github
  ".github/workflows"
  ".github/pull_request_template.md"

  # backend
  "backend/src"

  # frontend
  "frontend/src"
  "frontend/public"
)

check_objects_exist() {
  local all_exist=true
  for obj in "${EXPECTED_OBJECTS[@]}"; do
    if [ ! -e "$obj" ]; then
      echo "Missing $obj"
      all_exist=false
    fi
  done

  if $all_exist; then
    echo "E2E test passed"
    exit 0
  else
    echo "E2E test failed"
    exit 1
  fi
}

check_objects_exist