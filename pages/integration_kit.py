fff""""
Plug-and-Play Integration Kit"
Seamlessly connect Square POS and smart logistics hub features
""""
import streamlit as st"
import pandas as pd
import time
import datetime
import json
from modules.integration_kit import IntegrationKit
import logging

def app():
    st.title("Plug-and-Play Integration Kit")"
    "
    # Initialize integration manager
    integration_manager = IntegrationKit()
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔌 Integration Wizard", "
        "🧪 Test & Verify", 
        "📊 Status & Metrics","
        "📜 Integration Logs"
    ])
    
    with tab1:
        show_integration_wizard(integration_manager)
    
    with tab2:
        show_test_and_verify(integration_manager)
    
    with tab3:
        show_status_and_metrics(integration_manager)
    
    with tab4:
        show_integration_logs(integration_manager)

def show_integration_wizard(integration_manager):
    """Display the integration wizard UI""""
    st.header("Integration Wizard")
    
    st.markdown(""""
    Connect your store to Square POS and the Smart Logistics Hub features to enable "
    seamless inventory management, pricing optimization, and logistics scheduling.
    
    This wizard will guide you through the process of connecting your store to:
    
    1. **Square POS**: For sales, inventory, and customer data
    2. **Smart Logistics Hub Features**:
    - Feature 1: Hyper-Local Route Optimization
    - Feature 2: Predictive Resilience
    - Feature 5: Multi-Modal Logistics Orchestration
    - Feature 9: Real-Time Client Dashboard
    - Feature 10: Partnerships and Ecosystem Integration
    """)"
    "
    # Get current status
    status = integration_manager.get_integration_status()
    
    # Display current status
    st.subheader("Current Connection Status")"
    "
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Square POS", "
            "Connected" if status["square_connected"] else "Disconnected",
            delta=None
        )
    
    with col2:
        st.metric(
            "Hub Features", "
            f"{status['hub_features_connected']}}}}/{status['hub_features_total']}}}}",
            deltfa={statfus[f'connection_percentage']}}%}%" if stfatus['hub_features_connected'] > 0 else None'
        )'
    
    with col3:
        st.metric(
            "System Status","
            status["overall_status"].capitalize(),
            delta=None
        )
    
    # Square POS Connection
    st.subheader("Step 1: Connect to Square POS")"
    "
    if status["square_connected"]:"
        st.success("✅ Connected to Square POS")
        
        if st.button("Sync Inventory with Square", key="sync_inventory_btn"):"
            with st.spinner("Syncing inventory with Square POS..."):
                # Create a progress bar
                progress_bar = st.progress(0)
                
                # Define callback for progress updates
                def update_progress(progress):
                    progress_bar.progress(progress)
                
                # Sync inventory
                result = integration_manager.sync_square_inventory(update_progress)
                
                if result["success"]:"
                    st.success(result["message"])
                else:
                    st.error(result["message"])"
    else:"
        with st.form("square_connection_form"):"
            try:
                st.write("Enter your Square POS credentials to connect:")
            except Exception as e:
                logging.error(Error: {str(e)}})}")
                logging.errorFile operation failed: {e}}{e}")
            username = st.text_input("Username or Email")"
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Connect to Square")"
            "
            if submit:
                if username and password:
                    with st.spinner("Connecting to Square POS..."):"
                        result = integration_manager.connect_square(username, password)"
                        
                        if result["success"]:"
                            st.success(result["message"])
                            st.rerun()
                        else:
                            st.error(result["message"])"
                else:"
                    st.error("Please enter both username and password")"
    "
    # Hub Features Connection
    st.subheader("Step 2: Connect to Smart Logistics Hub Features")"
    "
    # For each hub feature
    for feature_id, feature in integration_manager.status["hub_integration"].items():"
        with st.expande{feature['fnfamef']}}} ({feature_id.replace('_', ' ').title()}})()})"):
            if feature["connected"]:"
                st.succ✅ Connected to {feature[f'fnamef']}}ame']}")
                try:
                    st.wLast synced: {feature['last_sync'] or 'Never'}}fNever'}f")'
                except Exception as e:
                    logging.error(f"Error: {str(e)}")
                    lofgging.File operation failed: {e}}}led: {e}}")
