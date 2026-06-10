---
name: build-dossier
description: Build a full sourced client dossier as a bilingual self-contained HTML (Arabic narrative for understanding + English copy-paste messages and tech specs + every claim cited with a sources appendix + email confidence tiers). The reference dossier in _handover/examples/ is the gold standard. Invoke when the operator wants a deep dossier on a serious target, or says "do a full dossier on X" / "same depth as the reference dossier".
---

# Skill: Build a Sourced Bilingual Client Dossier

For serious targets. The model is the gold-standard reference dossier in `_handover/examples/` (kept private); match its quality and honesty.

## Non-negotiables (these are why the reference one was good)
- **Bilingual:** `<html lang="ar" dir="rtl">`. Arabic for the narrative/analysis (so Anas understands fast). **English stays English** for: copy-paste messages, tech specs, names, URLs, numbers — each in its own `<pre dir="ltr">` block.
- **Every factual claim cited:** inline `<sup><a href="#src-N">[N]</a></sup>` → a numbered **Sources Appendix** at the end with, per entry: title, URL, date accessed, verbatim quote, confidence (HIGH/MEDIUM/LOW).
- **Email confidence tiers:** color-coded badges 🟢 VERIFIED / 🟡 PATTERN-CONFIRMED / 🔴 GUESS, each with its sources.
- **Messages labeled COMPOSED:** every copy-paste message carries a "✍️ COMPOSED — built from sources [x],[y]" label so the reader knows what's a sourced fact vs a drafted message.
- **Self-contained:** inline CSS/JS, opens offline. Copy buttons on every message (button label "نسخ", copies the English text). Status checkboxes per channel (localStorage). Toast "تم النسخ".
- **Honesty canon applied:** scan against `knowledge/honesty-canon.md`. No banned overclaims. No em dashes. Mark anything unverifiable as "غير مُتحقق منه" rather than citing a fake source.

## Structure (Arabic headings)
1. الغلاف + الملخص التنفيذي (cover + exec summary)
2. نبذة عن الشركة (company deep-dive, all facts cited)
3. خريطة القيادة (leadership map, with tiered emails)
4. الـ Tech Stack ونقاط الألم (their stack + real pain points)
5. ملاءمة Arkedia (the fit + which pitch angle, proof-of-delivery lines)
6. حزمة الـ Outreach (the channels: EN copy-paste messages, AR explanation around them, each message passing `write-message` self-check)
7. قائمة التنفيذ (a dated execution checklist)
8. ملحق المصادر (the numbered Sources Appendix)

## Procedure
1. Run/confirm `research-prospect` for the company AND each named contact (sourced).
2. Verify the email pattern (`knowledge/email-patterns.md`); tier every address.
3. Draft every outreach message via `write-message` (so each passes the self-check) and label them COMPOSED with source IDs.
4. Assemble the HTML to `accounts/<company>/dossier-ar.html` (use the dossier template). Brand palette: Navy #0d1a3a, Green #2d6a4a, Gold #c08a1c, Red #a02828, bg #f4f5f8; font 'Segoe UI','Tahoma','Noto Sans Arabic',sans-serif; A4-print friendly.
5. Update `accounts/<company>/status.md` and `pipeline/pipeline.md`.

## Quality bar
- Every claim has a working inline citation → appendix entry with a verbatim quote.
- Every email tiered; every message labeled COMPOSED; messages pass the self-check.
- No banned overclaim; no em dash; unverifiable items flagged honestly.
- Opens offline; copy buttons and checkboxes work.

## Render to PDF (optional)
Re-render with the operator's toolchain (e.g. `_handover` had a `print-one.js`). The HTML is the source of truth.
