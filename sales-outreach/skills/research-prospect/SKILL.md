---
name: research-prospect
description: Research a real prospect before any outreach - find the person and role, a public "where I found you" hook, the one real pain their role owns right now, and the verified email pattern with a confidence tier, capturing everything with sources. Invoke when the operator names a new target, says "research X", "who should I contact at Y", or before writing any first-touch message.
---

# Skill: Research a Prospect (sourced, before any message)

No message is written without this. The output feeds `write-message` and `build-dossier`.

## What to produce
1. **The person & role** — name, exact title, seniority, which buying role (economic buyer / technical evaluator / champion / blocker).
2. **The "where I found you" hook** — a specific public artifact you can name in the opener: a keynote, interview, signed MoU, product launch, hiring spree, conference talk. This is non-negotiable; without it the message can't open correctly.
3. **The one real pain** — the single problem this role owns *right now*, tied to a trigger event (funding, new exec, legacy pain, expansion, compliance deadline, a stated initiative). Map it to a pitch angle.
4. **Email pattern + tier** — verify via RocketReach/SignalHire/Hunter previews, cross-check one initial vs ZoomInfo (see `knowledge/email-patterns.md`). Tier it 🟢/🟡/🔴. Never invent.
5. **Sources** — for every claim: URL + date accessed + a verbatim quote. Confidence HIGH/MEDIUM/LOW.

## Procedure
- Use WebSearch + WebFetch. Search the person's name + company, recent news, conference speaker pages, press releases, signed MoUs, interviews, LinkedIn activity.
- For the email: confirm the domain pattern from 3+ sources and at least one initial cross-check.
- Be honest: if you can only confirm a pattern (not a verbatim email), say PATTERN-CONFIRMED, not VERIFIED. If a pain is inferred, say so.
- **Save** to `accounts/<name>/profile.md` (use the account-profile template), with the sources section filled.

## Channel-order rule
For senior KSA enterprise buyers: **LinkedIn connection request first**, then (if accepted or after a beat) email. Don't cold-blast email to a senior buyer.

## Quality bar
- A nameable where-found hook exists.
- Exactly one real pain identified and angle-mapped.
- Email tiered with sources, or explicitly "no reliable email yet."
- Every factual claim has a source + date + quote.

## Output
`accounts/<name>/profile.md` — ready for `write-message` (quick outreach) or `build-dossier` (serious target).
