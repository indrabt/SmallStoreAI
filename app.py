import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Import modules
from modules.inventory_manager import InventoryManager
from modules.pricing_analyzer import PricingAnalyzer
from modules.pricing_assistant import PricingAssistant
from modules.local_sourcing import LocalSourcingManager
from modules.weather_integration import WeatherIntegration
from modules.event_recommender import EventRecommender
from modules.hub_integration import LogisticsHubIntegration
from modules.waste_management import WasteManagement
from modules.integration_kit import IntegrationKit

# Set page configuration
st.set_page_config(
    page_title="Small Store AI Pack",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Dashboard'

# Sidebar navigation
st.sidebar.title("🏪 Small Store AI Pack")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard", 
        "Inventory Management", 
        "Pricing Optimization",
        "Dynamic Pricing Assistant",
        "Local Sourcing", 
        "Weather Forecasting", 
        "Event Recommendations",
        "Waste Management",
        "Logistics Hub",
        "Real-Time Dashboard",
        "Integration Kit",
        "Settings"
    ]
)

st.session_state['current_page'] = page

# Initialize modules
inventory_manager = InventoryManager()
pricing_analyzer = PricingAnalyzer()
pricing_assistant = PricingAssistant()
local_sourcing = LocalSourcingManager()
weather_integration = WeatherIntegration(location="Penrith, Australia")
event_recommender = EventRecommender()
logistics_hub = LogisticsHubIntegration()
waste_manager = WasteManagement()
integration_kit = IntegrationKit()

# Cache the weather data to avoid repeated API calls
@st.cache_data(ttl=3600)
def get_weather_forecast():
    return weather_integration.get_forecast()

# Dashboard
if page == "Dashboard":
    st.title("Small Store AI Dashboard")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total Inventory Items", value=inventory_manager.get_total_items())
    
    with col2:
        st.metric(label="Low Stock Items", value=inventory_manager.get_low_stock_count())
    
    with col3:
        summary = waste_manager.get_summary()
        st.metric(label="Donation Savings", value=f"${summary['cost_savings']:.2f}")
    
    with col4:
        st.metric(label="Price Alerts", value=pricing_analyzer.get_alert_count())
    
    # Weather and inventory suggestions
    st.subheader("📊 Weather-Based Stocking Recommendations")
    
    weather_data = get_weather_forecast()
    if not weather_data.empty:
        weather_col, rec_col = st.columns(2)
        
        with weather_col:
            st.write("Weather Forecast for Next 5 Days:")
            st.dataframe(weather_data[['date', 'condition', 'temp_c', 'precip_mm']])
        
        with rec_col:
            recommendations = weather_integration.get_stocking_recommendations(weather_data)
            st.write("Recommended Stocking Adjustments:")
            for category, items in recommendations.items():
                st.write(f"**{category}**:")
                for item in items:
                    st.write(f"- {item['name']}: {item['recommendation']}")
    # Add links to the new features
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 Check out our new [Weather & Event Demand Prediction](/demand_prediction) tool for more detailed stock recommendations!")
    with col2:
        st.info("💰 Try our new [Dynamic Pricing Assistant](/dynamic_pricing_assistant) for AI-powered pricing and promotions!")
    with col3:
        st.info("♻️ Try our new [Waste Management Lite](/waste_management_lite) for tracking donations and reducing waste!")
    
    # Upcoming events and recommendations
    st.subheader("🎉 Upcoming Events")
    events = event_recommender.get_upcoming_events()
    
    if events:
        event_col, event_rec_col = st.columns(2)
        
        with event_col:
            st.write("Local Events in the Next 30 Days:")
            for event in events:
                st.write(f"**{event['name']}** - {event['date']}")
                st.write(f"_{event['description']}_")
                st.write("---")
        
        with event_rec_col:
            st.write("Event-Based Product Recommendations:")
            for event in events:
                st.write(f"**For {event['name']}:**")
                recommendations = event_recommender.get_recommendations_for_event(event['id'])
                for rec in recommendations:
                    st.write(f"- {rec['product']} (Expected lift: {rec['expected_sales_lift']}%)")
    
    # Inventory trend chart
    st.subheader("📈 Inventory & Sales Trends")
    inventory_data = inventory_manager.get_inventory_trends()
    
    if inventory_data is not None:
        st.line_chart(inventory_data)