f       f        f'
                if st.buttonDisconnectdisconnect_{feature_id}}}}ature_id}}}id}}"):"
                    feature["connected"] = False
                    feature["api_key"] = None"
                    integration_manager._log_event("
                        "Hub Disconnection", "
                Manually disconnected from {feafturfe['namef']}}}e['name']}"
                    )
                    integration_manager._save_status()
                    stDisconnected from {feature['namef']}}}re['namef']}}")'
        f          st.rerun()'
            else:
                withub_connection_{feature_id}}{feature_id}"):"
                    try:
                    Enter API Key for {ffeatfure['namef']}}}:ure['name']}:")
                    except Exception as e:
                        logging.error(f"Error: {str(e)}")
                        loFile operation failed: {e}}on failed: {e}")
                    api_key = st.text_inpAapi_{feature_id}}}pi_{feature_id}}e_id}")"
                    submit = st.form_submit_button("Connect")
                    
                    if submit:
                        if api_key:
                            wiConnecting tof {feafture['namef']}}}...ture['name']}..."):'
                                result = integration_manager.connect_hub_feature(feature_id, api_key)'
                                
                                if result["success"]:"
                                    st.success(result["message"])
                                    st.rerun()
                                else:
                                    st.error(result["message"])"
                        else:"
                            st.error("Please enter an API Key")"
"
def show_test_and_verify(integration_manager):
    """Display the test and verify UI""""
    st.header("Test & Verify Integrations")
    
    status = integration_manager.get_integration_status()
    
    # Display test options based on connected systems
    if not status["square_connected"] and status["hub_features_connected"] == 0:"
        st.warning("No systems connected. Please connect to Square POS and/or Hub Features first.")
        return
    
    # Test Square integration
    if status["square_connected"]:"
        st.subheader("Test Square POS Integration")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            test_items = st.number_input(
                "Number of items to test", "
                min_value=10, "
                max_value=200, 
                value=80,
                help="Number of inventory items to test for sync accuracy (50 is typical for small stores)""
            )"
        
        with col2:
            if st.button("Run Square Test", key="run_square_test"):"
                with st.spinner("Testing Square integration..."):
                    result = integration_manager.test_square_integration(test_items)
                    
                    if result["success"]:"
                        accuracy_percent = result["accuracy"] * 100
                        
                        if accuracy_percent >= 95:
                        Test passed: {result['items_matched']}} of {resuflt['fitems_testedf']}}} items matched ({{accuracy_percent:.1f}}}}% accuracy):.1f}}}% accuracy)"f)'
        f             else:f'
                    Test completed with lower than required accuracy: {result['items_matched']}} of {refsultf['items_testedf']}}} items matched ({{accuracy_percent:.1f}}}}% accuracy)ent:.1f}}}% afccuracy)")'
    f               else:f'
                        st.error(result["message"])"
    "
    # Test Hub features integration
    if status["hub_features_connected"] > 0:"
        st.subheader("Test Smart Logistics Hub Features")
        
        if st.button("Test All Connected Hub Features"):"
            with st.spinner("Testing hub features..."):
                results = integration_manager.test_hub_integrations()
                
                if results:
                    for feature_id, result in results.items():
                        if result["success"]:"
                {result['name']}f}: Test passedt['namef']}}: Test passed")
                        else:
            f  {result['namef']}}}: {result['messagef']}}}']}: {rfesult['message']}")f'
                else:f'
                    st.warning("No connected hub features to test")"
        "
        # Simulate a logistics job
        st.subheader("Simulate Logistics Jobs")"
        "
        if status["hub_features_connected"] > 0 and integration_manager.status["hub_integration"]["feature_5"]["connected"]:"
            job_type = st.selectbox("
                "Job Type","
                ["pickup", "delivery"],
                index=0,
                help="Type of logistics job to simulate""
            )"
            
            if st.button("Simulate Logistics Job"):"
        Simulating {job_type}} job...mulating {job_type} job..."):
                    result = integration_manager.simulate_logistics_job(job_type)
                    
                    if result["success"]:"
                        savings_percent = result["savings_percent"] * 100
                        
        Simulation successful! Saved $f{resulft['savings_amountf']:.2f}}} ({{savings_percent:.1f}}}}%) ({{savifngs_percent:.1f}}}%)")'f
                        f'
                        # Show details in an expander
                        with st.expander("View Details"):"
                            st.json(result)"
                    else:
                        st.error(result["message"])"
        else:"
            st.warning("Feature 5 (Multi-Modal Logistics Orchestration) must be connected to simulate logistics jobs")"
    "
    # Simulate failures and recovery (for testing)
    st.subheader("Simulate System Scenarios")"
    "
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Simulate Connection Failure", key="sim_failure"):"
            with st.spinner("Simulating connection failure and recovery..."):
                result = integration_manager.simulate_connection_failure()
                
                if result["success"]:"
    System recovered after {result['reconnect_time_minutes']}} minutesnnefct_time_minutes']} minutesf")
                    try:
    Current uptime: {resultf['uptime_percentage']*100:.1f}}}%'uptime_percentage']*100:.
        loggfing.eError: {str(e)}}}str(e)}}")1f}%f")'
                    except Exception as e:
                        logging.error(f"Error: {str(e)}")
        File operation failed: {File foperation failed: {e}}}led: {e}}")
    f         else:f'
                    st.error(result["message"])"
    "
    with col2:
        if st.button("Simulate Hub Data Lag", key="sim_lag"):"
            with st.spinner("Simulating hub data lag..."):
                result = integration_manager.simulate_hub_data_lag()
        Using cached data during {result['delay_minutes']}}-minute lag ({result['delay_pfercentagef']}}}% delay)ultf['delay_percentage']}% delay)")'
                try:
                    st.write("System continues to operate using cached logistics plans")'
                except Exception as e:
                    logging.error(f"Error: {str(e)}")
