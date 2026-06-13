# 🔍 PR Reviewer - Arkedia AI Code-Review Agent

Reviews every pull request to your protected branch BEFORE it reaches the human lead, in the lead engineer's own voice and against the team's own coding rules. It is the quality gate that lets a small team ship AI-written code without the lead reading every line.

## Why it exists
However strong your prompts, an AI coding assistant writes code that runs but ignores your conventions: naming, layer boundaries, state rules, authorization, performance. Someone has to catch that before merge. That used to be the human lead, on every PR. This agent is that reviewer now, holding the same bar automatically.

## How it works
```
GitHub PR (opened/updated)
  -> webhook -> server.py pulls the diff
  -> Claude Code CLI reviews it with the lead-engineer system prompt + your team's rules
  -> posts APPROVE / REQUEST_CHANGES / COMMENT back on the PR
  -> optional auto-merge on a clean APPROVE
```

## Folder layout (matches the other team agents)
```
pr-reviewer/
├── SYSTEM_PROMPT.md   # the agent's brain - the persona + the one law
├── README.md          # this file
├── Dockerfile         # the container (Claude CLI + Flask)
├── src/
│   └── server.py      # the webhook server: diff -> review -> post back
└── knowledge/
    └── setup.md       # how to deploy it and adapt the rules to your stack
```

## Make it yours
The rule set in `src/server.py` is an EXAMPLE (a .NET 9 + Angular 20 stack). To make this YOUR reviewer, rewrite the `SYSTEM_PROMPT` rules for your stack (or load them from a `BUSINESS_CONTEXT.md`), and make the persona your real lead's voice. See `knowledge/setup.md`.

## Secrets
All via environment variables, never in the repo: `GITHUB_TOKEN`, `WEBHOOK_SECRET`, the Claude OAuth token, `TARGET_BRANCH`. See `knowledge/setup.md`.

---
*Part of the Arkedia AI agent team. Built in public under #ArkediaToolbox.*
