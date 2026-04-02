#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:-.claude/commands}"

mkdir -p "$TARGET"

count=0
for cmd in "$SCRIPT_DIR"/commands/*.md; do
  ln -sf "$cmd" "$TARGET/$(basename "$cmd")"
  count=$((count + 1))
done

echo "Installed $count commands into $TARGET"
