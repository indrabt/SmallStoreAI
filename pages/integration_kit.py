"""
Plug-and-Play Integration Kit
Seamlessly connect Square POS and smart logistics hub features
"""
import streamlit as st
import pandas as pd
import time
import datetime
import json
from modules.integration_kit import IntegrationKit

def app():
    st.title("Plug-and-Play Integration Kit")
    
    # Initialize integration manager
    integration_manager = IntegrationKit()
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔌 Integration Wizard", 
        "🧪 Test & Verify", 
        "📊 Status & Metrics",
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
    """Display the integration wizard UI"""
    st.header("Integration Wizard")
    
    st.markdown("""
    Connect your store to Square POS and the Smart Logistics Hub features to enable 
    seamless inventory management, pricing optimization, and logistics scheduling.
    
    This wizard will guide you through the process of connecting your store to:
    
    1. **Square POS**: For sales, inventory, and customer data
    2. **Smart Logistics Hub Features**:
       - Feature 1: Hyper-Local Route Optimization
       - Feature 2: Predictive Resilience
       - Feature 5: Multi-Modal Logistics Orchestration
       - Feature 9: Real-Time Client Dashboard
       - Feature 10: Partnerships and Ecosystem Integration
    """)
    
    # Get current status
    status = integration_manager.get_integration_status()
    
    # Display current status
    st.subheader("Current Connection Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Square POS", 
            "Connected" if status["square_connected"] else "Disconnected",
            delta=None
        )
    
    with col2:
        st.metric(
            "Hub Features", 
            f"{status['hub_features_connected']}/{status['hub_features_total']}",
            delta=f"{status['connection_percentage']}%" if status['hub_features_connected'] > 0 else None
        )
    
    with col3:
        st.metric(
            "System Status",
            status["overall_status"].capitalize(),
            delta=None
        )
    
    # Square POS Connection
    st.subheader("Step 1: Connect to Square POS")
    
    if status["square_connected"]:
        st.success("✅ Connected to Square POS")
        
        if st.button("Sync Inventory with Square", key="sync_inventory_btn"):
            with st.spinner("Syncing inventory with Square POS..."):
                # Create a progress bar
                progress_bar = st.progress(0)
                
                # Define callback for progress updates
                def update_progress(progress):
                    progress_bar.progress(progress)
                
                # Sync inventory
                result = integration_manager.sync_square_inventory(update_progress)
                
                if result["success"]:
                    st.success(result["message"])
                else:
                    st.error(result["message"])
    else:
        with st.form("square_connection_form"):
            st.write("Enter your Square POS credentials to connect:")
            username = st.text_input("Username or Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Connect to Square")
            
            if submit:
                if username and password:
                    with st.spinner("Connecting to Square POS..."):
                        result = integration_manager.connect_square(username, password)
                        
                        if result["success"]:
                            st.success(result["message"])
                            st.rerun()
                        else:
                            st.error(result["message"])
                else:
                    st.error("Please enter both username and password")
    
    # Hub Features Connection
    st.subheader("Step 2: Connect to Smart Logistics Hub Features")
    
    # For each hub feature
    for feature_id, feature in integration_manager.status["hub_integration"].items():
        with st.expander(f"{feature['name']} ({feature_id.replace('_', ' ').title()})"):
            if feature["connected"]:
                st.success(f"✅ Connected to {feature['name']}")
                st.write(f"Last synced: {feature['last_sync'] or 'Never'}")
                
                if st.button("Disconnect", key=f"disconnect_{feature_id}"):
                    feature["connected"] = False
                    feature["api_key"] = None
                    integration_manager._log_event(
                        "Hub Disconnection", 
                        f"Manually disconnected from {feature['name']}"
                    )
                    integration_manager._save_status()
                    st.success(f"Disconnected from {feature['name']}")
                    st.rerun()
            else:
                with st.form(f"hub_connection_{feature_id}"):
                    st.write(f"Enter API Key for {feature['name']}:")
                    api_key = st.text_input("API Key", key=f"api_{feature_id}")
                    submit = st.form_submit_button("Connect")
                    
                    if submit:
                        if api_key:
                            with st.spinner(f"Connecting to {feature['name']}..."):
                                result = integration_manager.connect_hub_feature(feature_id, api_key)
                                
                                if result["success"]:
                                    st.success(result["message"])
                                    st.rerun()
                                else:
                                    st.error(result["message"])
                        else:
                            st.error("Please enter an API Key")

