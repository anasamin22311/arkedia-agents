---
name: write-message
description: Write a cold or warm outreach message (LinkedIn connection note, post-accept DM, cold email, or follow-up) for Anas to send, following the Message Formula and passing the self-check rubric BEFORE showing him. Invoke whenever the operator wants a message, DM, email, connection request, or follow-up written or fixed. This is the skill that fixes the "robotic 2/10 message" problem.
---

# Skill: Write a Message Anas Will Actually Send

The previous consultant produced templates Anas rejected repeatedly. This skill guarantees a message that passes his bar on the first try.

## Inputs you need (research first if missing)
- Who: the real person + role.
- **Where you found them:** a specific public hook (keynote, interview, signed MoU, launch, hiring post). If you don't have one, go get it (`research-prospect`) — do not write without it.
- **One real pain** they own (map to a pitch angle in `knowledge/pitch-angles.md`).
- Channel + limit (LinkedIn note ≤200 chars / DM / email / follow-up).

## Procedure
1. **Pick ONE pitch angle** that fits their visible situation. One pain, not three.
2. **Draft using the Message Formula** (`knowledge/message-playbook.md`):
   1) polite opener + where-I-found-you → 2) one real pain in plain English → 3) one quiet why-us line (≤1 tech token) → 4) bounded soft ask. Add 5-word founder identity if needed.
3. **Run the SELF-CHECK rubric** (from the system prompt). If it fails ANY line, rewrite. Do not show Anas a failing draft. The rubric:
   - opener names where you found them (no curt `Name —`)
   - exactly one real researched pain, plain English
   - ≤1 tech token total
   - ask is specific & bounded (not "open to a chat?")
   - no banned overclaims (scan `knowledge/honesty-canon.md`)
   - zero em dashes
   - sounds like a founder peer, not a vendor
   - fits the channel char limit
4. **Strip em dashes** explicitly on a final pass.
5. **Present to Anas:** the recommended message, then a one-line note:
   `COMPOSED — angle: <x>; where-found: <source>; pain source: <source>.`
   Offer alternatives ONLY if he asks. Do not dump 3–5 options.
6. **Save** the message into `accounts/<name>/messages.md` with its channel, char count, and status.

## Channel specifics
- **Connection note:** compress the formula to ≤200 chars (see the GOOD example in the playbook). Report the exact char count.
- **Post-accept DM:** 4–6 sentences, add ONE proof-of-delivery line, concrete next step.
- **Cold email:** benefit/pain subject line; tight body; signature (`anas@arkedia.dev`, `+966 56 385 3092`); attach ONLY the Arkedia Profile (no NDA/cyber on first touch).
- **Follow-up:** new value each time, never "just following up"; polite break-up after 2–3.

## Quality bar
- Passes every self-check line.
- Reads human, formal, founder-to-peer.
- One pain, one proof, one ask. No buzzword soup. No em dashes.
- Every claim sourceable; message labeled COMPOSED.

## Anti-patterns (auto-reject)
`Name —` curt opener · no where-found · 2+ tech tokens · "open to a chat?" · numbers brag ("36+ platforms") · presumptuous "the stack YOU signed" · any banned overclaim · any em dash.
