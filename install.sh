#!/usr/bin/env bash
# Installs the Fiper skills as personal Claude Code skills (~/.claude/skills),
# so they are available in every project via /fiper-brand, /fiper-landing-section, ...
set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)/skills"
dest="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
mkdir -p "$dest"

for dir in "$src"/*/; do
  name="$(basename "$dir")"
  rm -rf "${dest:?}/$name"
  cp -R "$dir" "$dest/$name"
  echo "installed /$name -> $dest/$name"
done