# Inventory Management Page
elif page == "Inventory Management":
    st.title("Inventory Management")
    
    tab1, tab2, tab3 = st.tabs(["Current Inventory", "Stock Alerts", "Analytics"])
    
    with tab1:
        st.subheader("Current Inventory")
        inventory_data = inventory_manager.get_current_inventory()
        
        # Search and filter
        search = st.text_input("Search Products")
        category_filter = st.multiselect("Filter by Category", inventory_manager.get_categories())
        
        # Apply filters
        filtered_data = inventory_manager.filter_inventory(inventory_data, search, category_filter)
        
        # Display the inventory table
        st.dataframe(filtered_data)
        
        # Add new inventory form in an expander
        with st.expander("Add New Inventory Item"):
            with st.form("new_inventory_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Product Name")
                    category = st.selectbox("Category", inventory_manager.get_categories())
                    supplier = st.selectbox("Supplier", local_sourcing.get_suppliers())
                
                with col2:
                    quantity = st.number_input("Quantity", min_value=0)
                    cost_price = st.number_input("Cost Price ($)", min_value=0.0, format="%.2f")
                    selling_price = st.number_input("Selling Price ($)", min_value=0.0, format="%.2f")
                
                submitted = st.form_submit_button("Add Item")
                if submitted:
                    result = inventory_manager.add_inventory_item(
                        name, category, supplier, quantity, cost_price, selling_price
                    )
                    st.success(f"Added {name} to inventory!")
                    st.rerun()
    
    with tab2:
        st.subheader("Stock Alerts")
        alerts = inventory_manager.get_stock_alerts()
        
        if len(alerts) > 0:
            for alert in alerts:
                st.warning(f"**{alert['name']}**: {alert['message']}")
                st.button(f"Order {alert['name']}", key=f"order_{alert['id']}")
        else:
            st.success("No stock alerts at this time.")
    
    with tab3:
        st.subheader("Inventory Analytics")
        
        metric_type = st.selectbox(
            "Select Metric", 
            ["Inventory Value by Category", "Stock Turnover Rate", "Days of Supply"]
        )
        
        if metric_type == "Inventory Value by Category":
            data = inventory_manager.get_inventory_value_by_category()
            st.bar_chart(data)
            
        elif metric_type == "Stock Turnover Rate":
            data = inventory_manager.get_stock_turnover_rate()
            st.bar_chart(data)
            
        elif metric_type == "Days of Supply":
            data = inventory_manager.get_days_of_supply()
            st.bar_chart(data)

# Pricing Optimization Page
elif page == "Pricing Optimization":
    st.title("Pricing Optimization")
    
    tab1, tab2 = st.tabs(["Price Analysis", "Margin Optimization"])
    
    with tab1:
        st.subheader("Competitive Price Analysis")
        
        # Get pricing data
        pricing_data = pricing_analyzer.get_pricing_comparison()
        
        if pricing_data is not None:
            # Category filter
            categories = pricing_data['category'].unique()
            selected_category = st.selectbox("Select Category", ["All"] + list(categories))
            
            # Filter by category
            if selected_category != "All":
                filtered_data = pricing_data[pricing_data['category'] == selected_category]
            else:
                filtered_data = pricing_data
            
            # Display the pricing comparison
            st.dataframe(filtered_data)
            
            # Price position visualization
            st.subheader("Your Price Position")
            
            # Calculate average price difference percentage
            avg_diff = pricing_analyzer.calculate_average_price_difference(filtered_data)
            
            # Show a gauge chart for price competitiveness
            st.write(f"On average, your prices are **{abs(avg_diff):.1f}%** {'higher' if avg_diff > 0 else 'lower'} than competitors")
            
            # Show detailed price position for selected products
            position_data = pricing_analyzer.get_price_position_chart(filtered_data)
            st.bar_chart(position_data)
            
            # Price adjustment recommendations
            st.subheader("Recommended Price Adjustments")
            recommendations = pricing_analyzer.get_price_recommendations(filtered_data)
            
            for rec in recommendations:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{rec['product']}** ({rec['category']})")
                with col2:
                    st.write(f"Current: ${rec['current_price']:.2f}")
                with col3:
                    st.write(f"Suggested: ${rec['suggested_price']:.2f}")
                
                # Apply button
                if st.button(f"Apply New Price for {rec['product']}", key=f"apply_{rec['id']}"):
                    pricing_analyzer.update_price(rec['id'], rec['suggested_price'])
                    st.success(f"Updated price for {rec['product']}")
                    st.rerun()
    
    with tab2:
        st.subheader("Margin Optimization")
        
        # Get margin data
        margin_data = pricing_analyzer.get_margin_analysis()
        
        if margin_data is not None:
            # Display overall margin metrics
            avg_margin = margin_data['margin_percentage'].mean()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Average Margin", f"{avg_margin:.1f}%")
            with col2:
                target_margin = st.slider("Target Margin (%)", 10, 50, 25)
            
            # Filter low margin products
            low_margin = margin_data[margin_data['margin_percentage'] < target_margin]
            
            if not low_margin.empty:
                st.subheader("Products Below Target Margin")
                st.dataframe(low_margin)
                
                # Margin optimization recommendations
                st.subheader("Margin Optimization Recommendations")
                
                margin_recs = pricing_analyzer.get_margin_recommendations(low_margin, target_margin)
                
                for rec in margin_recs:
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
                    with col1:
                        st.write(f"**{rec['product']}** ({rec['category']})")
                    with col2:
                        st.write(f"Current: ${rec['current_price']:.2f}")
                    with col3:
                        st.write(f"Suggested: ${rec['suggested_price']:.2f}")
                    with col4:
                        st.write(f"New Margin: {rec['new_margin_percentage']:.1f}%")
                    
                    # Apply button
                    if st.button(f"Apply New Price for {rec['product']}", key=f"margin_{rec['id']}"):
                        pricing_analyzer.update_price(rec['id'], rec['suggested_price'])
                        st.success(f"Updated price for {rec['product']}")
                        st.rerun()
            else:
                st.success(f"All products are meeting or exceeding the target margin of {target_margin}%")

