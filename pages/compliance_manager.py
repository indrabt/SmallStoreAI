import streamlit as st
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime, timedelta
import time
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ComplianceManager
from modules.compliance_manager import ComplianceManager

# Set page config
st.set_page_config(
    page_title="StateSafe Compliance Manager",
    page_icon="🛡️",
    layout="wide"
)

# Title and description
st.title("🛡️ StateSafe Compliance Manager")
st.markdown(
    """
    This module helps you maintain compliance with food safety regulations by managing:
    - Business registration with local council
    - Food Safety Supervisor (FSS) requirements
    - Compliance status monitoring
    
    Complete the setup by selecting your state, registering your business, and assigning a Food Safety Supervisor.
    """
)

# Initialize Compliance Manager if not in session state
if "compliance_manager" not in st.session_state:
    st.session_state.compliance_manager = ComplianceManager()

# Access the compliance manager from session state
compliance_manager = st.session_state.compliance_manager

# Display current compliance status
status = compliance_manager.get_compliance_status()
registration = compliance_manager._load_registration()
fss_data = compliance_manager._load_fss_data()

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Setup & Configuration", 
    "🏢 Business Registration", 
    "👨‍🍳 Food Safety Supervisor", 
    "📊 Compliance Dashboard",
    "📆 Daily Operations",
    "🔄 Integration & Testing"
])

# Setup & Configuration Tab
with tab1:
    st.header("Setup & Configuration")
    
    # State selection
    st.subheader("Step 1: Select State/Territory")
    
    states = compliance_manager.get_states_list()
    state_options = {}
    
    for state_code in states:
        state_info = compliance_manager.get_state_rules(state_code)
        state_options[state_code] = f"{state_code} - {state_info['name']}"
    
    selected_state = st.selectbox(
        "Select your state/territory:",
        options=states,
        format_func=lambda x: state_options[x],
        index=states.index(registration["state"]) if registration["state"] in states else 0
    )
    
    # Display state rules
    if selected_state:
        st.success(f"You've selected {state_options[selected_state]}")
        
        state_rules = compliance_manager.get_state_rules(selected_state)
        
        st.subheader("State Compliance Rules")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📜 Key Legislation")
            for law in state_rules["legislation"]:
                st.markdown(f"- {law}")
        
        with col2:
            st.markdown("#### 📋 Requirements")
            st.markdown(f"- **FSS Required:** {'Yes' if state_rules['fss_required'] else 'No'}")
            if state_rules['fss_required']:
                st.markdown(f"- **FSS Certification:** Valid for {state_rules['fss_certification_period_years']} years")
            
            st.markdown(f"- **Registration Fee:** ${state_rules['registration_fee']}")
            st.markdown(f"- **Notification Method:** {state_rules['notification_method']}")
    
    # Next steps guidance
    st.subheader("Next Steps")
    
    if not registration["registered"]:
        st.warning("Please proceed to the 'Business Registration' tab to register your business.")
    elif state_rules["fss_required"] and not fss_data["assigned"]:
        st.warning("Please proceed to the 'Food Safety Supervisor' tab to assign an FSS.")
    else:
        st.success("Setup complete! Check your compliance status in the 'Compliance Dashboard' tab.")

