import streamlit as st
from typing import List

# --- Backend logic (based on your expertise) ---
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

# --- Streamlit UI ---
st.set_page_config(page_title="IT Infra & Security Advisor", page_icon="🛡️")
st.title("🛡️ IT Infra & Security Advisor (by Vicknes Nair)")

st.markdown("""
This interactive tool reflects 18+ years of real-world IT experience across Azure, infrastructure security, GRC audits, and IAM.
Select your area of guidance and input the necessary details to receive practical recommendations.
""")

engine = ITInfraSecurityLeadGPT()

tab = st.selectbox("Choose an area of guidance:", [
    "Cloud Migration Strategy",
    "Active Directory Rebuild Plan",
    "GRC Audit Checklist"
])

if tab == "Cloud Migration Strategy":
    infra = st.selectbox("Type of migration:", ["Exchange On-Prem to Office 365", "File Server to Azure"])
    users = st.number_input("Number of users involved:", min_value=10, max_value=10000, value=100)
    if st.button("Get Migration Plan"):
        st.success(engine.get_migration_strategy(infra, users))

elif tab == "Active Directory Rebuild Plan":
    country_list = st.text_input("Enter countries (comma-separated):")
    if st.button("Generate Plan"):
        countries = [c.strip() for c in country_list.split(',') if c.strip()]
        st.info(engine.generate_ad_rebuild_plan(countries))

elif tab == "GRC Audit Checklist":
    if st.button("Show Checklist"):
        checklist = engine.get_grc_audit_checklist()
        for item in checklist:
            st.markdown(f"- {item}")
