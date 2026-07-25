# Outbound Intelligence Agent

Takes a campaign brief (target vertical + a reference account) and produces:
1. Similar accounts that fit the ICP
2. Real contacts inside those accounts
3. A grounded research brief per account (real, public data)
4. A personalized outreach email per contact

## Architecture

Groq (`openai/gpt-oss-120b`, free tier) for generation + Tavily for real web
search, since Groq has no built-in browsing. Search always runs *before* the
LLM is called — the model only synthesizes real snippets, it's never asked to
recall facts from memory. Every stage is instructed to output the literal
string `NOT_FOUND` rather than invent a name, title, email, or statistic.

```
agent/search.py    Tavily wrapper — real web search
agent/prompts.py   4 stage prompts, all grounded + NOT_FOUND enforced
agent/pipeline.py  orchestrator — runs the 4 stages in sequence
app.py             Streamlit UI (the live deployed link)
run_cli.py         headless runner — fastest way to get proof of a real run
mindmap.html       self-contained flowchart of the design
```

## Get free API keys (2 minutes, no card)

- Groq: https://console.groq.com → API Keys → Create
- Tavily: https://tavily.com → Sign up → Dashboard → API key (1,000 free searches/mo)

## Run locally first (proof before deploy)

```bash
pip install -r requirements.txt
export GROQ_API_KEY=gsk_...
export TAVILY_API_KEY=tvly-...
python run_cli.py
```

This writes `outbound_report.json` (full structured trace of all 4 stages)
and `emails.md` (readable final output). Use these as the evidence in
`Submission.md`.

## Deploy (Streamlit Community Cloud — free, ~2 min)

```bash
git init
git add .
git commit -m "outbound intelligence agent"
git branch -M main
git remote add origin https://github.com/AbhyanandSharma2005/outbound-intelligence.git
git push -u origin main
```

Then go to https://share.streamlit.io → **New app** → select this repo →
main file `app.py` → **Deploy**. No secrets needed to configure — API keys
are entered in the sidebar at runtime.

## Known limitation

Contact discovery relies on public search snippets mentioning names/titles
alongside a company, so hit-rate varies by how much a company's leadership is
publicly indexed. Stage 2 is designed to return an honest empty list rather
than guess, which sometimes means fewer than the requested number of contacts
per account.