# Business Registration Tab
with tab2:
    st.header("Business Registration")
    
    # If already registered, show status
    if registration["registered"]:
        st.subheader("Registration Status")
        
        status_color = "green" if registration["registration_status"] == "Registered" else "orange"
        
        st.markdown(f"**Status:** <span style='color:{status_color};font-weight:bold'>{registration['registration_status']}</span>", unsafe_allow_html=True)
        st.markdown(f"**Business:** {registration['business_name']}")
        st.markdown(f"**Address:** {registration['business_address']}")
        st.markdown(f"**Phone:** {registration['business_phone']}")
        st.markdown(f"**State:** {registration['state']}")
        st.markdown(f"**Confirmation Code:** {registration['confirmation_code']}")
        
        reg_date = datetime.fromisoformat(registration['registration_date'])
        st.markdown(f"**Registration Date:** {reg_date.strftime('%d %b %Y, %H:%M')}")
        
        exp_date = datetime.fromisoformat(registration['registration_expiry'])
        st.markdown(f"**Expiry Date:** {exp_date.strftime('%d %b %Y')}")
        
        # If payment pending, show payment button
        if registration["registration_status"] == "Pending Payment":
            state_rules = compliance_manager.get_state_rules(registration["state"])
            
            st.warning(f"Payment of ${state_rules['registration_fee']} required to complete registration")
            
            if st.button("Complete Payment"):
                payment_result = compliance_manager.complete_payment()
                if payment_result["success"]:
                    st.success(payment_result["message"])
                    st.balloons()
                    st.rerun()
                else:
                    st.error(payment_result["message"])
        
        # Option to update registration
        if st.checkbox("Update Registration"):
            st.info("Update your business details below and click 'Update Registration'")
            show_reg_form = True
        else:
            show_reg_form = False
    else:
        st.info("Please complete the registration form below to register your business with the local council.")
        show_reg_form = True
    
    # Registration form
    if show_reg_form:
        st.subheader("Business Details")
        
        selected_state = st.selectbox(
            "State/Territory",
            options=compliance_manager.get_states_list(),
            index=compliance_manager.get_states_list().index(registration["state"]) if registration["state"] in compliance_manager.get_states_list() else 0,
            key="reg_state"
        )
        
        business_name = st.text_input(
            "Business Name",
            value=registration["business_name"] if registration["business_name"] else "",
            placeholder="e.g., Penrith Grocery"
        )
        
        business_address = st.text_input(
            "Business Address",
            value=registration["business_address"] if registration["business_address"] else "",
            placeholder="e.g., 123 High St, Penrith NSW 2750"
        )
        
        business_phone = st.text_input(
            "Business Phone",
            value=registration["business_phone"] if registration["business_phone"] else "",
            placeholder="e.g., 02 1234 5678"
        )
        
        # State rules for selected state
        state_rules = compliance_manager.get_state_rules(selected_state)
        
        # Show registration fee if applicable
        if state_rules["registration_fee"] > 0:
            st.warning(f"Registration fee: ${state_rules['registration_fee']} (payable after submission)")
        else:
            st.success("No registration fee required")
        
        # Register button
        if st.button("Register with Council" if not registration["registered"] else "Update Registration"):
            if not business_name or not business_address or not business_phone:
                st.error("Please fill in all fields")
            else:
                # Show spinner while registering
                with st.spinner("Submitting registration..."):
                    result = compliance_manager.register_business(
                        selected_state, business_name, business_address, business_phone
                    )
                
                if result["success"]:
                    st.success(result["message"])
                    
                    if state_rules["registration_fee"] == 0:
                        st.balloons()
                    
                    st.rerun()
                else:
                    st.error(result["message"])

