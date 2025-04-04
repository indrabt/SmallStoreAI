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
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Setup & Configuration", 
    "🏢 Business Registration", 
    "👨‍🍳 Food Safety Supervisor", 
    "📊 Compliance Dashboard"
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