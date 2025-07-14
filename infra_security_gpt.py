import streamlit as st
import pandas as pd
from io import BytesIO
import base64

st.set_page_config(page_title="IT Infra Public Dashboard", layout="wide")

# --- Title
st.markdown("""
# 🧠 IT Infrastructure Readiness Dashboard
Upload your ISO compliance evidence file to identify control gaps, readiness levels, and improvement suggestions.
""")

st.markdown("---")

# --- SECTION 1: Upload Compliance Evidence File
st.subheader("📤 Upload ISO Compliance Evidence File")
uploaded_file = st.file_uploader("Upload a CSV file using the template format provided", type=["csv"])

iso_27001_score = 0
iso_20000_score = 0
checklist = {}
recommendations = {}

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded and assessed successfully.")

    st.subheader("📄 Uploaded Data Preview")
    st.dataframe(df, use_container_width=True)

    # --- Analysis
    total_controls = len(df)
    compliant = df[df["Status"] == "Compliant"].shape[0]
    partial = df[df["Status"] == "Partially Compliant"].shape[0]
    non_compliant = df[df["Status"] == "Non-Compliant"].shape[0]
    evidence = df[df["Evidence Available"] == "Yes"].shape[0]

    iso_27001_score = round(((compliant + 0.5 * partial) / total_controls), 2)
    iso_20000_score = round((evidence / total_controls), 2)

    checklist = dict(zip(df["Control Name"], df["Status"] == "Compliant"))

    # Recommendation logic for non-compliant or partial items
    rec_map = {
        "Asset Inventory": "Ensure all assets are tracked and linked to owners.",
        "User Access Review": "Implement quarterly access rights reviews in IAM.",
        "Backup Policy": "Schedule regular backup verification and testing.",
        "Incident Logging and Tracking": "Introduce a centralized ticketing/logging tool.",
        "Service Availability Monitoring": "Automate alerts and track uptime SLAs.",
        "Change Management Procedure": "Document all changes and approvals in a system.",
        "Information Security Roles": "Define and publish information security roles in HR policy.",
        "Customer Satisfaction Assessment": "Deploy a post-resolution feedback form biannually."
    }

    # Build dynamic recommendations
    gap_df = df[df["Status"] != "Compliant"]
    for index, row in gap_df.iterrows():
        ctrl = row["Control Name"]
        recommendations[ctrl] = rec_map.get(ctrl, "Review control implementation.")

    # --- Summary block
    st.subheader("🔍 Compliance Summary")
    colc1, colc2, colc3 = st.columns(3)
    colc1.metric("✔️ Compliant", compliant)
    colc2.metric("➖ Partial", partial)
    colc3.metric("❌ Non-Compliant", non_compliant)

    # --- SECTION 2: Compliance Readiness Tracker
    st.subheader("🛡️ Compliance Readiness Tracker")
    col5, col6 = st.columns(2)
    with col5:
        st.markdown(f"**ISO/IEC 27001 Readiness: {int(iso_27001_score * 100)}%**")
        st.progress(iso_27001_score)
    with col6:
        st.markdown(f"**ISO/IEC 20000-1 Readiness: {int(iso_20000_score * 100)}%**")
        st.progress(iso_20000_score)

    # --- SECTION 3: GRC Checklist
    st.subheader("✅ GRC Readiness Checklist")
    with st.expander("Click to view your tailored GRC checklist"):
        for item, status in checklist.items():
            st.checkbox(item, value=status, disabled=True)

    # --- SECTION 4: Gap-Based Recommendations
    if recommendations:
        st.subheader("💡 Recommendations for Improvement")
        for ctrl, rec in recommendations.items():
            st.markdown(f"**🔸 {ctrl}**: {rec}")

    # --- SECTION 5: Download Report
    st.subheader("📥 Download Self-Assessment Summary")

    def create_summary():
        summary = f"""
        IT Infrastructure Self-Assessment Summary\n\n
        ISO 27001 Readiness: {int(iso_27001_score * 100)}%\n        ISO 20000 Readiness: {int(iso_20000_score * 100)}%\n\n
        GRC Checklist:\n        """
        for item, status in checklist.items():
            state = "✔️" if status else "❌"
            summary += f"- {state} {item}\n"

        if recommendations:
            summary += "\nRecommendations:\n"
            for ctrl, rec in recommendations.items():
                summary += f"- {ctrl}: {rec}\n"

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

else:
    st.info("Please upload a CSV file to begin your compliance assessment.")

# --- Footer
st.markdown("---")
st.caption("Designed by Vicknes Nair | Infra Self-Assessment Tool | Version 2.2")