# Food Safety Supervisor Tab
with tab3:
    st.header("Food Safety Supervisor")
    
    # Check if FSS is required for the registered state
    if not registration["registered"]:
        st.warning("Please register your business first in the 'Business Registration' tab.")
    else:
        state_rules = compliance_manager.get_state_rules(registration["state"])
        
        if not state_rules["fss_required"]:
            st.success(f"Food Safety Supervisor not required in {state_rules['name']}")
        else:
            st.subheader("FSS Requirements")
            st.markdown(f"- FSS certification valid for {state_rules['fss_certification_period_years']} years")
            st.markdown("- Must have completed approved training")
            st.markdown("- Must be reasonably accessible to food handlers")
            
            # If FSS already assigned, show status
            if fss_data["assigned"]:
                st.subheader("Current Food Safety Supervisor")
                
                # Check if FSS certification is still valid
                fss_expiry = datetime.fromisoformat(fss_data["fss_expiry_date"])
                fss_valid = fss_expiry > datetime.now()
                
                status_color = "green" if fss_valid else "red"
                certification_status = "Valid" if fss_valid else "Expired"
                
                st.markdown(f"**Name:** {fss_data['fss_name']}")
                st.markdown(f"**Certificate Number:** {fss_data['fss_certificate_number']}")
                st.markdown(f"**Status:** <span style='color:{status_color};font-weight:bold'>{certification_status}</span>", unsafe_allow_html=True)
                st.markdown(f"**Expiry Date:** {fss_expiry.strftime('%d %b %Y')}")
                
                if not fss_valid:
                    st.error("FSS certification has expired. Please assign a new FSS or update the certification.")
                
                # Option to update FSS
                if st.checkbox("Change Food Safety Supervisor"):
                    show_fss_form = True
                else:
                    show_fss_form = False
            else:
                st.warning("Food Safety Supervisor not assigned. Please assign an FSS below.")
                show_fss_form = True
            
            # FSS assignment form
            if show_fss_form:
                st.subheader("Assign Food Safety Supervisor")
                
                # Get staff list from Feature 8
                staff_list = compliance_manager.get_staff_list()
                
                # Filter staff with valid FSS certification
                certified_staff = [s for s in staff_list if s["fss_certified"]]
                
                if not certified_staff:
                    st.error("No staff members with FSS certification found. Please ensure staff complete FSS training.")
                else:
                    # Create staff options for dropdown
                    staff_options = {}
                    for staff in certified_staff:
                        expiry = datetime.fromisoformat(staff["fss_expiry"])
                        staff_options[staff["id"]] = f"{staff['name']} - FSS Cert: {staff['fss_certificate']} (Expires: {expiry.strftime('%d %b %Y')})"
                    
                    selected_staff_id = st.selectbox(
                        "Select FSS from certified staff:",
                        options=[s["id"] for s in certified_staff],
                        format_func=lambda x: staff_options[x]
                    )
                    
                    # Get selected staff details
                    selected_staff = next((s for s in certified_staff if s["id"] == selected_staff_id), None)
                    
                    if selected_staff:
                        st.info(f"Selected: {selected_staff['name']} ({selected_staff['position']})")
                        
                        # Check if certification is valid
                        expiry = datetime.fromisoformat(selected_staff["fss_expiry"])
                        if expiry <= datetime.now():
                            st.error("FSS certification has expired. Please select someone with a valid certification.")
                            can_assign = False
                        else:
                            st.success(f"FSS certification valid until {expiry.strftime('%d %b %Y')}")
                            can_assign = True
                        
                        # Assign button
                        if can_assign and st.button("Assign as FSS"):
                            with st.spinner("Assigning FSS..."):
                                result = compliance_manager.assign_fss(
                                    selected_staff["id"],
                                    selected_staff["name"],
                                    selected_staff["fss_certificate"],
                                    selected_staff["fss_expiry"]
                                )
                            
                            if result["success"]:
                                st.success(result["message"])
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(result["message"])

