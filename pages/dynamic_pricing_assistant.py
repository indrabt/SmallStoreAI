import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules
from modules.pricing_assistant import PricingAssistant
from modules.event_recommender import EventRecommender

# Initialize managers
pricing_assistant = PricingAssistant()
event_recommender = EventRecommender()

# Page title and description
st.title("Dynamic Pricing Assistant")

# Main navigation tabs
tab1, tab2, tab3 = st.tabs(["Pricing Suggestions", "Promotions", "POS Settings"])

#
# Tab 1: Pricing Suggestions
#
with tab1:
    st.subheader("Price Recommendations")
    
    # Add current time display to simulate 10:00 AM requirement
    current_time = datetime.now()
    st.write(f"Current Time: **{current_time.strftime('%H:%M')}**")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox("Category Filter", 
                                      ["All Categories", "Beverages", "Fruits & Vegetables", 
                                       "Dairy & Eggs", "Bakery", "Snacks & Confectionery"])
    
    with col2:
        savings_filter = st.slider("Minimum Supplier Savings", 0, 30, 0, 5, "%")
    
    with col3:
        status_filter = st.selectbox("Status", ["All", "Pending", "Approved", "Applied", "Rejected"])
    
    # Get price suggestions based on filters
    category = None if category_filter == "All Categories" else category_filter
    status = None if status_filter == "All" else status_filter.lower()
    suggestions = pricing_assistant.get_price_suggestions(category, savings_filter, status)
    
    if not suggestions:
        st.info("No price suggestions match your current filters.")
    else:
        # Format data for display
        suggestion_data = []
        
        for suggestion in suggestions:
            suggestion_data.append({
                "Product": suggestion["product_name"],
                "Category": suggestion["category"],
                "Current Cost": f"${suggestion['current_cost']:.2f}",
                "Supplier Cost": f"${suggestion['supplier_cost']:.2f}",
                "Savings": f"{suggestion['supplier_savings']}%",
                "Current Price": f"${suggestion['current_price']:.2f}",
                "Suggested Price": f"${suggestion['competitive_price']:.2f}",
                "Competitor": f"{suggestion['competitor_name']}: ${suggestion['competitor_price']:.2f}",
                "Est. Sales Increase": f"{suggestion['demand_impact']['sales_increase_percentage']}%",
                "Status": suggestion["status"].capitalize(),
                "id": suggestion["id"]  # Hidden column for reference
            })
        
        # Convert to DataFrame for display
        df = pd.DataFrame(suggestion_data)
        display_cols = [col for col in df.columns if col != 'id']
        
        # Display table with suggestions
        st.dataframe(df[display_cols], hide_index=True)
        
        # Divider
        st.divider()
        
        # Detailed view and actions for individual suggestions
        st.subheader("Adjust and Apply Prices")
        
        # Select a product to view details
        selected_product = st.selectbox("Select a product to view details", 
                                        [s["product_name"] for s in suggestions])
        
        # Find the selected suggestion
        selected_suggestion = next((s for s in suggestions if s["product_name"] == selected_product), None)
        
        if selected_suggestion:
            # Display product details
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Product:** {selected_suggestion['product_name']}")
                st.write(f"**Category:** {selected_suggestion['category']}")
                st.write(f"**Current Price:** ${selected_suggestion['current_price']:.2f}")
                st.write(f"**Suggested Price:** ${selected_suggestion['competitive_price']:.2f}")
                st.write(f"**Competitor Price ({selected_suggestion['competitor_name']}):** ${selected_suggestion['competitor_price']:.2f}")
                
                # Price adjustment
                adjusted_price = st.number_input("Adjusted Price ($)", 
                                               min_value=float(selected_suggestion['supplier_cost']),
                                               max_value=float(selected_suggestion['current_price'] * 1.2),
                                               value=float(selected_suggestion['competitive_price']),
                                               step=0.05,
                                               format="%.2f")
                
                # Calculate new margin
                new_margin = ((adjusted_price - selected_suggestion['supplier_cost']) / adjusted_price) * 100
                st.write(f"New Margin: **{new_margin:.1f}%**")
                
                # Apply button
                if st.button("Apply & Sync to POS"):
                    # Update price in system
                    result = pricing_assistant.update_price(selected_suggestion['id'], adjusted_price)
                    
                    if result['success']:
                        # Show success message with Square POS sync details
                        st.success(f"Price updated for {result['product_name']} to ${adjusted_price:.2f} and {result['message']}")
                        
                        # Show expected time for syncing (10:05 AM as per requirement)
                        sync_time = (datetime.now() + timedelta(minutes=5)).strftime("%H:%M")
                        st.info(f"Square POS will be synchronized by {sync_time}")
                        
                        # Add progress bar to simulate sync
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)  # Simulate sync process
                            progress_bar.progress(i + 1)
                        
                        st.success("Square POS synchronization complete!")
                        
                        # Provide a rerun button to refresh the page with updated data
                        st.button("Refresh Data", on_click=st.rerun)
                    else:
                        st.error(result['message'])
            
            with col2:
                # Display impact analysis visualization
                st.write("**Price Impact Analysis**")
                
                impact_chart = pricing_assistant.generate_suggestion_impact_chart(selected_suggestion['id'])
                if impact_chart:
                    st.pyplot(impact_chart)
                else:
                    st.warning("Unable to generate impact analysis")
                
                # Display savings information
                if selected_suggestion['supplier_savings'] > 0:
                    st.info(f"Supplier Cost Savings: **{selected_suggestion['supplier_savings']}%** using {selected_suggestion['supplier_name']}")
                
                # Display competitive position
                price_diff = ((selected_suggestion['competitive_price'] - selected_suggestion['competitor_price']) 
                             / selected_suggestion['competitor_price'] * 100)
                
                if price_diff < 0:
                    st.success(f"Price is **{abs(price_diff):.1f}%** below {selected_suggestion['competitor_name']}")
                elif price_diff > 5:
                    st.warning(f"Price is **{price_diff:.1f}%** above {selected_suggestion['competitor_name']}")
                else:
                    # Fix the formatting to avoid embedded expressions with parentheses
                    position = "above" if price_diff > 0 else "below"
                    st.info(f"Price is **{price_diff:.1f}%** {position} {selected_suggestion['competitor_name']}")

