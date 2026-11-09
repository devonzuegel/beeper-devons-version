# Maintaining this theme

- This repository is the canonical version of Devon’s Beeper CSS.
- Installed path on macOS: `~/Library/Application Support/BeeperTexts/custom.css`.
- Before an edit, compare the installed file with `custom.css`. Preserve and import any newer installed changes before proceeding; never overwrite them blindly.
- Make changes to repository `custom.css`, validate CSS syntax where tools are available, then use `scripts/install.sh` and reload CSS in Beeper.
- Make one descriptive Git commit per completed design change. Keep refactors separate from visual changes. Push completed changes to the existing origin when Devon authorizes saving/publishing them.
- Preserve light and dark appearances. Avoid layout shifts in selection states and changes to virtualized list row heights.
- Inspect current Beeper markup for uncertain selectors. Do not claim visual verification unless it was actually observed.
- Keep private chats, screenshots, app data, credentials, and machine-specific paths out of commits. Use fictional content for previews.
- Preserve icon attribution and third-party licenses. Do not substitute image symbols for unrelated attachment types.
