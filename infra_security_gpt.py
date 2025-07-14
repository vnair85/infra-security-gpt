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

# --- SECTION 2: Upload Compliance Evidence File
st.subheader("📤 Upload ISO Compliance Evidence File")
uploaded_file = st.file_uploader("Upload a CSV file using the template format provided", type=["csv"])

iso_27001_score = 0
iso_20000_score = 0
checklist = {}

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    total_controls = len(df)
    compliant = df[df["Status"] == "Compliant"].shape[0]
    partial = df[df["Status"] == "Partially Compliant"].shape[0]
    evidence = df[df["Evidence Available"] == "Yes"].shape[0]

    # Simple scoring logic
    iso_27001_score = round(((compliant + 0.5 * partial) / total_controls), 2)
    iso_20000_score = round((evidence / total_controls), 2)

    # Generate checklist from data
    checklist = dict(zip(df["Control Name"], df["Status"] == "Compliant"))

    st.success("✅ File uploaded and assessed successfully.")
else:
    st.info("Please upload a CSV file to assess compliance readiness.")

# --- SECTION 3: ISO Compliance Progress
if uploaded_file:
    st.subheader("🛡️ Compliance Readiness Tracker")
    col5, col6 = st.columns(2)
    with col5:
        st.markdown(f"**ISO/IEC 27001 Readiness: {int(iso_27001_score * 100)}%**")
        st.progress(iso_27001_score)
    with col6:
        st.markdown(f"**ISO/IEC 20000-1 Readiness: {int(iso_20000_score * 100)}%**")
        st.progress(iso_20000_score)

# --- SECTION 4: GRC Checklist
if checklist:
    st.subheader("✅ GRC Readiness Checklist")
    with st.expander("Click to view your tailored GRC checklist"):
        for item, status in checklist.items():
            st.checkbox(item, value=status, disabled=True)

# --- SECTION 5: Download Report
if uploaded_file:
    st.subheader("📄 Download Self-Assessment Summary")

    def create_summary():
        summary = f"""
        IT Infrastructure Self-Assessment Summary\n\n
        Organization Profile:\n
        - Company Size: {company_size}\n        - Industry: {industry}\n        - Environment: {environment}\n        - Region: {region}\n\n
        ISO 27001 Readiness: {int(iso_27001_score * 100)}%\n        ISO 20000 Readiness: {int(iso_20000_score * 100)}%\n\n
        GRC Checklist:\n        """
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
st.caption("Designed by Vicknes Nair | Infra Self-Assessment Tool | Version 2.0")