# Dynamic Pricing Assistant Page
elif page == "Dynamic Pricing Assistant":
    # Add link to the dynamic pricing assistant page
    st.info("Opening Dynamic Pricing Assistant...")
    st.switch_page("pages/dynamic_pricing_assistant.py")

# Local Sourcing Page
elif page == "Local Sourcing":
    st.title("Local Supplier Management")
    
    tab1, tab2, tab3 = st.tabs(["Supplier Directory", "Add Supplier", "Local Sourcing Analytics"])
    
    with tab1:
        st.subheader("Local Supplier Directory")
        
        # Get supplier data
        suppliers = local_sourcing.get_supplier_list()
        
        # Search and filter
        search = st.text_input("Search Suppliers")
        category_filter = st.multiselect("Filter by Category", local_sourcing.get_supplier_categories())
        distance_filter = st.slider("Max Distance (km)", 5, 100, 50)
        
        # Apply filters
        filtered_suppliers = local_sourcing.filter_suppliers(suppliers, search, category_filter, distance_filter)
        
        # Display suppliers on a map
        st.subheader("Supplier Locations")
        supplier_map = local_sourcing.get_supplier_map(filtered_suppliers)
        st.pyplot(supplier_map)
        
        # Display the supplier table
        for supplier in filtered_suppliers:
            with st.expander(f"{supplier['name']} ({supplier['distance']:.1f} km)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Contact**: {supplier['contact_name']}")
                    st.write(f"**Phone**: {supplier['phone']}")
                    st.write(f"**Email**: {supplier['email']}")
                    st.write(f"**Address**: {supplier['address']}")
                
                with col2:
                    st.write(f"**Categories**: {', '.join(supplier['categories'])}")
                    st.write(f"**Delivery Schedule**: {supplier['delivery_schedule']}")
                    st.write(f"**Min. Order**: ${supplier['min_order']:.2f}")
                    
                    # Products
                    st.write("**Products**:")
                    for product in supplier['products']:
                        st.write(f"- {product['name']}: ${product['price']:.2f} per {product['unit']}")
                
                # Order button
                if st.button("Place Order", key=f"order_supplier_{supplier['id']}"):
                    st.session_state['current_supplier'] = supplier['id']
                    st.session_state['current_page'] = 'Place Order'
                    st.rerun()
    
    with tab2:
        st.subheader("Add New Local Supplier")
        
        with st.form("new_supplier_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Supplier Name")
                contact_name = st.text_input("Contact Person")
                phone = st.text_input("Phone Number")
                email = st.text_input("Email Address")
                
            with col2:
                address = st.text_input("Address")
                categories = st.multiselect("Categories", local_sourcing.get_supplier_categories())
                delivery_schedule = st.selectbox("Delivery Schedule", ["Daily", "Twice a week", "Weekly", "Bi-weekly", "Monthly"])
                min_order = st.number_input("Minimum Order Value ($)", min_value=0.0, format="%.2f")
            
            # Product section
            st.subheader("Products")
            
            # Initialize product rows in session state
            if 'product_rows' not in st.session_state:
                st.session_state.product_rows = 1
            
            products = []
            for i in range(st.session_state.product_rows):
                col1, col2, col3 = st.columns(3)
                with col1:
                    product_name = st.text_input("Product Name", key=f"prod_name_{i}")
                with col2:
                    price = st.number_input("Price ($)", min_value=0.0, format="%.2f", key=f"prod_price_{i}")
                with col3:
                    unit = st.selectbox("Unit", ["kg", "g", "lb", "oz", "each", "bunch", "carton"], key=f"prod_unit_{i}")
                
                products.append({
                    "name": product_name,
                    "price": price,
                    "unit": unit
                })
            
            # Add more product rows
            if st.button("Add Another Product"):
                st.session_state.product_rows += 1
                st.rerun()
            
            submitted = st.form_submit_button("Add Supplier")
            if submitted:
                # Filter out empty products
                valid_products = [p for p in products if p['name']]
                
                if not name or not contact_name or not phone or not address or not categories or not valid_products:
                    st.error("Please fill out all required fields and add at least one product.")
                else:
                    result = local_sourcing.add_supplier(
                        name, contact_name, phone, email, address, 
                        categories, delivery_schedule, min_order, valid_products
                    )
                    st.success(f"Added {name} to supplier directory!")
                    # Reset product rows
                    st.session_state.product_rows = 1
                    st.rerun()
    
    with tab3:
        st.subheader("Local Sourcing Analytics")
        
        # Get local sourcing analytics
        analytics = local_sourcing.get_sourcing_analytics()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Local Suppliers", analytics['supplier_count'])
            st.metric("Average Distance", f"{analytics['avg_distance']:.1f} km")
        
        with col2:
            st.metric("Local Products", analytics['local_product_count'])
            st.metric("% Local Sourcing", f"{analytics['local_sourcing_percentage']:.1f}%")
        
        # Local sourcing by category
        st.subheader("Local Sourcing by Category")
        
        category_data = local_sourcing.get_sourcing_by_category()
        
        if category_data is not None:
            st.bar_chart(category_data)
        
        # Cost comparison
        st.subheader("Local vs. Non-Local Cost Comparison")
        
        cost_comparison = local_sourcing.get_cost_comparison()
        
        if cost_comparison is not None:
            st.bar_chart(cost_comparison)
            
            # Savings calculation
            savings = local_sourcing.calculate_savings()
            st.metric("Monthly Savings from Local Sourcing", f"${savings:.2f}")

