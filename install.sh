#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:-.claude/commands}"
# Agents live next to the commands dir: .claude/commands -> .claude/agents
AGENTS_TARGET="$(dirname "$TARGET")/agents"

mkdir -p "$TARGET" "$AGENTS_TARGET"

count=0
for cmd in "$SCRIPT_DIR"/commands/*.md; do
  ln -sf "$cmd" "$TARGET/$(basename "$cmd")"
  count=$((count + 1))
done

agents=0
for agent in "$SCRIPT_DIR"/agents/*.md; do
  ln -sf "$agent" "$AGENTS_TARGET/$(basename "$agent")"
  agents=$((agents + 1))
done

echo "Installed $count commands into $TARGET and $agents agents into $AGENTS_TARGET"