# Compliance Dashboard Tab
with tab4:
    st.header("Compliance Dashboard")
    
    # Check if setup is complete
    if not registration["registered"]:
        st.warning("Please register your business first in the 'Business Registration' tab.")
    else:
        # Get compliance status
        status = compliance_manager.get_compliance_status()
        
        # Display overall compliance status
        st.subheader("Overall Compliance Status")
        
        if status["overall_compliant"]:
            st.success("✅ Your business is fully compliant with food safety regulations")
        else:
            st.error("❌ Your business is not fully compliant - please address the alerts below")
        
        # Display alerts
        if status["alerts"]:
            st.subheader("Compliance Alerts")
            
            for alert in status["alerts"]:
                st.warning(f"⚠️ {alert}")
        
        # Display compliance details
        st.subheader("Compliance Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Registration compliance
            st.markdown("#### Business Registration")
            
            if status["registration_compliant"]:
                st.success("✅ Business properly registered with council")
                st.markdown(f"**Business:** {registration['business_name']}")
                st.markdown(f"**State:** {registration['state']}")
                
                exp_date = datetime.fromisoformat(registration['registration_expiry'])
                days_until_expiry = (exp_date - datetime.now()).days
                
                if days_until_expiry < 30:
                    st.warning(f"⚠️ Registration expires in {days_until_expiry} days")
                else:
                    st.markdown(f"**Expiry:** {exp_date.strftime('%d %b %Y')} ({days_until_expiry} days)")
            else:
                st.error("❌ Business registration incomplete")
                
                if not registration["registered"]:
                    st.markdown("- Business not registered with council")
                elif registration["registration_status"] == "Pending Payment":
                    st.markdown("- Registration payment pending")
        
        with col2:
            # FSS compliance
            st.markdown("#### Food Safety Supervisor")
            
            state_rules = compliance_manager.get_state_rules(registration["state"])
            
            if not state_rules["fss_required"]:
                st.info("ℹ️ FSS not required in this state")
                st.markdown(f"Food Safety Supervisor not required in {state_rules['name']}")
            elif status["fss_compliant"]:
                st.success("✅ Valid FSS assigned")
                st.markdown(f"**FSS:** {fss_data['fss_name']}")
                
                fss_expiry = datetime.fromisoformat(fss_data["fss_expiry_date"])
                days_until_expiry = (fss_expiry - datetime.now()).days
                
                if days_until_expiry < 90:
                    st.warning(f"⚠️ FSS certification expires in {days_until_expiry} days")
                else:
                    st.markdown(f"**Expiry:** {fss_expiry.strftime('%d %b %Y')} ({days_until_expiry} days)")
            else:
                st.error("❌ FSS requirements not met")
                
                if not fss_data["assigned"]:
                    st.markdown("- No Food Safety Supervisor assigned")
                else:
                    fss_expiry = datetime.fromisoformat(fss_data["fss_expiry_date"])
                    if fss_expiry <= datetime.now():
                        st.markdown("- FSS certification expired")
        
        # Compliance history
        st.subheader("Compliance Timeline")
        
        # Create a simple compliance timeline (for demo purposes)
        timeline_data = []
        
        if registration["registered"]:
            reg_date = datetime.fromisoformat(registration['registration_date'])
            timeline_data.append({
                "date": reg_date,
                "event": f"Business registered with {registration['state']} council",
                "type": "registration"
            })
        
        if fss_data["assigned"]:
            fss_assign_date = datetime.fromisoformat(fss_data['fss_certification_date'])
            timeline_data.append({
                "date": fss_assign_date,
                "event": f"{fss_data['fss_name']} assigned as Food Safety Supervisor",
                "type": "fss"
            })
        
        # Sort timeline by date
        timeline_data.sort(key=lambda x: x["date"])
        
        # Display timeline
        if timeline_data:
            for event in timeline_data:
                event_date = event["date"].strftime("%d %b %Y, %H:%M")
                if event["type"] == "registration":
                    st.markdown(f"🏢 **{event_date}** - {event['event']}")
                else:
                    st.markdown(f"👨‍🍳 **{event_date}** - {event['event']}")
        else:
            st.info("No compliance events recorded yet. Please complete the setup steps.")

# Daily Operations Tab
with tab5:
    st.header("📆 Daily Compliance Operations")
    
    # Check if setup is complete
    if not registration["registered"]:
        st.warning("Please register your business first in the 'Business Registration' tab.")
    else:
        # Load daily operations data
        daily_ops = compliance_manager._load_daily_ops()
        supplier_logs = compliance_manager._load_supplier_logs()
        inventory_checks = compliance_manager._load_inventory_checks()
        
        # Display daily checklist status
        st.subheader("Daily Compliance Checklist")
        
        last_checklist_date = ""
        if daily_ops["last_checklist_date"]:
            last_date = datetime.fromisoformat(daily_ops["last_checklist_date"])
            last_checklist_date = last_date.strftime("%d %b %Y")
            
        if last_checklist_date:
            st.markdown(f"Last checklist date: **{last_checklist_date}**")
        
        today = datetime.now().strftime("%d %b %Y")
        st.markdown(f"Today's date: **{today}**")
        
        # Create a progress bar for daily tasks
        tasks_completed = sum(1 for task, completed in daily_ops["today_tasks"].items() if completed)
        tasks_total = len(daily_ops["today_tasks"])
        completion_percentage = int((tasks_completed / tasks_total) * 100) if tasks_total > 0 else 0
        
        st.progress(completion_percentage / 100)
        st.markdown(f"**{tasks_completed}/{tasks_total}** tasks completed ({completion_percentage}%)")
        
        # Reset daily checklist button
        if st.button("Reset Daily Checklist"):
            reset_result = compliance_manager.reset_daily_checklist()
            st.success("Daily checklist reset successfully")
            st.rerun()
        
        # Display task checklist
        st.subheader("Today's Tasks")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # FSS Verification
            fss_verified = daily_ops["today_tasks"]["fss_verified"]
            fss_status = "✅ Verified" if fss_verified else "❌ Not Verified"
            
            st.markdown(f"**1. Verify FSS Status:** {fss_status}")
            
            if not fss_verified:
                if st.button("Verify FSS Status"):
                    result = compliance_manager.verify_fss_status()
                    
                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])
            
            # Supplier Logs Verification
            supplier_logs_verified = daily_ops["today_tasks"]["supplier_logs_verified"]
            supplier_status = "✅ Verified" if supplier_logs_verified else "❌ Not Verified"
            
            st.markdown(f"**2. Verify Supplier Logs:** {supplier_status}")
            
            if not supplier_logs_verified:
                # Simple form to log supplier receipt
                with st.expander("Log Supplier Receipt"):
                    supplier_name = st.text_input("Supplier Name", placeholder="e.g., Fresh Farms")
                    
                    receipt_data = {
                        "products": st.text_area("Products Received", placeholder="e.g., Vegetables, Milk, Bread"),
                        "quantity": st.number_input("Total Quantity", min_value=1, value=10),
                        "total_price": st.number_input("Total Price ($)", min_value=0.0, value=50.0, format="%.2f"),
                        "payment_method": st.selectbox("Payment Method", ["Cash", "Credit Card", "Invoice", "Bank Transfer"])
                    }
                    
                    receipt_file = st.file_uploader("Upload Receipt (optional)", type=["pdf", "jpg", "png"])
                    
                    if st.button("Log Receipt"):
                        if not supplier_name:
                            st.error("Please enter supplier name")
                        else:
                            result = compliance_manager.log_supplier_receipt(supplier_name, receipt_data, receipt_file)
                            
                            if result["success"]:
                                st.success(result["message"])
                                st.rerun()
                            else:
                                st.error(result["message"])
        
        with col2:
            # Inventory Checks
            inventory_checks_complete = daily_ops["today_tasks"]["inventory_checks_complete"]
            inventory_status = "✅ Complete" if inventory_checks_complete else "❌ Incomplete"
            
            st.markdown(f"**3. Inventory Checks:** {inventory_status}")
            
            if not inventory_checks_complete:
                # Simple form to log inventory check
                with st.expander("Log Inventory Check"):
                    product_name = st.text_input("Product Name", placeholder="e.g., Fresh Milk")
                    quantity = st.number_input("Current Quantity", min_value=0, value=10)
                    
                    today = datetime.now().date()
                    expiry_date = st.date_input("Expiry Date", value=today + timedelta(days=7), min_value=today)
                    notes = st.text_area("Notes", placeholder="Optional notes about the inventory check")
                    
                    if st.button("Log Inventory Check"):
                        if not product_name:
                            st.error("Please enter product name")
                        else:
                            result = compliance_manager.log_inventory_check(
                                product_name, 
                                quantity, 
                                expiry_date.isoformat(), 
                                notes
                            )
                            
                            if result["success"]:
                                st.success(result["message"])
                                st.rerun()
                            else:
                                st.error(result["message"])
            
            # Inspection Readiness
            inspection_ready = daily_ops["today_tasks"]["inspection_readiness_verified"]
            inspection_status = "✅ Verified" if inspection_ready else "❌ Not Verified"
            
            st.markdown(f"**4. Inspection Readiness:** {inspection_status}")
            
            if not inspection_ready:
                if st.button("Verify Inspection Readiness"):
                    readiness = compliance_manager.verify_inspection_readiness()
                    st.success(f"Inspection readiness verified: {readiness['score']}/5 ({readiness['percentage']}%)")
                    st.rerun()
            
            # Compliance Report
            report_generated = daily_ops["today_tasks"]["report_generated"]
            report_status = "✅ Generated" if report_generated else "❌ Not Generated"
            
            st.markdown(f"**5. Generate Report:** {report_status}")
            
            if not report_generated:
                if st.button("Generate Compliance Report"):
                    report = compliance_manager.generate_compliance_report()
                    st.success("Compliance report generated successfully")
                    st.rerun()
        
        # Display recent logs/checks
        st.subheader("Recent Activity")
        
        recent_logs_tab, recent_checks_tab = st.tabs(["Recent Supplier Logs", "Recent Inventory Checks"])
        
        with recent_logs_tab:
            recent_logs = compliance_manager.get_recent_supplier_logs(5)
            
            if recent_logs:
                for log in recent_logs:
                    log_date = datetime.fromisoformat(log["date"]).strftime("%d %b %Y, %H:%M")
                    st.markdown(f"**{log_date}** - {log['supplier_name']}")
                    st.markdown(f"Products: {log['receipt_data'].get('products', 'N/A')}")
                    st.markdown(f"Total: ${log['receipt_data'].get('total_price', 'N/A')}")
                    st.markdown("---")
            else:
                st.info("No supplier logs recorded yet")
        
        with recent_checks_tab:
            recent_checks = compliance_manager.get_recent_inventory_checks(5)
            
            if recent_checks:
                for check in recent_checks:
                    check_date = datetime.fromisoformat(check["date"]).strftime("%d %b %Y, %H:%M")
                    expiry_date = datetime.fromisoformat(check["expiry_date"]).strftime("%d %b %Y")
                    
                    status_color = "green"
                    if check.get("compliance_status") == "Warning":
                        status_color = "orange"
                    elif check.get("compliance_status") == "Non-Compliant":
                        status_color = "red"
                    
                    st.markdown(f"**{check_date}** - {check['product_name']}")
                    st.markdown(f"Quantity: {check['quantity']}")
                    st.markdown(f"Expiry: {expiry_date}")
                    st.markdown(f"Status: <span style='color:{status_color};font-weight:bold'>{check.get('compliance_status', 'Unknown')}</span>", unsafe_allow_html=True)
                    st.markdown("---")
            else:
                st.info("No inventory checks recorded yet")

