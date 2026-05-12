import streamlit as st
import time

# --- CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Unity Catalog Expert | Databricks PoC")

st.markdown("""
    <style>
    .stApp { background-color: #0b141a; color: #f9f9f9; font-family: 'Inter', sans-serif; }
    .centered-text { 
        text-align: center; color: #8b949e; margin-top: -10px; margin-bottom: 20px; 
        text-transform: uppercase; letter-spacing: 2px; font-size: 0.75rem; font-weight: 600;
    }
    .sql-card { 
        background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 2px solid #ff3621; padding-top: 30px; }
    .stTextArea textarea { 
        background-color: #0d1117 !important; color: #58a6ff !important; 
        border: 1px solid #30363d !important; font-family: 'JetBrains Mono', monospace; font-size: 15px !important;
    }
    .stButton button { 
        width: 100%; background-color: #ff3621; color: white; font-weight: 600; 
        border-radius: 6px; border: none; height: 3rem; transition: 0.3s ease;
    }
    .stButton button:hover { background-color: #e6311e; transform: translateY(-1px); }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'flow_step' not in st.session_state:
    st.session_state.flow_step = 1

# --- SIDEBAR: THE UNITY CATALOG EXPERT ---
with st.sidebar:
    st.image("https://commons.wikimedia.org/wiki/File:Databricks_Logo.png", width=220)
    st.markdown('<p class="centered-text">Unity Catalog Expert</p>', unsafe_allow_html=True)
    st.title("🛡️ Your AI Assistant")
    st.write("---")
    
    if st.session_state.flow_step == 1:
        st.success("🟢 Monitoring Workspace")
        st.caption("Listening for Unity Catalog telemetry signals...")
    
    elif st.session_state.flow_step == 2:
        st.error("🚨 Governance Alert")
        st.info("**Expert Logic:** You are trying to access non-anonymized PII records; let's help you with this.")
        if st.button("Provision Unity Sandbox"):
            with st.spinner("Initializing JIT Infrastructure..."):
                time.sleep(1.5)
                st.session_state.flow_step = 3
                st.rerun()
            
    elif st.session_state.flow_step == 3:
        st.warning("⚡ JIT Sandbox Active")
        st.write("I've provisioned a synthetic schema. **Action Required:** Re-run your query logic using the sanitized table:")
        st.code("synthetic_samples.hr_salary_masked", language="sql")
        
    elif st.session_state.flow_step == 4:
        st.balloons()
        st.success("✅ Mastery Verified")
        st.write("Your logic respects masking policies. 'Proof of Mastery' has been synced with your production access request.")
        if st.button("Sync to Learning Dashboard"):
            st.session_state.flow_step = 5
            st.rerun()

# --- MAIN WORKSPACE ---
if st.session_state.flow_step < 5:
    st.header("Databricks SQL Editor")
    
    with st.container():
        st.markdown('<div class="sql-card">', unsafe_allow_html=True)
        
        # PHASES 1 & 2: THE "CLEAN SLATE" WORKSPACE
        if st.session_state.flow_step <= 2:
            st.caption("Target: PROD_CLUSTER_MAIN | Catalog: main | User: randall.edwards")
            query_input = st.text_area("SQL Workspace", placeholder="e.g., SELECT * FROM main.hr_pii.salary_records;", height=300)
            
            if st.button("▶️ Execute Query"):
                if not query_input:
                    st.warning("Please input a query to monitor telemetry.")
                elif "salary" in query_input.lower() or "pii" in query_input.lower():
                    with st.spinner("Checking Unity Catalog Permissions..."):
                        time.sleep(1.2)
                        st.error("Error: [403] PERMISSION_DENIED. Access to 'main.hr_pii' is restricted by Global Governance Policy.")
                        st.session_state.flow_step = 2
                        st.rerun()
                else:
                    st.info("Query executed. Results returned (No PII detected).")
        
        # PHASES 3 & 4: THE SANDBOX VALIDATION
        else:
            st.caption("Target: JIT_SANDBOX_881 | Catalog: sandbox | Mode: Verification")
            sandbox_input = st.text_area("Sandbox Workspace", placeholder="-- Use the synthetic table provided by the Expert...", height=300)
            
            if st.button("▶️ Execute Sandbox Query"):
                if "synthetic_samples" in sandbox_input.lower():
                    with st.spinner("Validating against synthetic data..."):
                        time.sleep(1)
                        st.success("Query Validated. Logic matches synthetic schema constraints.")
                        st.table([{"user_id": 1024, "salary": "REDACTED"}, {"user_id": 1025, "salary": "REDACTED"}])
                        st.session_state.flow_step = 4
                else:
                    st.error("Sandbox Error: Table not found. Please use the table suggested by the Unity Catalog Expert.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- PHASE 5: CONTINUAL LEARNING DASHBOARD ---
else:
    st.header("📖 Personal Learning Dashboard")
    st.subheader("Continual Enablement Recap")
    st.info("**The Incident Event:** At 11:15 AM, you hit a Unity Catalog 403 block. You successfully used a JIT Sandbox to resolve the logic gap.")
    st.markdown("---")
    st.markdown("### Mastery Verification Challenge")
    st.write("Which Databricks component identified the PII restriction and triggered the Expert assistant?")
    choice = st.radio("Select the correct architectural layer:", ["The Spark Engine", "Unity Catalog", "The Hive Metastore"])
    
    if st.button("Submit & Finalize Credential"):
        st.balloons()
        st.success("Verified. Your 'Unity Catalog Expert' badge is now live in your Databricks profile.")
        if st.button("Reset Presentation"):
            st.session_state.flow_step = 1
            st.rerun()
