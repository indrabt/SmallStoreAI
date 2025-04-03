import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json

# Import modules
from modules.demand_predictor import DemandPredictor
from modules.weather_integration import WeatherIntegration
from modules.event_recommender import EventRecommender

# Set page configuration
st.set_page_config(
    page_title="Demand Prediction - Small Store AI Pack",
    page_icon="🏪",
    layout="wide",
)

# Initialize modules
demand_predictor = DemandPredictor()
weather_integration = WeatherIntegration(location="Penrith, Australia")
event_recommender = EventRecommender()

# Page header
st.title("📊 Weather & Event Demand Prediction")
st.write("Predict stock needs based on Penrith's weather and events with editable templates.")

# Initialize session state for editing predictions
if 'predictions' not in st.session_state:
    st.session_state.predictions = []
    
if 'edited_quantities' not in st.session_state:
    st.session_state.edited_quantities = {}

if 'confirmed_orders' not in st.session_state:
    st.session_state.confirmed_orders = []

if 'has_sales_history' not in st.session_state:
    st.session_state.has_sales_history = True  # Default to having sales history

if 'show_limited_data_warning' not in st.session_state:
    st.session_state.show_limited_data_warning = False

# Function to update edited quantity
def update_quantity(product_name, new_quantity):
    st.session_state.edited_quantities[product_name] = new_quantity

# Layout with tabs for different types of predictions
tab1, tab2, tab3, tab4 = st.tabs([
    "📆 Today's Predictions", 
    "🌤️ Weather-Based", 
    "🎭 Event-Based",
    "📝 Confirmed Orders"
])

# Get weather forecast and upcoming events
weather_forecast = weather_integration.get_forecast()
upcoming_events = event_recommender.get_upcoming_events(days=7)  # Next 7 days

# Helper function to format confidence as stars
def format_confidence(score):
    full_stars = int(score * 5)
    return "★" * full_stars + "☆" * (5 - full_stars)

# Today's Combined Predictions Tab
with tab1:
    st.subheader("Today's Stock Recommendations")
    
    # Demo toggle for limited data scenario
    col1, col2 = st.columns([3, 1])
    with col2:
        demo_mode = st.selectbox(
            "Demo Mode:", 
            ["Normal Mode", "Limited Data Mode"]
        )
        st.session_state.has_sales_history = (demo_mode == "Normal Mode")
    
    # Weather summary
    with col1:
        try:
            if not weather_forecast.empty:
                today = weather_forecast.iloc[0]
                st.write(f"**Today's Weather:** {today['condition']}, {today['temp_c']}°C")
                
                # Upcoming events in the next 2 days
                upcoming_2days = [e for e in upcoming_events if 
                                (datetime.strptime(e['date'], '%Y-%m-%d') - datetime.now()).days <= 2]
                
                if upcoming_2days:
                    st.write("**Upcoming Events:**")
                    for event in upcoming_2days:
                        st.write(f"- {event['name']} ({event['date']})")
        except Exception as e:
            st.error(f"Error displaying weather and events: {e}")
    
    # Show limited data warning if in demo mode
    if not st.session_state.has_sales_history and not st.session_state.show_limited_data_warning:
        st.warning("**Limited Data Available:** Using Western Sydney regional averages with ±15% accuracy.")
        st.session_state.show_limited_data_warning = True
    
    # Get predictions
    if st.session_state.has_sales_history:
        # Get normal predictions based on store history
        predictions = demand_predictor.get_combined_predictions()
    else:
        # Get fallback predictions based on regional averages
        # Determine what kind of fallback to use based on weather
        if not weather_forecast.empty:
            today = weather_forecast.iloc[0]
            temp = today['temp_c']
            condition = today['condition'].lower()
            
            if temp >= 30:
                predictions = demand_predictor.get_fallback_predictions(category="high_temperature")
            elif 'rain' in condition or 'storm' in condition:
                predictions = demand_predictor.get_fallback_predictions(category="rainy")
            else:
                # Check if there's an event
                if upcoming_2days:
                    event_type = upcoming_2days[0].get('type', 'festival')
                    predictions = demand_predictor.get_fallback_predictions(category=event_type)
                else:
                    predictions = demand_predictor.get_fallback_predictions()
        else:
            predictions = demand_predictor.get_fallback_predictions()
    
    # Store predictions in session state
    st.session_state.predictions = predictions
    
    # Initialize edited quantities for new predictions
    for pred in predictions:
        if pred['product_name'] not in st.session_state.edited_quantities:
            st.session_state.edited_quantities[pred['product_name']] = pred['suggested_quantity']
    
    # Display the prediction table with editing
    if predictions:
        st.write("### Recommended Stock Adjustments")
        
        # Create columns for the editable table
        cols = st.columns([3, 1, 1, 2, 2])
        cols[0].write("**Product**")
        cols[1].write("**Suggested**")
        cols[2].write("**Adjusted**")
        cols[3].write("**Confidence**")
        cols[4].write("**Factors**")
        
        for pred in predictions:
            product = pred['product_name']
            suggested = pred['suggested_quantity']
            confidence = pred['confidence_score']
            factors = pred['impact_factors']
            
            cols = st.columns([3, 1, 1, 2, 2])
            cols[0].write(product)
            cols[1].write(f"+{suggested}")
            
            # Editable quantity
            edited_value = st.session_state.edited_quantities.get(product, suggested)
            cols[2].number_input(
                f"Adjust {product}",
                min_value=0,
                value=edited_value,
                key=f"edit_{product}",
                label_visibility="collapsed",
                on_change=update_quantity,
                args=(product, st.session_state[f"edit_{product}"])
            )
            
            # Confidence and factors
            cols[3].write(format_confidence(confidence))
            
            factor_text = ", ".join(factors)
            if len(factor_text) > 60:
                factor_text = factor_text[:57] + "..."
            cols[4].write(factor_text)
        
        # Confirm button
        if st.button("Confirm Stock Orders", type="primary"):
            confirmed = []
            for pred in predictions:
                product = pred['product_name']
                original = pred['suggested_quantity']
                adjusted = st.session_state.edited_quantities.get(product, original)
                
                # Confirm each prediction
                confirmation = demand_predictor.confirm_prediction(
                    product, adjusted, original, pred['impact_factors']
                )
                confirmed.append(confirmation)
            
            st.session_state.confirmed_orders = confirmed
            st.success(f"✅ Confirmed {len(confirmed)} stock orders! Orders sent to inventory management.")
            
    else:
        st.info("No predictions available for today. Check back tomorrow or update weather forecasts.")

