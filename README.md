# Arkedia AI Agent Team · #ArkediaToolbox

Anas, founder of [Arkedia](https://arkedia.dev), is building an AI agent team that runs the studio's operations, and publishing it in public, one agent at a time.

There is no framework and no code here. **Each agent IS a folder:** a system prompt (the brain), a knowledge base (verified facts and rules), skills (when and how each behavior runs), and templates. You run it by loading the folder into Claude.

بالعربي: ده فريق الـ AI agents اللي بيدير شغل Arkedia. كل agent عبارة عن فولدر فيه system prompt ومعرفة و skills. مفيش كود، الفولدر نفسه هو الـ agent.

## Published so far

### `sales-outreach/` (Day 1)
The client-acquisition agent. What makes it different is what it refuses to do:

1. No first message without a "where I found you" line and one researched pain.
2. No claim without a source. A banned-claims list (the honesty canon) overrides everything.
3. No email used before its pattern is verified across sources and confidence-tiered.
4. No draft reaches the operator before passing a self-check rubric; weak drafts get rewritten, not shown.

## Try it

Open a Claude session with this folder available and say:

> Act as Sales & Outreach using `sales-outreach/SYSTEM_PROMPT.md`.

Then give it work: "research [person] at [company] and draft a first-touch", "update the pipeline", "build a dossier on [company]". Each skill file in `sales-outreach/skills/` documents one behavior.

## What is intentionally NOT here

Live prospect data: `accounts/`, `pipeline/`, email patterns, and the internal handover. The method is public; the targets are private.

## Follow the series

Built in public under **#ArkediaToolbox** on LinkedIn. More agents (video director, BD manager, social media) get published as the series continues.
