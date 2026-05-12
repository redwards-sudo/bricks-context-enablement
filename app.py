import streamlit as st
import time

# --- CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Unity Pilot | AI Assistant")

# Professional Databricks-inspired Styling
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

# --- SIDEBAR (THE "PILOT" LOGIC) ---
with st.sidebar:
    st.title("🧩 Unity Pilot")
    st.markdown("**Your Unity Catalog Expert**")
    st.markdown("---")
    
    if st.session_state.flow_step == 1:
        st.write("🛰️ **Status:** Monitoring Workspace")
        st.caption("Listening for Unity Catalog signals...")
    elif st.session_state.flow_step == 2:
        st.warning("🚨 **Permission Block**")
        st.write("**Target:** `main.hr_pii.salary_records`")
        st.write("**Logic:** You are trying to access non-anonymized PII records; let's help you with this.")
        if st.button("Provision Unity Sandbox"):
            st.session_state.flow_step = 3
            st.rerun()
    elif st.session_state.flow_step == 3:
        st.success("⚡ **Sandbox Active**")
        st.write("**Environment:** Serverless Node 881")
        st.write("**Dataset:** Synthetic Masked Sample")
    elif st.session_state.flow_step == 4:
        st.balloons()
        st.success("✅ **Mastery Verified**")
        st.write("Validation metadata sent to Admin.")

# --- MAIN WORKSPACE ---
st.header("Databricks SQL Editor")

col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.flow_step < 3:
        # STEP 1: The Production Attempt
        st.caption("Production Workspace: `/main/hr_data/`")
        query = st.text_area("SQL Editor", 
                            value="SELECT * FROM main.hr_pii.salary_records LIMIT 10;", 
                            height=250)
        if st.button("Run Query"):
            with st.spinner("Executing..."):
                time.sleep(1)
                st.error("Error: [403] User lacks permissions. Access to 'main.hr_pii' is restricted by Global Governance Policy.")
                st.session_state.flow_step = 2
                st.rerun()
    else:
        # STEP 3: The Sandbox Success
        st.caption("📍 Working in: `temp_unity_sandbox_session_881`")
        sandbox_query = st.text_area("Sandbox Editor", 
                                    value="SELECT user_id, 'REDACTED' as salary FROM synthetic_samples.hr_salary;", 
                                    height=250)
        if st.button("Validate in Sandbox"):
            with st.spinner("Validating logic..."):
                time.sleep(1)
                st.table([{"user_id": 1, "salary": "REDACTED"}, {"user_id": 2, "salary": "REDACTED"}])
                st.session_state.flow_step = 4

with col2:
    st.subheader("Unity Pilot Insights")
    if st.session_state.flow_step == 1:
        st.write("I am monitoring your workspace telemetry. If you hit a technical or governance hurdle, I will provide real-time 'hydration'.")
    
    if st.session_state.flow_step == 2:
        st.info("I've identified the permission block in **Unity Catalog**. Instead of stopping work, let's validate your query logic in a synthetic sandbox.")
    
    if st.session_state.flow_step == 3:
        st.write("Run the query in the Sandbox to demonstrate you can handle masked data correctly. This verifies your mastery to the Admin team.")
    
    if st.session_state.flow_step == 4:
        st.markdown("### Next Steps")
        st.write("Your logic is verified. I've prepared a pre-filled access request with your validation metadata.")
        if st.button("📝 Submit Access Request"):
            st.info("Request #4492 submitted to Unity Catalog Governance Team.")
        if st.button("Reset Demo"):
            st.session_state.flow_step = 1
            st.rerun()