# Weather-Based Predictions Tab
with tab2:
    st.subheader("Weather-Based Stock Recommendations")
    
    # Display weather forecast
    if not weather_forecast.empty:
        st.write("### 5-Day Weather Forecast")
        st.dataframe(weather_forecast[['date', 'condition', 'temp_c', 'precip_mm']])
        
        # Display weather-based predictions
        weather_predictions = demand_predictor.get_weather_based_predictions(weather_forecast)
        
        if weather_predictions:
            st.write("### Weather Impact on Products")
            
            for pred in weather_predictions:
                expander = st.expander(f"{pred['product_name']} (+{pred['suggested_quantity']} units)")
                with expander:
                    st.write(f"**Confidence:** {format_confidence(pred['confidence_score'])}")
                    st.write("**Impact Factors:**")
                    for factor in pred['impact_factors']:
                        st.write(f"- {factor}")
        else:
            st.info("No significant weather impacts on products predicted.")
    else:
        st.warning("Weather forecast data is not available.")

# Event-Based Predictions Tab
with tab3:
    st.subheader("Event-Based Stock Recommendations")
    
    # Display upcoming events
    if upcoming_events:
        st.write("### Upcoming Events")
        
        for event in upcoming_events:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d').strftime('%A, %B %d')
            expander = st.expander(f"{event['name']} - {event_date}")
            with expander:
                st.write(f"**Location:** {event['location']}")
                st.write(f"**Expected Attendance:** {event['expected_attendance']} people")
                st.write(f"**Description:** {event['description']}")
                
                # Status dropdown for event updates
                new_status = st.selectbox(
                    "Event Status",
                    ["Scheduled", "Cancelled", "Postponed", "Rescheduled"],
                    key=f"status_{event['id']}"
                )
                
                if new_status != "Scheduled":
                    if st.button("Update Event Status", key=f"update_{event['id']}"):
                        result = demand_predictor.update_event(event['id'], new_status.lower())
                        if result:
                            st.success(f"Event status updated to '{new_status}'. Stock recommendations will be adjusted.")
        
        # Display event-based predictions
        event_predictions = demand_predictor.get_event_based_predictions(upcoming_events)
        
        if event_predictions:
            st.write("### Event Impact on Products")
            
            # Group predictions by event
            event_products = {}
            for pred in event_predictions:
                event_name = pred.get('event_name', 'Unknown Event')
                if event_name not in event_products:
                    event_products[event_name] = []
                event_products[event_name].append(pred)
            
            # Display products by event
            for event_name, products in event_products.items():
                st.write(f"**{event_name}**")
                
                for prod in products:
                    st.write(f"- {prod['product_name']}: +{prod['suggested_quantity']} units " +
                            f"({format_confidence(prod['confidence_score'])})")
        else:
            st.info("No significant event impacts on products predicted.")
    else:
        st.info("No upcoming events in the next 7 days.")

# Confirmed Orders Tab
with tab4:
    st.subheader("Confirmed Stock Orders")
    
    if st.session_state.confirmed_orders:
        st.write("### Recent Orders")
        
        for order in st.session_state.confirmed_orders:
            confirmation_time = datetime.fromisoformat(order['confirmation_date']).strftime('%Y-%m-%d %H:%M')
            
            # Calculate adjustment percentage
            if order['original_quantity'] > 0:
                adjustment = ((order['adjusted_quantity'] - order['original_quantity']) / 
                              order['original_quantity'] * 100)
                adjustment_text = f"{adjustment:.1f}% adjustment"
            else:
                adjustment_text = "New addition"
            
            st.write(f"**{order['product_name']}** - Confirmed at {confirmation_time}")
            st.write(f"Original: +{order['original_quantity']} → Adjusted: +{order['adjusted_quantity']} ({adjustment_text})")
            st.write("---")
    else:
        st.info("No confirmed orders yet. Use the 'Today's Predictions' tab to confirm stock orders.")

# Help information at the bottom
with st.expander("ℹ️ How to use the Demand Prediction Tool"):
    st.write("""
    **Instructions:**
    1. Review the recommended stock quantities on the 'Today's Predictions' tab.
    2. Adjust quantities as needed based on your knowledge of the store.
    3. Click 'Confirm Stock Orders' to send the orders to inventory management.
    4. Check the 'Weather-Based' and 'Event-Based' tabs for more detailed information.
    5. Use the 'Confirmed Orders' tab to review your recent orders.
    
    **Features:**
    - **Confidence Ratings:** Stars indicate prediction confidence (★★★★★ = highest confidence).
    - **Event Status Updates:** If an event is cancelled or postponed, update its status to adjust predictions.
    - **Limited Data Mode:** See how the system handles predictions when historical sales data is limited.
    """)
