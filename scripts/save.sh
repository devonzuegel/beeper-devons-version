#!/bin/sh
set -eu

if [ "$#" -ne 1 ] || [ -z "$1" ]; then
  printf 'Usage: ./scripts/save.sh "Describe the change"\n' >&2
  exit 1
fi
repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
installed_css="$HOME/Library/Application Support/BeeperTexts/custom.css"
if [ ! -f "$installed_css" ]; then
  printf 'Installed Beeper stylesheet not found.\n' >&2
  exit 1
fi
cd "$repo_dir"
# Do not import over uncommitted repository edits or include unrelated staged files.
if ! git diff --quiet -- custom.css || ! git diff --cached --quiet; then
  printf 'Commit or stash repository edits and staged files before importing installed CSS.\n' >&2
  exit 1
fi
if ! cmp -s "$installed_css" custom.css; then
  cp "$installed_css" custom.css
  git add -- custom.css
  git commit -m "$1" -- custom.css
else
  printf 'No CSS changes to commit.\n'
fi
git push
