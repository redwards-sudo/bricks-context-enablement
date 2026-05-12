import streamlit as st
import time

# --- CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Unity Catalog Expert | Enablement PoC")

st.markdown("""
    <style>
    .stApp { background-color: #11262d; color: #f9f9f9; }
    .stTextArea textarea { background-color: #1b3139 !important; color: #00f2ff !important; border: 1px solid #3c5e6b; }
    .stButton button { width: 100%; background-color: #ff3621; color: white; font-weight: bold; }
    .stAlert { background-color: #1b3139; border: 1px solid #3c5e6b; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'flow_step' not in st.session_state:
    st.session_state.flow_step = 1

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Your Unity Catalog Expert")
    st.markdown("**Governed Enablement Infrastructure**")
    st.markdown("---")
    
    steps = ["Monitoring", "Block Detected", "Sandbox Active", "Validation Complete", "Learning Follow-up"]
    st.write(f"**Current Phase:** {steps[st.session_state.flow_step-1]}")
    
    if st.session_state.flow_step == 2:
        if st.button("Provision Unity Sandbox"):
            st.session_state.flow_step = 3
            st.rerun()
    elif st.session_state.flow_step == 4:
        st.success("✅ Logic Verified")
        if st.button("End Session & Sync Learning"):
            st.session_state.flow_step = 5
            st.rerun()

# --- MAIN WORKSPACE ---
col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.flow_step < 5:
        st.header("Databricks SQL Editor")
        if st.session_state.flow_step < 3:
            st.caption("Production Workspace: `/main/hr_data/`")
            query = st.text_area("SQL Editor", value="SELECT * FROM main.hr_pii.salary_records LIMIT 10;", height=200)
            if st.button("Run Query"):
                st.error("Error: [403] PERMISSION_DENIED. Access to 'main.hr_pii' is restricted.")
                st.session_state.flow_step = 2
                st.rerun()
        else:
            st.caption("📍 Working in: `temp_unity_sandbox_session_881`")
            st.text_area("Sandbox Editor", value="SELECT user_id, 'REDACTED' as salary FROM synthetic_samples.hr_salary;", height=200)
            if st.button("Validate in Sandbox"):
                st.table([{"user_id": 1, "salary": "REDACTED"}])
                st.session_state.flow_step = 4
    else:
        # STEP 5: THE CONTINUAL LEARNING MODULE
        st.header("📖 Personal Learning Dashboard")
        st.subheader("Daily Recap: Governance & PII Masking")
        st.write("Earlier today, you encountered a **Unity Catalog 403 Block**. Great job using the Sandbox to validate your logic!")
        
        st.info("**Deep Dive:** Why is `main.hr_pii` restricted? \n\nThis schema contains Tier-1 sensitive data. By using the 'Masked' view, you reduced company risk while maintaining project velocity.")
        
        st.markdown("### Mastery Challenge")
        choice = st.radio("Which system allows for centralized access control across the Databricks Lakehouse?", ["Unity Catalog", "Delta Lake", "Hive Metastore"])
        if st.button("Submit Answer"):
            st.balloons()
            st.success("Correct! You've earned the **'Unity Catalog Power User'** badge.")

with col2:
    st.subheader("Expert Insights")
    if st.session_state.flow_step == 1:
        st.write("I am monitoring your workspace telemetry. If you hit a technical or governance hurdle, I will provide real-time 'hydration'.")
    elif st.session_state.flow_step == 2:
        st.info("**Logic:** You are trying to access non-anonymized PII records; let's help you with this.")
        st.write("Instead of a support ticket, let's validate your query logic in a synthetic sandbox environment.")
    elif st.session_state.flow_step == 4:
        st.write("Your mastery is verified. I've prepared your access request and scheduled a deep-dive module for later today.")
    elif st.session_state.flow_step == 5:
        st.write("This is the 'Continual' phase. We turn point-in-time friction into long-term organizational knowledge.")
        if st.button("Restart Scenario"):
            st.session_state.flow_step = 1
            st.rerun()
