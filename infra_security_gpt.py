import streamlit as st
import pandas as pd
from io import BytesIO
import base64

st.set_page_config(page_title="IT Infra Public Dashboard", layout="wide")

# --- SESSION STATE INITIATION ---
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
    st.session_state.session_active = False

# --- Title
st.markdown("""
# 🧠 IT Infrastructure Readiness Dashboard
Upload your ISO compliance evidence file to identify control gaps, readiness levels, and improvement suggestions.
""")

st.markdown("---")

# --- SECTION 0: User Identification
st.subheader("👤 Enter Your Email to Start")
email_input = st.text_input("Your Email Address", value=st.session_state.user_email)
if email_input:
    st.session_state.user_email = email_input
    st.session_state.session_active = True

if not st.session_state.session_active:
    st.warning("Please enter your email address to start your session.")
    st.stop()

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

    # --- SECTION 2: ISO Domain-Based Control Breakdown
    st.subheader("📘 ISO Domain Control Summary")
    df["Domain"] = df["Control ID"].apply(lambda x: x.split(".")[0] if isinstance(x, str) and "." in x else "Other")
    domain_summary = df.groupby(["Domain", "Status"]).size().unstack(fill_value=0)

    import plotly.express as px
    domain_summary_reset = domain_summary.reset_index()
    domain_melted = domain_summary_reset.melt(id_vars='Domain', var_name='Status', value_name='Count')
    fig = px.bar(
        domain_melted,
        x='Count',
        y='Domain',
        color='Status',
        orientation='h',
        barmode='stack',
        title='Compliance Breakdown by ISO Domain'
    )
    st.plotly_chart(fig, use_container_width=True)

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

    # --- SECTION 4: Upload Supporting Evidence Files
    st.subheader("📎 Attach Evidence Files Per Control")
    evidence_files = {}
    for ctrl in df["Control Name"]:
        with st.expander(f"📂 {ctrl}"):
            uploaded_evidence = st.file_uploader(
                f"Upload evidence for '{ctrl}'",
                type=["pdf", "png", "jpg", "jpeg", "docx"],
                key=ctrl
            )
            if uploaded_evidence:
                evidence_files[ctrl] = uploaded_evidence

    # --- Export Uploaded Evidence Summary
    if evidence_files:
        st.subheader("📦 Evidence Upload Summary")
        for ctrl, file in evidence_files.items():
            st.markdown(f"✅ **{ctrl}**: `{file.name}` ({round(file.size / 1024, 2)} KB)")

        from zipfile import ZipFile
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "evidence_bundle.zip")
            with ZipFile(zip_path, 'w') as zipf:
                for ctrl, file in evidence_files.items():
                    file_path = os.path.join(temp_dir, file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.read())
                    zipf.write(file_path, arcname=file.name)

            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📦 Download All Evidence Files (.zip)",
                    data=f.read(),
                    file_name="evidence_bundle_" + st.session_state.user_email.replace("@", "_at_").replace(".", "_") + ".zip",
                    mime="application/zip"
                )

        st.download_button(
            label="📥 Export Evidence Log (.txt)",
            data="
".join([f"{ctrl}: {file.name}" for ctrl, file in evidence_files.items()]),
            file_name="evidence_upload_log_" + st.session_state.user_email.replace("@", "_at_").replace(".", "_") + ".txt",
            mime="text/plain"
        )
            label="📥 Export Evidence Log (.txt)",
            data="
".join([f"{ctrl}: {file.name}" for ctrl, file in evidence_files.items()]),
            file_name="evidence_upload_log.txt",
            mime="text/plain"
        )

# --- SECTION 4: Gap-Based Recommendations
    if recommendations:
        st.subheader("💡 Recommendations for Improvement")
        for ctrl, rec in recommendations.items():
            st.markdown(f"**🔸 {ctrl}**: {rec}")

    # --- SECTION 6: AI Assistant for Control Remediation
    import openai
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    st.subheader("🤖 AI Assistant for Control Remediation")
    with st.expander("Ask for remediation guidance on any control"):
        selected_control = st.selectbox("Select a non-compliant or partial control:", gap_df["Control Name"].unique())
        prompt = st.text_area("Optional: Add context or describe your environment")
        if st.button("🧠 Get AI Guidance"):
            st.markdown(f"**Remediation Plan for `{selected_control}`:**")
            with st.spinner("Generating AI recommendation..."):
                messages = [
                    {"role": "system", "content": "You are an expert ISO compliance consultant."},
                    {"role": "user", "content": f"How can we remediate the ISO control: '{selected_control}'? Context: {prompt}"}
                ]
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=messages
                    )
                    ai_reply = response.choices[0].message.content.strip()
                    st.markdown(ai_reply)
                except Exception as e:
                    st.error("⚠️ Failed to retrieve response from AI. Please check your API key or try again.")
            st.markdown(f"**Remediation Plan for `{selected_control}`:**")
            if selected_control in rec_map:
                st.markdown(f"✅ Recommendation: {rec_map[selected_control]}")
            else:
                st.markdown("🔎 Sorry, no specific recommendation found. Please consult an ISO advisor.")

# --- SECTION 5: Download Report
    from fpdf import FPDF
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
        href = f'<a href="data:file/txt;base64,{b64}" download="infra_self_assessment_' + st.session_state.user_email.replace('@', '_at_').replace('.', '_') + '.txt">📥 Download Report (.txt)</a>'
        return href

    def generate_pdf():
        content = create_summary().splitlines()
        pdf = FPDF()

        # --- Cover Page ---
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "IT INFRASTRUCTURE COMPLIANCE ASSESSMENT REPORT", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Prepared for: {st.session_state.user_email}", ln=True, align='C')
        from datetime import datetime
        pdf.cell(200, 10, f"Generated on: {datetime.now().strftime('%B %d, %Y')}", ln=True, align='C')
        pdf.cell(200, 10, "Standards Covered: ISO/IEC 27001, ISO/IEC 20000-1", ln=True, align='C')
        pdf.cell(200, 10, "Prepared by: V&E Solutions | ve-solutions.com", ln=True, align='C')

        # --- Main Content ---
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in content:
            pdf.multi_cell(0, 10, line)

        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer

    st.markdown(download_button(), unsafe_allow_html=True)

    st.download_button(
        label="📄 Download PDF Report",
        data=generate_pdf(),
        file_name="infra_self_assessment_" + st.session_state.user_email.replace("@", "_at_").replace(".", "_") + ".pdf",
        mime="application/pdf"
    )

else:
    st.info("Please upload a CSV file to begin your compliance assessment.")

# --- Footer
st.markdown("---")
st.caption("Designed by Vicknes Nair | Infra Self-Assessment Tool | Version 2.2")