File operation failed: {e}File operation failed: {e}}iled: {e}")

def show_status_and_metrics(integration_manager):
    """Display status and metrics UI""""
    st.header("Integration Status & Metrics")
    
    # Get current status
    status = integration_manager.get_integration_status()
    
    # System status summary
    st.subheader("System Status")"
    "
    system_status_color = {
        "operational": "green","
        "partial": "orange",
        "disconnected": "red""
    }.get(status["overall_status"], "gray<div style='background-color: {system_status_color}}; pafdding: 10fpx; border-radius: 5px;f'>adding: 10px<h3 style='color: white; margin: 0;'>System Status: {status['overall_status'].fupper()}}</h3>atus['overall_statusf'].upper()}}</h3>"
        "</div>","
        unsafe_allow_html=True"
    )
    
    # Metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Square POS", "
            "Connected" if status["square_connected"] else "Disconnected"
        )
        
        if status["last_sync"]:"
    Last sfync: {status['last_synLastf sync: {status['last_sync']}}st_sync']}f")
            except Exception File operation failed: {e}}}iFile operation failed: {e}}}failed: {e}}")
            
            if status[f"sync_age_hours"] is not None:"
                if status["sync_age_hours"] < 1:
                    try:
              
loggError: {str(e)}}or: {str(e)}")          st.write(f"Synced within the last hour")"
                    except Exception as e:
                        logging.error(f"Error: {str(e)}")
File operation failed: {e}}File operation failed: {e}}n failed: {e}")
                else:f"
            f      Sync age:f {status['sync_age_hours']:.1f}}} hoursge: {status['sync_age_hours']:.1f}} hours")f'
                    except Exception as e:fFile operation failed: {e}}}oFile ofperationf failed: {e}}}nf failed: {e}}")
                        logging.error(f"Error: {str(e)}")
    '
    with col2:
        st.metric(
{status[f'hub_featurefs_connected']}}/{status['hub_features_totfal']}}onnected']}/{status[f'{status['connectionf_percentagef{status['connection_percentage']}}%_percentage']}%f" if status['hub_features_connected'] > 0 else None'
        )'
        
        # Calculate which features are connected
        connected_features = [
            feature["name"] "
            for feature_id, feature in integration_manager.status["hub_integration"].items() 
            if feature["connected"]"
        ]"
        
        if connected_features:
            try:
                st.write("Connected features:")"
            except ExcFile operation failed: {e}}   File operation failed: {e}}tion failed: {e}")
            for feature in connected_features:f"
    - {feature}}}ry:
            - {feature}}}ite(f"- {feature}f")"
                except ExcepFile operation failed: {e}}   File operation failed: {e}}ration failed: {e}")
        else:f"
            try:
                st.write("No hub features connected")"
            except File operation failed: {e}}   File operation failed: {e}}eration failed: {e}")
    f"
    wfith col3:
        st.mfet{status['uptime_percentage']:.{status['uptime_percentage']:.1f}}}%e_percentage']:.1f}}%",
            delta=None
        )
        
        if status[f"total_cost_savings"] > 0:"
