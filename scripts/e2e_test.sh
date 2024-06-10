#!/bin/bash

if [ $# -lt 1 ]; then
  REPO_NAME="test-repo"
else
  REPO_NAME=$1
fi

SCRIPTS_DIR="$(dirname "$0")"
chmod +x "$SCRIPTS_DIR"/simulate_cli.exp
./"$SCRIPTS_DIR"/simulate_cli.exp $REPO_NAME

if [ -d "$REPO_NAME" ]; then
  echo "E2E test passed"
  exit 0
else
  echo "E2E test failed"
  exit 1
fi