---
name: conventional-commit
description: Write a conventional-commit message for a set of changes — type(scope) subject plus an optional description that lets a future agent understand the change. Use when asked to commit, to draft a commit message, or when a diff needs to be turned into history a future reader can trust.
---

# Conventional Commit

Turn a diff into history: `type(scope): subject` plus enough description for a future agent to understand the coherent change.

## Workflow

1. **Read the actual change.** `git diff --staged` (or the named files) — never write a message from the task description alone.
2. **Pick one type.** feat / fix / refactor / docs / test / chore / perf. Mixed changes = split the commit, not the type.
3. **Subject line.** Give the staged change a concise, distinguishable name: `fix(mcp): skip sse entries when importing codex config`. Wording is free; accuracy and recognizability matter more than a sentence template.
4. **Body.** Add a description when the subject alone does not carry enough context. Summarize the outcome and intent of the change, plus constraints, verification, migration, or risk when they matter. Use as much text as the change needs.
5. **Footer** only for real metadata: `BREAKING CHANGE:`, issue refs, co-authors.

## Anti-patterns

- Do not write `fix: fix bug` / `chore: update code` — a subject that could describe any commit gives a future agent no name for this change.
- Do not list every touched file in the body; name the semantic change once.
- Do not commit unrelated changes together to avoid writing two messages.

## Done when

Someone reading `git log --oneline` a year later can identify the coherent change, and the full message carries enough context for a future agent to understand it.
