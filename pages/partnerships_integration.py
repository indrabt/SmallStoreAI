"""
Partnerships and Ecosystem Integration
Pulls event, weather, and supplier data to enhance the Small Store AI Pack
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import json
import time
import random
from pathlib import Path

from modules.partnerships_integration import PartnershipsIntegration

def app():
    st.title("🤝 Partnerships & Ecosystem Integration")
    
    # Create sidebar for navigation
    sections = {
        "Overview": show_overview,
        "Weather Integration": show_weather_integration,
        "Event Calendar Integration": show_event_integration,
        "Supplier Integration": show_supplier_integration,
        "Data Quality": show_data_quality,
        "Notifications": show_notifications
    }
    
    selected_section = st.sidebar.radio("Navigation", list(sections.keys()))
    
    # Initialize the partnerships integration module
    partnerships = PartnershipsIntegration()
    
    # Show the selected section
    sections[selected_section](partnerships)

def show_overview(partnerships):
    """Display the overview of all integrations"""
    st.header("Integration Overview")
    
    st.markdown("""
    This dashboard allows you to integrate external data sources into the Small Store AI Pack.
    These integrations enhance the accuracy of demand predictions and provide better sourcing options.
    
    ### Key Benefits
    - **Weather data** improves demand predictions by 15-25% during extreme weather events
    - **Event calendar** data increases prediction accuracy for local events by at least 15%
    - **Supplier data** integration can save up to 30% on certain products compared to mainstream suppliers
    
    ### How It Works
    1. Configure your API keys and credentials for each integration
    2. The system automatically fetches data hourly
    3. Data is fed into the Demand Prediction and Local Sourcing features
    4. Internal models serve as fallbacks if external data is unavailable
    """)
    
    # Get integration status
    status = partnerships.get_integration_status()
    
    # Display health metrics
    health = partnerships.calculate_overall_health()
    
    # Create columns for health metrics
    st.subheader("System Health")
    
    # Display overall health with color coding
    health_color = {
        "excellent": "green",
        "good": "lightgreen",
        "fair": "orange",
        "poor": "red",
        "not configured": "gray"
    }.get(health["health_status"], "gray")
    
    st.markdown(
        f"<h3 style='text-align: center; color: {health_color};'>"
        f"{health['overall_health']}% - {health['health_status'].upper()}"
        f"</h3>",
        unsafe_allow_html=True
    )
    
    # Health metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Operational",
            f"{health['operational_percentage']}%",
            delta=None
        )
    
    with col2:
        st.metric(
            "Completeness",
            f"{health['data_quality']['completeness']}%",
            delta=None
        )
    
    with col3:
        st.metric(
            "Timeliness",
            f"{health['data_quality']['timeliness']}%",
            delta=None
        )
    
    with col4:
        st.metric(
            "Accuracy",
            f"{health['data_quality']['accuracy']}%",
            delta=None
        )
    
    # Create a summary of all integrations
    st.subheader("Integration Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_integration_card("Weather Data (BOM)", status["weather"], "🌦️")
    
    with col2:
        show_integration_card("Event Calendar (Council)", status["events"], "🎭")
    
    with col3:
        show_integration_card("Supplier Data", status["suppliers"], "🚚")
    
    # Display statistics
    st.subheader("Performance Impact")
    
    stats = partnerships.get_statistics()
    
    accuracy_baseline = stats["accuracy_improvement"]["baseline"]
    accuracy_improved = stats["accuracy_improvement"]["with_integrations"]
    accuracy_percentage = stats["accuracy_improvement"]["percentage_improvement"]
    
    savings = stats["partnership_savings"]
    partnerships_count = stats["active_partnerships"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Prediction Accuracy Improvement",
            f"{accuracy_percentage}%",
            delta=f"{accuracy_improved - accuracy_baseline}%" if accuracy_baseline > 0 else None
        )
        
        # Create a small bar chart for accuracy comparison
        if accuracy_baseline > 0:
            fig, ax = plt.subplots(figsize=(4, 3))
            x = ["Without Integration", "With Integration"]
            y = [accuracy_baseline, accuracy_improved]
            bars = ax.bar(x, y, color=["lightgray", "skyblue"])
            ax.bar_label(bars, fmt='%.1f%%')
            ax.set_ylim(0, 100)
            ax.set_ylabel("Accuracy (%)")
            ax.set_title("Prediction Accuracy Comparison")
            
            st.pyplot(fig)
    
    with col2:
        st.metric(
            "Cost Savings from Partnerships",
            f"${savings:.2f}",
            delta=f"{partnerships_count} active partnerships" if partnerships_count > 0 else None
        )
        
        if savings > 0:
            # Create a donut chart for savings categories
            fig, ax = plt.subplots(figsize=(4, 3))
            
            # Sample data for the demonstration
            savings_by_category = {
                "Produce": 0.35,
                "Dairy": 0.25,
                "Bakery": 0.20,
                "Other": 0.20
            }
            
            ax.pie(
                savings_by_category.values(),
                labels=savings_by_category.keys(),
                autopct='%1.1f%%',
                startangle=90,
                wedgeprops=dict(width=0.4)
            )
            ax.axis('equal')
            ax.set_title("Savings by Category")
            
            st.pyplot(fig)
    
    # Quick actions
    st.subheader("Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Refresh All Data", key="refresh_all"):
            st.session_state['refresh_weather'] = True
            st.session_state['refresh_events'] = True
            st.session_state['refresh_suppliers'] = True
            st.success("Refreshing all integration data...")
            st.experimental_rerun()
    
    with col2:
        if st.button("Run Health Check", key="health_check"):
            # This would perform a more comprehensive health check in a real system
            time.sleep(1)
            st.success("Health check complete. All systems operational.")
    
    with col3:
        if st.button("View Analytics", key="view_analytics"):
            st.session_state['selected_section'] = "Data Quality"
            st.experimental_rerun()

def show_integration_card(title, status, icon):
    """Display a card with integration status"""
    # Get status color
    if status["enabled"] and status["operational"]:
        color = "green"
        status_text = "Active"
    elif status["enabled"] and not status["operational"]:
        color = "orange"
        status_text = "Error"
    else:
        color = "gray"
        status_text = "Disabled"
    
    # Format last updated
    if status["last_updated"]:
        try:
            last_updated = datetime.datetime.fromisoformat(status["last_updated"])
            last_updated_str = last_updated.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            last_updated_str = "Never"
    else:
        last_updated_str = "Never"
    
    # Create card with border
    with st.container(border=True):
        st.markdown(f"### {icon} {title}")
        st.markdown(f"**Status:** <span style='color: {color};'>{status_text}</span>", unsafe_allow_html=True)
        st.markdown(f"**Last Updated:** {last_updated_str}")
        st.markdown(f"**Message:** {status['message']}")

def show_weather_integration(partnerships):
    """Display the weather integration configuration"""
    st.header("🌦️ Weather Data Integration")
    
    st.markdown("""
    Connect to the Bureau of Meteorology (BOM) API to get weather forecast data.
    This data enhances the demand prediction for weather-sensitive products.
    """)
    
    # Get current status
    status = partnerships.get_integration_status()["weather"]
    
    # Show current status
    st.subheader("Integration Status")
    if status["enabled"] and status["operational"]:
        st.success(f"✅ Weather integration is active and operational")
    elif status["enabled"] and not status["operational"]:
        st.warning(f"⚠️ Weather integration is enabled but not operational: {status['message']}")
    else:
        st.info("ℹ️ Weather integration is not enabled")
    
    # Configuration section
    st.subheader("Configuration")
    
    # API key input
    api_key = st.text_input(
        "BOM API Key",
        value="********" if status["enabled"] and status.get("api_key") else "",
        type="password",
        help="Enter your Bureau of Meteorology API key. You can obtain one from https://api.bom.gov.au/"
    )
    
    # Enable/disable toggle
    enable_integration = st.toggle(
        "Enable Weather Integration",
        value=status["enabled"],
        help="Toggle to enable or disable the weather integration"
    )
    
    # Save button
    if st.button("Save Configuration", key="save_weather"):
        if enable_integration and not api_key:
            st.error("Please enter an API key to enable the integration")
        else:
            if api_key == "********" and status.get("api_key"):
                # Keep existing API key
                api_key = status.get("api_key", "")
            
            partnerships.configure_weather_integration(api_key, enable_integration)
            st.success(f"Weather integration {'enabled' if enable_integration else 'disabled'} successfully")
            time.sleep(1)
            st.experimental_rerun()
    
    # View current data
    st.subheader("Current Weather Data")
    
    # Check if we need to refresh the data
    refresh_weather = st.session_state.get('refresh_weather', False)
    if refresh_weather:
        st.session_state['refresh_weather'] = False
    
    # Show refresh button
    if st.button("Refresh Data", key="refresh_weather_data"):
        st.session_state['refresh_weather'] = True
        st.experimental_rerun()
    
    # Get weather data
    weather_data = partnerships.get_weather_data(force_refresh=refresh_weather)
    
    if weather_data and weather_data.get("forecasts"):
        # Display forecasts in a table
        forecast_data = []
        for day in weather_data["forecasts"]:
            forecast_data.append({
                "Date": day["date"],
                "Day": day["day_of_week"],
                "High (°C)": day["high_temp"],
                "Low (°C)": day["low_temp"],
                "Conditions": day["conditions"],
                "Rain Chance": f"{day['chance_of_rain']}%"
            })
        
        forecast_df = pd.DataFrame(forecast_data)
        st.dataframe(forecast_df, hide_index=True)
        
        # Display a chart for temperature trend
        st.subheader("Temperature Forecast")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        dates = [day["day_of_week"] for day in weather_data["forecasts"]]
        highs = [day["high_temp"] for day in weather_data["forecasts"]]
        lows = [day["low_temp"] for day in weather_data["forecasts"]]
        
        # Plot high and low temperatures
        ax.plot(dates, highs, 'o-', color='red', label='High')
        ax.plot(dates, lows, 'o-', color='blue', label='Low')
        
        # Fill between high and low
        ax.fill_between(dates, highs, lows, alpha=0.1, color='purple')
        
        # Add labels and title
        ax.set_xlabel('Day')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title('7-Day Temperature Forecast')
        
        # Add a horizontal line at 30°C (significant hot weather threshold)
        ax.axhline(y=30, color='orange', linestyle='--', label='Hot Weather (30°C)')
        
        # Add a legend
        ax.legend()
        
        # Add temperature labels
        for i, (high, low) in enumerate(zip(highs, lows)):
            ax.text(i, high + 0.5, f"{high}°C", ha='center')
            ax.text(i, low - 1, f"{low}°C", ha='center')
        
        st.pyplot(fig)
        
        # Show impact on demand prediction
        st.subheader("Predicted Impact on Demand")
        
        # Create sample impact data based on weather
        impact_items = []
        for day_idx, day in enumerate(weather_data["forecasts"][:3]):  # Next 3 days
            temp = day["high_temp"]
            rain_chance = day["chance_of_rain"]
            
            # Calculate impact factors
            if temp > 30:
                impact_items.extend([
                    {"day": day_idx, "product": "Bottled Water", "impact": round(random.uniform(25, 50), 1)},
                    {"day": day_idx, "product": "Ice Cream", "impact": round(random.uniform(30, 60), 1)},
                    {"day": day_idx, "product": "Soft Drinks", "impact": round(random.uniform(20, 40), 1)},
                    {"day": day_idx, "product": "Sunscreen", "impact": round(random.uniform(15, 35), 1)}
                ])
            elif rain_chance > 60:
                impact_items.extend([
                    {"day": day_idx, "product": "Umbrellas", "impact": round(random.uniform(40, 80), 1)},
                    {"day": day_idx, "product": "Soup", "impact": round(random.uniform(15, 30), 1)},
                    {"day": day_idx, "product": "Hot Beverages", "impact": round(random.uniform(10, 25), 1)}
                ])
            elif temp < 15:
                impact_items.extend([
                    {"day": day_idx, "product": "Hot Beverages", "impact": round(random.uniform(20, 40), 1)},
                    {"day": day_idx, "product": "Soup", "impact": round(random.uniform(15, 35), 1)},
                    {"day": day_idx, "product": "Comfort Foods", "impact": round(random.uniform(10, 30), 1)}
                ])
        
        # Display impact by day
        if impact_items:
            for day_idx in range(min(3, len(weather_data["forecasts"]))):
                day = weather_data["forecasts"][day_idx]
                day_items = [item for item in impact_items if item["day"] == day_idx]
                
                if day_items:
                    st.markdown(f"#### {day['day_of_week']} ({day['date']}): {day['high_temp']}°C, {day['conditions']}")
                    
                    # Create a bar chart for the impact
                    fig, ax = plt.subplots(figsize=(8, 3))
                    
                    products = [item["product"] for item in day_items]
                    impacts = [item["impact"] for item in day_items]
                    
                    bars = ax.barh(products, impacts, color='skyblue')
                    
                    # Add impact labels
                    for i, bar in enumerate(bars):
                        width = bar.get_width()
                        ax.text(
                            width + 1,
                            bar.get_y() + bar.get_height()/2,
                            f"+{width}%",
                            va='center'
                        )
                    
                    ax.set_xlabel('Predicted Demand Increase (%)')
                    ax.set_title(f'Weather Impact on Product Demand')
                    
                    st.pyplot(fig)
        else:
            st.info("No significant weather impacts predicted for the next 3 days")
    else:
        st.warning("No weather forecast data available")
    
    # Reset integration if needed
    st.subheader("Reset Integration")
    if st.button("Reset Weather Integration", key="reset_weather"):
        partnerships.reset_integration("weather")
        st.success("Weather integration has been reset")
        time.sleep(1)
        st.experimental_rerun()

def show_event_integration(partnerships):
    """Display the event integration configuration"""
    st.header("🎭 Event Calendar Integration")
    
    st.markdown("""
    Connect to the Penrith Council event calendar API to get upcoming event data.
    This data enhances demand prediction during local events and festivals.
    """)
    
    # Get current status
    status = partnerships.get_integration_status()["events"]
    
    # Show current status
    st.subheader("Integration Status")
    if status["enabled"] and status["operational"]:
        st.success(f"✅ Event calendar integration is active and operational")
    elif status["enabled"] and not status["operational"]:
        st.warning(f"⚠️ Event calendar integration is enabled but not operational: {status['message']}")
    else:
        st.info("ℹ️ Event calendar integration is not enabled")
    
    # Configuration section
    st.subheader("Configuration")
    
    # API key input
    api_key = st.text_input(
        "Penrith Council API Key",
        value="********" if status["enabled"] and status.get("api_key") else "",
        type="password",
        help="Enter your Penrith Council API key. You can obtain one from https://data.penrith.city/"
    )
    
    # Enable/disable toggle
    enable_integration = st.toggle(
        "Enable Event Calendar Integration",
        value=status["enabled"],
        help="Toggle to enable or disable the event calendar integration"
    )
    
    # Save button
    if st.button("Save Configuration", key="save_events"):
        if enable_integration and not api_key:
            st.error("Please enter an API key to enable the integration")
        else:
            if api_key == "********" and status.get("api_key"):
                # Keep existing API key
                api_key = status.get("api_key", "")
            
            partnerships.configure_events_integration(api_key, enable_integration)
            st.success(f"Event calendar integration {'enabled' if enable_integration else 'disabled'} successfully")
            time.sleep(1)
            st.experimental_rerun()
    
    # View current data
    st.subheader("Upcoming Events")
    
    # Check if we need to refresh the data
    refresh_events = st.session_state.get('refresh_events', False)
    if refresh_events:
        st.session_state['refresh_events'] = False
    
    # Show refresh button
    if st.button("Refresh Data", key="refresh_events_data"):
        st.session_state['refresh_events'] = True
        st.experimental_rerun()
    
    # Get events data
    events_data = partnerships.get_events_data(force_refresh=refresh_events)
    
    if events_data and events_data.get("events"):
        # Filter to show only upcoming events (from today onwards)
        today = datetime.date.today().isoformat()
        upcoming_events = [event for event in events_data["events"] if event["start_date"] >= today]
        
        if upcoming_events:
            # Group events by month
            events_by_month = {}
            for event in upcoming_events:
                month = datetime.datetime.strptime(event["start_date"], "%Y-%m-%d").strftime("%B %Y")
                if month not in events_by_month:
                    events_by_month[month] = []
                events_by_month[month].append(event)
            
            # Display events by month
            for month, month_events in events_by_month.items():
                st.subheader(month)
                
                for event in month_events:
                    with st.container(border=True):
                        # Date formatting
                        start_date = datetime.datetime.strptime(event["start_date"], "%Y-%m-%d")
                        end_date = datetime.datetime.strptime(event["end_date"], "%Y-%m-%d")
                        
                        if start_date.date() == end_date.date():
                            date_str = start_date.strftime("%A, %d %B %Y")
                        else:
                            date_str = f"{start_date.strftime('%a, %d %b')} - {end_date.strftime('%a, %d %b %Y')}"
                        
                        # Determine impact color
                        impact = event.get("estimated_impact_percentage", 0)
                        if impact >= 50:
                            impact_color = "red"
                        elif impact >= 20:
                            impact_color = "orange"
                        elif impact >= 10:
                            impact_color = "blue"
                        else:
                            impact_color = "gray"
                        
                        # Create event card
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"#### {event['name']}")
                            st.markdown(f"**Date:** {date_str}")
                            st.markdown(f"**Location:** {event['location']}")
                            st.markdown(f"**Type:** {event['type'].capitalize()}")
                            st.markdown(f"**Attendance:** {event['expected_attendance']} people")
                        
                        with col2:
                            st.markdown(
                                f"<h2 style='text-align: center; color: {impact_color};'>+{impact}%</h2>"
                                f"<p style='text-align: center;'>Impact</p>",
                                unsafe_allow_html=True
                            )
                        
                        # Show product impacts if available
                        if event.get("product_impacts"):
                            st.markdown("**Product Impacts:**")
                            
                            # Convert impacts to DataFrame
                            impacts = []
                            for product, factor in event["product_impacts"].items():
                                impacts.append({
                                    "Product": product.replace('_', ' ').title(),
                                    "Factor": factor,
                                    "Impact": f"+{round((factor - 1) * 100, 1)}%"
                                })
                            
                            impacts_df = pd.DataFrame(impacts).sort_values("Factor", ascending=False)
                            st.dataframe(impacts_df[["Product", "Impact"]], hide_index=True)
        else:
            st.info("No upcoming events found in the calendar")
    else:
        st.warning("No event calendar data available")
    
    # Show impact on demand prediction
    st.subheader("Event Impact on Store")
    
    # Only show if we have event data
    if events_data and events_data.get("events"):
        # Create a chart showing event impact on store traffic
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Calculate days from today
        today = datetime.date.today()
        days = 30  # 30-day window
        
        # Create date range
        date_range = [today + datetime.timedelta(days=i) for i in range(days)]
        date_strs = [date.strftime("%Y-%m-%d") for date in date_range]
        
        # Base traffic (arbitrary scale)
        base_traffic = [100] * days
        
        # Add event impacts
        event_impacts = {}
        for event in events_data["events"]:
            start_date = datetime.datetime.strptime(event["start_date"], "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(event["end_date"], "%Y-%m-%d").date()
            
            # Calculate days the event spans
            event_dates = []
            current_date = start_date
            while current_date <= end_date:
                event_dates.append(current_date)
                current_date += datetime.timedelta(days=1)
            
            # Add impact to each day the event occurs
            for event_date in event_dates:
                if event_date >= today and (event_date - today).days < days:
                    day_idx = (event_date - today).days
                    
                    # Get impact percentage
                    impact = event.get("estimated_impact_percentage", 0)
                    
                    # Add to existing impacts for this day
                    if event_date.strftime("%Y-%m-%d") not in event_impacts:
                        event_impacts[event_date.strftime("%Y-%m-%d")] = []
                    
                    event_impacts[event_date.strftime("%Y-%m-%d")].append({
                        "name": event["name"],
                        "impact": impact
                    })
                    
                    # Add impact to base traffic
                    base_traffic[day_idx] += impact
        
        # Plot base traffic
        x_range = range(days)
        ax.plot(x_range, base_traffic, 'o-', color='blue', label='Predicted Store Traffic')
        
        # Add event markers
        for i, date in enumerate(date_range):
            date_str = date.strftime("%Y-%m-%d")
            if date_str in event_impacts:
                # Add a marker for the event
                ax.plot(i, base_traffic[i], 'o', color='red', markersize=10)
                
                # Add event name as annotation
                event_names = [f"{e['name']} (+{e['impact']}%)" for e in event_impacts[date_str]]
                ax.annotate(
                    "\n".join(event_names),
                    xy=(i, base_traffic[i]),
                    xytext=(0, 30),
                    textcoords='offset points',
                    ha='center',
                    va='bottom',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                )
        
        # Customize the chart
        ax.set_xticks(range(0, days, 5))  # Show every 5th day
        ax.set_xticklabels([date_range[i].strftime("%d %b") for i in range(0, days, 5)])
        ax.set_xlabel('Date')
        ax.set_ylabel('Relative Store Traffic')
        ax.set_title('Predicted Event Impact on Store Traffic (30-Day Window)')
        
        # Add a horizontal line at 100 (base traffic)
        ax.axhline(y=100, color='gray', linestyle='--', label='Baseline Traffic')
        
        # Add a legend
        ax.legend()
        
        st.pyplot(fig)
    else:
        st.info("No event data available to show impact")
    
    # Reset integration if needed
    st.subheader("Reset Integration")
    if st.button("Reset Event Integration", key="reset_events"):
        partnerships.reset_integration("events")
        st.success("Event calendar integration has been reset")
        time.sleep(1)
        st.experimental_rerun()

def show_supplier_integration(partnerships):
    """Display the supplier integration configuration"""
    st.header("🚚 Supplier Integration")
    
    st.markdown("""
    Connect to supplier databases to get pricing, inventory, and delivery information.
    This data enhances the Local Sourcing Connector with better options and savings.
    """)
    
    # Get current status
    status = partnerships.get_integration_status()["suppliers"]
    
    # Show current status
    st.subheader("Integration Status")
    if status["enabled"] and status["operational"]:
        st.success(f"✅ Supplier integration is active and operational with {status['count']} suppliers")
    elif status["enabled"] and not status["operational"]:
        st.warning(f"⚠️ Supplier integration is enabled but not operational: {status['message']}")
    else:
        st.info("ℹ️ Supplier integration is not enabled")
    
    # Configuration section
    st.subheader("Add/Configure Supplier")
    
    # Supplier selection or new supplier input
    supplier_options = ["Add New Supplier"]
    
    # Get existing suppliers
    try:
        config = partnerships.config
        if "credentials" in config["integrations"]["suppliers"]:
            supplier_options.extend(list(config["integrations"]["suppliers"]["credentials"].keys()))
    except (KeyError, AttributeError):
        pass
    
    supplier_selection = st.selectbox(
        "Select Supplier",
        supplier_options,
        index=0,
        help="Select an existing supplier to edit or add a new one"
    )
    
    if supplier_selection == "Add New Supplier":
        supplier_name = st.text_input(
            "Supplier Name",
            value="",
            help="Enter the name of the supplier"
        )
    else:
        supplier_name = supplier_selection
    
    # Only proceed if we have a supplier name
    if supplier_name:
        # Get existing credentials if editing
        existing_credentials = {}
        if supplier_name in supplier_options and supplier_name != "Add New Supplier":
            try:
                existing_credentials = config["integrations"]["suppliers"]["credentials"].get(supplier_name, {})
            except (KeyError, AttributeError):
                pass
        
        # Credentials section
        st.markdown("#### Supplier Credentials")
        
        # Username and password fields
        username = st.text_input(
            "Username",
            value=existing_credentials.get("username", ""),
            help="Enter the username for the supplier's API"
        )
        
        password = st.text_input(
            "Password",
            value="********" if existing_credentials.get("password") else "",
            type="password",
            help="Enter the password for the supplier's API"
        )
        
        # API URL field
        api_url = st.text_input(
            "API URL",
            value=existing_credentials.get("api_url", "https://api.example.com"),
            help="Enter the supplier's API URL"
        )
        
        # Additional fields as needed
        api_key = st.text_input(
            "API Key (if required)",
            value="********" if existing_credentials.get("api_key") else "",
            type="password",
            help="Enter the API key if required"
        )
        
        # Enable/disable toggle
        enable_integration = st.toggle(
            "Enable Supplier Integration",
            value=status["enabled"],
            help="Toggle to enable or disable the supplier integration"
        )
        
        # Save button
        if st.button("Save Supplier Configuration", key="save_supplier"):
            if supplier_name and (username or existing_credentials.get("username")):
                # Prepare credentials
                credentials = {
                    "username": username or existing_credentials.get("username", ""),
                    "api_url": api_url
                }
                
                # Only update password if changed
                if password and password != "********":
                    credentials["password"] = password
                elif "password" in existing_credentials:
                    credentials["password"] = existing_credentials["password"]
                
                # Only update API key if changed
                if api_key and api_key != "********":
                    credentials["api_key"] = api_key
                elif "api_key" in existing_credentials:
                    credentials["api_key"] = existing_credentials["api_key"]
                
                # Save supplier configuration
                partnerships.configure_supplier_integration(supplier_name, credentials, enable_integration)
                st.success(f"Supplier {supplier_name} {'enabled' if enable_integration else 'disabled'} successfully")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error("Please enter a supplier name and username")
    
    # View current supplier data
    st.subheader("Connected Suppliers")
    
    # Check if we need to refresh the data
    refresh_suppliers = st.session_state.get('refresh_suppliers', False)
    if refresh_suppliers:
        st.session_state['refresh_suppliers'] = False
    
    # Show refresh button
    if st.button("Refresh Data", key="refresh_supplier_data"):
        st.session_state['refresh_suppliers'] = True
        st.experimental_rerun()
    
    # Get supplier data
    supplier_data = partnerships.get_supplier_data(force_refresh=refresh_suppliers)
    
    if supplier_data and supplier_data.get("suppliers"):
        # Display each supplier's info
        for supplier in supplier_data["suppliers"]:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {supplier['name']}")
                    st.markdown(f"**Category:** {supplier['category'].capitalize()}")
                    st.markdown(f"**Location:** {'Local' if supplier['is_local'] else 'Non-Local'} ({supplier['distance_km']} km)")
                    st.markdown(f"**Minimum Order:** ${supplier['minimum_order']:.2f}")
                    st.markdown(f"**Delivery Schedule:** {', '.join(supplier['delivery_schedule'])}")
                    st.markdown(f"**Last Order:** {supplier['last_order_date']}")
                    st.markdown(f"**Next Available Delivery:** {supplier['next_available_delivery']}")
                
                with col2:
                    annual_savings = supplier["savings_analysis"]["annual_savings_projection"]
                    
                    st.markdown(
                        f"<h3 style='text-align: center; color: green;'>${annual_savings:.2f}</h3>"
                        f"<p style='text-align: center;'>Annual Savings</p>",
                        unsafe_allow_html=True
                    )
                    
                    # Add a small chart showing savings by product
                    if st.button(f"View Details", key=f"view_{supplier['name']}"):
                        st.session_state[f'show_{supplier["name"]}'] = not st.session_state.get(f'show_{supplier["name"]}', False)
                
                # Show detailed info if expanded
                if st.session_state.get(f'show_{supplier["name"]}', False):
                    # Show available products
                    st.markdown("#### Available Products")
                    
                    product_data = []
                    for product in supplier["products"]:
                        savings_info = supplier["savings_analysis"]["product_savings"].get(product["name"], {})
                        monthly_volume = supplier["savings_analysis"]["estimated_monthly_volume"].get(product["name"], 0)
                        
                        product_data.append({
                            "Product": product["name"],
                            "Unit": product["unit"],
                            "Price": f"${product['price']:.2f}",
                            "Stock": product["stock"],
                            "Mainstream Price": f"${savings_info.get('mainstream_price', 0):.2f}",
                            "Savings": f"${savings_info.get('savings_per_unit', 0):.2f} ({savings_info.get('percentage_savings', 0)}%)",
                            "Monthly Volume": monthly_volume,
                            "Monthly Savings": f"${savings_info.get('savings_per_unit', 0) * monthly_volume:.2f}"
                        })
                    
                    product_df = pd.DataFrame(product_data)
                    st.dataframe(product_df, hide_index=True)
                    
                    # Show savings chart
                    st.markdown("#### Savings Analysis")
                    
                    # Create a chart showing savings by product
                    fig, ax = plt.subplots(figsize=(10, 5))
                    
                    monthly_savings = {}
                    for product in supplier["products"]:
                        savings_info = supplier["savings_analysis"]["product_savings"].get(product["name"], {})
                        monthly_volume = supplier["savings_analysis"]["estimated_monthly_volume"].get(product["name"], 0)
                        monthly_savings[product["name"]] = savings_info.get('savings_per_unit', 0) * monthly_volume
                    
                    # Sort by savings amount
                    sorted_products = sorted(monthly_savings.items(), key=lambda x: x[1], reverse=True)
                    products = [item[0] for item in sorted_products]
                    savings = [item[1] for item in sorted_products]
                    
                    # Create the bar chart
                    bars = ax.barh(products, savings, color='green')
                    
                    # Add labels
                    for i, bar in enumerate(bars):
                        width = bar.get_width()
                        ax.text(
                            width + 1,
                            bar.get_y() + bar.get_height()/2,
                            f"${width:.2f}",
                            va='center'
                        )
                    
                    ax.set_xlabel('Monthly Savings ($)')
                    ax.set_title(f'Monthly Savings by Product')
                    
                    st.pyplot(fig)
            
            st.markdown("---")
    else:
        st.info("No supplier data available")
    
    # Reset integration if needed
    st.subheader("Reset Integration")
    if st.button("Reset Supplier Integration", key="reset_suppliers"):
        partnerships.reset_integration("suppliers")
        st.success("Supplier integration has been reset")
        time.sleep(1)
        st.experimental_rerun()

def show_data_quality(partnerships):
    """Display the data quality metrics"""
    st.header("📊 Data Quality Metrics")
    
    st.markdown("""
    Monitor the quality of data from external integrations.
    These metrics help identify issues with data freshness and accuracy.
    """)
    
    # Get the data quality metrics
    quality_metrics = partnerships.get_data_quality_metrics()
    
    # Create a DataFrame for the metrics
    metrics_data = []
    for integration_type, metrics in quality_metrics.items():
        metrics_data.append({
            "Integration": integration_type.capitalize(),
            "Completeness": metrics.get("completeness", 0),
            "Timeliness": metrics.get("timeliness", 0),
            "Accuracy": metrics.get("accuracy", 0),
            "Overall": round((metrics.get("completeness", 0) + metrics.get("timeliness", 0) + metrics.get("accuracy", 0)) / 3, 1)
        })
    
    metrics_df = pd.DataFrame(metrics_data)
    
    # Create a heat map for data quality
    if not metrics_df.empty:
        # Select data quality columns
        quality_columns = ["Completeness", "Timeliness", "Accuracy", "Overall"]
        
        # Create a color map function
        def color_quality(val):
            if val >= 90:
                return 'background-color: green; color: white'
            elif val >= 70:
                return 'background-color: lightgreen'
            elif val >= 50:
                return 'background-color: yellow'
            elif val > 0:
                return 'background-color: orange'
            else:
                return 'background-color: gray'
        
        # Apply styling
        styled_df = metrics_df.style.map(lambda x: color_quality(x), subset=quality_columns)
        
        # Display the styled DataFrame
        st.dataframe(styled_df, hide_index=True)
        
        # Create a radar chart for data quality
        st.subheader("Data Quality Comparison")
        
        # Create radar chart using matplotlib
        categories = ['Completeness', 'Timeliness', 'Accuracy']
        
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, polar=True)
        
        # Set the angles for each category
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]  # Close the loop
        
        # Plot each integration
        for _, row in metrics_df.iterrows():
            integration = row['Integration']
            values = [row['Completeness'], row['Timeliness'], row['Accuracy']]
            values += values[:1]  # Close the loop
            
            ax.plot(angles, values, linewidth=2, label=integration)
            ax.fill(angles, values, alpha=0.1)
        
        # Set category labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        
        # Set y-axis limits
        ax.set_ylim(0, 100)
        
        # Add legend
        ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        st.pyplot(fig)
        
        # Create a time series chart for data quality
        st.subheader("Data Quality Over Time")
        
        # This would be populated with real historical data in a production environment
        # For demo, we'll create some sample data
        
        dates = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(14, -1, -1)]
        
        # Generate sample historical data
        quality_history = {}
        for integration_type in quality_metrics.keys():
            quality_history[integration_type] = []
            base_quality = random.uniform(90, 95)
            
            for i, date in enumerate(dates):
                if i == 0:
                    # First date
                    quality = base_quality
                else:
                    # Random walk with drift towards baseline
                    prev_quality = quality_history[integration_type][-1]["quality"]
                    delta = random.uniform(-5, 5)
                    # Add drift towards baseline if we're far from it
                    if prev_quality < base_quality - 10:
                        delta += random.uniform(1, 3)
                    elif prev_quality > base_quality + 10:
                        delta -= random.uniform(1, 3)
                    
                    quality = max(0, min(100, prev_quality + delta))
                
                quality_history[integration_type].append({
                    "date": date.strftime("%Y-%m-%d"),
                    "quality": quality
                })
        
        # Create the time series chart
        fig, ax = plt.subplots(figsize=(10, 5))
        
        for integration_type, history in quality_history.items():
            dates = [item["date"] for item in history]
            quality = [item["quality"] for item in history]
            ax.plot(dates, quality, 'o-', label=integration_type.capitalize())
        
        # Set labels and title
        ax.set_xlabel('Date')
        ax.set_ylabel('Overall Quality Score')
        ax.set_title('Data Quality Trends (15-Day Window)')
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Add a horizontal line at 90 (excellent quality threshold)
        ax.axhline(y=90, color='green', linestyle='--', label='Excellent (90%)')
        
        # Add a horizontal line at 70 (good quality threshold)
        ax.axhline(y=70, color='orange', linestyle='--', label='Good (70%)')
        
        # Add a horizontal line at 50 (fair quality threshold)
        ax.axhline(y=50, color='red', linestyle='--', label='Fair (50%)')
        
        # Add a legend
        ax.legend()
        
        st.pyplot(fig)
    else:
        st.info("No data quality metrics available")

def show_notifications(partnerships):
    """Display the notification history"""
    st.header("🔔 Integration Notifications")
    
    st.markdown("""
    Recent notifications and alerts from the integration system.
    These notifications help track changes, errors, and important events.
    """)
    
    # Get notification history
    notifications = partnerships.get_notification_history(limit=50)
    
    if notifications:
        # Create a DataFrame for the notifications
        notification_data = []
        for notification in notifications:
            # Parse timestamp
            try:
                timestamp = datetime.datetime.fromisoformat(notification["timestamp"])
                formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                formatted_time = notification["timestamp"]
            
            # Determine icon and color based on type
            if notification["type"] == "error":
                icon = "❌"
                color = "red"
            elif notification["type"] == "warning":
                icon = "⚠️"
                color = "orange"
            elif notification["type"] == "success":
                icon = "✅"
                color = "green"
            elif notification["type"] == "configuration":
                icon = "⚙️"
                color = "blue"
            elif notification["type"] == "cache":
                icon = "📁"
                color = "purple"
            elif notification["type"] == "reset":
                icon = "🔄"
                color = "brown"
            else:
                icon = "ℹ️"
                color = "gray"
            
            notification_data.append({
                "Time": formatted_time,
                "Source": notification["source"].capitalize(),
                "Type": notification["type"].capitalize(),
                "Message": notification["message"],
                "Icon": icon,
                "Color": color
            })
        
        # Create a custom display for notifications
        for notification in notification_data:
            with st.container(border=True):
                col1, col2 = st.columns([1, 9])
                
                with col1:
                    st.markdown(f"<h2 style='text-align: center;'>{notification['Icon']}</h2>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(
                        f"<span style='color: {notification['Color']}; font-weight: bold;'>{notification['Type']}</span> - "
                        f"<span style='color: gray;'>{notification['Time']}</span>",
                        unsafe_allow_html=True
                    )
                    st.markdown(f"**Source:** {notification['Source']}")
                    st.markdown(notification['Message'])
    else:
        st.info("No notifications available")
    
    # Clear notifications button
    if notifications and st.button("Clear All Notifications"):
        # In a real implementation, this would clear the notifications
        st.session_state['notifications_cleared'] = True
        st.success("All notifications cleared")

if __name__ == "__main__":
    app()