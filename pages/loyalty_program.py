import streamlit as st
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required modules
from modules.loyalty_program import LoyaltyProgram
from modules.event_recommender import EventRecommender

# Page configuration
st.set_page_config(page_title="One-Click Loyalty Program", page_icon="🎁", layout="wide")

# Initialize modules
loyalty_program = LoyaltyProgram()
event_recommender = EventRecommender()

# Page header
st.title("One-Click Loyalty Program")
st.markdown("Reward customer loyalty and track preferences with an integrated points system")

# Current time display for context
current_time = datetime.datetime.now().strftime("%A, %d %B %Y, %I:%M %p")
st.write(f"Current time: {current_time}")

# Program status and settings
program_settings = loyalty_program.get_settings()

# Create main tabs
overview_tab, transactions_tab, customers_tab, settings_tab = st.tabs([
    "Program Overview", "Transactions & Redemptions", "Customer Management", "Program Settings"
])

with overview_tab:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Loyalty Program Dashboard")
        
        # Display program status
        enabled = program_settings["enabled"]
        status_color = "green" if enabled else "red"
        st.markdown(f"""
        <div style="background-color: {'#d4f1d4' if enabled else '#f7dddc'}; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <h3 style="color: {'green' if enabled else 'red'}; margin: 0;">Program Status: {"Enabled" if enabled else "Disabled"}</h3>
            <p>Points per dollar: {program_settings["points_per_dollar"]}</p>
            <p>Redemption threshold: {program_settings["redemption_threshold"]} points</p>
            <p>Redemption value: {program_settings["redemption_value"]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get top customers
        top_customers = loyalty_program.get_top_customers(limit=5)
        
        st.write("### Top Customers")
        
        if top_customers:
            customer_data = [
                {
                    "Customer": customer["name"],
                    "Points": customer["points"],
                    "Total Spend": f"${customer['total_spend']:.2f}",
                    "Visits": customer["visit_count"],
                    "Last Visit": customer["last_visit"]
                }
                for customer in top_customers
            ]
            
            st.dataframe(pd.DataFrame(customer_data), use_container_width=True)
            
            # Visualize top customer points
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x=[c["name"] for c in top_customers], y=[c["points"] for c in top_customers], ax=ax)
            ax.set_title("Top Customer Points")
            ax.set_xlabel("Customer")
            ax.set_ylabel("Points")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No customers enrolled in the loyalty program yet")
    
    with col2:
        st.subheader("Quick Actions")
        
        # Program toggle
        current_status = program_settings["enabled"]
        new_status = st.toggle("Enable Loyalty Program", value=current_status)
        
        if new_status != current_status:
            loyalty_program.toggle_program(new_status)
            st.success(f"Loyalty program is now {'enabled' if new_status else 'disabled'}")
            st.rerun()
        
        # Record a transaction
        st.write("### Record Transaction")
        
        # Get all customers for the dropdown
        all_customers = loyalty_program.get_customers()
        customer_options = [(c["id"], c["name"]) for c in all_customers]
        
        if customer_options:
            selected_customer_tuple = st.selectbox(
                "Select Customer",
                options=customer_options,
                format_func=lambda x: x[1]
            )
            
            selected_customer_id = selected_customer_tuple[0]
            
            transaction_amount = st.number_input("Purchase Amount ($)", min_value=1.0, value=20.0, step=1.0)
            
            # Check for upcoming events for double points
            upcoming_events = event_recommender.get_upcoming_events(days=7)
            has_events = len(upcoming_events) > 0
            
            double_points = st.checkbox(
                "Double Points",
                value=has_events,
                help="Apply double points for special events"
            )
            
            event_name = None
            if double_points and has_events:
                event_options = [(e["id"], e["name"]) for e in upcoming_events]
                selected_event_tuple = st.selectbox(
                    "Select Event",
                    options=event_options,
                    format_func=lambda x: x[1]
                )
                event_name = selected_event_tuple[1]
            
            if st.button("Record Purchase"):
                points_per_dollar = program_settings["points_per_dollar"]
                base_points = int(transaction_amount * points_per_dollar)
                total_points = base_points * 2 if double_points else base_points
                
                transaction = loyalty_program.record_transaction(
                    selected_customer_id, 
                    transaction_amount, 
                    double_points=double_points,
                    event_name=event_name
                )
                
                if "error" in transaction:
                    st.error(transaction["error"])
                else:
                    st.success(f"Transaction recorded: ${transaction_amount:.2f}, {total_points} points earned")
                    
                    # Show receipt message
                    receipt_msg = f"Points earned: {total_points}"
                    if double_points:
                        receipt_msg += f" (Double points for {event_name})"
                    
                    st.info(f"Receipt message: {receipt_msg}")
        else:
            st.warning("No customers enrolled in the loyalty program yet")
        
        # Redeem points
        st.write("### Redeem Points")
        
        if customer_options:
            selected_customer_for_redemption = st.selectbox(
                "Select Customer for Redemption",
                options=customer_options,
                format_func=lambda x: x[1],
                key="redemption_customer"
            )
            
            # Get the customer's current points
            selected_customer = loyalty_program.get_customer(selected_customer_for_redemption[0])
            current_points = selected_customer["points"]
            
            redemption_threshold = program_settings["redemption_threshold"]
            
            st.write(f"Current points: {current_points}")
            st.write(f"Redemption threshold: {redemption_threshold} points")
            
            if current_points >= redemption_threshold:
                redemption_item = st.text_input("Item for Redemption", value="Water Bottle")
                staff_member = st.text_input("Staff Member Processing Redemption")
                
                if st.button("Process Redemption"):
                    redemption = loyalty_program.redeem_points(
                        selected_customer_for_redemption[0],
                        points=redemption_threshold,
                        item=redemption_item,
                        staff_member=staff_member
                    )
                    
                    if "error" in redemption:
                        st.error(redemption["error"])
                    else:
                        st.success(f"Redeemed {redemption_threshold} points for {redemption_item}")
                        st.balloons()
            else:
                st.warning(f"Customer needs {redemption_threshold - current_points} more points to redeem")
        else:
            st.warning("No customers enrolled in the loyalty program yet")
        
        # Sync offline cache
        if program_settings.get("offline_mode", False):
            st.write("### Sync Offline Data")
            
            if st.button("Sync with Square POS"):
                sync_result = loyalty_program.sync_offline_cache()
                st.write(f"Synced {sync_result['synced']} items with {sync_result['errors']} errors")
                st.write(f"Last sync: {sync_result['last_sync']}")

with transactions_tab:
    st.subheader("Transactions & Redemptions")
    
    # Create sub-tabs
    trans_tab, redeem_tab = st.tabs(["Transactions", "Redemptions"])
    
    with trans_tab:
        st.write("### Recent Transactions")
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Customer filter
            all_customers = loyalty_program.get_customers()
            customer_options = [(None, "All Customers")] + [(c["id"], c["name"]) for c in all_customers]
            
            selected_customer_filter = st.selectbox(
                "Filter by Customer",
                options=customer_options,
                format_func=lambda x: x[1] if x else "All Customers"
            )
            
            customer_id_filter = selected_customer_filter[0] if selected_customer_filter else None
        
        with col2:
            # Date range
            start_date = st.date_input(
                "Start Date",
                value=(datetime.datetime.now() - timedelta(days=30)).date()
            )
        
        with col3:
            end_date = st.date_input(
                "End Date",
                value=datetime.datetime.now().date()
            )
        
        # Get transactions
        transactions = loyalty_program.get_transactions(
            customer_id=customer_id_filter,
            start_date=start_date.strftime("%Y-%m-%d") if start_date else None,
            end_date=end_date.strftime("%Y-%m-%d") if end_date else None
        )
        
        # Display transactions
        if transactions:
            transaction_data = [
                {
                    "Date": t["date"],
                    "Customer": t["customer_name"],
                    "Amount": f"${t['amount']:.2f}",
                    "Points Earned": t["points_earned"],
                    "Double Points": "✅" if t["double_points"] else "❌",
                    "Event": t["event_name"] if t["event_name"] else "",
                    "Receipt": t["receipt_number"],
                    "Synced": "✅" if t["synced_to_square"] else "❌"
                }
                for t in transactions
            ]
            
            st.dataframe(pd.DataFrame(transaction_data), use_container_width=True)
            
            # Transaction summary
            total_transactions = len(transactions)
            total_amount = sum(t["amount"] for t in transactions)
            total_points = sum(t["points_earned"] for t in transactions)
            double_points_count = sum(1 for t in transactions if t["double_points"])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Transactions", total_transactions)
            col2.metric("Total Amount", f"${total_amount:.2f}")
            col3.metric("Total Points", total_points)
            col4.metric("Double Points Events", double_points_count)
        else:
            st.info("No transactions found for the selected filters")
    
    with redeem_tab:
        st.write("### Recent Redemptions")
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Customer filter
            all_customers = loyalty_program.get_customers()
            customer_options = [(None, "All Customers")] + [(c["id"], c["name"]) for c in all_customers]
            
            selected_customer_filter = st.selectbox(
                "Filter by Customer",
                options=customer_options,
                format_func=lambda x: x[1] if x else "All Customers",
                key="redemption_customer_filter"
            )
            
            customer_id_filter = selected_customer_filter[0] if selected_customer_filter else None
        
        with col2:
            # Date range
            start_date = st.date_input(
                "Start Date",
                value=(datetime.datetime.now() - timedelta(days=30)).date(),
                key="redemption_start_date"
            )
        
        with col3:
            end_date = st.date_input(
                "End Date",
                value=datetime.datetime.now().date(),
                key="redemption_end_date"
            )
        
        # Get redemptions
        redemptions = loyalty_program.get_redemptions(
            customer_id=customer_id_filter,
            start_date=start_date.strftime("%Y-%m-%d") if start_date else None,
            end_date=end_date.strftime("%Y-%m-%d") if end_date else None
        )
        
        # Display redemptions
        if redemptions:
            redemption_data = [
                {
                    "Date": r["date"],
                    "Customer": r["customer_name"],
                    "Points Redeemed": r["points_redeemed"],
                    "Item": r["item_redeemed"],
                    "Staff": r["staff_member"],
                    "Transaction ID": r["transaction_id"],
                    "Synced": "✅" if r["synced_to_square"] else "❌"
                }
                for r in redemptions
            ]
            
            st.dataframe(pd.DataFrame(redemption_data), use_container_width=True)
            
            # Redemption summary
            total_redemptions = len(redemptions)
            total_points_redeemed = sum(r["points_redeemed"] for r in redemptions)
            
            col1, col2 = st.columns(2)
            col1.metric("Total Redemptions", total_redemptions)
            col2.metric("Total Points Redeemed", total_points_redeemed)
        else:
            st.info("No redemptions found for the selected filters")

with customers_tab:
    st.subheader("Customer Management")
    
    # Search and filter
    search_term = st.text_input("Search Customers", placeholder="Name, email, or phone")
    
    sort_options = {
        "points": "Points (high to low)",
        "last_visit": "Last Visit (recent first)",
        "visit_count": "Visit Count (high to low)",
        "total_spend": "Total Spend (high to low)",
        "name": "Name (A to Z)"
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        sort_by = st.selectbox("Sort By", options=list(sort_options.keys()), format_func=lambda x: sort_options[x])
    
    with col2:
        descending = sort_by != "name"  # Default ascending for name, descending for others
        sort_direction = st.radio("Sort Direction", options=["Descending", "Ascending"], horizontal=True, index=0 if descending else 1)
        descending = sort_direction == "Descending"
    
    # Get customers
    customers = loyalty_program.get_customers(search_term=search_term, sort_by=sort_by, descending=descending)
    
    # Display customers
    if customers:
        # Quick stats
        total_customers = len(customers)
        active_customers = sum(1 for c in customers if (datetime.datetime.now().date() - datetime.datetime.strptime(c["last_visit"], "%Y-%m-%d").date()).days <= 30)
        total_points = sum(c["points"] for c in customers)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Customers", total_customers)
        col2.metric("Active Customers (30 days)", active_customers)
        col3.metric("Total Outstanding Points", total_points)
        
        # Customer table
        customer_data = [
            {
                "Name": c["name"],
                "Email": c["email"],
                "Phone": c["phone"],
                "Points": c["points"],
                "Lifetime Points": c["lifetime_points"],
                "Visits": c["visit_count"],
                "Total Spend": f"${c['total_spend']:.2f}",
                "Last Visit": c["last_visit"],
                "Status": "Opted Out" if c["opted_out"] else "Active"
            }
            for c in customers
        ]
        
        st.dataframe(pd.DataFrame(customer_data), use_container_width=True)
        
        # Customer detail and actions
        st.write("### Customer Details")
        
        selected_customer_tuple = st.selectbox(
            "Select Customer",
            options=[(c["id"], c["name"]) for c in customers],
            format_func=lambda x: x[1]
        )
        
        selected_customer_id = selected_customer_tuple[0]
        selected_customer = loyalty_program.get_customer(selected_customer_id)
        
        if selected_customer:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### Customer Information")
                st.write(f"**Name:** {selected_customer['name']}")
                st.write(f"**Email:** {selected_customer['email']}")
                st.write(f"**Phone:** {selected_customer['phone']}")
                st.write(f"**Points:** {selected_customer['points']}")
                st.write(f"**Lifetime Points:** {selected_customer['lifetime_points']}")
                st.write(f"**Sign-up Date:** {selected_customer['signup_date']}")
                st.write(f"**Visit Count:** {selected_customer['visit_count']}")
                st.write(f"**Total Spend:** ${selected_customer['total_spend']:.2f}")
                st.write(f"**Last Visit:** {selected_customer['last_visit']}")
                
                if selected_customer["preferences"]:
                    st.write("**Preferences:**")
                    for pref in selected_customer["preferences"]:
                        st.write(f"- {pref}")
                
                if selected_customer["notes"]:
                    st.write(f"**Notes:** {selected_customer['notes']}")
            
            with col2:
                st.write("#### Customer Actions")
                
                # Add notes
                new_note = st.text_area("Add Notes")
                if st.button("Save Notes"):
                    if new_note:
                        current_notes = selected_customer["notes"]
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        updated_notes = f"{current_notes}\n{timestamp}: {new_note}" if current_notes else f"{timestamp}: {new_note}"
                        
                        updated_customer = loyalty_program.update_customer(
                            selected_customer_id,
                            {"notes": updated_notes}
                        )
                        
                        if updated_customer:
                            st.success("Notes saved successfully")
                            st.rerun()
                
                # Opt-out handling
                if not selected_customer["opted_out"]:
                    st.write("#### Opt-Out Request")
                    st.warning("Opting out will schedule the customer data for deletion within 24 hours")
                    
                    confirm_optout = st.checkbox("Confirm customer has requested to opt out")
                    
                    if confirm_optout and st.button("Process Opt-Out"):
                        result = loyalty_program.opt_out_customer(selected_customer_id)
                        
                        if result["success"]:
                            st.success(result["message"])
                            st.rerun()
                        else:
                            st.error(result["message"])
                else:
                    st.info("This customer has opted out and is scheduled for deletion")
        
        # Add new customer
        st.write("### Add New Customer")
        with st.expander("Add New Customer Form"):
            new_name = st.text_input("Customer Name")
            new_email = st.text_input("Customer Email")
            new_phone = st.text_input("Customer Phone")
            
            if st.button("Add Customer"):
                if new_name and new_email:
                    new_customer = loyalty_program.add_customer(new_name, new_email, new_phone)
                    st.success(f"Added new customer: {new_customer['name']}")
                    st.rerun()
                else:
                    st.error("Name and email are required fields")
    else:
        st.info("No customers enrolled in the loyalty program yet")
        
        # Add first customer
        st.write("### Add First Customer")
        new_name = st.text_input("Customer Name")
        new_email = st.text_input("Customer Email")
        new_phone = st.text_input("Customer Phone")
        
        if st.button("Add Customer"):
            if new_name and new_email:
                new_customer = loyalty_program.add_customer(new_name, new_email, new_phone)
                st.success(f"Added new customer: {new_customer['name']}")
                st.rerun()
            else:
                st.error("Name and email are required fields")

with settings_tab:
    st.subheader("Program Settings")
    
    # Current settings
    current_settings = loyalty_program.get_settings()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Basic Settings")
        
        enabled = st.toggle("Enable Loyalty Program", value=current_settings["enabled"])
        points_per_dollar = st.number_input("Points Per Dollar", min_value=1, value=current_settings["points_per_dollar"])
        redemption_threshold = st.number_input("Redemption Threshold (Points)", min_value=1, value=current_settings["redemption_threshold"])
        redemption_value = st.text_input("Redemption Value", value=current_settings["redemption_value"])
        
        # Offline mode
        offline_mode = st.toggle("Offline Mode", value=current_settings.get("offline_mode", False))
        
        if st.button("Save Basic Settings"):
            settings_updates = {
                "enabled": enabled,
                "points_per_dollar": points_per_dollar,
                "redemption_threshold": redemption_threshold,
                "redemption_value": redemption_value,
                "offline_mode": offline_mode
            }
            
            updated_settings = loyalty_program.update_settings(settings_updates)
            st.success("Settings updated successfully")
    
    with col2:
        st.write("### Event Settings")
        
        st.write("Double Points Events")
        
        # Get upcoming events
        upcoming_events = event_recommender.get_upcoming_events(days=30)
        
        if upcoming_events:
            event_options = [(e["id"], e["name"]) for e in upcoming_events]
            double_points_events = current_settings.get("double_points_events", [])
            
            for event_id, event_name in event_options:
                is_double = event_name in double_points_events
                if st.checkbox(f"Double points for {event_name}", value=is_double):
                    if event_name not in double_points_events:
                        double_points_events.append(event_name)
                else:
                    if event_name in double_points_events:
                        double_points_events.remove(event_name)
            
            if st.button("Save Event Settings"):
                settings_updates = {
                    "double_points_events": double_points_events
                }
                
                updated_settings = loyalty_program.update_settings(settings_updates)
                st.success("Event settings updated successfully")
        else:
            st.info("No upcoming events found. Add events in the Event Recommender section.")
    
    # Notification settings
    st.write("### Notification Settings")
    
    notification_emails = st.text_input(
        "Notification Emails (comma-separated)",
        value=", ".join(current_settings.get("notification_emails", []))
    )
    
    if st.button("Save Notification Settings"):
        email_list = [email.strip() for email in notification_emails.split(",") if email.strip()]
        
        settings_updates = {
            "notification_emails": email_list
        }
        
        updated_settings = loyalty_program.update_settings(settings_updates)
        st.success("Notification settings updated successfully")
    
    # Square POS integration
    st.write("### Square POS Integration")
    st.info("In a production environment, this section would contain Square API configuration settings.")
    
    # Last sync information
    last_sync = current_settings.get("last_square_sync", "Never")
    st.write(f"Last sync with Square: {last_sync}")