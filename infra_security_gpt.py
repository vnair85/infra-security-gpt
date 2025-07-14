import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IT Infra Executive Dashboard", layout="wide")

# --- Title
st.markdown("""
# 🧠 IT Infrastructure Executive Dashboard
Gain high-level insights into your IT landscape. Designed for Infrastructure Leads, CISOs, and IT Managers.
""")

# --- Key Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🌐 Total Sites Connected", 12)
with col2:
    st.metric("🧰 Active Projects", 8)
with col3:
    st.metric("🚨 Critical Risks", 3)

st.markdown("---")

# --- Risk Heatmap
st.subheader("🔴 Infrastructure Risk Heatmap")
risk_data = pd.DataFrame({
    "Risk Area": ["Legacy OS", "IAM Gaps", "Backup Failures", "Misconfigured Firewalls", "Weak Wi-Fi Security"],
    "Risk Level": [9, 7, 8, 6, 5]
})
risk_fig = px.bar(risk_data, x="Risk Area", y="Risk Level", color="Risk Level",
                  color_continuous_scale="reds", title="Top 5 Infrastructure Weak Points")
st.plotly_chart(risk_fig, use_container_width=True)

# --- GRC Checklist
st.subheader("✅ GRC Audit Quick Checklist")
with st.expander("Click to view GRC audit readiness checks"):
    st.markdown("""
    - [x] Asset Inventory Documented
    - [x] IAM Policies Audited (Joiner-Mover-Leaver)
    - [ ] Patch Management Reports Available
    - [ ] Vulnerability Scan Completed (Last 30 Days)
    - [ ] DR Test Conducted This Year
    - [ ] MFA Enforced for All Admins
    """)

# --- Compliance Radar
st.subheader("🛡️ Compliance Radar")
col4, col5 = st.columns(2)
with col4:
    st.markdown("**ISO27001 Readiness: 70%**")
    st.progress(0.7)
with col5:
    st.markdown("**ISO20000 Readiness: 55%**")
    st.progress(0.55)

# --- Footer
st.markdown("---")
st.caption("Designed by Vicknes Nair | For IT Infra Leaders | Version 1.0")
