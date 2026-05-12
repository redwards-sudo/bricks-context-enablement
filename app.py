import streamlit as st
import time

# --- 1. SESSION STATE INITIALIZATION (MUST BE FIRST) ---
# This prevents the NameError by ensuring these keys exist before any logic runs
if 'flow_step' not in st.session_state:
    st.session_state.flow_step = 1

if 'query_content' not in st.session_state:
    st.session_state.query_content = "SELECT user_id, full_name, salary \nFROM main.hr_pii.salary_records \nWHERE department = 'Engineering';"

# Force set the editor key for Step 1
if st.session_state.flow_step == 1:
    st.session_state["prod_editor"] = st.session_state.query_content

# --- 2. CONFIG & THEME ---
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

# --- 3. SIDEBAR: THE UNITY CATALOG EXPERT ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/63/Databricks_Logo.png", width=220)
    st.markdown('<p class="centered-text">Governed Enablement Infrastructure</p>', unsafe_allow_html=True)
    st.title("🛡️ Unity Catalog Expert")
    st.write("---")
    
    if st.session_state.flow_step == 1:
        st.info("🟢 **System:** Active")
        st.write("Monitoring workspace telemetry. Review the pre-filled query and click 'Execute'.")
    
    elif st.session_state.flow_step == 2:
        st.error("🚨 **Governance Alert**")
        st.markdown("**Expert Logic:** You are trying to access non-anonymized PII records; let's help you with this.")
        if st.button("Provision Unity Sandbox", key="provision_btn"):
            with st.spinner("Initializing JIT Infrastructure..."):
                time.sleep(1.5)
                st.session_state.flow_step = 3
                # Update the sandbox editor state directly
                st.session_state["sandbox_editor"] = "SELECT user_id, salary \nFROM synthetic_samples.hr_salary_masked \nWHERE department = 'Engineering';"
                st.rerun()
            
    elif st.session_state.flow_step == 3:
        st.warning("⚡ **JIT Sandbox Active**")
        st.write("Synthetic schema provisioned. Re-run the query using the masked table logic.")
        st.code("synthetic_samples.hr_salary_masked", language="sql")
        
    elif st.session_state.flow_step == 4:
        st.balloons()
        st.success("✅ **Mastery Verified**")
        st.write("Logic validated. 'Proof of Mastery' synced.")
        if st.button("Sync to Learning Dashboard", key="sync_btn"):
            st.session_state.flow_step = 5
            st.rerun()

# --- 4. MAIN WORKSPACE ---
if st.session_state.flow_step < 5:
    st.header("Databricks SQL Editor")
    
    with st.container():
        st.markdown('<div class="sql-card">', unsafe_allow_html=True)
        
        # PHASES 1 & 2: PROD WORKSPACE
        if st.session_state.flow_step <= 2:
            st.caption("Target: PROD_CLUSTER_MAIN | Catalog: main")
            
            query_input = st.text_area("SQL Workspace", 
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
        
        # PHASES 3 & 4: SANDBOX WORKSPACE
        else:
            st.caption("Target: JIT_SANDBOX_881 | Catalog: sandbox")
            
            sandbox_input = st.text_area("Sandbox Workspace", 
                                        height=250, 
                                        key="sandbox_editor")
            
            if st.button("▶️ Execute Sandbox Query", key="exec_sandbox"):
                if "synthetic_samples" in sandbox_input.lower():
                    with st.spinner("Validating..."):
                        time.sleep(1)
                        st.session_state.flow_step = 4
                        st.rerun()
                else:
                    st.error("Sandbox Error: Please use the 'synthetic_samples' table.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# RESULTS TABLE FOR STEP 4
if st.session_state.flow_step == 4:
    st.table([{"user_id": 1024, "salary": "REDACTED"}, {"user_id": 1025, "salary": "REDACTED"}])

# --- 5. PHASE 5: DASHBOARD ---
elif st.session_state.flow_step == 5:
    st.header("📖 Personal Learning Dashboard")
    st.subheader("Continual Enablement Recap")
    st.info("**Incident Event:** You encountered a Unity Catalog 403 block and successfully used a JIT Sandbox to resolve it.")
    
    st.markdown("### Mastery Verification Challenge")
    choice = st.radio("Which component triggered the Expert assistant?", ["The Spark Engine", "Unity Catalog", "The Hive Metastore"])
    
    if st.button("Submit & Finalize Credential"):
        st.balloons()
        st.success("Verified. Your 'Unity Catalog Expert' badge is now live.")
        if st.button("Reset Presentation"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
