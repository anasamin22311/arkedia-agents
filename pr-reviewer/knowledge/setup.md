# Setup & Deploy

## Environment variables (required)
- `GITHUB_TOKEN` - a token with `repo` scope to read PR diffs and post reviews.
- `CLAUDE_CODE_OAUTH_TOKEN` - OAuth token for the Claude Code CLI (the container uses the CLI, not a raw API key).
- `WEBHOOK_SECRET` - shared secret to verify GitHub webhook signatures. Set it; an empty secret skips verification (insecure).
- `TARGET_BRANCH` - the branch to gate (default `development`).
- `PORT` - default `7891`.

Never commit any of these. They are read from the environment at runtime.

## Run it
```
docker build -t pr-reviewer .
docker run -d -p 7891:7891 \
  -e GITHUB_TOKEN=*** \
  -e CLAUDE_CODE_OAUTH_TOKEN=*** \
  -e WEBHOOK_SECRET=*** \
  -e TARGET_BRANCH=development \
  pr-reviewer
```

Then add a GitHub webhook on your repo: payload URL `https://your-host/webhook`, content type `application/json`, secret = `WEBHOOK_SECRET`, events = Pull requests. A `/health` endpoint and a `/review` manual-trigger endpoint are also exposed.

## Adapt the rules to your team
The `SYSTEM_PROMPT` in `src/server.py` is an example .NET 9 + Angular 20 rule set. Two ways to make it yours:
1. **Edit the prompt** directly: replace the backend/frontend hard rules with your stack's conventions, and rewrite the persona to sound like your real lead engineer.
2. **External context (no redeploy):** mount your repo into the container and put team-specific rules in `.github/BUSINESS_CONTEXT.md`. The server loads it at `/project/.github/BUSINESS_CONTEXT.md`, so a git push updates the reviewer's knowledge without rebuilding.

## Output contract
The Claude call must return strict JSON: `verdict` (APPROVE / REQUEST_CHANGES / COMMENT), `summary`, `blocking_issues[]`, `suggestions[]`, `praise[]`. The server formats that into a GitHub review comment. A hard-rule violation must be REQUEST_CHANGES.

## Notes
- The CLI runs with `--dangerously-skip-permissions` as a non-root user inside the container (the CLI refuses that flag as root, hence the `reviewer` user in the Dockerfile).
- Auto-merge fires only on a genuine APPROVE (squash merge). If the PR author is the same as the reviewer identity, GitHub blocks APPROVE/REQUEST_CHANGES, so the server falls back to a COMMENT and skips auto-merge.
