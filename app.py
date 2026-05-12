# --- MAIN WORKSPACE ---
if st.session_state.flow_step < 5:
    st.header("Databricks SQL Editor")
    
    with st.container():
        st.markdown('<div class="sql-card">', unsafe_allow_html=True)
        
        # PHASES 1 & 2: PROD WORKSPACE
        if st.session_state.flow_step <= 2:
            st.caption("Target: PROD_CLUSTER_MAIN | Catalog: main")
            
            # DEBUG FIX: Force the session state key to match the intended content
            if "prod_editor" not in st.session_state or st.session_state.flow_step == 1:
                st.session_state["prod_editor"] = "SELECT user_id, full_name, salary \nFROM main.hr_pii.salary_records \nWHERE department = 'Engineering';"

            query_input = st.text_area("SQL Workspace", 
                                      height=250, 
                                      key="prod_editor") # Value is now driven by the key
            
            if st.button("▶️ Execute Query", key="exec_prod"):
                if "salary" in query_input.lower() or "pii" in query_input.lower():
                    with st.spinner("Checking Unity Catalog Permissions..."):
                        time.sleep(1.2)
                        st.session_state.flow_step = 2
                        st.rerun()
        
        # PHASES 3 & 4: SANDBOX WORKSPACE
        else:
            st.caption("Target: JIT_SANDBOX_881 | Catalog: sandbox")
            
            # DEBUG FIX: Update the sandbox key when entering step 3
            if st.session_state.flow_step == 3:
                st.session_state["sandbox_editor"] = "SELECT user_id, salary \nFROM synthetic_samples.hr_salary_masked \nWHERE department = 'Engineering';"

            sandbox_input = st.text_area("Sandbox Workspace", 
                                        height=250, 
                                        key="sandbox_editor")
            
            if st.button("▶️ Execute Sandbox Query", key="exec_sandbox"):
                if "synthetic_samples" in sandbox_input.lower():
                    with st.spinner("Validating..."):
                        time.sleep(1)
                        st.session_state.flow_step = 4
                        st.rerun()
