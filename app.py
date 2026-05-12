import streamlit as st
import time

# Page Config for a Professional Technical Look
st.set_page_config(layout="wide", page_title="Databricks Guardian Agent")

# Professional Styling
st.markdown("""
    <style>
    .stApp { background-color: #082535; color: white; }
    .stTextArea textarea { background-color: #1b3139 !important; color: #00f2ff !important; font-family: 'Source Code Pro', monospace; }
    .stButton button { background-color: #ff3621; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧱 Databricks 'Guardian' Agent")
st.subheader("Contextual Enablement & JIT Sandbox Infrastructure")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 🖥️ Databricks SQL Editor")
    query = st.text_area("Workspace: /Users/randall.edwards@aws.com/", 
                        value="SELECT user_id, email, last_login \nFROM prod.hr_data.pii_records \nWHERE region = 'US-EAST';", 
                        height=250)
    
    if st.button("▶️ Execute Query"):
        with st.spinner('Checking Unity Catalog Permissions...'):
            time.sleep(1.5)
            st.error("🚨 [403] PERMISSION_DENIED: User lacks SELECT privilege on 'prod.hr_data.pii_records'. Access to PII restricted by Policy: 'Global_Data_Privacy_v2'.")

with col2:
    st.markdown("### 🤖 Guardian Insights")
    st.info("I've analyzed your request against **Unity Catalog** metadata.")
    
    st.markdown("""
    **The Situation:**
    You are attempting to access PII data in the `prod` catalog. 
    Your current **SSO Group** only allows access to 'Anonymized' or 'Sample' schemas.
    """)

    st.warning("Action Required: Submit a Request in **Immuta** or **Unity Catalog** for permanent access.")

    if st.button("🚀 Hydrate JIT Sandbox"):
        st.write("---")
        st.subheader("⚡ JIT Sandbox Ready")
        st.write("I've provisioned a temporary **Serverless SQL Warehouse** with synthetic data that matches the schema of your target table.")
        st.code("""
-- Use this sandbox table to test your logic while waiting for approval
SELECT user_id, 'REDACTED' as email, last_login 
FROM sandbox.synthetic_hr.pii_records_sample 
WHERE region = 'US-EAST';
        """, language="sql")
        st.success("Outcome: User is unblocked. Organizational Latency reduced by 98%.")
