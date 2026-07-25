"""
Four stage prompts. Every stage is told explicitly:
- Only use facts present in the SEARCH CONTEXT block given to you.
- If something can't be verified, write NOT_FOUND -- never invent it.
- Output strict JSON, no markdown fences, no commentary.
"""

SYSTEM_GUARD = (
    "You are a precise B2B research and outreach assistant. "
    "You must ONLY use facts that literally appear in the SEARCH CONTEXT provided. "
    "Never invent a company, person, title, email, or number. "
    "If a fact is not present in the search context, write the literal string "
    "NOT_FOUND for that field. "
    "Respond with ONLY valid JSON -- no markdown fences, no preamble, no explanation."
)


def stage1_accounts_prompt(vertical: str, reference_account: str, search_context: str) -> str:
    return f"""SEARCH CONTEXT:
{search_context}

TASK: Based only on the SEARCH CONTEXT above, identify 5 companies that fit this
Ideal Customer Profile (ICP):
- Target vertical: {vertical}
- Reference account (similar company to model against): {reference_account}

For each company return: name, why_similar (1-2 lines tying it to the reference
account and vertical, grounded in the search context), estimated_size, and
source_url (the URL from the search context that supports this company being
relevant; NOT_FOUND if none).

Return JSON:
{{
  "accounts": [
    {{"name": "...", "why_similar": "...", "estimated_size": "...", "source_url": "..."}}
  ]
}}"""


def stage2_contacts_prompt(account_name: str, search_context: str) -> str:
    return f"""SEARCH CONTEXT:
{search_context}

TASK: Based only on the SEARCH CONTEXT above, find real people at "{account_name}"
who would be relevant buyers/influencers for an outbound sales outreach
(titles like Head of Operations, VP Sales, Founder, CTO, Procurement Lead, etc).

For each person return: name, title, linkedin_or_source_url, evidence (the exact
phrase/context from the search results that proves this person holds this role
at this company). If no real contacts are found, return an empty list -- do not
invent placeholder names.

Return JSON:
{{
  "account": "{account_name}",
  "contacts": [
    {{"name": "...", "title": "...", "source_url": "...", "evidence": "..."}}
  ]
}}"""


def stage3_research_prompt(account_name: str, search_context: str) -> str:
    return f"""SEARCH CONTEXT:
{search_context}

TASK: Based only on the SEARCH CONTEXT above, build a short research brief on
"{account_name}" useful for personalizing outbound sales outreach.

Cover: recent_news (a real recent development, or NOT_FOUND), pain_point_signal
(an inferred operational challenge grounded in something concrete found, e.g. a
job posting, expansion announcement, or public complaint), business_context
(what they do, in 1-2 lines), and source_urls (list of URLs actually used).

Return JSON:
{{
  "account": "{account_name}",
  "recent_news": "...",
  "pain_point_signal": "...",
  "business_context": "...",
  "source_urls": ["..."]
}}"""


def stage4_email_prompt(account_name: str, contact_name: str, contact_title: str,
                         research_brief: str, our_product: str) -> str:
    return f"""RESEARCH BRIEF ON {account_name}:
{research_brief}

CONTACT: {contact_name}, {contact_title} at {account_name}

OUR PRODUCT/COMPANY WE ARE SELLING: {our_product}

TASK: Write one short, personalized cold outreach email from a BDR to this
specific contact. Rules:
- No {{placeholder}} style templating of any kind -- every line must read as
  written specifically for this person and company.
- Reference one concrete, real detail from the research brief (not a generic
  vertical statement).
- 90-130 words, plain text, no markdown.
- End with a soft, low-friction call to action (e.g. "worth a 15-min chat next
  week?"), not a hard sell.
- Do not fabricate any fact not present in the research brief above.

Return JSON:
{{
  "to": "{contact_name}",
  "subject": "...",
  "body": "..."
}}"""