# Integration & Testing Tab
with tab6:
    st.header("🔄 Integration & Testing")
    
    # Check if setup is complete
    if not registration["registered"]:
        st.warning("Please register your business first in the 'Business Registration' tab.")
    else:
        integration_tab, testing_tab, deployment_tab = st.tabs([
            "Integration Status", 
            "Compliance Test Suite", 
            "Deployment Planning"
        ])
        
        with integration_tab:
            st.subheader("Feature Integration Status")
            
            # Supplier data from Feature 2
            st.markdown("#### 🧑‍🌾 Feature 2: Low-Cost Local Sourcing")
            
            supplier_data = compliance_manager.get_supplier_data_from_feature2()
            
            if supplier_data["success"]:
                st.success(f"✅ Connected: {supplier_data['supplier_count']} suppliers available")
                
                # Show some supplier data
                if "suppliers" in supplier_data and supplier_data["suppliers"]:
                    with st.expander("View Supplier Data"):
                        for supplier in supplier_data["suppliers"]:
                            st.markdown(f"**{supplier['name']}**")
                            for product in supplier.get('products', []):
                                st.markdown(f"- {product.get('name', 'Unknown')}: ${product.get('price', 0)}/{product.get('unit', 'unit')}")
                
                # Show recent orders
                if "recent_orders" in supplier_data and supplier_data["recent_orders"]:
                    with st.expander("View Recent Orders"):
                        for order in supplier_data["recent_orders"]:
                            order_date = datetime.fromisoformat(order["date"]).strftime("%d %b %Y")
                            st.markdown(f"**Order {order['id']}** - {order_date} from {order.get('supplier', 'Unknown')}")
                            st.markdown(f"Total: ${order.get('total', 0):.2f}")
            else:
                st.error(f"❌ Connection failed: {supplier_data.get('message', 'Unknown error')}")
            
            # Inventory data from Feature 4
            st.markdown("#### 🍎 Feature 4: Perishable Inventory Tracker")
            
            inventory_data = compliance_manager.get_inventory_data_from_feature4()
            
            if inventory_data["success"]:
                st.success(f"✅ Connected: {inventory_data['inventory_count']} inventory items tracked")
                
                # Show expiry alerts
                if "expiry_alerts" in inventory_data and inventory_data["expiry_alerts"]:
                    with st.expander("View Expiry Alerts"):
                        for alert in inventory_data["expiry_alerts"]:
                            st.warning(f"⚠️ {alert.get('message', 'No message')}")
            else:
                st.error(f"❌ Connection failed: {inventory_data.get('message', 'Unknown error')}")
            
            # Integration status from Feature 7
            st.markdown("#### 🔄 Feature 7: Plug-and-Play Integration Kit")
            
            integration_status = compliance_manager.get_integration_status_from_feature7()
            
            if integration_status["success"]:
                st.success(f"✅ Connected: {len(integration_status.get('connected_systems', []))} systems connected")
                
                # Show connected systems
                if "connected_systems" in integration_status and integration_status["connected_systems"]:
                    st.markdown("**Connected Systems:**")
                    for system in integration_status["connected_systems"]:
                        st.markdown(f"- {system}")
            else:
                st.error(f"❌ Connection failed: {integration_status.get('message', 'Unknown error')}")
            
            # Staff data from Feature 8
            st.markdown("#### 👨‍🍳 Feature 8: Staff Training Tutorials")
            
            staff_data = compliance_manager.get_staff_data_from_feature8()
            
            if staff_data["success"]:
                st.success(f"✅ Connected: {staff_data['staff_count']} staff members tracked")
                
                # Show FSS certified staff
                if "fss_certified_staff" in staff_data and staff_data["fss_certified_staff"]:
                    with st.expander("View FSS Certified Staff"):
                        for staff in staff_data["fss_certified_staff"]:
                            expiry = datetime.fromisoformat(staff["fss_expiry"]).strftime("%d %b %Y")
                            st.markdown(f"**{staff['name']}** ({staff['position']})")
                            st.markdown(f"FSS Certificate: {staff['fss_certificate']} (Expires: {expiry})")
            else:
                st.error(f"❌ Connection failed: {staff_data.get('message', 'Unknown error')}")
            
            # Dashboard data from Feature 9
            st.markdown("#### 📊 Feature 9: Real-Time Client Dashboard")
            
            dashboard_data = compliance_manager.get_realtime_data_from_feature9()
            
            if dashboard_data["success"]:
                st.success("✅ Connected: Real-time dashboard data available")
                
                # Show some dashboard data
                if "dashboard_data" in dashboard_data:
                    data = dashboard_data["dashboard_data"]
                    st.markdown(f"**Scores on Doors:** {data.get('scores_on_doors', 'N/A')}/5")
                    st.markdown(f"**Compliance Status:** {data.get('compliance_status', 'Unknown')}")
            else:
                st.error(f"❌ Connection failed: {dashboard_data.get('message', 'Unknown error')}")
        
        with testing_tab:
            st.subheader("Compliance Test Suite")
            
            # State selection for testing
            st.markdown("#### Select State for Testing")
            
            test_state = st.selectbox(
                "State/Territory",
                options=compliance_manager.get_states_list(),
                index=compliance_manager.get_states_list().index(registration["state"]) if registration["state"] in compliance_manager.get_states_list() else 0,
                key="test_state"
            )
            
            # Run test suite button
            if st.button("Run Compliance Test Suite"):
                with st.spinner("Running tests..."):
                    test_results = compliance_manager.run_compliance_test_suite(test_state)
                
                # Display test results
                if test_results["success"]:
                    st.success(f"Test suite passed: {test_results['passed_tests']}/{test_results['total_tests']} tests passed")
                else:
                    st.error(f"Test suite failed: {test_results['passed_tests']}/{test_results['total_tests']} tests passed")
                
                # Show test details
                for test in test_results["tests"]:
                    test_color = "green" if test["status"] == "Passed" else ("orange" if test["status"] == "Skipped" else "red")
                    st.markdown(f"**{test['name']}:** <span style='color:{test_color};font-weight:bold'>{test['status']}</span> - {test['message']}", unsafe_allow_html=True)
                
                # Show overall score
                st.markdown(f"**Overall Score:** {test_results['score']}/5")
        
        with deployment_tab:
            st.subheader("Deployment Planning")
            
            # Get deployment estimate
            deployment_data = compliance_manager.get_deployment_estimate()
            
            # Cost estimate
            st.markdown("#### Cost Estimate")
            
            cost_data = deployment_data["cost_estimate"]
            st.markdown(f"**Development Cost:** ${cost_data['development']}")
            st.markdown(f"**API Integration:** ${cost_data['apis']}")
            st.markdown(f"**Total Cost:** ${cost_data['total']}")
            
            # Timeline
            st.markdown("#### Timeline")
            
            timeline_data = deployment_data["timeline"]
            st.markdown(f"**Build:** {timeline_data['build_weeks']} weeks")
            st.markdown(f"**Testing:** {timeline_data['test_week']} week")
            st.markdown(f"**Deployment Date:** {timeline_data['deployment_date']}")
            
            if timeline_data.get('q3_completion', False):
                st.success("✅ On track for Q3 completion")
            else:
                st.warning("⚠️ Q3 completion at risk")
            
            # Requirements
            st.markdown("#### Requirements")
            
            requirements_data = deployment_data["requirements"]
            
            st.markdown("**API Keys Required:**")
            for api in requirements_data["api_keys"]:
                if api["required"]:
                    st.markdown(f"- {api['name']}")
            
            st.markdown(f"**Storage:** {requirements_data['storage']}")
            st.markdown(f"**Processing:** {requirements_data['processing']}")
            
            # Scale plan
            st.markdown("#### Scaling Plan")
            
            scale_data = deployment_data["scale_plan"]
            st.markdown(f"**Current Stores:** {scale_data['current_stores']}")
            st.markdown(f"**Q4 Target:** {scale_data['q4_target']} stores")
            
            st.markdown("**Scaling Challenges:**")
            for challenge in scale_data["scaling_challenges"]:
                st.markdown(f"- {challenge}")