import streamlit as st
from typing import List

# --- Backend logic ---
class ITInfraSecurityLeadGPT:
    def __init__(self):
        pass

    def get_migration_strategy(self, infra_type: str, users: int) -> str:
        if infra_type == "Exchange On-Prem to Office 365":
            return f"Recommended: Hybrid Migration for {users} users using tools like MigrationWiz, with validation and post-checks."
        elif infra_type == "File Server to Azure":
            return f"Use Azure Arc + agentless migration. Test performance pre-cutover."
        else:
            return "Please choose a supported infra type."

    def generate_ad_rebuild_plan(self, countries: List[str]) -> str:
        return f"Rebuilding AD in Azure for: {', '.join(countries)}. Ensure GPOs, DNS, and sync validations are in place."

    def get_grc_audit_checklist(self) -> List[str]:
        return [
            "✔️ IT asset inventory",
            "✔️ Patch & vulnerability management logs",
            "✔️ IAM onboarding/offboarding history",
            "✔️ Backup & DR testing reports",
            "✔️ ISO27001 control mapping"
        ]

    def get_iam_guide(self) -> List[str]:
        return [
            "📌 Define roles and access levels using RBAC.",
            "🔐 Apply the principle of least privilege (PoLP).",
            "⚙️ Automate provisioning/deprovisioning via HR systems.",
            "🔍 Monitor user activity logs (Azure AD, Defender).",
            "✅ Enforce MFA and conditional access policies."
        ]

# --- UI Layout ---
st.set_page_config(page_title="IT Infra & Security Advisor", page_icon="🛡️")

with st.sidebar:
    st.image("https://img.icons8.com/external-flaticons-lineal-color-flat-icons/64/000000/external-cyber-security-information-technology-flaticons-lineal-color-flat-icons.png", width=64)
    st.title("InfraSec Advisor")
    st.caption("By Vicknes Nair")
    tab = st.radio("Select a module:", [
        "Cloud Migration Strategy",
        "Active Directory Rebuild Plan",
        "GRC Audit Checklist",
        "IAM Guide"
    ])

st.markdown("""
    <style>
    .stTitle { color: #007BFF; }
    .stMarkdown h4 { margin-top: 25px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ IT Infra & Security Advisor (by Vicknes Nair)")
st.markdown("""
This interactive tool reflects 18+ years of real-world IT experience across Azure, infrastructure security, GRC audits, and IAM.
Select your area of guidance and input the necessary details to receive practical recommendations.
""")

engine = ITInfraSecurityLeadGPT()

if tab == "Cloud Migration Strategy":
    st.subheader("📦 Cloud Migration Strategy")
    infra = st.selectbox("Type of migration:", ["Exchange On-Prem to Office 365", "File Server to Azure"])
    users = st.number_input("Number of users involved:", min_value=10, max_value=10000, value=100)
    if st.button("Get Migration Plan"):
        st.success(engine.get_migration_strategy(infra, users))

elif tab == "Active Directory Rebuild Plan":
    st.subheader("🌐 Active Directory Rebuild Plan")
    country_list = st.text_input("Enter countries (comma-separated):")
    if st.button("Generate Plan"):
        countries = [c.strip() for c in country_list.split(',') if c.strip()]
        st.info(engine.generate_ad_rebuild_plan(countries))

elif tab == "GRC Audit Checklist":
    st.subheader("📋 GRC Audit Checklist")
    if st.button("Show Checklist"):
        checklist = engine.get_grc_audit_checklist()
        for item in checklist:
            st.markdown(f"- {item}")

elif tab == "IAM Guide":
    st.subheader("🔐 IAM Onboarding/Offboarding Guide")
    if st.button("Generate IAM Guidelines"):
        iam_steps = engine.get_iam_guide()
        for step in iam_steps:
            st.markdown(f"- {step}")
