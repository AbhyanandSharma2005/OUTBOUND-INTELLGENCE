# Submission — Outbound Account & Contact Generation

## What I built

An agent pipeline that turns a campaign brief (target vertical + reference
account) into similar ICP accounts, real contacts inside them, a grounded
research brief per account, and a personalized outreach email per contact —
running live at: **[PASTE STREAMLIT LINK HERE]**

## Architecture (see also `mindmap.html`)

Search-then-synthesize, not synthesize-then-hope: Tavily runs real web
searches first; Groq's LLM (`openai/gpt-oss-120b`) only ever writes from those
real snippets. Four sequential stages:

1. **ICP account discovery** — search for companies similar to the reference
   account in the target vertical; LLM extracts candidates with a
   similarity reason and source URL.
2. **Contact discovery** — per account, search for leadership/LinkedIn
   mentions; LLM extracts real names/titles with supporting evidence, or an
   honest empty list.
3. **Account research** — per account, search recent news and public
   signals; LLM produces a grounded brief (news, pain-point signal, context).
4. **Personalized outreach** — LLM writes one email per contact using only
   the Stage 3 brief — no placeholders, one concrete real detail per email.

Guardrail used throughout: every prompt requires the literal string
`NOT_FOUND` instead of an invented fact, for any field not backed by the
search context handed to that call.

## Real run output (fill in after `python run_cli.py`)

**Campaign brief used:**
- Vertical: `[fill in]`
- Reference account: `[fill in]`

**Example account found:** `[fill in — company name]`
- Why similar: `[fill in — paste from outbound_report.json]`
- Source: `[fill in URL]`

**Example contact found:** `[fill in — name, title]`
- Evidence: `[fill in]`

**Example research brief:** `[fill in — paste research JSON for one account]`

**Example generated email:**
```
Subject: [fill in]

[fill in full email body from emails.md]
```

Full trace attached: `outbound_report.json` (produced by `run_cli.py`,
committed to the repo alongside this file).

## Known limitation & fix applied

Contact discovery hit-rate depends on how much a company's leadership is
publicly indexed by search; when a search returns nothing verifiable, Stage
2 returns an empty contact list for that account rather than guessing a name
— visible directly in `outbound_report.json` for any account where this
happened during the real run.

## What I'd improve with more time

- Add a reference-account fetch step (pull structured firmographic data, not
  just search snippets) to make Stage 1 similarity scoring more rigorous.
- Cache Tavily results per company across a session to cut duplicate calls
  when re-running with the same vertical.
- Add a lightweight email quality check (length, personalization keyword
  check) before showing it as final output.
