---
name: pr-description
description: Write a pull-request description a reviewer can act on before reading the diff — what changed and why, how it was verified, what to look at first, known risks. Use when opening or updating a PR, or when asked to summarize a branch for review.
---

# PR Description

Give the reviewer a map before they enter the diff.

## Structure

1. **Why** (1–3 sentences): the problem or goal this PR exists for. Link the issue / Space when one exists.
2. **What changed**: the semantic changes as short bullets, grouped by subsystem — not a file list.
3. **How it was verified**: the exact commands run (tests, typecheck, manual steps) and their outcomes. Unverified parts are named as unverified.
4. **Review guide**: which file to start with, what is mechanical vs. load-bearing, any change a reviewer might mistake for a bug.
5. **Risk / rollout**: behavior changes, migrations, feature flags, revert plan — only when they exist; omit empty sections.

## Anti-patterns

- Do not restate the commit list as the description; the description is the aggregate story.
- Do not claim "tests pass" without naming which suite ran.
- Do not hide breaking changes in the middle of a bullet list — they lead the risk section.

## Done when

A reviewer who reads only the description can decide where to focus, how much to trust the verification, and what could break.
