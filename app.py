import streamlit as st
import time

# --- 1. SESSION STATE INITIALIZATION ---
if 'flow_step' not in st.session_state:
    st.session_state.flow_step = 1

if 'query_content' not in st.session_state:
    st.session_state.query_content = "SELECT user_id, full_name, salary \nFROM main.hr_pii.salary_records \nWHERE department = 'Engineering';"

if st.session_state.flow_step == 1:
    st.session_state["prod_editor"] = st.session_state.query_content

# --- 2. CONFIG & THEME (CONSISTENT FORMATTING) ---
st.set_page_config(layout="wide", page_title="Unity Catalog Expert | Databricks PoC")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #11262d; font-family: 'Inter', sans-serif; }
    
    /* Standardized Text Sizing */
    p, span, label, .stMarkdown { font-size: 16px !important; line-height: 1.6; }
    .stCaption { font-size: 14px !important; font-weight: 500; }
    
    /* Environment Headers */
    .env-header-prod {
        background-color: #11262d; color: #ffffff !important; padding: 12px;
        border-radius: 8px 8px 0 0; text-align: center; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: -1px;
    }
    .env-header-non-prod {
        background-color: #ff3621; color: #ffffff !important; padding: 12px;
        border-radius: 8px 8px 0 0; text-align: center; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: -1px;
    }

    /* Container Styles */
    .workspace-card { 
        background-color: #f9fbfb; border: 1px solid #dae0e2; border-radius: 0 0 12px 12px; 
        padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    [data-testid="stSidebar"] { background-color: #f0f4f5; border-right: 3px solid #ff3621; }
    .stTextArea textarea { 
        background-color: #ffffff !important; border: 1px solid #cfd8dc !important; 
        font-family: 'JetBrains Mono', monospace; font-size: 15px !important;
    }
    .stButton button { 
        background-color: #ff3621; color: white; font-weight: 600; 
        border-radius: 6px; border: none; height: 3.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: THE UNITY CATALOG EXPERT ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/63/Databricks_Logo.png", width=220)
    st.title("🛡️ Unity Catalog Expert")
    st.write("---")
    
    if st.session_state.flow_step <= 2:
        st.info("🟢 **System Monitoring:** Active")
        st.write("Current Workspace: **PROD_MAIN**")
    
    elif st.session_state.flow_step == 3:
        st.warning("⚡ **Intervention Active**")
        st.markdown("**Status:** User is now in a safe, non-production environment.")
        if st.button("Provision Enablement Table"):
            with st.spinner("Executing Delta Deep Clone..."):
                time.sleep(1.5)
                st.session_state.flow_step = 4
                st.session_state["sandbox_editor"] = "SELECT user_id, salary \nFROM synthetic_samples.hr_salary_masked \nWHERE department = 'Engineering';"
                st.rerun()

    elif st.session_state.flow_step == 4:
        st.success("✅ **Sandbox Ready**")
        st.write("Run the masked query to verify your access logic.")

# --- 4. MAIN WORKSPACE ---
if st.session_state.flow_step < 5:
    st.header("Databricks SQL Workspace")
    
    # PRODUCTION FLOW
    if st.session_state.flow_step <= 2:
        st.markdown('<div class="env-header-prod">Production Environment - Live Cluster</div>', unsafe_allow_html=True)
        st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
        st.caption("Context: main.hr_pii | Restricted Access")
        
        query_input = st.text_area("SQL Editor", height=250, key="prod_editor")
        
        if st.button("▶️ Execute Query", key="exec_prod"):
            if "salary" in query_input.lower() or "pii" in query_input.lower():
                with st.spinner("Checking Governance Policies..."):
                    time.sleep(1.2)
                    st.session_state.flow_step = 2 # Trigger block
                    st.rerun()
        
        if st.session_state.flow_step == 2:
            st.error("**HTTP 403: FORBIDDEN** - Direct access to PII records is restricted by Unity Catalog.")
            if st.button("Launch Unblocking Assistant"):
                st.session_state.flow_step = 3
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # NON-PRODUCTION FLOW (THE VISUAL DELINEATION)
    else:
        st.markdown('<div class="env-header-non-prod">Non-Production Environment - Enablement Sandbox</div>', unsafe_allow_html=True)
        st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
        st.caption("Context: sandbox.synthetic_data | Zero Production Risk")
        
        sandbox_input = st.text_area("Sandbox Editor", height=250, key="sandbox_editor")
        
        if st.button("▶️ Execute Validated Query", key="exec_sandbox"):
            if "synthetic_samples" in sandbox_input.lower():
                st.session_state.flow_step = 5 # Move to Mastery
                st.rerun()
            else:
                st.error("Governance Tip: Use the provisioned 'synthetic_samples' table to maintain compliance.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. MASTERY & FEEDBACK (UPDATED QUESTION) ---
elif st.session_state.flow_step == 5:
    st.header("Mastery Verification Dashboard")
    st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
    st.success("Query Successful! You have successfully accessed masked data in a safe environment.")
    
    st.subheader("Knowledge Check")
    st.write("To finalize your 'Brick Index' update, please answer the following:")
    
    q1 = st.radio("**What triggered the initial access block in the Production environment?**", 
                  ["The query syntax was incorrect", 
                   "Unauthorized access to raw PII/Salary records", 
                   "The cluster was down for maintenance"])
    
    q2 = st.radio("**How was your workflow successfully unblocked?**", 
                  ["An admin manually approved a Jira ticket", 
                   "You waited 48 hours for permission sync", 
                   "The system provisioned a synthetic, masked replica of the data for safe testing"])
    
    if st.button("Submit & Sync Mastery"):
        if "PII" in q1 and "synthetic" in q2:
            st.balloons()
            st.success("Skill internalised. Transitioning back to Production with verified expertise.")
            if st.button("Restart Demonstration"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()
        else:
            st.warning("Review the problem/solution flow and try again.")
    st.markdown('</div>', unsafe_allow_html=True)
