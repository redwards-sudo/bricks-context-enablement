import streamlit as st
import time

# --- CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Unity Catalog Expert | Databricks PoC")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #11262d; font-family: 'Inter', sans-serif; }
    .centered-text { 
        text-align: center; color: #63757e; margin-top: -10px; margin-bottom: 20px; 
        text-transform: uppercase; letter-spacing: 2px; font-size: 0.75rem; font-weight: 600;
    }
    .sql-card { 
        background-color: #f9fbfb; border: 1px solid #dae0e2; border-radius: 12px; 
        padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    [data-testid="stSidebar"] { background-color: #f0f4f5; border-right: 2px solid #ff3621; padding-top: 30px; }
    .stTextArea textarea { 
        background-color: #ffffff !important; color: #11262d !important; 
        border: 1px solid #cfd8dc !important; font-family: 'JetBrains Mono', monospace; font-size: 15px !important;
    }
    .stButton button { 
        width: 100%; background-color: #ff3621; color: white; font-weight: 600; 
        border-radius: 6px; border: none; height: 3rem; transition: 0.2s ease;
    }
    h1, h2, h3, p, span { color: #11262d !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE MANAGEMENT ---
if 'flow_step' not in st.session_state:
    st.session_state.flow_step = 1

# Initial query state: Pre-filled with the PII-accessing query
if 'query_content' not in st.session_state:
    st.session_state.query_content = "SELECT user_id, full_name, salary \nFROM main.hr_pii.salary_records \nWHERE department = 'Engineering';"

# --- SIDEBAR: THE UNITY CATALOG EXPERT ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/63/Databricks_Logo.png", width=220)
    st.markdown('<p class="centered-text">Governed Enablement Infrastructure</p>', unsafe_allow_html=True)
    st.title("🛡️ Unity Catalog Expert")
    st.write("---")
    
    if st.session_state.flow_step == 1:
        st.info("🟢 **System:** Active")
        st.write("Monitoring workspace telemetry. Review the pre-filled query and click 'Execute' to begin.")
    
    elif st.session_state.flow_step == 2:
        st.error("🚨 **Governance Alert**")
        st.markdown("**Expert Logic:** You are trying to access non-anonymized PII records; let's help you with this.")
        if st.button("Provision Unity Sandbox", key="provision_btn"):
            with st.spinner("Initializing JIT Infrastructure..."):
                time.sleep(1.5)
                st.session_state.flow_step = 3
                # Update content for the sandbox step
                st.session_state.query_content = "SELECT user_id, salary \nFROM synthetic_samples.hr_salary_masked \nWHERE department = 'Engineering';"
                st.rerun()
            
    elif st.session_state.flow_step == 3:
        st.warning("⚡ **JIT Sandbox Active**")
        st.write("Synthetic schema provisioned. Re-run the query using the masked table logic below.")
        st.code("synthetic_samples.hr_salary_masked", language="sql")
        
    elif st.session_state.flow_step == 4:
        st.balloons()
        st.success("✅ **Mastery Verified**")
        st.write("Logic validated. 'Proof of Mastery' synced with your production access request.")
        if st.button("Sync to Learning Dashboard", key="sync_btn"):
            st.session_state.flow_step = 5
            st.rerun()

# --- MAIN WORKSPACE ---
if st.session_state.flow_step < 5:
    st.header("Databricks SQL Editor")
    
    with st.container():
        st.markdown('<div class="sql-card">', unsafe_allow_html=True)
        
        # PHASES 1 & 2: PROD WORKSPACE (PRE-FILLED)
        if st.session_state.flow_step <= 2:
            st.caption("Target: PROD_CLUSTER_MAIN | Catalog: main")
            
            query_input = st.text_area("SQL Workspace", 
                                      value=st.session_state.query_content,
                                      height=250, 
                                      key="prod_editor")
            
            if st.button("▶️ Execute Query", key="exec_prod"):
                if "salary" in query_input.lower() or "pii" in query_input.lower():
                    with st.spinner("Checking Unity Catalog Permissions..."):
                        time.sleep(1.2)
                        st.session_state.flow_step = 2
                        st.rerun()
                else:
                    st.info("Query executed. No PII detected.")
        
        # PHASES 3 & 4: SANDBOX WORKSPACE (PRE-FILLED WITH CORRECTED LOGIC)
        else:
            st.caption("Target: JIT_SANDBOX_881 | Catalog: sandbox")
            sandbox_input = st.text_area("Sandbox Workspace", 
                                        value=st.session_state.query_content,
                                        height=250, 
                                        key="sandbox_editor")
            
            if st.button("▶️ Execute Sandbox Query", key="exec_sandbox"):
                if "synthetic_samples" in sandbox_input.lower():
                    with st.spinner("Validating..."):
                        time.sleep(1)
                        st.session_state.flow_step = 4
                        st.rerun()
                else:
                    st.error("Sandbox Error: Please use the 'synthetic_samples' table as suggested.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# RESULTS DISPLAY (Step 4)
if st.session_state.flow_step == 4:
    st.table([{"user_id": 1024, "salary": "REDACTED"}, {"user_id": 1025, "salary": "REDACTED"}])

# --- PHASE 5: DASHBOARD ---
elif st.session_state.flow_step == 5:
    st.header("📖 Personal Learning Dashboard")
    st.subheader("Continual Enablement Recap")
    st.info("**Incident Event:** At 11:15 AM, you hit a Unity Catalog 403 block. You successfully used a JIT Sandbox to resolve the logic gap.")
    
    st.markdown("### Mastery Verification Challenge")
    choice = st.radio("Which component triggered the Expert assistant?", ["The Spark Engine", "Unity Catalog", "The Hive Metastore"])
    
    if st.button("Submit & Finalize Credential"):
        st.balloons()
        st.success("Verified. Your 'Unity Catalog Expert' badge is now live.")
        if st.button("Reset Presentation"):
            st.session_state.flow_step = 1
            # Reset query to the original problematic one
            st.session_state.query_content = "SELECT user_id, full_name, salary \nFROM main.hr_pii.salary_records \nWHERE department = 'Engineering';"
            st.rerun()
