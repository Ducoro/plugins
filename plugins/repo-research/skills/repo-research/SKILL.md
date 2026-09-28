---
name: repo-research
description: Research a public GitHub repository through its AI-generated wiki (DeepWiki MCP) — map the doc structure, read relevant topics, ask targeted questions. Use to understand an unfamiliar repo's architecture, find where a feature lives, or see how another project solved a problem.
---

# Repo Research

Turn "what is this repo / how does it do X" questions into a short, sourced answer using the DeepWiki connector's three tools.

## Prerequisite

This skill uses the `deepwiki` MCP connector (`read_wiki_structure`, `read_wiki_contents`, `ask_wiki_question`). If those tools are unavailable, check `ducoro-cli mcp list --json` for an existing definition. With the user's authorization, add a missing definition and verify connectivity:

```sh
ducoro-cli mcp add --slug deepwiki --transport http --url https://mcp.deepwiki.com/mcp
ducoro-cli mcp probe deepwiki
```

If a definition already exists, probe it first and explain any connection failure. Follow the service's current authentication instructions if required; keep credentials in Ducoro's credential storage. Continue once the tools are available, and report missing access instead of inventing results.

## Workflow

1. **Map first.** Call `read_wiki_structure` with `repoName` (`owner/repo`). Skim the topic list to locate the 1–3 topics that plausibly answer the question.
2. **Choose the right depth.** For a focused question, call `ask_wiki_question` with `repoName` and `question`. For broader context, call `read_wiki_contents` with `repoName`; it returns repository-wide wiki content. Extract the relevant topics from that response.
3. **Ask targeted.** For questions that span topics ("where is rate limiting enforced?"), use `ask_wiki_question` with `repoName` and a single, specific `question`. One good question beats three vague ones.
4. **Answer with pointers.** Summarize in your own words and cite which wiki topics the claims came from, so the human can verify.

## Anti-patterns

- Do not clone or grep the repository when the wiki answers the question — that is this skill's whole point.
- Do not paste raw wiki dumps into the conversation; extract what the question needs.
- Do not guess `repoName` — confirm the exact `owner/repo` with the user if ambiguous.

## Done when

The question is answered in a few paragraphs, each load-bearing claim maps to a wiki topic you actually read, and unanswerable parts are named explicitly.
