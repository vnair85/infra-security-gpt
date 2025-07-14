import streamlit as st
import pandas as pd
import plotly.express as px

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

# Basic logic to vary risk severity based on selections
risk_matrix = {
    "Small": [5, 6, 4, 3, 6],
    "Medium": [6, 7, 5, 4, 7],
    "Large": [8, 9, 7, 6, 8]
}

labels = ["Legacy OS", "IAM Gaps", "Backup Failures", "Firewall Misconfig", "Insufficient Visibility"]
severity = risk_matrix.get(company_size, [5, 6, 5, 4, 6])

# Slight modifiers based on environment
if environment == "Cloud":
    severity[0] -= 2  # Less legacy OS
    severity[4] += 1  # Visibility harder in cloud
elif environment == "Hybrid":
    severity[4] += 2

risk_df = pd.DataFrame({"Risk Area": labels, "Severity": severity})
fig = px.bar(risk_df, x="Risk Area", y="Severity", color="Severity",
             color_continuous_scale="reds", title="Top 5 Infra Weaknesses for Your Organization")
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Designed by Vicknes Nair | Infra Self-Assessment Tool | Version 1.0")
