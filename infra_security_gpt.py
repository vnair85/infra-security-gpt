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

    def handle_incident(self, incident_type: str) -> str:
        if incident_type == "Data Breach":
            return (
                "### 🛡️ Incident Response: Data Breach\n"
                "1. 🛑 **Isolate affected systems immediately**\n"
                "2. 🔍 **Identify breach source and impacted data**\n"
                "3. 📢 **Notify legal, compliance, and stakeholders**\n"
                "4. 🔐 **Change credentials and block compromised access**\n"
                "5. 📄 **Document the breach and lessons learned**\n"
            )
        elif incident_type == "Ransomware Attack":
            return (
                "### 🛡️ Incident Response: Ransomware\n"
                "1. 🚫 **Disconnect infected systems from the network**\n"
                "2. 🔒 **Check backups and avoid paying ransom**\n"
                "3. 🧼 **Wipe & restore affected systems from clean backups**\n"
                "4. 🚨 **Report incident to regulatory body if required**\n"
                "5. 📊 **Review security gaps and update tools**\n"
            )
        elif incident_type == "Insider Threat":
            return (
                "### 🛡️ Incident Response: Insider Threat\n"
                "1. 🧠 **Identify suspicious user behavior or access**\n"
                "2. 🔍 **Audit logs and collect evidence securely**\n"
                "3. 🗣️ **Interview involved parties confidentially**\n"
                "4. 🧑‍⚖️ **Suspend access and begin HR/legal procedures**\n"
                "5. 📁 **Update IAM policies and monitoring alerts**\n"
            )
        else:
            return "🚫 Unsupported incident type."

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
        "IAM Guide",
        "Incident Response Simulator"
    ])

st.markdown("""
    <style>
    .stTitle { color: #007BFF; }
    .stMarkdown h4 { margin-top: 25px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ IT Infra & Security Advisor (by Vicknes Nair)")
st.markdown("""
This interactive tool reflects 18+ years of real-world IT experience across Azure, infrastructure security, GRC audits, IAM, and incident response planning.
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

elif tab == "Incident Response Simulator":
    st.subheader("🧪 Incident Response Simulator")
    incident_type = st.selectbox("Select Incident Type", ["Data Breach", "Ransomware Attack", "Insider Threat"])
    if st.button("Simulate Response"):
        st.markdown(engine.handle_incident(incident_type))
