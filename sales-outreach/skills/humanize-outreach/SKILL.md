---
name: humanize-outreach
description: Final humanizing pass on any outreach message (LinkedIn note, DM, InMail, email) before it is shown to Anas. Cuts adjectives, buzzwords, and dead sentences until the message reads like a founder typed it himself. Invoke as the LAST step after write-message, or whenever a draft feels robotic, salesy, or over-engineered.
---

# Skill: Humanize Outreach

Your job is NOT to write impressive messages. Your job is to get replies from busy executives. This pass strips out everything that sounds like a consultant and keeps only what a smart founder would actually type.

## The cut rules

When reviewing outreach, delete:
- **50% of adjectives**
- **50% of buzzwords**
- **50% of explanations**

If removing a sentence does not change the meaning, **remove it**.

Shorter is usually better. More human is always better.

## The tests (run all four)

1. **Anti-Claude test:** "Would Anas actually send this from his own LinkedIn account?" If no — rewrite, don't polish.
2. **Read-aloud test:** if a sentence sounds like a press release or a deck, say it the way you'd say it on a phone call, then write *that*.
3. **First-2-lines test:** an executive reads the first 2 lines and the last line. Is the value for *them* in the first 2 lines? Is the ask the last line?
4. **Reality test:** every claim provable today? "Guarantee", invented metrics, and demo-projects-cited-as-deliveries fail this test.

## Swap table (apply on sight)

| Delete | Write instead |
|---|---|
| "I came across your insightful presentation" | "I saw your talk" |
| "We believe there may be strategic opportunities for collaboration" | "I think we can help" |
| "We deliver measurable outcomes" | "We build software that helps teams move faster" |
| "We have deep expertise in PropTech" | "We've worked on a couple of projects in that space" |
| "premium solutions", "world-class", "cutting-edge", "enterprise-grade", "best-in-class" | name the actual thing, plainly |
| "leverage", "synergies", "transformative", "strategic alignment", "digital transformation", "robust framework" | normal English or nothing |
| "open to a chat?" / "just let me know" | "Worth a short call next week?" |

## Procedure

1. Take the rubric-passing draft from `write-message`.
2. Apply the cut rules and swap table. Strip em dashes again (they creep back).
3. Run the four tests. Any failure → rewrite that line, re-run.
4. Re-check the channel limit after cutting (LinkedIn connection note ≤ 200 chars; report the exact count).
5. Hand Anas the humanized version only. Never show the pre-humanized draft alongside it unless he asks.
