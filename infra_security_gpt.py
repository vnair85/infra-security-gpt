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

# Placeholder message for next phase
st.info("✅ Profile saved. Click next to generate your tailored risk insights and compliance overview.")

# Footer
st.markdown("---")
st.caption("Designed by Vicknes Nair | Infra Self-Assessment Tool | Version 1.0")