def show_test_and_verify(integration_manager):
    """Display the test and verify UI"""
    st.header("Test & Verify Integrations")
    
    status = integration_manager.get_integration_status()
    
    # Display test options based on connected systems
    if not status["square_connected"] and status["hub_features_connected"] == 0:
        st.warning("No systems connected. Please connect to Square POS and/or Hub Features first.")
        return
    
    # Test Square integration
    if status["square_connected"]:
        st.subheader("Test Square POS Integration")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            test_items = st.number_input(
                "Number of items to test", 
                min_value=10, 
                max_value=200, 
                value=80,
                help="Number of inventory items to test for sync accuracy (50 is typical for small stores)"
            )
        
        with col2:
            if st.button("Run Square Test", key="run_square_test"):
                with st.spinner("Testing Square integration..."):
                    result = integration_manager.test_square_integration(test_items)
                    
                    if result["success"]:
                        accuracy_percent = result["accuracy"] * 100
                        
                        if accuracy_percent >= 95:
                            st.success(f"Test passed: {result['items_matched']} of {result['items_tested']} items matched ({accuracy_percent:.1f}% accuracy)")
                        else:
                            st.warning(f"Test completed with lower than required accuracy: {result['items_matched']} of {result['items_tested']} items matched ({accuracy_percent:.1f}% accuracy)")
                    else:
                        st.error(result["message"])
    
    # Test Hub features integration
    if status["hub_features_connected"] > 0:
        st.subheader("Test Smart Logistics Hub Features")
        
        if st.button("Test All Connected Hub Features"):
            with st.spinner("Testing hub features..."):
                results = integration_manager.test_hub_integrations()
                
                if results:
                    for feature_id, result in results.items():
                        if result["success"]:
                            st.success(f"{result['name']}: Test passed")
                        else:
                            st.error(f"{result['name']}: {result['message']}")
                else:
                    st.warning("No connected hub features to test")
        
        # Simulate a logistics job
        st.subheader("Simulate Logistics Jobs")
        
        if status["hub_features_connected"] > 0 and integration_manager.status["hub_integration"]["feature_5"]["connected"]:
            job_type = st.selectbox(
                "Job Type",
                ["pickup", "delivery"],
                index=0,
                help="Type of logistics job to simulate"
            )
            
            if st.button("Simulate Logistics Job"):
                with st.spinner(f"Simulating {job_type} job..."):
                    result = integration_manager.simulate_logistics_job(job_type)
                    
                    if result["success"]:
                        savings_percent = result["savings_percent"] * 100
                        
                        st.success(f"Simulation successful! Saved ${result['savings_amount']:.2f} ({savings_percent:.1f}%)")
                        
                        # Show details in an expander
                        with st.expander("View Details"):
                            st.json(result)
                    else:
                        st.error(result["message"])
        else:
            st.warning("Feature 5 (Multi-Modal Logistics Orchestration) must be connected to simulate logistics jobs")
    
    # Simulate failures and recovery (for testing)
    st.subheader("Simulate System Scenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Simulate Connection Failure", key="sim_failure"):
            with st.spinner("Simulating connection failure and recovery..."):
                result = integration_manager.simulate_connection_failure()
                
                if result["success"]:
                    st.success(f"System recovered after {result['reconnect_time_minutes']} minutes")
                    st.write(f"Current uptime: {result['uptime_percentage']*100:.1f}%")
                else:
                    st.error(result["message"])
    
    with col2:
        if st.button("Simulate Hub Data Lag", key="sim_lag"):
            with st.spinner("Simulating hub data lag..."):
                result = integration_manager.simulate_hub_data_lag()
                
                st.info(f"Using cached data during {result['delay_minutes']}-minute lag ({result['delay_percentage']}% delay)")
                st.write("System continues to operate using cached logistics plans")

