import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64

st.set_page_config(page_title="IT Infra Public Dashboard", layout="wide")

# --- Title
st.markdown("""
# 🧠 IT Infrastructure Readiness Dashboard
Use this free tool to assess your organization's infrastructure risk, compliance posture, and GRC readiness in real-time.
""")

st.markdown("---")

# --- SECTION 1: ORG PROFILE INPUT
st.subheader("🏢 Organizational Profile")
col1, col2, col3 = st.columns(3)

company_size = col1.selectbox("Company Size", ["Small", "Medium", "Large"])
industry = col2.selectbox("Industry", ["Finance", "Technology", "Healthcare", "Retail", "Education"])
environment = col3.selectbox("IT Environment", ["On-Prem", "Cloud", "Hybrid"])

col4, _ = st.columns(2)
region = col4.selectbox("Region", ["APAC", "EU", "North America", "Global"])

st.markdown("---")

# --- SECTION 2: Risk Dashboard Generator
st.subheader("🔴 Tailored Risk Heatmap")

risk_matrix = {
    "Small": [5, 6, 4, 3, 6],
    "Medium": [6, 7, 5, 4, 7],
    "Large": [8, 9, 7, 6, 8]
}

labels = ["Legacy OS", "IAM Gaps", "Backup Failures", "Firewall Misconfig", "Insufficient Visibility"]
severity = risk_matrix.get(company_size, [5, 6, 5, 4, 6])

if environment == "Cloud":
    severity[0] -= 2
    severity[4] += 1
elif environment == "Hybrid":
    severity[4] += 2

risk_df = pd.DataFrame({"Risk Area": labels, "Severity": severity})
fig = px.bar(risk_df, x="Risk Area", y="Severity", color="Severity",
             color_continuous_scale="reds", title="Top 5 Infra Weaknesses for Your Organization")
st.plotly_chart(fig, use_container_width=True)

# --- SECTION 3: ISO Compliance Progress
st.subheader("🛡️ Compliance Readiness Tracker")
iso_27001 = 0.55
iso_20000 = 0.45

if company_size == "Large":
    iso_27001 += 0.15
    iso_20000 += 0.1
elif company_size == "Medium":
    iso_27001 += 0.05
    iso_20000 += 0.05

if environment == "Cloud":
    iso_27001 += 0.1
if environment == "Hybrid":
    iso_27001 += 0.05
    iso_20000 += 0.05

col5, col6 = st.columns(2)
with col5:
    st.markdown(f"**ISO/IEC 27001 Readiness: {int(iso_27001 * 100)}%**")
    st.progress(iso_27001)
with col6:
    st.markdown(f"**ISO/IEC 20000-1 Readiness: {int(iso_20000 * 100)}%**")
    st.progress(iso_20000)

# --- SECTION 4: GRC Checklist
st.subheader("✅ GRC Readiness Checklist")
checklist = {
    "Asset Inventory Documented": True,
    "IAM Joiner-Mover-Leaver Process": company_size != "Small",
    "Patch Management Program Active": True,
    "Vulnerability Scan (Last 30 Days)": company_size != "Small",
    "Disaster Recovery Test Completed": environment != "On-Prem",
    "MFA Enforced for Admin Access": True
}

with st.expander("Click to view your tailored GRC checklist"):
    for item, status in checklist.items():
        st.checkbox(item, value=status, disabled=True)

# --- SECTION 5: Download Report
st.subheader("📄 Download Self-Assessment Summary")

def create_summary():
    summary = f"""
    IT Infrastructure Self-Assessment Summary\n\n
    Organization Profile:\n
    - Company Size: {company_size}\n    - Industry: {industry}\n    - Environment: {environment}\n    - Region: {region}\n\n
    ISO 27001 Readiness: {int(iso_27001 * 100)}%\n    ISO 20000 Readiness: {int(iso_20000 * 100)}%\n\n
    Top Risks:\n    """
    for i in range(len(labels)):
        summary += f"- {labels[i]}: {severity[i]}/10\n"

    summary += "\nGRC Checklist:\n"
    for item, status in checklist.items():
        state = "✔️" if status else "❌"
        summary += f"- {state} {item}\n"

    return summary

def download_button():
    content = create_summary()
    b = BytesIO()
    b.write(content.encode())
    b.seek(0)
    b64 = base64.b64encode(b.read()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="infra_self_assessment.txt">📥 Download Report (.txt)</a>'
    return href

st.markdown(download_button(), unsafe_allow_html=True)

# --- Footer
st.markdown("---")
st.caption("Designed by Vicknes Nair | Infra Self-Assessment Tool | Version 1.0")
