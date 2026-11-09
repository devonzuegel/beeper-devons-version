#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_css=${1:-"$repo_dir/custom.css"}
target_dir="$HOME/Library/Application Support/BeeperTexts"
target_css="$target_dir/custom.css"

if [ ! -f "$source_css" ]; then
  printf 'Stylesheet not found: %s\n' "$source_css" >&2
  exit 1
fi
if [ ! -d "$target_dir" ]; then
  printf 'Beeper settings folder not found: %s\n' "$target_dir" >&2
  exit 1
fi
if [ -f "$target_css" ] && cmp -s "$source_css" "$target_css"; then
  printf 'Beeper already has this stylesheet. Click Reload CSS to apply it.\n'
  exit 0
fi
if [ -e "$target_css" ]; then
  backup_dir="$target_dir/custom-css-backups"
  mkdir -p "$backup_dir"
  backup_file=$(mktemp "$backup_dir/custom-$(date +%Y%m%d-%H%M%S).XXXXXX")
  cp "$target_css" "$backup_file"
  printf 'Backed up previous CSS to %s\n' "$backup_file"
fi
cp "$source_css" "$target_css"
printf 'Installed theme. In Beeper, click Settings → Appearance → Reload CSS.\n'
