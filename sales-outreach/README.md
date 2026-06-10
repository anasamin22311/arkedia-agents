# 📣 Sales & Outreach — Arkedia Client-Acquisition Agent

The third member of your AI team. It runs cold-and-warm client acquisition for Arkedia: researching real prospects, building **sourced** client dossiers, and writing the actual messages (LinkedIn DMs, emails, follow-ups) you send under your own name.

## Why it exists
The previous consultant produced robotic, generic, tech-dump messages you had to reject five times each. This agent's whole job is to fix that. It writes like a credible founder reaching out to a peer, and it **runs its own quality self-check before showing you anything** — so you stop getting 2/10 drafts.

## The two laws
1. **The Message Formula (order is fixed):** ① where I found you → ② one real, researched pain in plain English → ③ one quiet why-us line (≤1 tech token) → ④ a bounded soft ask. No curt openers, no buzzword soup, no "open to a chat?".
2. **Truth-first:** never invent a client, metric, email, or source. The **honesty canon** is absolute (banned overclaims listed). Facts are sourced and tiered; messages are labeled COMPOSED.

## Folder layout (matches the other team agents)
```
sales-outreach/
├── SYSTEM_PROMPT.md         # the brain — the two laws + the self-check rubric
├── README.md                # this file
├── knowledge/
│   ├── arkedia-facts.md     # single source of truth (contradictions resolved)
│   ├── honesty-canon.md     # banned overclaims — the override authority
│   ├── message-playbook.md  # the formula + the real bad-vs-good canon
│   ├── pitch-angles.md      # the 3 reusable angles, pain-first
│   └── email-patterns.md    # how to verify + tier emails (live patterns stay private)
├── skills/
│   ├── research-prospect/   # sourced research + where-found hook + tiered email
│   ├── write-message/       # THE fix: formula + self-check before showing you
│   ├── humanize-outreach/   # final pass: cut adjectives/buzzwords/dead sentences, founder voice
│   ├── build-dossier/       # bilingual sourced HTML dossier (a real one is the gold standard)
│   └── track-pipeline/      # stages, dated next actions, drop dead threads
├── templates/               # account-profile, message-set, pipeline-board
├── accounts/                # one folder per live prospect (sourced)
├── pipeline/pipeline.md     # the LIVE board (seeded from handover)
├── _handover/               # curated extract from the previous consultant (read-only reference)
└── output/                  # one-off deliverables
```

## How to use it
1. **Start the agent** by loading `SYSTEM_PROMPT.md` (or: "Act as Sales & Outreach using E:\Work\Team\agents\sales-outreach\SYSTEM_PROMPT.md").
2. **Give it work**, e.g.:
   - "Write the [person] / [company] LinkedIn connection note." → it returns one message that already passed the self-check, plus a one-line angle note.
   - "Research [person] at [company] and draft a first-touch." → sourced profile + message.
   - "Build a full dossier on [company], same depth as the reference dossier." → bilingual sourced HTML.
   - "Update the pipeline and tell me the #1 action today."
3. It keeps live state in `pipeline/` and `accounts/`, all sourced.

## What's already loaded
- **Arkedia's real, verified facts** (CR 7040606969, `anas@arkedia.dev`, 25+ specialists, the 10 client-owned portfolio projects) with old contradictions resolved.
- **The honesty canon** (APS is not in production, no Aramco-proximity framing, the 4 real legal docs, no em dashes, NDA/cyber only after a reply).
- **The bad-vs-good message canon** from your own history, so the tone is locked in.
- **The live pipeline**, seeded from the handover: every thread has a dated next action, and dormant threads are flagged as drop candidates.

## Guardrails
- Never shows you a message that fails its own rubric.
- Never invents emails — verifies and tiers them (🟢/🟡/🔴).
- Recommends ONE message, not five options, unless you ask.
- Tells you the truth: dead threads get dropped, weak targets get flagged.

---
*Agent #3 of the Arkedia AI team. Siblings: `video-director/`, `business-development-manager/`. The `_handover/` folder is the curated source material this agent was built on.*