# Weather Forecasting Page
elif page == "Weather Forecasting":
    st.title("Weather-Based Inventory Planning")
    
    # Get weather forecast
    weather_data = get_weather_forecast()
    
    if not weather_data.empty:
        # Display weather forecast
        st.subheader("5-Day Weather Forecast for Penrith")
        
        # Display each day's forecast in columns
        cols = st.columns(min(5, len(weather_data)))
        
        for i, (col, day_data) in enumerate(zip(cols, weather_data.iterrows())):
            with col:
                day = day_data[1]  # Index into the row data
                st.write(f"**{day['date']}**")
                
                # Weather icon based on condition
                condition = day['condition'].lower()
                if 'rain' in condition or 'shower' in condition:
                    st.write("🌧️")
                elif 'cloud' in condition:
                    st.write("⛅")
                elif 'sun' in condition or 'clear' in condition:
                    st.write("☀️")
                else:
                    st.write("🌤️")
                
                st.write(f"{day['temp_c']}°C")
                st.write(f"{day['condition']}")
                if day['precip_mm'] > 0:
                    st.write(f"Rain: {day['precip_mm']} mm")
        
        # Weather impact on sales
        st.subheader("Weather Impact on Sales")
        
        # Get weather impact data
        impact_data = weather_integration.get_weather_sales_impact()
        
        if impact_data is not None:
            st.line_chart(impact_data)
        
        # Weather-based recommendations
        st.subheader("Weather-Based Stocking Recommendations")
        
        recommendations = weather_integration.get_stocking_recommendations(weather_data)
        
        # Group recommendations by day
        for day_idx, day_data in enumerate(weather_data.iterrows()):
            day = day_data[1]
            
            with st.expander(f"Recommendations for {day['date']} ({day['condition']}, {day['temp_c']}°C)"):
                for category, items in recommendations.items():
                    st.write(f"**{category}**:")
                    for item in items:
                        # Calculate adjustment percentage
                        adjustment = item.get('adjustment_percentage', 0)
                        
                        if adjustment > 0:
                            st.success(f"Increase {item['name']} by {adjustment}% (Weather: {day['condition']})")
                        elif adjustment < 0:
                            st.warning(f"Decrease {item['name']} by {abs(adjustment)}% (Weather: {day['condition']})")
                        else:
                            st.info(f"Keep {item['name']} at normal levels")
        
        # Apply recommendations
        st.subheader("Apply Weather-Based Adjustments")
        
        if st.button("Apply All Recommendations to Inventory"):
            result = weather_integration.apply_recommendations_to_inventory(recommendations)
            st.success("Applied weather-based adjustments to inventory planning!")