def show_status_and_metrics(integration_manager):
    """Display status and metrics UI"""
    st.header("Integration Status & Metrics")
    
    # Get current status
    status = integration_manager.get_integration_status()
    
    # System status summary
    st.subheader("System Status")
    
    system_status_color = {
        "operational": "green",
        "partial": "orange",
        "disconnected": "red"
    }.get(status["overall_status"], "gray")
    
    st.markdown(
        f"<div style='background-color: {system_status_color}; padding: 10px; border-radius: 5px;'>"
        f"<h3 style='color: white; margin: 0;'>System Status: {status['overall_status'].upper()}</h3>"
        "</div>",
        unsafe_allow_html=True
    )
    
    # Metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Square POS", 
            "Connected" if status["square_connected"] else "Disconnected"
        )
        
        if status["last_sync"]:
            st.write(f"Last sync: {status['last_sync']}")
            
            if status["sync_age_hours"] is not None:
                if status["sync_age_hours"] < 1:
                    st.write("Synced within the last hour")
                else:
                    st.write(f"Sync age: {status['sync_age_hours']:.1f} hours")
    
    with col2:
        st.metric(
            "Hub Features", 
            f"{status['hub_features_connected']}/{status['hub_features_total']}",
            delta=f"{status['connection_percentage']}%" if status['hub_features_connected'] > 0 else None
        )
        
        # Calculate which features are connected
        connected_features = [
            feature["name"] 
            for feature_id, feature in integration_manager.status["hub_integration"].items() 
            if feature["connected"]
        ]
        
        if connected_features:
            st.write("Connected features:")
            for feature in connected_features:
                st.write(f"- {feature}")
        else:
            st.write("No hub features connected")
    
    with col3:
        st.metric(
            "System Uptime",
            f"{status['uptime_percentage']:.1f}%",
            delta=None
        )
        
        if status["total_cost_savings"] > 0:
            st.metric(
                "Total Cost Savings",
                f"${status['total_cost_savings']:.2f}",
                delta=None
            )
    
    # Detailed integration metrics
    st.subheader("Integration Metrics")
    
    # Format metrics for display
    metrics = integration_manager.status["integration_metrics"]
    
    metrics_df = pd.DataFrame([
        {"Metric": "Total Syncs", "Value": metrics["total_syncs"]},
        {"Metric": "Average Sync Time", "Value": f"{metrics['average_sync_time']:.2f} seconds"},
        {"Metric": "Total Errors", "Value": metrics["total_errors"]},
        {"Metric": "Cost Savings", "Value": f"${metrics['cost_savings']:.2f}"},
        {"Metric": "Cached Data Usage Count", "Value": metrics["cached_data_usage"]}
    ])
    
    st.dataframe(metrics_df, hide_index=True)
    
    # Square integration details
    if status["square_connected"]:
        st.subheader("Square POS Integration Details")
        
        square_data = integration_manager.status["square_integration"]
        
        # Test results if available
        if square_data["test_results"]:
            test_results = square_data["test_results"]
            
            st.write("Last Test Results:")
            test_df = pd.DataFrame([
                {"Metric": "Items Tested", "Value": test_results["items_tested"]},
                {"Metric": "Items Matched", "Value": test_results["items_matched"]},
                {"Metric": "Accuracy", "Value": f"{test_results['accuracy']*100:.1f}%"},
                {"Metric": "Test Date", "Value": test_results["timestamp"]}
            ])
            
            st.dataframe(test_df, hide_index=True)
        
        # Sync status
        st.write(f"Sync Status: {square_data['sync_status'].capitalize()}")
        st.write(f"Items Synced: {square_data['items_synced']}")
        st.write(f"Sync Accuracy: {square_data['sync_accuracy']*100:.1f}%")
        st.write(f"Error Count: {square_data['error_count']}")
        st.write(f"Retry Count: {square_data['retry_count']}")

def show_integration_logs(integration_manager):
    """Display integration logs UI"""
    st.header("Integration Logs")
    
    # Get logs
    logs = integration_manager.get_recent_logs(limit=50)
    
    # Filter options
    log_types = ["All Types"] + list(set(log["type"] for log in logs))
    log_statuses = ["All Statuses"] + list(set(log["status"] for log in logs))
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_type = st.selectbox("Filter by Type", log_types)
    
    with col2:
        selected_status = st.selectbox("Filter by Status", log_statuses)
    
    # Apply filters
    filtered_logs = logs
    if selected_type != "All Types":
        filtered_logs = [log for log in filtered_logs if log["type"] == selected_type]
    
    if selected_status != "All Statuses":
        filtered_logs = [log for log in filtered_logs if log["status"] == selected_status]
    
    # Display logs
    if filtered_logs:
        for log in filtered_logs:
            # Choose color based on status
            status_color = {
                "info": "blue",
                "success": "green",
                "warning": "orange",
                "error": "red"
            }.get(log["status"], "gray")
            
            st.markdown(
                f"<div style='border-left: 4px solid {status_color}; padding-left: 10px; margin-bottom: 10px;'>"
                f"<span style='color: gray;'>{log['timestamp']}</span> | "
                f"<span style='color: {status_color}; font-weight: bold;'>{log['type']}</span><br/>"
                f"{log['details']}"
                "</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No logs found with the selected filters")

if __name__ == "__main__":
    app()