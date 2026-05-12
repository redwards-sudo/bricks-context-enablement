import streamlit as st
import time

# --- CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Unity Guide | Databricks PoC")

# CSS: Professional Light Mode UI
st.markdown("""
    <style>
    /* Main Background and Typography */
    .stApp { background-color: #FFFFFF; color: #11262d; font-family: 'Inter', sans-serif; }
    
    /* Centering and Styling Subheader */
    .centered-text { 
        text-align: center; 
        color: #63757e; 
        margin-top: -10px;
        margin-bottom: 20px; 
        text-transform: uppercase; 
        letter-spacing: 2px; 
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* Section Separation - Clean Cards */
    .sql-card { 
        background-color: #f9fbfb; 
        border: 1px solid #dae0e2; 
        border-radius: 12px; 
        padding: 25px; 
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Assistant Sidebar - Distinct Light Gray */
    [data-testid="stSidebar"] { 
        background-color: #f0f4f5; 
        border-right: 2px solid #ff3621; 
        padding-top: 30px; 
    }
    
    /* SQL Editor Styling - Light Mode Syntax Feel */
    .stTextArea textarea { 
        background-color: #ffffff !important; 
        color: #11262d !important; 
        border: 1px solid #cfd8dc !important; 
        font-family: 'JetBrains Mono', monospace;
        font-size: 15px !important;
        border-radius: 4px;
    }
    
    /* Buttons - Databricks Red */
    .stButton button { 
        width: 100%; 
        background-color: #ff3621; 
        color: white; 
        font-weight: 600; 
        border-radius: 6px;
        border: none;
        height: 3rem;
        transition: 0.2s ease;
    }
    .stButton button:hover { background-color: #e6311e; box-shadow: 0 4px 8px rgba(255,54,33,0.2); }
    
    /* Text Color Fixes for Light Mode */
    h1, h2, h3, p, span { color: #11262d !important; }
    .stMarkdown p { color: #40565d !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE MANAGEMENT ---
if 'flow_step' not in st.session_state:
    st.session_state.flow_step = 1

# --- SIDEBAR: THE UNITY GUIDE ---
with st.sidebar:
    # Logo and Subheader
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/63/Databricks_Logo.png", width=220)
    st.markdown('<p class="centered-text">Governed Enablement Infrastructure</p>', unsafe_allow_html=True)
    st.title("🛡️ Unity Catalog Guide")
    st.write("---")
    
    if st.session_state.flow_step == 1:
        st.info("🟢 **System:** Active")
        st.write("I am monitoring workspace telemetry. Enter a query to begin.")
    
    elif st.session_state.flow_step == 2:
        st.error("🚨 **Governance Alert**")
        st.markdown("**Expert Logic:** You are trying to access non-anonymized PII records; let's help you with this.")
        if st.button("Provision Unity Sandbox"):
            with st.spinner("Initializing JIT Infrastructure..."):
                time.sleep(1.5)
                st.session_state.flow_step = 3
                st.rerun()
            
    elif st.session_state.flow_step == 3:
        st.warning("⚡ **JIT Sandbox Active**")
        st.write("I've provisioned a synthetic schema. **Action Required:** Re-run your query logic using the sanitized table:")
        st.code("synthetic_samples.hr_salary_masked", language="sql")
        
    elif st.session_state.flow_step == 4:
        st.balloons()
        st.success("✅ **Mastery Verified**")
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
            st.caption("Target: PROD_CLUSTER_MAIN | Catalog: main")
            
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
            st.caption("Target: JIT_SANDBOX_881 | Catalog: sandbox")
            sandbox_input = st.text_area("Sandbox Workspace", placeholder="-- Use the synthetic table provided by the Expert...", height=300)
            
            if st.button("▶️ Execute Sandbox Query"):
                if "synthetic_samples" in sandbox_input.lower():
                    with st.spinner("Validating against synthetic data..."):
                        time.sleep(1)
                        st.success("Query Validated. Logic matches synthetic schema constraints.")
                        st.table([{"user_id": 1024, "salary": "REDACTED"}, {"user_id": 1025, "salary": "REDACTED"}])
                        st.session_state.flow_step = 4
                else:
                    st.error("Sandbox Error: Table not found. Please use the table suggested by the Unity Guide.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- PHASE 5: CONTINUAL LEARNING DASHBOARD ---
else:
    st.header("📖 Personal Learning Dashboard")
    st.subheader("Continual Enablement Recap")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("**Incident Event:** At 11:15 AM, you hit a Unity Catalog 403 block. You successfully used a JIT Sandbox to resolve the logic gap.")
    
    with col_b:
        st.success("**Knowledge Milestone:** You demonstrated the ability to operate within PII masking frameworks. This session is now synced to your profile.")

    st.markdown("---")
    st.markdown("### Mastery Verification Challenge")
    st.write("Which Databricks component identified the PII restriction and triggered the Expert assistant?")
    choice = st.radio("Select the correct architectural layer:", [
        "The Spark Engine",
        "Unity Catalog",
        "The Hive Metastore"
    ])
    
    if st.button("Submit & Finalize Credential"):
        st.balloons()
        st.success("Verified. Your 'Unity Catalog Guide' badge is now live.")
        if st.button("Reset Presentation"):
            st.session_state.flow_step = 1
            st.rerun()