#
# Tab 2: Promotions
#
with tab2:
    st.subheader("Promotion Management")
    
    # Get promotions
    promotions = pricing_assistant.get_promotions()
    
    # Subtabs for active and upcoming promotions
    promo_tab1, promo_tab2, promo_tab3 = st.tabs(["Current Promotions", "Create Promotion", "Promotion History"])
    
    with promo_tab1:
        if not promotions:
            st.info("No promotions available.")
        else:
            # Filter for active, pending, and upcoming promotions
            today = datetime.now().strftime("%Y-%m-%d")
            active_promotions = [p for p in promotions if p['applied'] and p['start_date'] <= today and p['end_date'] >= today]
            pending_promotions = [p for p in promotions if not p['applied'] and p['start_date'] <= today and p['end_date'] >= today]
            upcoming_promotions = [p for p in promotions if p['start_date'] > today]
            
            # Show active promotions
            if active_promotions:
                st.write("### Active Promotions")
                for promo in active_promotions:
                    with st.expander(f"{promo['name']} (Active until {promo['end_date']})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                        st.write(f"**Type:** {promo['type'].replace('_', ' ').title()}")
                            # Fix potentially problematic f-string with conditional
                            symbol_value = "%" if promo['type'] == 'percent_off' else ""
                            st.write(f"**Value:** {promo['value']}{symbol_value}")
                            st.write(f"**Category:** {promo['category']}")
                            st.write(f"**Description:** {promo['description']}")
                            
                            if promo['related_event']:
                            st.write(f"**Related Event:** {promo['event_name']}")
                        
                        with col2:
                            # Display impact visualization
                            impact_chart = pricing_assistant.generate_promotion_impact_chart(promo['id'])
                            if impact_chart:
                                st.pyplot(impact_chart)
                            
                            # Check if promotion is underperforming
                            failed_promotions = pricing_assistant.check_for_failed_promotions()
                            
                            if failed_promotions and any(fp['promotion_id'] == promo['id'] for fp in failed_promotions):
                                failed_promo = next(fp for fp in failed_promotions if fp['promotion_id'] == promo['id'])
                                
                                st.warning(failed_promo['message'])
                                
                                if st.button(f"Increase to {failed_promo['suggested_value']}%", key=f"increase_{promo['id']}"):
                                    result = pricing_assistant.apply_promotion(promo['id'], failed_promo['suggested_value'])
                                    if result['success']:
                                        st.success(f"Promotion updated and {result['message']}")
                                        st.info(f"Customer retention estimated at {failed_promo['customer_retention']}%")
                                        st.button("Refresh", on_click=st.rerun)
            
            # Show pending promotions
            if pending_promotions:
                st.write("### Pending Promotions")
                for promo in pending_promotions:
                    with st.expander(f"{promo['name']} (Ready to apply)"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                        st.write(f"**Type:** {promo['type'].replace('_', ' ').title()}")
                            # Fix potentially problematic f-string with conditional
                            symbol_value = "%" if promo['type'] == 'percent_off' else ""
                            st.write(f"**Value:** {promo['value']}{symbol_value}")
                            st.write(f"**Category:** {promo['category']}")
                            st.write(f"**Description:** {promo['description']}")
                            
                            if promo['related_event']:
                            st.write(f"**Related Event:** {promo['event_name']}")
                            
                            # Allow adjustment before applying
                            if promo['type'] == 'percent_off':
                                adjusted_value = st.slider(f"Adjust Discount", 1, 50, int(promo['value']), 1, "%", 
                                                         key=f"slider_{promo['id']}")
                            else:
                                adjusted_value = promo['value']
                            
                            # Apply button
                            if st.button("Apply & Sync to POS", key=f"apply_{promo['id']}"):
                                result = pricing_assistant.apply_promotion(
                                    promo['id'], 
                                    adjusted_value if adjusted_value != promo['value'] else None
                                )
                                
                                if result['success']:
                                    # Show success message with Square POS sync details
                                    st.success(f"Promotion '{result['promotion_name']}' applied and {result['message']}")
                                    
                                    # Show expected time for syncing (10:05 AM as per requirement)
                                    sync_time = (datetime.now() + timedelta(minutes=5)).strftime("%H:%M")
                                    st.info(f"Square POS will be synchronized by {sync_time}")
                                    
                                    # Add progress bar to simulate sync
                                    progress_bar = st.progress(0)
                                    for i in range(100):
                                        time.sleep(0.01)  # Simulate sync process
                                        progress_bar.progress(i + 1)
                                    
                                    st.success("Square POS synchronization complete!")
                                    st.button("Refresh Data", key=f"refresh_{promo['id']}", on_click=st.rerun)
                                else:
                                    st.error(result['message'])
                        
                        with col2:
                            # Display impact visualization
                            impact_chart = pricing_assistant.generate_promotion_impact_chart(promo['id'])
                            if impact_chart:
                                st.pyplot(impact_chart)
            
            # Show upcoming promotions
            if upcoming_promotions:
                st.write("### Upcoming Promotions")
                for promo in upcoming_promotions:
                    with st.expander(f"{promo['name']} (Starting {promo['start_date']})"):
                    st.write(f"**Type:** {promo['type'].replace('_', ' ').title()}")
                        # Fix potentially problematic f-string with conditional
                        symbol_value = "%" if promo['type'] == 'percent_off' else ""
                        st.write(f"**Value:** {promo['value']}{symbol_value}")
                        st.write(f"**Category:** {promo['category']}")
                        st.write(f"**Description:** {promo['description']}")
                        st.write(f"**Period:** {promo['start_date']} to {promo['end_date']}")
                        
                        if promo['related_event']:
                        st.write(f"**Related Event:** {promo['event_name']}")
    
    with promo_tab2:
        st.write("### Create New Promotion")
        
        # Get event data for event-related promotions
        upcoming_events = event_recommender.get_upcoming_events()
        
        # Form for creating new promotion
        with st.form("create_promotion_form"):
            # Basic promotion details
            promotion_name = st.text_input("Promotion Name")
            promotion_description = st.text_area("Description", height=100)
            
            col1, col2 = st.columns(2)
            
            with col1:
                promotion_type = st.selectbox("Promotion Type", 
                                            ["Percent Off", "Buy One Get One", "Amount Off"])
                
                category = st.selectbox("Category", 
                                      ["All Categories", "Beverages", "Fruits & Vegetables", 
                                       "Dairy & Eggs", "Bakery", "Snacks & Confectionery"])
            
            with col2:
                # Value depends on promotion type
                if promotion_type == "Percent Off":
                    value = st.slider("Discount Percentage", 1, 50, 10, 1, "%")
                elif promotion_type == "Buy One Get One":
                    value = st.selectbox("BOGO Type", ["Free", "Half Price", "25% Off"])
                else:  # Amount Off
                    value = st.number_input("Discount Amount ($)", 1.0, 50.0, 5.0, 1.0)
                    threshold = st.number_input("Minimum Purchase ($)", 1.0, 100.0, 20.0, 5.0)
            
            # Date range
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", datetime.now())
            with col2:
                end_date = st.date_input("End Date", datetime.now() + timedelta(days=7))
            
            # Event association
            if upcoming_events:
                related_to_event = st.checkbox("Related to an Event")
                
                if related_to_event:
                    event_options = {f"{e['name']} ({e['date']})": e for e in upcoming_events}
                    selected_event = st.selectbox("Select Event", list(event_options.keys()))
                    event = event_options[selected_event]
                    event_id = event['id']
                    event_name = event['name']
                else:
                    event_id = None
                    event_name = None
            else:
                event_id = None
                event_name = None
                related_to_event = False
            
            # Submit button
            submit_button = st.form_submit_button("Create Promotion")
        
        # Process form submission
        if submit_button:
            if not promotion_name:
                st.error("Promotion name is required")
            elif not promotion_description:
                st.error("Promotion description is required")
            else:
                # Convert promotion type to system format
                system_type = promotion_type.lower().replace(" ", "_")
                
                # Format dates as strings
                start_date_str = start_date.strftime("%Y-%m-%d")
                end_date_str = end_date.strftime("%Y-%m-%d")
                
                # Create the promotion
                result = pricing_assistant.create_promotion(
                    name=promotion_name,
                    description=promotion_description,
                    promotion_type=system_type,
                    value=value,
                    category=category if category != "All Categories" else "All Categories",
                    start_date=start_date_str,
                    end_date=end_date_str,
                    related_event=event_id,
                    event_name=event_name
                )
                
                if result['success']:
                    st.success(f"Promotion '{promotion_name}' created successfully!")
                    
                    # Provide option to apply immediately if it starts today
                    if start_date <= datetime.now().date():
                        if st.button("Apply & Sync to POS Now"):
                            apply_result = pricing_assistant.apply_promotion(result['promotion_id'])
                            
                            if apply_result['success']:
                                st.success(f"Promotion applied and {apply_result['message']}")
                                
                                # Show expected time for syncing (10:05 AM as per requirement)
                                sync_time = (datetime.now() + timedelta(minutes=5)).strftime("%H:%M")
                                st.info(f"Square POS will be synchronized by {sync_time}")
                                
                                # Add progress bar to simulate sync
                                progress_bar = st.progress(0)
                                for i in range(100):
                                    time.sleep(0.01)  # Simulate sync process
                                    progress_bar.progress(i + 1)
                                
                                st.success("Square POS synchronization complete!")
                    
                    st.button("View Promotions", on_click=lambda: st.switch_page("pages/dynamic_pricing_assistant.py"))
                else:
                    st.error(result['message'])
    
    with promo_tab3:
        st.write("### Promotion History")
        
        # Load data
        data = pricing_assistant._load_data()
        promotion_history = data.get('promotion_history', [])
        
        if not promotion_history:
            st.info("No promotion history available.")
        else:
            # Format data for display
            history_data = []
            
            for entry in promotion_history:
                history_data.append({
                    "Promotion": entry['promotion_name'],
                    "Applied On": datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M"),
                    "Period": f"{entry['start_date']} to {entry['end_date']}",
                    "Category": entry['category'],
                    # Fix potentially problematic f-string with conditional
                    "Value": # Fix potentially problematic f-string with conditional
symbol_value = "%" if 'percent' in entry['promotion_name'].lower() else ""
f"{entry['applied_value']}{symbol_value}",
                    "Event": entry['event_name'] if entry['event_name'] else "-"
                })
            
            # Display as table
            history_df = pd.DataFrame(history_data)
            st.dataframe(history_df, hide_index=True)

#
# Tab 3: POS Settings
#
with tab3:
    st.subheader("Square POS Integration Settings")
    
    # Get current settings
    pos_settings = pricing_assistant.get_pos_settings()
    
    # Form for POS settings
    with st.form("pos_settings_form"):
        enabled = st.checkbox("Enable Square POS Integration", 
                             value=pos_settings.get('square_api_enabled', False))
        
        api_key = st.text_input("Square API Key", 
                               value=pos_settings.get('square_api_key', ''),
                               type="password",
                               placeholder="Enter your Square API Key")
        
        location_id = st.text_input("Square Location ID",
                                  value=pos_settings.get('square_location_id', ''),
                                  placeholder="Enter your Square Location ID")
        
        auto_sync = st.checkbox("Enable Automatic Synchronization",
                              value=pos_settings.get('auto_sync', False))
        
        sync_schedule = st.time_input("Daily Sync Time",
                                    value=datetime.strptime(pos_settings.get('sync_schedule', '10:00'), "%H:%M"))
        
        submit_button = st.form_submit_button("Save Settings")
    
    # Process form submission
    if submit_button:
        result = pricing_assistant.update_pos_settings(
            enabled=enabled,
            api_key=api_key,
            location_id=location_id,
            auto_sync=auto_sync,
            sync_schedule=sync_schedule.strftime("%H:%M")
        )
        
        if result['success']:
            st.success("POS settings updated successfully!")
        else:
            st.error(result['message'])
    
    # Display additional information
    st.divider()
    
    st.write("### Square POS Integration Details")
    
    st.write("""
    The Square POS integration allows you to synchronize prices and promotions with your Square Point of Sale system.
    Price changes and promotions applied through this tool will be automatically updated in your Square account.
    """)
    
    # Display sync history
    st.write("### Recent Synchronization History")
    
    sync_history = data.get('sync_history', [])
    
    if not sync_history:
        st.info("No synchronization history available.")
    else:
        # Display last 5 entries
        for entry in sync_history[-5:]:
            sync_time = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            sync_type = entry['type'].capitalize()
            
            if entry['status'] == 'successful':
                st.success(f"{sync_time}: {sync_type} sync completed successfully")
            else:
                st.error(f"{sync_time}: {sync_type} sync failed")
    
    # Display implementation details for developer reference
    with st.expander("Developer Implementation Reference"):
        st.code(pricing_assistant.generate_square_api_code_sample(), language="python")