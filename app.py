import streamlit as st
import time

# --- 1. SESSION STATE INITIALIZATION ---
if 'flow_step' not in st.session_state:
    st.session_state.flow_step = 1

if 'query_content' not in st.session_state:
    st.session_state.query_content = "SELECT user_id, full_name, salary \nFROM main.hr_pii.salary_records \nWHERE department = 'Engineering';"

# Force set the editor key for Step 1
if st.session_state.flow_step == 1:
    st.session_state["prod_editor"] = st.session_state.query_content

# --- 2. CONFIG & ENHANCED THEME ---
st.set_page_config(layout="wide", page_title="Unity Catalog Expert | Databricks PoC")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #11262d; font-family: 'Inter', sans-serif; }
    .centered-text { 
        text-align: center; color: #63757e; margin-top: -10px; margin-bottom: 20px; 
        text-transform: uppercase; letter-spacing: 2px; font-size: 0.75rem; font-weight: 600;
    }
    /* Distinct Card Styles */
    .prod-card { 
        background-color: #f9fbfb; border: 2px solid #dae0e2; border-radius: 12px; 
        padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .sandbox-card { 
        background-color: #fffdf5; border: 2px solid #ffcc00; border-radius: 12px; 
        padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(255, 204, 0, 0.2);
    }
    /* Sandbox Status Bar */
    .sandbox-header {
        background: #ffcc00; color: #4d3d00 !important; padding: 10px; 
        border-radius: 8px 8px 0 0; font-weight: 700; text-align: center;
        margin-bottom: -1px; font-size: 0.9rem;
    }
    [data-testid="stSidebar"] { background-color: #f0f4f5; border-right: 3px solid #ff3621; padding-top: 30px; }
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
        st.markdown("**Expert Logic:** You are attempting to access raw PII records. I've intercepted this 403 event.")
        if st.button("Provision JIT Sandbox", key="provision_btn"):
            with st.spinner("Executing Delta Deep Clone..."): # Slide 12 Ref
                time.sleep(1.8)
                st.session_state.flow_step = 3
                st.session_state["sandbox_editor"] = "SELECT user_id, salary \nFROM synthetic_samples.hr_salary_masked \nWHERE department = 'Engineering';"
                st.rerun()
    
    elif st.session_state.flow_step == 3:
        st.warning("⚡ **JIT Sandbox Active**")
        st.markdown("""
        **Environment Details:**
        - **Isolation:** Delta Deep Clone 
        - **Compute:** Serverless SQL 
        - **TTL:** 30m (Reaper Job Active) 
        """)
        st.code("synthetic_samples.hr_salary_masked", language="sql")
        
    elif st.session_state.flow_step == 4:
        st.balloons()
        st.success("✅ **Mastery Verified**")
        st.write("Logic validated in sandbox. State transition written to 'mastery_events'.")
        if st.button("Sync to Brick Index", key="sync_btn"):
            st.session_state.flow_step = 5
            st.rerun()

# --- 4. MAIN WORKSPACE ---
if st.session_state.flow_step < 5:
    st.header("Databricks SQL Editor")
    
    # PHASES 1 & 2: PROD WORKSPACE
    if st.session_state.flow_step <= 2:
        st.markdown('<div class="prod-card">', unsafe_allow_html=True)
        st.caption("🔴 TARGET: PROD_CLUSTER_MAIN | Catalog: main")
        
        query_input = st.text_area("SQL Workspace", 
                                  height=250, 
                                  key="prod_editor")
        
        if st.button("▶️ Execute Query", key="exec_prod"):
            if "salary" in query_input.lower() or "pii" in query_input.lower():
                with st.spinner("Unity Catalog Intercepting..."):
                    time.sleep(1.2)
                    st.session_state.flow_step = 2
                    st.rerun()
            else:
                st.info("Query executed on PROD. No governance triggers detected.")
        st.markdown('</div>', unsafe_allow_html=True)

    # PHASES 3 & 4: SANDBOX WORKSPACE (THE VISUAL DELINEATION)
    else:
        st.markdown('<div class="sandbox-header">🚧 EPHEMERAL ANALYTICAL SANDBOX 🚧</div>', unsafe_allow_html=True)
        st.markdown('<div class="sandbox-card">', unsafe_allow_html=True)
        st.caption("🟡 TARGET: JIT_SANDBOX_UC_881 | Catalog: sandbox_catalog")
        
        sandbox_input = st.text_area("Sandbox Workspace (Isolated Metadata)", 
                                    height=250, 
                                    key="sandbox_editor")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("▶️ Execute Sandbox Query", key="exec_sandbox"):
                if "synthetic_samples" in sandbox_input.lower():
                    with st.spinner("Validating Skill Mastery..."):
                        time.sleep(1)
                        st.session_state.flow_step = 4
                        st.rerun()
                else:
                    st.error("Error: Please use the provisioned 'synthetic_samples' replica.")
        with col2:
            st.markdown(f"**Reaper TTL:** 29m 42s")
        
        st.markdown('</div>', unsafe_allow_html=True)

# RESULTS TABLE FOR STEP 4
if st.session_state.flow_step == 4:
    st.subheader("Sandbox Query Results (Masked Output)")
    st.table([{"user_id": 1024, "salary": "#### (MASKED)"}, {"user_id": 1025, "salary": "#### (MASKED)"}])

# --- 5. PHASE 5: BRICK INDEX DASHBOARD ---
elif st.session_state.flow_step == 5:
    st.header("🧱 Practitioner 'Brick Index' Dashboard")
    st.subheader("Competency Growth Tracking")
    st.info("**SCD Type 2 Log:** Transitioned from 'BLOCKED' to 'MASTERED' on Unity Catalog Volume Access.")
    
    st.markdown("### Mastery Verification")
    choice = st.radio("How did we isolate the test environment?", 
                      ["A custom if/then script", "Delta Deep Clone and Serverless SQL", "Shared Prod Clusters"])
    
    if st.button("Finalize Mastery Signal"):
        st.balloons()
        st.success("State Machine Updated. 'Proof of Mastery' synced to Enablement Roadmap[cite: 125].")
        if st.button("Reset Presentation"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
