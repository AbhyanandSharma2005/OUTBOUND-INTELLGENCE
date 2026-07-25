"""
Headless run -- no browser needed. Fastest way to get real proof-of-run
output for your Submission.md before you even touch deployment.

Usage:
    export GROQ_API_KEY=...
    export TAVILY_API_KEY=...
    python run_cli.py
"""
import os
import json
import sys
from agent.pipeline import run_full_pipeline

VERTICAL = os.environ.get("CAMPAIGN_VERTICAL", "warehouse automation / robotics")
REFERENCE_ACCOUNT = os.environ.get("CAMPAIGN_REFERENCE_ACCOUNT", "FlytBase")
OUR_PRODUCT = os.environ.get(
    "OUR_PRODUCT",
    "an autonomous drone-in-a-box inspection and monitoring platform for "
    "industrial and warehouse sites",
)


def main():
    groq_key = os.environ.get("GROQ_API_KEY")
    tavily_key = os.environ.get("TAVILY_API_KEY")
    if not groq_key or not tavily_key:
        print("ERROR: set GROQ_API_KEY and TAVILY_API_KEY environment variables first.")
        sys.exit(1)

    print(f"Campaign brief -> vertical='{VERTICAL}', reference_account='{REFERENCE_ACCOUNT}'\n")

    report = run_full_pipeline(
        groq_key, tavily_key, VERTICAL, REFERENCE_ACCOUNT, OUR_PRODUCT,
        max_accounts=3, max_contacts_per_account=2,
    )

    with open("outbound_report.json", "w") as f:
        json.dump(report, f, indent=2)

    with open("emails.md", "w") as f:
        f.write(f"# Outreach emails -- {VERTICAL} campaign (ref: {REFERENCE_ACCOUNT})\n\n")
        for acc in report["accounts"]:
            name = acc["account_meta"].get("name", "NOT_FOUND")
            f.write(f"## {name}\n\n")
            f.write(f"_Why similar_: {acc['account_meta'].get('why_similar', 'NOT_FOUND')}\n\n")
            for ce in acc["contacts_and_emails"]:
                contact = ce["contact"]
                email = ce["email"]
                f.write(f"### To: {contact.get('name', 'NOT_FOUND')} ({contact.get('title', 'NOT_FOUND')})\n\n")
                f.write(f"**Subject:** {email.get('subject', 'NOT_FOUND')}\n\n")
                f.write(f"{email.get('body', 'NOT_FOUND')}\n\n---\n\n")

    print("\nDone.")
    print(" -> outbound_report.json  (full structured trace, all 4 stages)")
    print(" -> emails.md             (readable final outreach output)")


if __name__ == "__main__":
    main()