# Event Recommendations Page
elif page == "Event Recommendations":
    st.title("Event-Based Recommendations")
    
    # Get upcoming events
    events = event_recommender.get_upcoming_events()
    
    if events:
        # Display event calendar
        st.subheader("Upcoming Local Events")
        
        # Calendar view using a dataframe with styling
        month_events = event_recommender.get_event_calendar()
        st.dataframe(month_events)
        
        # Event details and recommendations
        st.subheader("Event Details & Product Recommendations")
        
        for event in events:
            with st.expander(f"{event['name']} - {event['date']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Date**: {event['date']}")
                    st.write(f"**Location**: {event['location']}")
                    st.write(f"**Expected Attendance**: {event['expected_attendance']}")
                    st.write(f"**Description**: {event['description']}")
                
                with col2:
                    st.subheader("Recommended Products")
                    recommendations = event_recommender.get_recommendations_for_event(event['id'])
                    
                    for rec in recommendations:
                        col_prod, col_lift = st.columns([3, 1])
                        with col_prod:
                            st.write(f"**{rec['product']}**")
                        with col_lift:
                            st.write(f"+{rec['expected_sales_lift']}%")
                        
                        st.write(f"_{rec['recommendation_reason']}_")
                        st.write("---")
                
                # Apply recommendations
                if st.button("Apply Recommendations", key=f"apply_event_{event['id']}"):
                    result = event_recommender.apply_event_recommendations(event['id'])
                    st.success(f"Applied recommendations for {event['name']} to inventory planning!")
        
        # Add custom event
        st.subheader("Add Custom Event")
        
        with st.form("add_event_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                event_name = st.text_input("Event Name")
                event_date = st.date_input("Event Date")
                event_location = st.text_input("Location")
            
            with col2:
                event_attendance = st.number_input("Expected Attendance", min_value=1)
                event_description = st.text_area("Description")
            
            submitted = st.form_submit_button("Add Event")
            if submitted:
                if not event_name or not event_location or not event_description:
                    st.error("Please fill out all required fields.")
                else:
                    result = event_recommender.add_event(
                        event_name, event_date, event_location, 
                        event_attendance, event_description
                    )
                    st.success(f"Added {event_name} to event calendar!")
                    st.rerun()
    else:
        st.info("No upcoming events found. Add a custom event below.")
        
        # Add custom event
        st.subheader("Add Custom Event")
        
        with st.form("add_event_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                event_name = st.text_input("Event Name")
                event_date = st.date_input("Event Date")
                event_location = st.text_input("Location")
            
            with col2:
                event_attendance = st.number_input("Expected Attendance", min_value=1)
                event_description = st.text_area("Description")
            
            submitted = st.form_submit_button("Add Event")
            if submitted:
                if not event_name or not event_location or not event_description:
                    st.error("Please fill out all required fields.")
                else:
                    result = event_recommender.add_event(
                        event_name, event_date, event_location, 
                        event_attendance, event_description
                    )
                    st.success(f"Added {event_name} to event calendar!")
                    st.rerun()

# Waste Management Page
elif page == "Waste Management":
    # Redirect to the waste management page
    st.info("Opening Waste Management Lite...")
    st.switch_page("pages/waste_management_lite.py")

# Logistics Hub Integration Page
elif page == "Logistics Hub":
    st.title("Smart Logistics Hub Integration")
    
    tab1, tab2, tab3 = st.tabs(["Route Optimization", "Predictive Resilience", "Multi-Modal Logistics"])

# Real-Time Dashboard Page
elif page == "Real-Time Dashboard":
    # Redirect to the real-time dashboard page
    st.info("Opening Real-Time Client Dashboard...")
    st.switch_page("pages/realtime_dashboard.py")

# Integration Kit Page
elif page == "Integration Kit":
    # Redirect to the integration kit page
    st.info("Opening Plug-and-Play Integration Kit...")
    st.switch_page("pages/integration_kit.py")

# Settings Page
elif page == "Settings":
    st.title("Settings & Configuration")
    
    tab1, tab2, tab3 = st.tabs(["Store Profile", "Integration Settings", "Data Management"])
    
    with tab1:
        st.subheader("Store Profile")
        
        # Get current store profile
        store_profile = {
            "name": "Your Grocery Store",
            "address": "123 Main St, Penrith, Australia",
            "phone": "+61 2 1234 5678",
            "email": "contact@yourgrocerystore.com",
            "operating_hours": "Mon-Sat: 8:00 AM - 8:00 PM, Sun: 9:00 AM - 6:00 PM",
            "manager": "John Smith"
        }
        
        # Edit store profile form
        with st.form("edit_profile_form"):
            name = st.text_input("Store Name", value=store_profile["name"])
            address = st.text_input("Address", value=store_profile["address"])
            phone = st.text_input("Phone Number", value=store_profile["phone"])
            email = st.text_input("Email", value=store_profile["email"])
            operating_hours = st.text_input("Operating Hours", value=store_profile["operating_hours"])
            manager = st.text_input("Manager Name", value=store_profile["manager"])
            
            submitted = st.form_submit_button("Update Profile")
            if submitted:
                # Update profile logic would go here
                st.success("Store profile updated successfully!")
    
    with tab2:
        st.subheader("Integration Settings")
        
        # Logistics Hub Integration
        st.write("**Smart Logistics Hub Integration**")
        
        hub_api_key = st.text_input("Logistics Hub API Key", type="password", value="********")
        hub_endpoint = st.text_input("Hub API Endpoint", value="https://logistics-hub.example.com/api")
        
        hub_enabled = st.toggle("Enable Logistics Hub Integration", value=True)
        
        # Weather API Integration
        st.write("**Weather API Integration**")
        
        weather_api_key = st.text_input("Weather API Key", type="password", value="********")
        
        weather_location = st.text_input("Default Location", value="Penrith, Australia")
        weather_units = st.selectbox("Units", ["Metric (°C)", "Imperial (°F)"])
        
        weather_enabled = st.toggle("Enable Weather Integration", value=True)
        
        # Save settings
        if st.button("Save Integration Settings"):
            # Save settings logic would go here
            st.success("Integration settings saved successfully!")
    
    with tab3:
        st.subheader("Data Management")
        
        # Backup options
        st.write("**Backup Settings**")
        
        backup_frequency = st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
        backup_retention = st.slider("Backup Retention (days)", 7, 90, 30)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Backup Now"):
                # Backup logic would go here
                st.success("Backup created successfully!")
        
        with col2:
            if st.button("Restore from Backup"):
                # Restore logic would go here
                st.warning("This will overwrite current data. Are you sure?")
                confirm = st.checkbox("Yes, I understand")
                
                if confirm and st.button("Confirm Restore"):
                    st.success("Data restored successfully!")
        
        # Import/Export Data
        st.write("**Import/Export Data**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="Export All Data (CSV)",
                data="sample,data,export",
                file_name="store_data_export.csv",
                mime="text/csv"
            )
        
        with col2:
            uploaded_file = st.file_uploader("Import Data (CSV)", type="csv")
            
            if uploaded_file is not None:
                if st.button("Process Import"):
                    # Import logic would go here
                    st.success("Data imported successfully!")

# Always show the footer
st.sidebar.markdown("---")
st.sidebar.info("Small Store AI Pack v1.0")
st.sidebar.write("© 2023 Small Store AI Solutions")
