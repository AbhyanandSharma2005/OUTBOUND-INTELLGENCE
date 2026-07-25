"""
Orchestrator: Campaign brief -> similar accounts -> contacts -> research -> emails.

Design (matches the problem statement's 4-stage breakdown):
  Stage 1: ICP account discovery   (search + LLM synthesis)
  Stage 2: Contact discovery       (search + LLM synthesis, per account)
  Stage 3: Account research        (search + LLM synthesis, per account)
  Stage 4: Personalized outreach   (LLM only, grounded in Stage 3 output)

Every LLM call is forced into strict JSON and grounded in real search text.
If parsing fails or the model can't find something, we surface NOT_FOUND /
empty lists rather than silently filling gaps with invented data.
"""
import json
import re
from groq import Groq

from agent.search import run_search, multi_search
from agent import prompts

MODEL_PRIMARY = "openai/gpt-oss-120b"
MODEL_FALLBACK = "llama-3.1-8b-instant"


def _clean_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    return text


def _call_llm(groq_key: str, system: str, user: str) -> dict:
    client = Groq(api_key=groq_key)
    last_err = None
    for model in (MODEL_PRIMARY, MODEL_FALLBACK):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=0.3,
                max_tokens=2000,
            )
            raw = resp.choices[0].message.content
            return json.loads(_clean_json(raw))
        except Exception as e:
            last_err = e
            continue
    return {"error": f"LLM_CALL_FAILED: {last_err}"}


def stage1_find_accounts(groq_key, tavily_key, vertical, reference_account, log=print):
    log(f"[Stage 1] Searching for companies similar to '{reference_account}' in '{vertical}'...")
    ctx = multi_search(tavily_key, [
        f"companies similar to {reference_account} {vertical} industry",
        f"{vertical} companies competitors of {reference_account}",
        f"top {vertical} companies 2026",
    ])
    prompt = prompts.stage1_accounts_prompt(vertical, reference_account, ctx)
    result = _call_llm(groq_key, prompts.SYSTEM_GUARD, prompt)
    log(f"[Stage 1] Done. Found {len(result.get('accounts', []))} candidate accounts.")
    return result


def stage2_find_contacts(groq_key, tavily_key, account_name, log=print):
    log(f"[Stage 2] Finding contacts at '{account_name}'...")
    ctx = multi_search(tavily_key, [
        f"{account_name} leadership team executives",
        f"{account_name} VP OR Head OR Director LinkedIn",
        f"{account_name} founder CEO CTO",
    ])
    prompt = prompts.stage2_contacts_prompt(account_name, ctx)
    result = _call_llm(groq_key, prompts.SYSTEM_GUARD, prompt)
    log(f"[Stage 2] Done. Found {len(result.get('contacts', []))} contacts at {account_name}.")
    return result


def stage3_research_account(groq_key, tavily_key, account_name, log=print):
    log(f"[Stage 3] Researching '{account_name}'...")
    ctx = multi_search(tavily_key, [
        f"{account_name} recent news 2026",
        f"{account_name} company overview what they do",
        f"{account_name} hiring OR expansion OR challenges",
    ])
    prompt = prompts.stage3_research_prompt(account_name, ctx)
    result = _call_llm(groq_key, prompts.SYSTEM_GUARD, prompt)
    log(f"[Stage 3] Done researching {account_name}.")
    return result


def stage4_write_email(groq_key, account_name, contact, research_brief, our_product, log=print):
    log(f"[Stage 4] Drafting email for {contact.get('name')} ({contact.get('title')})...")
    prompt = prompts.stage4_email_prompt(
        account_name, contact.get("name", "NOT_FOUND"),
        contact.get("title", "NOT_FOUND"),
        json.dumps(research_brief), our_product,
    )
    result = _call_llm(groq_key, prompts.SYSTEM_GUARD, prompt)
    log(f"[Stage 4] Email drafted for {contact.get('name')}.")
    return result


def run_full_pipeline(groq_key, tavily_key, vertical, reference_account, our_product,
                       max_accounts=3, max_contacts_per_account=2, log=print):
    """Runs the entire 4-stage flow and returns one structured report."""
    report = {
        "vertical": vertical,
        "reference_account": reference_account,
        "our_product": our_product,
        "accounts": [],
    }

    stage1 = stage1_find_accounts(groq_key, tavily_key, vertical, reference_account, log)
    accounts = stage1.get("accounts", [])[:max_accounts]

    for acc in accounts:
        acc_name = acc.get("name", "NOT_FOUND")
        if acc_name == "NOT_FOUND":
            continue

        research = stage3_research_account(groq_key, tavily_key, acc_name, log)
        contacts_result = stage2_find_contacts(groq_key, tavily_key, acc_name, log)
        contacts = contacts_result.get("contacts", [])[:max_contacts_per_account]

        emails = []
        for c in contacts:
            email = stage4_write_email(groq_key, acc_name, c, research, our_product, log)
            emails.append({"contact": c, "email": email})

        report["accounts"].append({
            "account_meta": acc,
            "research": research,
            "contacts_and_emails": emails,
        })

    log("[Pipeline] Complete.")
    return report
