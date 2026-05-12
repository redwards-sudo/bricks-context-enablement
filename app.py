import streamlit as st
import time

# --- CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Unity Catalog Expert | Databricks PoC")

# CSS: Professional "Lakehouse" UI with distinct sections
st.markdown("""
    <style>
    /* Main Background and Typography */
    .stApp { background-color: #0b141a; color: #f9f9f9; font-family: 'Inter', sans-serif; }
    
    /* Centering the Subheader */
    .centered-text { text-align: center; color: #8b949e; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; font-size: 0.8rem; }
    
    /* SQL Editor Card */
    .sql-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
    
    /* Sidebar Branding */
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #ff3621; padding-top: 20px; }
    
    /* SQL Text Area */
    .stTextArea textarea { 
        background-color: #0d1117 !important; 
        color: #58a6ff !important; 
        border: 1px solid #30363d !important; 
        font-family: 'JetBrains Mono', monospace;
        font-size: 15px !important;
    }
    
    /* Buttons */
    .stButton button { 
        width: 100%; 
        background-color: #ff3621; 
        color: white; 
        font-weight: 600; 
        border-radius: 4px;
        border: none;
        transition: 0.3s;
    }
    .stButton button:hover { background-color: #e6311e; transform: translateY(-1px); }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'flow_step' not in st.session_state:
    st.session_state.flow_step = 1

# --- SIDEBAR: THE UNITY CATALOG EXPERT ---
with st.sidebar:
    # Databricks Logo
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/63/Databricks_Logo.png", width=200)
    st.markdown('<p class="centered-text">Governed Enablement Infrastructure</p>', unsafe_allow_html=True)
    st.title("🛡️ Unity Catalog Expert")
    st.write("---")
    
    if st.session_state.flow_step == 1:
        st.success("🟢 Monitoring Workspace")
        st.caption("Awaiting telemetry signals from the SQL Editor...")
    
    elif st.session_state.flow_step == 2:
        st.error("🚨 Governance Alert")
        st.info("**Expert Logic:** You are trying to access non-anonymized PII records; let's help you with this.")
        if st.button("Provision Unity Sandbox"):
            with st.spinner("Initializing Serverless Compute..."):
                time.sleep(1.5)
                st.session_state.flow_step = 3
                st.rerun()
            
    elif st.session_state.flow_step == 3:
        st.warning("⚡ JIT Sandbox Active")
        st.write("I've provisioned a synthetic schema. **Action:** Re-run your query logic using the sanitized table:")
        st.code("synthetic_samples.hr_salary_masked", language="sql")
        
    elif st.session_state.flow_step == 4:
        st.balloons()
        st.success("✅ Mastery Verified")
        st.write("Your logic respects masking policies. I have synced this 'Proof of Mastery' with your production access request.")
        if st.button("Complete & Sync Dashboard"):
            st.session_state.flow_step = 5
            st.rerun()

# --- MAIN WORKSPACE ---
if st.session_state.flow_step < 5:
    st.header("Databricks SQL Editor")
    
    # CARD 1: THE EDITOR
    with st.container():
        st.markdown('<div class="sql-card">', unsafe_allow_html=True)
        
        if st.session_state.flow_step <= 2:
            st.caption("Target Environment: PROD_CLUSTER_MAIN | Catalog: main")
            # Start with a clear/blank editor
            query_input = st.text_area("SQL Workspace", placeholder="SELECT * FROM main.hr_pii.salary_records;", height=300)
            
            if st.button("▶️ Execute Query"):
                if not query_input:
                    st.warning("Please input a query to monitor telemetry.")
                elif "salary" in query_input.lower() or "pii" in query_input.lower():
                    with st.spinner("Checking Unity Catalog Permissions..."):
                        time.sleep(1)
                        st.error("Error: [403] PERMISSION_DENIED. Access to non-anonymized PII is restricted by Global Policy.")
                        st.session_state.flow_step = 2
                        st.rerun()
                else:
                    st.info("Query executed. No governance triggers detected.")
        
        else:
            # SANDBOX EDITOR
            st.caption("Target Environment: JIT_SANDBOX_881 | Catalog: sandbox")
            sandbox_input = st.text_area("Sandbox Workspace", placeholder="-- Paste query logic using synthetic_samples table...", height=300)
            
            if st.button("▶️ Execute Sandbox Query"):
                if "synthetic_samples" in sandbox_input.lower():
                    with st.spinner("Validating against synthetic data..."):
                        time.sleep(1)
                        st.success("Query Successful. 2 rows returned (Masked).")
                        st.table([{"user_id": 1024, "salary": "REDACTED"}, {"user_id": 1025, "salary": "REDACTED"}])
                        st.session_state.flow_step = 4
                else:
                    st.error("Sandbox Error: Table not found. Please use the 'synthetic_samples' table provided by the Expert.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- STEP 5: CONTINUAL LEARNING DASHBOARD ---
else:
    st.header("📖 Personal Learning Dashboard")
    st.subheader("Daily Recap: Governance & PII Masking")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("**The 'Struggle' Event:** \n\nAt 11:15 AM, you hit a Unity Catalog 403 block on `main.hr_pii`. You successfully used a JIT Sandbox to resolve the logic gap.")
    
    with col_b:
        st.success("**Mastery Earned:** \n\nYou demonstrated ability to operate within PII masking frameworks. Your 'Unity Catalog Practitioner' badge is now active.")

    st.markdown("---")
    st.markdown("### Mastery Challenge")
    st.write("Why was your initial query blocked by the Expert?")
    choice = st.radio("Select the correct reason:", [
        "The cluster was down.",
        "Unity Catalog identified PII in the schema with no authorized 'SELECT' privilege.",
        "The syntax was incorrect."
    ])
    
    if st.button("Submit & Finalize"):
        st.balloons()
        st.success("Correct. You've closed the loop for today's learning.")
        if st.button("Reset Presentation"):
            st.session_state.flow_step = 1
            st.rerun()
