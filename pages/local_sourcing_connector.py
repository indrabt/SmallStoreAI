import streamlit as st
import pandas as pd
import datetime
import uuid
import os
import time
from modules.local_sourcing import LocalSourcingManager
from modules.hub_integration import LogisticsHubIntegration

def generate_time_slots():
    """Generate time slots for pickup window selection"""
    current_time = datetime.datetime.now()
    start_hour = 8  # 8:00 AM
    end_hour = 18   # 6:00 PM
    
    # Round to the nearest hour
    current_hour = current_time.replace(minute=0, second=0, microsecond=0)
    
    # If it's after end_hour, start with tomorrow
    if current_time.hour >= end_hour:
        current_hour = (current_hour + datetime.timedelta(days=1)).replace(hour=start_hour)
    elif current_time.hour < start_hour:
        current_hour = current_hour.replace(hour=start_hour)
    else:
        # Round up to the next hour
        current_hour = current_hour + datetime.timedelta(hours=1)
    
    time_slots = []
    max_days = 7  # Generate slots for up to 7 days
    
    for day_offset in range(max_days):
        day = current_hour + datetime.timedelta(days=day_offset)
        
        # For the first day, start from the current hour
        day_start_hour = day.hour if day_offset == 0 else start_hour
        
        for hour in range(day_start_hour, end_hour):
            slot_time = day.replace(hour=hour)
            formatted_time = slot_time.strftime("%Y-%m-%d %H:%M")
            time_slots.append(formatted_time)
    
    return time_slots

