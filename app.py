import json
import streamlit as st
from agent.pipeline import run_full_pipeline

st.set_page_config(page_title="Outbound Intelligence Agent", page_icon="🎯", layout="wide")

st.title("🎯 Outbound Intelligence Agent")
st.caption(
    "Campaign brief in → similar ICP accounts → real contacts → grounded research "
    "→ personalized outreach emails, out."
)

with st.sidebar:
    st.header("API Keys")
    groq_key = st.text_input("Groq API key", type="password", help="console.groq.com — free tier")
    tavily_key = st.text_input("Tavily API key", type="password", help="tavily.com — 1,000 free searches/mo")
    st.divider()
    st.header("Depth")
    max_accounts = st.slider("Max accounts", 1, 5, 3)
    max_contacts = st.slider("Max contacts / account", 1, 3, 2)

st.subheader("Campaign brief")
col1, col2 = st.columns(2)
with col1:
    vertical = st.text_input("Target vertical", value="warehouse automation / robotics")
with col2:
    reference_account = st.text_input("Reference account", value="FlytBase")

our_product = st.text_area(
    "What are we selling? (used to personalize the emails)",
    value="an autonomous drone-in-a-box inspection and monitoring platform for industrial and warehouse sites",
    height=80,
)

run = st.button("🚀 Run agent", type="primary", use_container_width=True)

if run:
    if not groq_key or not tavily_key:
        st.error("Add both API keys in the sidebar first.")
        st.stop()

    log_box = st.empty()
    logs = []

    def log(msg):
        logs.append(msg)
        log_box.code("\n".join(logs[-12:]))

    with st.spinner("Running the 4-stage pipeline..."):
        try:
            report = run_full_pipeline(
                groq_key, tavily_key, vertical, reference_account, our_product,
                max_accounts=max_accounts, max_contacts_per_account=max_contacts, log=log,
            )
        except Exception as e:
            st.error(f"Pipeline error: {e}")
            st.stop()

    st.success("Done. Results below.")
    st.session_state["report"] = report

if "report" in st.session_state:
    report = st.session_state["report"]
    st.divider()
    st.subheader("Results")

    for acc in report["accounts"]:
        meta = acc["account_meta"]
        with st.expander(f"🏢 {meta.get('name', 'NOT_FOUND')}", expanded=True):
            st.markdown(f"**Why similar:** {meta.get('why_similar', 'NOT_FOUND')}")
            st.markdown(f"**Estimated size:** {meta.get('estimated_size', 'NOT_FOUND')}")
            st.markdown(f"**Source:** {meta.get('source_url', 'NOT_FOUND')}")

            research = acc["research"]
            st.markdown("**Research brief**")
            st.json(research, expanded=False)

            st.markdown("**Contacts & personalized outreach**")
            for ce in acc["contacts_and_emails"]:
                contact, email = ce["contact"], ce["email"]
                st.markdown(f"— **{contact.get('name', 'NOT_FOUND')}**, {contact.get('title', 'NOT_FOUND')}")
                st.text_input("Subject", email.get("subject", "NOT_FOUND"),
                               key=f"subj-{meta.get('name')}-{contact.get('name')}", disabled=True)
                st.text_area("Email body", email.get("body", "NOT_FOUND"),
                              key=f"body-{meta.get('name')}-{contact.get('name')}", height=140, disabled=True)

    st.download_button(
        "⬇️ Download full report (JSON)",
        data=json.dumps(report, indent=2),
        file_name="outbound_report.json",
        mime="application/json",
        use_container_width=True,
    )
