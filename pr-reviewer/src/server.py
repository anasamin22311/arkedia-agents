#!/usr/bin/env python3
"""
PR Reviewer Webhook Server
Receives GitHub PR webhooks, reviews with Claude Code CLI (OAuth), posts back.
The lead-engineer persona and stack rules below are an EXAMPLE set; replace them
with your own team's conventions (or load them from BUSINESS_CONTEXT.md).
"""

import hashlib
import hmac
import json
import os
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from flask import Flask, request, jsonify

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

GITHUB_TOKEN    = os.environ["GITHUB_TOKEN"]
WEBHOOK_SECRET  = os.environ.get("WEBHOOK_SECRET", "")
TARGET_BRANCH   = os.environ.get("TARGET_BRANCH", "development")
PORT            = int(os.environ.get("PORT", 7891))

# Business context lives in the mounted project repo, updated by git push, no redeploy needed
BUSINESS_CONTEXT_PATH = "/project/.github/BUSINESS_CONTEXT.md"

def _load_business_context() -> str:
    try:
        with open(BUSINESS_CONTEXT_PATH, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[WARN] Business context not found at {BUSINESS_CONTEXT_PATH}, using fallback.")
        return "(Business context unavailable — review code quality only)"

BUSINESS_CONTEXT = _load_business_context()

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are the lead engineer and architect of the platform.
You have 10+ years of experience building multi-tenant, bilingual SaaS products.
Your job is to review every PR to the `development` branch before it merges.

────────────────────────────────────────────────────────────────────────
PERSONALITY & REVIEW PHILOSOPHY
────────────────────────────────────────────────────────────────────────

- You are direct, concise, and opinionated. No fluff.
- You reject over-engineering immediately. The simplest correct solution wins.
- Three similar lines of code beat a premature abstraction.
- You never invent hypothetical future requirements as a reason to add complexity.
- You praise clean, focused code and call out lazy or careless work.
- When you spot a violation you say *what* the rule is, *why* it exists, and *how* to fix it.
- Performance matters: you catch N+1 queries, missing OnPush, unsubscribed observables.
- Security matters: you catch missing authorization attributes and exposed internals.
- You don't rubber-stamp PRs — you hold the bar high.

────────────────────────────────────────────────────────────────────────
TECH STACK
────────────────────────────────────────────────────────────────────────

Backend:  .NET 9 | Clean Architecture | CQRS (MediatR) | EF Core | SQL Server
Frontend: Angular 20 | Standalone Components | Zoneless | Signals | Angular Material
API:      Auto-generated client (NSwag/OpenAPI) — never hand-edited
i18n:     Arabic + English with RTL support — all user-facing text uses MultiLangEntry

────────────────────────────────────────────────────────────────────────
BACKEND — HARD RULES (any violation = REQUEST_CHANGES)
────────────────────────────────────────────────────────────────────────

ENDPOINTS
  ✅ DO   : [Endpoint(EndpointMethod.Post, "GroupName")]
  ❌ NEVER: [HttpGet], [HttpPost], [Route], [ApiController]
  ❌ NEVER: Group names with /api/ prefix, leading slashes, or route params like Events/{id}

CQRS
  ✅ Command + Handler in same file, Validator in separate file
  ✅ Use `record` types: `public record CreateEventCommand : IRequest<EventDto>`
  ✅ Naming: Create{Entity}Command, Get{Entity}ByIdQuery, {Entity}Dto
  ❌ NEVER skip a validator for any Command — every Command needs FluentValidation

VALIDATORS
  ✅ Use custom extensions: .RequiredMultiLang(), .OptionalMultiLang(), .ValidUrl()
  ✅ Validator file: {Action}{Entity}CommandValidator.cs

DTOs
  ✅ Always use factory methods: EventDto.FromEntity(entity)
  ❌ NEVER map properties manually in handlers — that belongs in FromEntity()

ENTITIES
  ✅ Default base class: SoftDeletableEntity
  ✅ Hierarchy: BaseEntity → BaseAuditableEntity → SoftDeletableEntity → MultiTenantEntity
  ❌ NEVER use plain string for bilingual text — always MultiLangEntry with .Ar / .En

LAYER BOUNDARIES
  ✅ Business logic in Application layer only
  ✅ DB access via IApplicationDbContext interface only
  ❌ NEVER put business logic in Web or Infrastructure layers
  ❌ NEVER access DbContext directly in Application — use the interface

AUTHORIZATION
  ✅ Add [Authorize(Permissions = DomainPermissions.Feature.Action)] on all write endpoints
  ❌ NEVER leave a mutating endpoint without an authorization attribute unless it's intentionally public

FILE NAMING
  Commands   : {Action}{Entity}Command.cs
  Validators : {Action}{Entity}CommandValidator.cs
  Queries    : Get{Entity}Query.cs
  DTOs       : {Entity}Dto.cs
  Entities   : {Entity}.cs

FOLDER STRUCTURE
  Application/{Feature}/Commands/{Action}{Entity}/
    {Action}{Entity}Command.cs
    {Action}{Entity}CommandValidator.cs
  Application/{Feature}/Queries/Get{Entity}ById/
    Get{Entity}ByIdQuery.cs
  Application/{Feature}/Dtos/
    {Entity}Dto.cs

────────────────────────────────────────────────────────────────────────
FRONTEND — HARD RULES (any violation = REQUEST_CHANGES)
────────────────────────────────────────────────────────────────────────

COMPONENTS
  ✅ standalone: true on every component, directive, pipe
  ✅ changeDetection: ChangeDetectionStrategy.OnPush on every component
  ✅ inject() for all dependency injection — no constructor injection
  ❌ NEVER use NgModule — everything is standalone
  ❌ NEVER use NgRx or any external state management — use Angular Signals

STATE
  ✅ signal(), computed(), effect() for all reactive state
  ✅ finalize(() => this.loading.set(false)) for loading state on observables

SUBSCRIPTIONS (memory leak = immediate REQUEST_CHANGES)
  ✅ takeUntilDestroyed(this.destroyRef) on ALL subscriptions
  ✅ OR takeUntil(this.destroy$) with complete() in ngOnDestroy
  ❌ NEVER leave a subscription without cleanup

IMPORTS
  ✅ imports: [...DASHBOARD_LIST_IMPORTS] or [...DASHBOARD_FORM_IMPORTS] from @shared/imports
  ❌ NEVER manually list Material/CDK module imports in a component

ERROR HANDLING
  ✅ catchError(() => { this.toast.showError(...); return EMPTY; })
  ❌ NEVER use console.log or console.error — always toast service

DOM ACCESS
  ❌ NEVER use document.getElementById() or any direct DOM access
  ✅ Use ViewChild or Renderer2

TYPES
  ❌ NEVER use `any` type — always a proper interface or type alias

PATH ALIASES
  ✅ Use @core, @shared, @features, @env, @api for cross-module imports
  ❌ NEVER use relative paths (../../) for cross-module references

AUTO-GENERATED CODE
  ❌ NEVER modify api-client.ts — it is auto-generated by NSwag
  ✅ Regenerate with: cd src/client && npm run generate-client

i18n
  ✅ All user-facing strings must use translate pipe: {{ 'key' | translate }}
  ✅ TypeScript strings: this.translate.instant('key')
  ❌ NEVER use a translation key that doesn't exist in BOTH en.json AND ar.json
  ❌ NEVER hardcode user-facing strings

SHARED COMPONENTS (use these, don't reinvent them)
  app-loading-button   — submit buttons (text content only, NO icons inside)
  app-input            — form inputs
  app-search-input     — list page search
  app-confirm-dialog   — delete/destructive confirmations
  app-page-header      — page titles

ROUTING
  ✅ permissionGuard(PermissionType.X) on all dashboard routes
  ✅ Navigate back to list on successful form save
  ✅ Use forkJoin for parallel data loading in resolvers/ngOnInit

FILE NAMING
  List page : {feature}-list.component.ts
  Form page : {feature}-form.component.ts

────────────────────────────────────────────────────────────────────────
GENERAL QUALITY RULES
────────────────────────────────────────────────────────────────────────

REJECT immediately:
  - Commented-out code blocks (just delete it — git remembers)
  - TODO comments without a linked issue
  - Dead code / unused imports / unused variables
  - Duplicate logic that an existing shared service/component already handles
  - Any feature flag or backwards-compat shim for removed code
  - Error handling for impossible scenarios
  - Unnecessary abstractions created "just in case"

PERFORMANCE — flag these:
  - N+1 queries: loading collections in loops without Include() or batch loading
  - Missing .AsNoTracking() on read-only queries
  - Missing indexes hinted by queries with WHERE / ORDER BY on unindexed columns
  - Observable chains that could be forkJoin but are sequential
  - Missing OnPush (already a hard rule, but double-check)

SECURITY — flag these:
  - Missing [Authorize] on write endpoints
  - Tenant isolation: multi-tenant queries must filter by tenant
  - Exposing internal IDs or sensitive data in DTOs unnecessarily

────────────────────────────────────────────────────────────────────────
OUTPUT FORMAT — RESPOND WITH VALID JSON ONLY. NO MARKDOWN WRAPPER.
────────────────────────────────────────────────────────────────────────

{
  "verdict": "APPROVE" | "REQUEST_CHANGES" | "COMMENT",
  "summary": "2-4 sentence blunt assessment of the PR",
  "blocking_issues": [
    {
      "file": "relative/path/to/File.cs",
      "line": 42,
      "title": "Short issue title",
      "body": "What the rule is, why it exists, and exactly how to fix it."
    }
  ],
  "suggestions": [
    {
      "file": "relative/path/to/file.ts",
      "line": 15,
      "title": "Short suggestion title",
      "body": "Non-blocking improvement with concrete example."
    }
  ],
  "praise": ["Specific things done well (only genuine praise, not padding)"]
}

VERDICT RULES:
- APPROVE         → Zero blocking issues. Code is clean and follows all conventions.
- REQUEST_CHANGES → One or more blocking issues. Be specific.
- COMMENT         → No hard-rule violations but has suggestions worth noting.

Do not add any text outside the JSON object. No preamble, no sign-off."""

FULL_SYSTEM = SYSTEM_PROMPT + "\n\n" + BUSINESS_CONTEXT

# ─────────────────────────────────────────────────────────────────────────────
# GITHUB HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def gh_get(url: str, accept: str = "application/vnd.github+json") -> bytes:
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": accept,
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()

def gh_post(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {e.code}: {body[:300]}") from e

def gh_put(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {e.code}: {body[:300]}") from e

def get_pr_meta(repo: str, pr_number: int) -> dict:
    raw = gh_get(f"https://api.github.com/repos/{repo}/pulls/{pr_number}")
    data = json.loads(raw)
    return {
        "title":        data["title"],
        "body":         data.get("body") or "",
        "additions":    data.get("additions", 0),
        "deletions":    data.get("deletions", 0),
        "changedFiles": data.get("changed_files", 0),
        "head_sha":     data["head"]["sha"],
    }

def get_pr_diff(repo: str, pr_number: int) -> str:
    raw = gh_get(
        f"https://api.github.com/repos/{repo}/pulls/{pr_number}",
        accept="application/vnd.github.diff",
    )
    diff = raw.decode("utf-8", errors="replace")
    return diff[:50000]  # cap at 50k chars

# ─────────────────────────────────────────────────────────────────────────────
# CLAUDE CALL
# ─────────────────────────────────────────────────────────────────────────────

def call_claude(user_message: str) -> dict:
    print("[claude] Running review...", flush=True)
    env = os.environ.copy()
    # Remove ANTHROPIC_API_KEY if it's mistakenly set to an OAuth token — the CLI
    # will use CLAUDE_CODE_OAUTH_TOKEN instead.
    if env.get("ANTHROPIC_API_KEY", "").startswith("sk-ant-oat"):
        env.pop("ANTHROPIC_API_KEY")
    proc = subprocess.run(
        [
            "claude",
            "--print",
            "--output-format", "text",
            "--system-prompt", FULL_SYSTEM,
            "--dangerously-skip-permissions",
            user_message,
        ],
        capture_output=True,
        text=True,
        timeout=240,
        cwd="/tmp",   # avoid any CLAUDE.md in mounted /project
        env=env,
    )

    if proc.returncode != 0:
        print(f"[claude] exit {proc.returncode}", flush=True)
        print(f"[claude] stdout: {proc.stdout[:500]}", flush=True)
        print(f"[claude] stderr: {proc.stderr[:500]}", flush=True)
        raise RuntimeError(f"Claude CLI exited {proc.returncode}: {proc.stdout[:300]}")

    raw = proc.stdout.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:])
        if "```" in raw:
            raw = raw[: raw.rfind("```")]

    return json.loads(raw.strip())

# ─────────────────────────────────────────────────────────────────────────────
# BUILD REVIEW BODY
# ─────────────────────────────────────────────────────────────────────────────

def build_review_body(review: dict) -> str:
    verdict    = review.get("verdict", "COMMENT")
    summary    = review.get("summary", "")
    blocking   = review.get("blocking_issues", [])
    suggestions = review.get("suggestions", [])
    praise     = review.get("praise", [])

    emoji = {"APPROVE": "✅", "REQUEST_CHANGES": "❌", "COMMENT": "💬"}.get(verdict, "💬")
    parts = [f"## {emoji} AI Code Review — {verdict}\n\n{summary}"]

    if praise:
        parts.append("### ✅ What's good\n" + "\n".join(f"- {p}" for p in praise))

    if blocking:
        items = []
        for i, issue in enumerate(blocking, 1):
            loc = f"`{issue.get('file','?')}`"
            if issue.get("line"):
                loc += f" line ~{issue['line']}"
            items.append(f"**{i}. {issue.get('title','Issue')}**\n📄 {loc}\n\n{issue.get('body','')}")
        parts.append("### ❌ Blocking Issues\n_Must be resolved before merge._\n\n" + "\n\n---\n\n".join(items))

    if suggestions:
        items = []
        for i, s in enumerate(suggestions, 1):
            loc = f"`{s.get('file','?')}`"
            if s.get("line"):
                loc += f" line ~{s['line']}"
            items.append(f"**{i}. {s.get('title','Suggestion')}**\n📄 {loc}\n\n{s.get('body','')}")
        parts.append("### 💡 Suggestions\n_Non-blocking._\n\n" + "\n\n---\n\n".join(items))

    if not blocking and not suggestions:
        parts.append("_No issues found. Ship it._")

    parts.append("---\n_Reviewed by AI Lead Engineer — Claude Opus via Claude Max subscription_")
    return "\n\n".join(parts)

# ─────────────────────────────────────────────────────────────────────────────
# REVIEW RUNNER (background thread)
# ─────────────────────────────────────────────────────────────────────────────

def run_review(pr_number: int, repo: str):
    print(f"[review] Starting PR #{pr_number} in {repo}", flush=True)
    try:
        meta = get_pr_meta(repo, pr_number)
        diff = get_pr_diff(repo, pr_number)

        if not diff.strip():
            print(f"[review] PR #{pr_number} has empty diff, skipping.", flush=True)
            return

        user_message = (
            f"## Pull Request: {meta['title']}\n\n"
            f"**Description:**\n{meta['body'] or '(none)'}\n\n"
            f"**Stats:** +{meta['additions']} / -{meta['deletions']} lines, "
            f"{meta['changedFiles']} files changed\n\n"
            f"## Diff\n```diff\n{diff}\n```\n\n"
            "Review this PR and respond with the JSON object only."
        )

        review = call_claude(user_message)

        verdict = review.get("verdict", "COMMENT")
        blocking_count = len(review.get("blocking_issues", []))
        print(f"[review] PR #{pr_number} → {verdict} ({blocking_count} blocking)", flush=True)

        body = build_review_body(review)
        event = {"APPROVE": "APPROVE", "REQUEST_CHANGES": "REQUEST_CHANGES", "COMMENT": "COMMENT"}.get(verdict, "COMMENT")

        try:
            result = gh_post(
                f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews",
                {"commit_id": meta["head_sha"], "body": body, "event": event},
            )
        except RuntimeError as e:
            if "422" in str(e) and event in ("REQUEST_CHANGES", "APPROVE"):
                # Can't review your own PR — fall back to COMMENT
                print(f"[review] 422 on {event} — falling back to COMMENT (PR author == reviewer)", flush=True)
                result = gh_post(
                    f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews",
                    {"commit_id": meta["head_sha"], "body": body, "event": "COMMENT"},
                )
                event = "COMMENT"  # mark as comment so we skip auto-merge
            else:
                raise
        print(f"[review] Posted: {result.get('html_url', '?')}", flush=True)

        # Auto-merge on APPROVE (only when we actually posted an APPROVE review, not a fallback COMMENT)
        if verdict == "APPROVE" and event == "APPROVE":
            print(f"[review] Verdict APPROVE — auto-merging PR #{pr_number}...", flush=True)
            try:
                merge_result = gh_put(
                    f"https://api.github.com/repos/{repo}/pulls/{pr_number}/merge",
                    {
                        "commit_title": f"Auto-merged: {meta['title']} (#{pr_number})",
                        "commit_message": "Passed AI code review. All conventions satisfied.",
                        "merge_method": "squash",
                    },
                )
                print(f"[review] Merged! SHA: {merge_result.get('sha', '?')}", flush=True)
            except RuntimeError as e:
                print(f"[review] Merge failed (may need manual merge): {e}", flush=True)

    except Exception as e:
        print(f"[review] ERROR on PR #{pr_number}: {e}", flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# FLASK WEBHOOK SERVER
# ─────────────────────────────────────────────────────────────────────────────

app = Flask(__name__)

def _verify_signature(raw_body: bytes, sig_header: str) -> bool:
    if not WEBHOOK_SECRET:
        return True  # no secret configured = skip check
    expected = "sha256=" + hmac.new(WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig_header or "", expected)

@app.route("/health")
def health():
    return "ok", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    # Validate GitHub signature
    sig = request.headers.get("X-Hub-Signature-256", "")
    if not _verify_signature(request.data, sig):
        return "Invalid signature", 401

    event = request.headers.get("X-GitHub-Event", "")
    data = request.get_json(silent=True) or {}

    if event != "pull_request":
        return jsonify({"skip": True, "reason": "not a PR event"}), 200

    action = data.get("action", "")
    if action not in ("opened", "synchronize", "reopened", "ready_for_review"):
        return jsonify({"skip": True, "reason": f"action={action}"}), 200

    pr = data.get("pull_request", {})
    if pr.get("draft"):
        return jsonify({"skip": True, "reason": "draft PR"}), 200

    base_branch = pr.get("base", {}).get("ref", "")
    if base_branch != TARGET_BRANCH:
        return jsonify({"skip": True, "reason": f"base={base_branch}"}), 200

    pr_number = pr["number"]
    repo = data["repository"]["full_name"]

    thread = threading.Thread(target=run_review, args=(pr_number, repo), daemon=True)
    thread.start()

    print(f"[webhook] Queued review for PR #{pr_number} in {repo}", flush=True)
    return jsonify({"queued": True, "pr": pr_number}), 202

@app.route("/review", methods=["POST"])
def manual_review():
    """Manual trigger endpoint — called by GitHub Action workflow_dispatch."""
    secret = request.headers.get("X-Webhook-Secret", "")
    if WEBHOOK_SECRET and not hmac.compare_digest(secret, WEBHOOK_SECRET):
        return "Unauthorized", 401

    data = request.get_json(silent=True) or {}
    pr_number = int(data.get("pr_number", 0))
    repo = data.get("repo", "")

    if not pr_number or not repo:
        return jsonify({"error": "pr_number and repo required"}), 400

    thread = threading.Thread(target=run_review, args=(pr_number, repo), daemon=True)
    thread.start()

    return jsonify({"queued": True, "pr": pr_number}), 202

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"[startup] PR Reviewer listening on :{PORT}", flush=True)
    print(f"[startup] Target branch: {TARGET_BRANCH}", flush=True)
    print(f"[startup] Webhook secret: {'set' if WEBHOOK_SECRET else 'NOT SET (insecure)'}", flush=True)
    print(f"[startup] Business context: {'loaded' if 'unavailable' not in BUSINESS_CONTEXT else 'MISSING'}", flush=True)
    app.run(host="0.0.0.0", port=PORT, threaded=True)
