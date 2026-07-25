<div align="center">

# 🎯 Outbound Intelligence Agent

**Turn a one-line campaign brief into researched accounts, real contacts, and personalized outreach — automatically.**

*Built in a 8-hour hackathon sprint for the BDR Outbound Account & Contact Generation challenge.*

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen?style=for-the-badge)](https://outbound-intellgence-73nk3jjbg6qcanapppp55z44.streamlit.app/)
[![Python](https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PC9zdmc+&logoColor=white)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](#license)

**[🚀 Try it live](https://outbound-intellgence-73nk3jjbg6qcanapppp55z44.streamlit.app/)** · **[📄 Read the Submission](./Submission.md)** · **[🧠 View the Mind Map](./mindmap.html)**

</div>

---

## 📌 The Problem

A BDR (Business Development Representative) gets a campaign brief — *"find companies like FlytBase in warehouse robotics"* — and then spends hours manually:

1. Researching which companies actually fit the ICP (Ideal Customer Profile)
2. Hunting down the right decision-makers inside each one
3. Digging up real, recent, relevant facts about each account
4. Writing a personalized email for every single contact — not a templated blast

**This agent compresses that entire workflow into one click**, without ever fabricating a company, a name, or a fact.

---

## ✨ What It Does

```
 Campaign Brief                                                     Personalized
 (vertical + reference   ──▶  🔎  ──▶  🧑‍💼  ──▶  📰  ──▶  ✉️   ──▶  Outreach
  account)                 Accounts    Contacts   Research  Emails      Ready to Send
```

| Stage | What happens | Grounded in |
|---|---|---|
| **1. ICP Account Discovery** | Finds 3–5 real companies similar to your reference account, in your target vertical | Live web search |
| **2. Contact Discovery** | Surfaces real decision-makers (CEO, CTO, VP Sales, etc.) at each account | Live web search |
| **3. Account Research** | Builds a grounded brief: recent news, pain-point signals, business context | Live web search |
| **4. Personalized Outreach** | Writes one unique, non-templated email per contact, referencing a real detail | Stage 3's brief only |

---

## 🖥️ Live Demo

**👉 [outbound-intellgence-73nk3jjbg6qcanapppp55z44.streamlit.app](https://outbound-intellgence-73nk3jjbg6qcanapppp55z44.streamlit.app/)**

No setup required to try it — bring your own free Groq + Tavily API keys (instructions below), paste them into the sidebar, and run a real campaign in under a minute.

<details>
<summary><b>📸 See a real, unedited run of this system</b></summary>

Campaign brief: `vertical = warehouse automation / robotics`, `reference account = FlytBase`

**Found:** Locus Robotics, Daifuku, Symbotic — each with a grounded research brief, real named contacts (e.g. Rick Faulk, CEO of Locus Robotics; Takuya Gondoh, CTO of Daifuku; Rick Cohen, CEO of Symbotic), and a unique personalized email per contact.

Full trace with sources: [`outbound_report.json`](./outbound_report.json) · Readable output: [`emails.md`](./emails.md) · Full writeup: [`Submission.md`](./Submission.md)

</details>

---

## 🏗️ Architecture

The core design decision: **search first, generate second.** The LLM (Groq) has no built-in browsing, so nothing it writes is ever "recalled from memory" — every fact comes from a real Tavily search result handed to it as context.

```
┌─────────────────┐     ┌──────────────┐     ┌───────────────────┐     ┌──────────────┐
│  Campaign Brief  │────▶│    Tavily    │────▶│   Groq LLM         │────▶│  Structured  │
│ vertical + ref.  │     │  web search  │     │ (openai/gpt-oss-   │     │     JSON     │
│     account      │     │ (real data)  │     │  120b) synthesizes │     │   response   │
└─────────────────┘     └──────────────┘     └───────────────────┘     └──────────────┘
                                                        │
                          Every prompt enforces: if a fact isn't in the
                          search context → output "NOT_FOUND", never invent it.
```

This repeats across all four stages, chaining each stage's real output into the next.

### Why this stack

| Choice | Reasoning |
|---|---|
| **Groq** (`openai/gpt-oss-120b`) | Free tier, extremely fast inference — critical under a hackathon time limit |
| **Tavily** | Purpose-built search API for LLM agents, generous free tier, clean structured results |
| **Streamlit** | Fastest path from code to a shareable live link — deploys straight from GitHub |
| **Strict JSON + `NOT_FOUND` contract** | Directly enforces the "do not fabricate" requirement at the prompt level, not as an afterthought |

---

## 📂 Project Structure

```
outbound-intelligence/
├── agent/
│   ├── search.py       # Tavily wrapper — every real web search goes through here
│   ├── prompts.py       # The 4 stage prompts — grounding + NOT_FOUND rules baked in
│   └── pipeline.py       # Orchestrator — chains the 4 stages together
├── app.py                # Streamlit UI — the live deployed product
├── run_cli.py            # Headless runner — fastest way to get proof-of-run output
├── mindmap.html           # Self-contained flowchart of the system design
├── outbound_report.json  # Full structured trace from a real run (all 4 stages)
├── emails.md              # Human-readable final output from that same run
├── Submission.md           # Full write-up with real, verifiable example output
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Get two free API keys (no credit card required)

| Service | Link | Free tier |
|---|---|---|
| **Groq** | [console.groq.com](https://console.groq.com) | 30 requests/min, up to 14,400/day |
| **Tavily** | [tavily.com](https://tavily.com) | 1,000 searches/month |

### 2. Run it locally

```bash
git clone https://github.com/AbhyanandSharma2005/outbound-intelligence.git
cd outbound-intelligence
pip install -r requirements.txt

export GROQ_API_KEY=gsk_...       # macOS/Linux
export TAVILY_API_KEY=tvly-...
# Windows PowerShell: $env:GROQ_API_KEY="gsk_...", $env:TAVILY_API_KEY="tvly-..."

python run_cli.py
```

This produces `outbound_report.json` (full trace) and `emails.md` (readable output) — real, run-it-yourself proof, not a mockup.

### 3. Or just launch the UI

```bash
streamlit run app.py
```

Enter your keys in the sidebar, fill in a campaign brief, click **Run agent**.

### 4. Deploy your own copy

1. Push this repo to your own GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Point it at your repo, main file `app.py` → **Deploy**

No secrets configuration needed — keys are entered at runtime in the sidebar.

---

## 🛡️ Anti-Hallucination Guardrails

This was the single hardest constraint in the brief — *"do not fabricate accounts, contacts, or facts"* — so it's enforced structurally, not just requested politely:

- **Search always precedes generation.** The LLM only ever sees real search snippets; it is never asked a question it could answer from training data alone.
- **Explicit `NOT_FOUND` contract.** Every prompt requires the literal string `NOT_FOUND` for any field not backed by the search context — the model is never given room to guess.
- **Honest empty results.** If Stage 2 can't verify a real contact at a company, it returns an empty list. It does not invent a plausible-sounding name to fill a quota.
- **Emails only ground in Stage 3's brief.** The email-writing stage never touches raw search results directly — it can only reference what already survived the research stage's grounding check, preventing hallucinations from compounding across stages.

---

## ⚠️ Known Limitations

- **Contact hit-rate varies by company.** Discovery depends on how much a company's leadership is publicly indexed by search engines — smaller or more private companies may surface fewer verified contacts. This is treated as an honest limitation, not papered over with invented names.
- **Search snippet quality varies.** Tavily returns strong results for well-covered companies; niche or very new companies may produce thinner research briefs.
- **No CRM integration (yet).** Output is currently JSON + Markdown; piping directly into a CRM or sequencer is a natural next step.

---

## 🔭 What's Next

- [ ] Structured firmographic enrichment for more rigorous ICP similarity scoring
- [ ] Session-level caching of Tavily results to cut duplicate calls on repeated runs
- [ ] Automated email quality scoring (length, personalization density) before display
- [ ] Direct CRM / sequencing tool export (CSV, HubSpot, Outreach)

---

## 📄 License

MIT — see [LICENSE](./LICENSE).

<div align="center">

**[Live Demo](https://outbound-intellgence-73nk3jjbg6qcanapppp55z44.streamlit.app/)** · **[Full Submission](./Submission.md)** · **[Mind Map](./mindmap.html)**

Built by [Abhyanand Sharma](https://github.com/AbhyanandSharma2005)

</div>