# Changelog

## Unreleased

- Replace the ribbon’s generic WhatsApp handset with a recognizable duotone WhatsApp bubble badge.

- Bold the chat name inside the composer placeholder with an embedded contextual font; keep the prefix, network name, and actual drafts unchanged.

- Lighten the message composer placeholder without changing typed text.

- Remove unreliable removal press feedback: ordinary clicks unmount reactions before the effect can meaningfully play. Keep addition animations.

- Add shrink-and-fade press feedback when removing your own reactions. Remote removals remain immediate because Beeper unmounts them without an exit hook.

- Reduce reaction emoji to 16px, slightly smaller than the neighboring 18px avatars.

- Add a quick pop-in for newly appearing reaction emoji and reactor avatars, respecting reduced motion.

- Add a small top gap above the Custom CSS section title.

- Align settings section titles with the left edge of their controls and groups.

- Use pointer cursors for Custom CSS actions and bring Reset closer to Reload.

- Style clickable call entries with the same full-width, centered event card as call-ended notices.

- Align event cards with the outgoing bubble edge by laying their footer below the card instead of beside it.

- Improve avatar typing badges with slightly larger, higher-contrast dots and a soft blue tint.

- Restyle Custom CSS controls with compact labels, duotone icons, a primary Reload button, and a quieter Reset action.

- Fix the cramped active filter button with a soft tint, comfortable height, and a trailing dropdown cue.

- Add a tiny white inner rim to light-mode avatars while keeping their faint shadow.

- Move the Custom CSS heading and controls to the top of Appearance settings.

- Match filter, search, and compose toolbar buttons to the ribbon’s muted Lucide duotone icons.

- Try a faint shadow instead of the light-mode avatar border; retain the dark-mode rim.

- Add a pale grey inner rim to light-mode avatars, including reaction photos, without changing their size.

- Replace reaction pills with unframed emoji and compact photo-avatar groups, preserving overflow counts and marking your own reactions.

- Add a faint, layout-neutral inner border to avatars in dark mode.

- Hide the last pinned chat’s row divider, retaining the pinned-section divider.

- Preserve the native gap below event cards so surrounding spacing stays balanced.

- Expand event cards to the conversation width and center the icon, label, and inline time.

- Align call-summary cards with incoming messages and keep the time beside the event label.

## 0.1.0 — 2026-11-09

- Preserve Devon’s current Beeper stylesheet as the initial versioned baseline.
- Include the corrected centered notice styling for Signal’s “Call ended” notices.
- Add installation, backup, save-and-push, and rollback instructions.
- Add illustrative light / dark previews using fictional conversations.

Earlier iterations were developed before this repository existed. They are not represented as individual historical commits.