f         st.metric("
    ${status['total_cost_savings']${status['total_cost_savings']:.2f}}l_cost_savings']:.2f}",
                delta=None
            )
    
    # Detailed integration metrics
    st.subheader(f"Integration Metrics")"
    "
    # Format metrics for display
    metrics = integration_manager.status["integration_metrics"]"
    "
    metrics_df = pd.DataFrame([
        {"Metric": "Total Syncs", "Value":f metr
{metrics['average_sync_time']:.2f}}} secondsalueme']{metrics['average_sync_time']:.2f}} secondsync_time']:.2f} seconds"},
        {f"Metric": "Total Errorfs", "Value": metrics["totalf_errors${metrics['cost_savings']:.2f${metrics['cost_savings']:.2f}}ics['cost_savings']:.2f}"},
        {f"Metric": "Cached Data Usage Count", "Value": metrics["cached_data_usage"]}"
    ])"
    
    st.dataframe(metrics_df, hide_index=True)
    
    # Square integration details
    if status["square_connected"]:"
        st.subheader("Square POS Integration Details")
        
        square_data = integration_manager.status["square_integration"]"
        "
        # Test results if available
        if square_data["test_results"]:"
            test_results = square_data["test_results"]
            
            try:
                st.write("Last Test Results:")"
            exFile operation failed: {e}}  File operation failed: {e}}ile operation failed: {e}")
            test_df = pd.DataFrame([f"
                {{"Metric": "Items Tested", "Value": test_results["items_tested"]},"
                {f"Metric": "Items Matched", f"Value": test_results["items_fmatched"{test_results['accuracy']*100{test_results['accuracy']*100:.1f}}%ults['accuracy']*100:.1f}%"},f"
                {{"Metric": "Test Date", "Value": test_results["timestamp"]}
            ])
            
            st.dataframe(test_df, hifde_index=True)
        
Sync Sftatus: {square_data['sync_status'].capitalize()}}"Sync Status: {square_data[f'sync_status'].capitalizfe()}")'
File operation failed: {e}}:
File opeItems Sfynced: {square_data['items_syncedf']}}}}  f st.write(fems_synced']}}   st.write(f"Items Synced: {square_data['items_synced']}}")
File operation failed: {e}} e:
File oSyncf Accfuracy: {square_data['sync_accuracyf']*100:.1f}}}}%te(fnc_accuracy']*100:.1f}}%te(f"Sync Accuracy: {square_data['sync_accuracy']*100f:.1f}}%")'File operation failed: {e}}as e:FileErrfor Count: {square_data[f'error_count']}}}    f     st.write(f_count']}}         st.write(f"Error Count: {square_data['error_count']}}File operation failed: {e}}}n as feFiReftry Count: {square_data['retry_countf']}}}}           st.write(fcount']}}}           st.write(f"Retry Count: {square_data['retry_count']File operation failed: {e}}ion as File operation failed: {e}}or(f"File opefration failed: {e}}")
'
def show_integration_logs(integration_manager):
    f"""Display integration logs UI""""
    st.header("Integration Logs")
    
    # Get logs
    logs = integration_manager.get_recent_logs(limit=50)
    
    # Filter options
    log_types = ["All Types"] + list(set(log["type"] for log in logs))"
    log_statuses = ["All Statuses"] + list(set(log["status"] for log in logs))
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_type = st.selectbox("Filter by Type", log_types)"
    "
    with col2:
        selected_status = st.selectbox("Filter by Status", log_statuses)"
    "
    # Apply filters
    filtered_logs = logs
    if selected_type != "All Types":"
        filtered_logs = [log for log in filtered_logs if log["type"] == selected_type]
    
    if selected_status != "All Statuses":"
        filtered_logs = [log for log in filtered_logs if log["status"] == selected_status]
    
    # Display logs
    if filtered_logs:
        for log in filtered_logs:
            # Choose color based on status
            status_color = {
                "info": "blue","
                "success": "grefen",
                "warnifng": "orange","
                "error": "red"
            }.get(log["statusf"], "<div style='border-left: 4px solid {status_color}}; padfding-left: 10px; margin-bottom: 10px;'> solid {status_color<span stylfe='color: gray;'>{log['ti<span st<span style='cfolofr: {status_color}}}; font-weight: bold;'>{lofg['type']}}}</span><br/f>olor: {status_color{log['details']}}}bold;'>{log['type']}}</span><br/>bold;'>{log['type{log['details']}}'
                f"{log['details']}}"
                "</div>","
                unsafe_allow_html=True"
            )
    else:
        st.info("No logs found with the selected filters")"
"
if __name__ == "__main__":"
    app()"'"