def main():
    st.title("Low-Cost Local Sourcing Connector")
    
    # Initialize managers
    sourcing_manager = LocalSourcingManager()
    hub_manager = LogisticsHubIntegration()
    
    st.markdown("""
    ### Send automated orders to local suppliers
    Connect with farmers and suppliers, send automated SMS/email orders, and schedule pickups.
    """)
    
    # Create tabs for different functions
    tab1, tab2, tab3, tab4 = st.tabs(["Create Order", "Order Status", "Response Management", "Driver Assignment"])
    
    with tab1:
        st.subheader("Create New Order")
        
        # Get supplier data
        all_suppliers = sourcing_manager.get_supplier_list()
        local_suppliers = [s for s in all_suppliers if s['is_local']]
        
        # Supplier selection
        selected_supplier_name = st.selectbox(
            "Select Supplier", 
            options=[s['name'] for s in local_suppliers],
            index=0
        )
        
        # Get selected supplier details
        selected_supplier = sourcing_manager.get_supplier_by_name(selected_supplier_name)
        
        if selected_supplier:
            # Display supplier info
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Contact:** {selected_supplier['contact_name']}")
                st.info(f"**Distance:** {selected_supplier['distance']} km from Penrith")
            with col2:
                st.info(f"**Min. Order:** ${selected_supplier['min_order']:.2f}")
                st.info(f"**Reliability Score:** {selected_supplier['reliability_score']}/10")
            
            # Get supplier products
            products = selected_supplier['products']
            
            # Product selection and quantity
            col1, col2 = st.columns(2)
            with col1:
                selected_product = st.selectbox(
                    "Select Product",
                    options=[f"{p['name']} (${p['price']:.2f}/{p['unit']})" for p in products]
                )
                
                # Extract product name from selection
                product_name = selected_product.split(" (")[0]
            
            with col2:
                quantity = st.number_input("Quantity", min_value=1, value=10)
                
                # Get product details
                product_details = None
                for p in products:
                    if p['name'] == product_name:
                        product_details = p
                        break
                
                if product_details:
                    total_cost = quantity * product_details['price']
                    st.write(f"**Total Cost:** ${total_cost:.2f}")
                    
                    # Check if meets minimum order
                    if total_cost < selected_supplier['min_order']:
                        st.warning(f"Order total is below supplier's minimum order (${selected_supplier['min_order']:.2f})")
            
            # Pickup window selection
            st.subheader("Pickup Window")
            time_slots = generate_time_slots()
            
            col1, col2 = st.columns(2)
            with col1:
                pickup_start = st.selectbox("Pickup Start Time", time_slots, index=0)
            with col2:
                # Filter end times to be after start time
                start_index = time_slots.index(pickup_start)
                valid_end_times = time_slots[start_index + 1:start_index + 7]  # Allow up to 6 hours window
                
                # Handle case where we're at the end of the time slots
                if not valid_end_times:
                    valid_end_times = [time_slots[-1]]
                
                pickup_end = st.selectbox("Pickup End Time", valid_end_times, index=min(2, len(valid_end_times)-1))
            
            # Notification method
            notification_method = st.radio("Notification Method", ["SMS", "Email"], horizontal=True)
            
            # Process form submission
            if st.button("Send Order"):
                with st.spinner("Processing order..."):
                    # Create order in the system
                    order = sourcing_manager.create_order(
                        selected_supplier['id'],
                        product_name,
                        quantity,
                        pickup_start,
                        pickup_end
                    )
                    
                    if order:
                        # Send notification
                        notification_type = "sms" if notification_method == "SMS" else "email"
                        result = sourcing_manager.send_order_notification(order['id'], notification_type)
                        
                        if result['success']:
                            st.success(f"Order sent to {selected_supplier_name}! {result['message']}")
                            
                            # Show order details
                            st.write("**Order Details:**")
                            st.write(f"- Order ID: #{order['id'][:8]}")
                            st.write(f"- Product: {product_name}")
                            st.write(f"- Quantity: {quantity}")
                            st.write(f"- Total Cost: ${total_cost:.2f}")
                            st.write(f"- Pickup Window: {pickup_start} to {pickup_end}")
                            st.write(f"- Notification: {notification_method}")
                            
                            # Show expected timing
                            order_time = datetime.datetime.now()
                            expected_confirmation = order_time + datetime.timedelta(minutes=5)
                            st.info(f"Expected confirmation by: {expected_confirmation.strftime('%H:%M')} (within 5 minutes)")
                        else:
                            st.error(f"Failed to send notification: {result['message']}")
                    else:
                        st.error("Failed to create order. Please try again.")
    
    with tab2:
        st.subheader("Order Status")
        
        # Get orders
        orders = sourcing_manager.get_orders()
        
        if not orders:
            st.info("No orders have been placed yet.")
        else:
            # Create a DataFrame for easier display
            order_data = []
            for order in orders:
                order_data.append({
                    "Order ID": order['id'][:8],
                    "Supplier": order['supplier_name'],
                    "Product": order['product']['name'],
                    "Quantity": order['quantity'],
                    "Total": f"${order['total_amount']:.2f}",
                    "Pickup": f"{order['pickup_window']['start']} to {order['pickup_window']['end']}",
                    "Status": order['status'].title(),
                    "Created": datetime.datetime.fromisoformat(order['order_date']).strftime("%Y-%m-%d %H:%M")
                })
            
            order_df = pd.DataFrame(order_data)
            
            # Order filtering
            st.write("Filter orders:")
            col1, col2 = st.columns(2)
            with col1:
                filter_supplier = st.multiselect(
                    "By Supplier",
                    options=list(set(order_df["Supplier"]))
                )
            with col2:
                filter_status = st.multiselect(
                    "By Status",
                    options=list(set(order_df["Status"]))
                )
            
            # Apply filters
            filtered_df = order_df
            if filter_supplier:
                filtered_df = filtered_df[filtered_df["Supplier"].isin(filter_supplier)]
            if filter_status:
                filtered_df = filtered_df[filtered_df["Status"].isin(filter_status)]
            
            # Display orders
            st.dataframe(filtered_df, use_container_width=True)
            
            # Order details
            st.subheader("Order Details")
            selected_order_id = st.selectbox(
                "Select Order",
                options=order_df["Order ID"].tolist(),
                format_func=lambda x: f"{x} - {order_df[order_df['Order ID'] == x]['Supplier'].iloc[0]}, {order_df[order_df['Order ID'] == x]['Product'].iloc[0]}"
            )
            
            # Find the full order
            full_order_id = None
            for order in orders:
                if order['id'][:8] == selected_order_id:
                    full_order_id = order['id']
                    selected_order = order
                    break
            
            if full_order_id:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Supplier:** {selected_order['supplier_name']}")
                    st.write(f"**Contact:** {selected_order['supplier_contact']['name']}")
                    st.write(f"**Phone:** {selected_order['supplier_contact']['phone']}")
                    st.write(f"**Email:** {selected_order['supplier_contact']['email']}")
                
                with col2:
                    st.write(f"**Product:** {selected_order['product']['name']}")
                    st.write(f"**Quantity:** {selected_order['quantity']} {selected_order['product']['unit']}")
                    st.write(f"**Price:** ${selected_order['product']['price']:.2f}/{selected_order['product']['unit']}")
                    st.write(f"**Total:** ${selected_order['total_amount']:.2f}")
                
                st.write(f"**Pickup Window:** {selected_order['pickup_window']['start']} to {selected_order['pickup_window']['end']}")
                st.write(f"**Status:** {selected_order['status'].title()}")
                
                # Status history
                st.write("**Status History:**")
                for status in selected_order['status_history']:
                    status_time = datetime.datetime.fromisoformat(status['timestamp']).strftime("%Y-%m-%d %H:%M")
                    st.write(f"- {status_time} - {status['status'].title()}: {status['note']}")
                
                # Notification history
                if selected_order['notification_history']:
                    st.write("**Notification History:**")
                    for notification in selected_order['notification_history']:
                        notification_time = datetime.datetime.fromisoformat(notification['timestamp']).strftime("%Y-%m-%d %H:%M")
                        st.write(f"- {notification_time} - {notification['type'].upper()}: {notification['status'].title()}")
    
    with tab3:
        st.subheader("Supplier Response Management")
        
        # Get pending orders
        pending_orders = sourcing_manager.get_orders(status="pending")
        
        if not pending_orders:
            st.info("No pending orders that need response management.")
        else:
            # Create options for pending orders
            pending_options = []
            for order in pending_orders:
                order_id_short = order['id'][:8]
                supplier_name = order['supplier_name']
                product_name = order['product']['name']
                quantity = order['quantity']
                
                option_text = f"{order_id_short} - {supplier_name}: {quantity} {product_name}"
                pending_options.append((option_text, order['id']))
            
            # Create a mapping of display option to full ID
            option_to_id = {opt[0]: opt[1] for opt in pending_options}
            
            # Select order to process
            selected_pending = st.selectbox(
                "Select Order to Process",
                options=[opt[0] for opt in pending_options],
                index=0
            )
            
            selected_order_id = option_to_id[selected_pending]
            selected_order = sourcing_manager.get_order_by_id(selected_order_id)
            
            # Display order info
            if selected_order:
                st.info(f"**Order:** {selected_order['quantity']} {selected_order['product']['name']} from {selected_order['supplier_name']}")
                st.info(f"**Pickup:** {selected_order['pickup_window']['start']} to {selected_order['pickup_window']['end']}")
                
                # Response simulation
                st.subheader("Supplier Response")
                
                response_type = st.radio("Response Type", ["Confirmed", "Rejected", "Custom"], horizontal=True)
                
                if response_type == "Confirmed":
                    response_text = f"Confirmed, ready by {selected_order['pickup_window']['start']}"
                elif response_type == "Rejected":
                    response_text = "Cannot fulfill this order today due to stock issues"
                else:
                    response_text = st.text_area("Enter Response Text", "")
                
                if st.button("Process Response"):
                    with st.spinner("Processing response..."):
                        result = sourcing_manager.process_supplier_response(selected_order_id, response_text)
                        
                        if result['success']:
                            status = result['status']
                            if status == "confirmed":
                                st.success(f"Order has been confirmed!")
                                st.write("Response has been logged and order status updated.")
                            elif status == "rejected":
                                st.warning("Order has been rejected by the supplier.")
                                
                                # Get alternative suppliers
                                alternatives = sourcing_manager.get_alternative_suppliers(
                                    selected_order['product']['name'],
                                    selected_order['supplier_id']
                                )
                                
                                if alternatives:
                                    st.subheader("Alternative Suppliers")
                                    st.write(f"Here are alternative suppliers for {selected_order['product']['name']}:")
                                    
                                    for i, alt in enumerate(alternatives[:3]):  # Show top 3
                                        supplier = alt['supplier']
                                        product = alt['product']
                                        
                                        st.write(f"**Option {i+1}: {supplier['name']}**")
                                        st.write(f"- Product: {product['name']}")
                                        st.write(f"- Price: ${product['price']:.2f}/{product['unit']}")
                                        st.write(f"- Distance: {supplier['distance']} km")
                                        st.write(f"- Reliability: {supplier['reliability_score']}/10")
                                        
                                        # Calculate potential new delivery time (2 hours later)
                                        original_pickup = datetime.datetime.strptime(
                                            selected_order['pickup_window']['start'], 
                                            "%Y-%m-%d %H:%M"
                                        )
                                        new_pickup = original_pickup + datetime.timedelta(hours=2)
                                        st.write(f"- Estimated New Pickup: {new_pickup.strftime('%Y-%m-%d %H:%M')}")
                                else:
                                    st.error("No alternative suppliers found for this product.")
                            else:
                                st.info("Response recorded, but manual review may be needed.")
                        else:
                            st.error(f"Failed to process response: {result['message']}")
                
                # Retry sending notification
                st.subheader("Retry Notification")
                notification_type = st.radio("Notification Method", ["SMS", "Email"], horizontal=True, key="retry_notification")
                
                if st.button("Resend Notification"):
                    with st.spinner("Sending notification..."):
                        notification_method = "sms" if notification_type == "SMS" else "email"
                        result = sourcing_manager.send_order_notification(selected_order_id, notification_method)
                        
                        if result['success']:
                            st.success(f"Notification sent! {result['message']}")
                        else:
                            st.error(f"Failed to send notification: {result['message']}")
    
    with tab4:
        st.subheader("Driver Assignment")
        
        # Get confirmed orders without drivers
        confirmed_orders = [
            order for order in sourcing_manager.get_orders(status="confirmed") 
            if not order.get('driver_assigned', False)
        ]
        
        if not confirmed_orders:
            st.info("No confirmed orders that need driver assignment.")
        else:
            # Create options for orders
            order_options = []
            for order in confirmed_orders:
                order_id_short = order['id'][:8]
                supplier_name = order['supplier_name']
                product_name = order['product']['name']
                quantity = order['quantity']
                pickup_start = order['pickup_window']['start']
                
                option_text = f"{order_id_short} - {supplier_name}: {quantity} {product_name} (Pickup: {pickup_start})"
                order_options.append((option_text, order['id']))
            
            # Create a mapping of display option to full ID
            option_to_id = {opt[0]: opt[1] for opt in order_options}
            
            # Select order to assign
            selected_order_option = st.selectbox(
                "Select Order to Assign",
                options=[opt[0] for opt in order_options],
                index=0
            )
            
            selected_order_id = option_to_id[selected_order_option]
            selected_order = sourcing_manager.get_order_by_id(selected_order_id)
            
            # Display order info
            if selected_order:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Supplier:** {selected_order['supplier_name']}")
                    st.write(f"**Address:** {sourcing_manager.get_supplier_by_id(selected_order['supplier_id'])['address']}")
                    st.write(f"**Distance:** {sourcing_manager.get_supplier_by_id(selected_order['supplier_id'])['distance']} km")
                
                with col2:
                    st.write(f"**Product:** {selected_order['product']['name']}")
                    st.write(f"**Quantity:** {selected_order['quantity']}")
                    st.write(f"**Pickup:** {selected_order['pickup_window']['start']} to {selected_order['pickup_window']['end']}")
                
                # Driver assignment
                st.subheader("Assign Driver")
                
                # Get available drivers (dummy data)
                available_drivers = ["John Smith", "Emma Wong", "David Chen", "Sarah Johnson", "Michael Zhang"]
                
                selected_driver = st.selectbox("Select Driver", available_drivers)
                
                if st.button("Assign Driver"):
                    with st.spinner("Assigning driver..."):
                        updated_order = sourcing_manager.assign_driver(selected_order_id, selected_driver)
                        
                        if updated_order:
                            st.success(f"Driver {selected_driver} assigned to order #{updated_order['id'][:8]}!")
                            
                            # Get route optimization from hub
                            routes = hub_manager.get_optimized_routes()
                            
                            st.subheader("Route Information")
                            st.write("**Optimized Route:**")
                            
                            # Show route info (sample data)
                            route_info = {
                                "estimated_distance": round(sourcing_manager.get_supplier_by_id(selected_order['supplier_id'])['distance'] * 2.1, 1),
                                "estimated_time": round(sourcing_manager.get_supplier_by_id(selected_order['supplier_id'])['distance'] * 2.1 / 30, 1),  # 30 km/h average speed
                                "estimated_fuel": round(sourcing_manager.get_supplier_by_id(selected_order['supplier_id'])['distance'] * 2.1 * 0.1, 1)  # 0.1L per km
                            }
                            
                            st.write(f"- Estimated Distance: {route_info['estimated_distance']} km (round trip)")
                            st.write(f"- Estimated Time: {route_info['estimated_time']} hours")
                            st.write(f"- Estimated Fuel: {route_info['estimated_fuel']} L")
                            
                            # Display sample route
                            if routes:
                                st.write("**Route Map:**")
                                st.image(hub_manager.get_route_map())
                        else:
                            st.error("Failed to assign driver. Please try again.")

# Run the main function
if __name__ == "__main__":
    main()