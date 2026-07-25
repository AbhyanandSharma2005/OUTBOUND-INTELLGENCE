# Submission — Outbound Account & Contact Generation

## What I built

An agent pipeline that turns a campaign brief (target vertical + reference
account) into similar ICP accounts, real contacts inside them, a grounded
research brief per account, and a personalized outreach email per contact —
running live at:

**https://outbound-intellgence-73nk3jjbg6qcanapppp55z44.streamlit.app/**

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

## Real run output

**Campaign brief used:**
- Vertical: `warehouse automation / robotics`
- Reference account: `FlytBase`

The pipeline found 3 accounts, researched each, surfaced 6 real contacts
across them, and wrote 6 fully personalized emails. Full trace below and in
`outbound_report.json`.

---

### Account 1 — Locus Robotics

**Why similar:** Develops autonomous mobile robots for warehouse automation,
similar to FlytBase's autonomous drone solutions for inventory management.
**Source:** https://www.skyquestt.com/report/warehouse-robotics-market/companies

**Research brief:**
- *Recent news:* Locus Robotics acquired Nexera Robotics, integrating
  Nexera's NeuraGrasp grasping technology into Locus' physical AI platforms
  to expand mobile manipulation (May 19, 2026).
- *Pain-point signal:* Notes labor challenges such as hiring and turnover,
  indicating difficulty scaling workforce and a need for robots to maintain
  productivity.
- *Business context:* Provides autonomous mobile robots and AI-powered
  warehouse automation — directed picking, putaway, and mezzanine management
  for retailers, 3PLs, healthcare, and industrial sectors.

**Contact found:** Rick Faulk, CEO
**Evidence:** "Locus Robotics's Chief Executive Officer, Board Member is
Rick Faulk." (via LinkedIn)

**Generated email:**
```
Subject: Enhancing Locus Robotics' Mobile Manipulation with Aerial Insight

Hi Rick,

Congrats on the recent acquisition of Nexera Robotics and the integration of
NeuraGrasp technology – it's exciting to see Locus expanding mobile
manipulation capabilities. As you tackle labor hiring and turnover
challenges, adding an autonomous drone-in-a-box platform could give your
warehouses an extra set of eyes, handling high-reach inspections and
monitoring without extra staff. Our solution operates safely indoors,
delivers real-time visual data, and integrates with existing warehouse
management systems, helping maintain productivity during peak seasons.
Would a brief 15-minute call next week be worth exploring how this could
complement Locus's robot fleet?

Regards,
```

*(A second contact, Mike Johnson — President & COO — was also found and
emailed; see `outbound_report.json` for the full text.)*

---

### Account 2 — Daifuku

**Why similar:** A global leader in material handling and warehouse
automation systems, operating in the same vertical as FlytBase's warehouse
robotics offerings.
**Source:** https://www.skyquestt.com/report/warehouse-robotics-market/companies

**Research brief:**
- *Recent news:* Completed construction of a new factory building for
  cleanroom systems for semiconductor production lines at Shiga Works on
  April 3, 2026, increasing domestic cleanroom capacity by 30%.
- *Pain-point signal:* Expanding globally is challenging because many
  employees lack experience outside Japan, making it difficult to replicate
  successful logistics solutions in new markets.
- *Business context:* Designs, manufactures, installs and services
  material-handling and automation equipment, including cleanroom
  transport/storage systems for semiconductors and other logistics solutions.

**Contact found:** Takuya Gondoh, Chief Technology Officer
**Evidence:** "Senior Managing Officer | Takuya Gondoh | Chief Technology
Officer Business Innovation Division Manager"

**Generated email:**
```
Subject: Congrats on Shiga Works cleanroom expansion

Hi Takuya,

I saw Daifuku's recent completion of the new cleanroom systems factory at
Shiga Works on April 3 2026 and the 30% boost in domestic capacity –
impressive work. As you look to replicate that success internationally, I
understand the challenge of limited overseas experience among staff. Our
autonomous drone-in-a-box platform can give your teams real-time visual
insights of new sites without needing extensive on-ground expertise, helping
accelerate global roll-outs while keeping safety and quality high. The
system can operate safely in cleanroom environments, complementing your
transport and storage solutions. Would a brief 15-minute call next week be
worth exploring?

Best,
[Your Name]
```

*(A second contact, Tomoaki Terai — President and CEO/COO — was also found
and emailed; see `outbound_report.json` for the full text.)*

---

### Account 3 — Symbotic

**Why similar:** Provides AI-based warehouse automation solutions that
combine robotics and machine learning, aligning with FlytBase's focus on
autonomous technology for warehouses.
**Source:** https://www.skyquestt.com/report/warehouse-robotics-market/companies

**Research brief:**
- *Recent news:* Reported Q2 fiscal year 2026 revenue of $676 million, up
  23% year-over-year, and net income of $9 million (May 6, 2026).
- *Pain-point signal:* Skilled labor constraints — hiring and training
  bottlenecks for engineers and technicians may delay system rollouts and
  increase labor costs.
- *Business context:* Automation technology leader providing an AI-powered
  robotic and software platform for large retail, wholesale, and food &
  beverage warehouses.

**Contact found:** Rick Cohen, Chairman of the Board and Chief Executive Officer
**Evidence:** "said Rick Cohen, Chairman of the Board and Chief Executive
Officer." (via LinkedIn)

**Generated email:**
```
Subject: Congrats on Q2 growth – quick idea for warehouse inspections

Hi Rick,

Congratulations on Symbotic's impressive Q2 FY2026 results – $676 million in
revenue and a 23% year-over-year increase is a strong signal of market
traction. I noticed you highlighted skilled-labor constraints as a challenge
for engineers and technicians. Our autonomous drone-in-a-box platform can
continuously inspect and monitor warehouse equipment without adding
headcount, giving your team real-time data while freeing engineers to focus
on higher-value work. It integrates with existing AI-driven warehouse
systems and requires minimal training. Would you be open to a brief
15-minute call next week to explore how this could complement Symbotic's
automation roadmap?

Best regards,
```

*(A second contact, Izzy Martins — CFO — was also found and emailed; see
`outbound_report.json` for the full text.)*

---

Full structured trace (all 3 accounts, all 6 contacts, all 6 emails,
research, and source URLs) is committed alongside this file as
`outbound_report.json`.

## Known limitation & fix applied

Contact discovery hit-rate depends on how much a company's leadership is
publicly indexed by search. In this real run every account surfaced usable
contacts, but Stage 2 is explicitly designed to return an empty contact list
for an account rather than invent a name if search evidence is missing —
that's an intentional honesty trade-off over completeness.

## What I'd improve with more time

- Add a reference-account fetch step (pull structured firmographic data, not
  just search snippets) to make Stage 1 similarity scoring more rigorous.
- Cache Tavily results per company across a session to cut duplicate calls
  when re-running with the same vertical.
- Add a lightweight email quality check (length, personalization keyword
  check) before showing it as final output.