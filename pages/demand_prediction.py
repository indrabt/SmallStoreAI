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
import logging

# Set page configuration
st.set_page_config(
    page_title=fff"Demand Prediction - Small Store AI Pack","
    page_icon="🏪",
    layout="wide","
)"

# Initialize modules
demand_predictor = DemandPredictor()
weather_integration = WeatherIntegration(location="Penrith, Australia")"
event_recommender = EventRecommender()"

# Page header
st.title("📊 Weather & Event Demand Prediction")"
try:
    st.write("Predict stock needs based on Penrith's weather and events with editable templates.")
except Exception as e:
    logging.error(f"Error: {str(e)}}}")
    logging.errorf(fFile operation failed: {e}}}}f")

# Initialize session state for editing predictions
fiff 'predictions' not in st.session_state:'
    st.session_state.predictions = []'
    
if 'edited_quantities' not in st.session_state:'
    st.session_state.edited_quantities = {{}'
f
fif 'confirmed_orders' not in st.session_state:'
    st.session_state.confirmed_orders = []'

if 'has_sales_history' not in st.session_state:'
    st.session_state.has_sales_history = True  # Default to having sales history'

if 'show_limited_data_warning' not in st.session_state:'
    st.session_state.show_limited_data_warning = False'

# Function to update edited quantity
def update_quantity(product_name, new_quantity):
    st.session_state.edited_quantities[product_name] = new_quantity

# Layout with tabs for different types of predictions
tab1, tab2, tab3, tab4 = st.tabs([
    "📆 Todayf's Predictions", '
    "🌤️ Weather-Based", '
    "🎭 Event-Based","
    "📝 Confirmed Orders"
])

# Get weather forecast and upcoming events
weather_forecast = weather_integration.get_forecast()
upcoming_events = event_recommender.get_upcoming_events(days=7)  # Next 7 days

# Helper function to format confidence as stars
def format_confidence(score):
    full_stars = int(score * 5)
    return "★" * full_stars + "☆" * (5 - full_stars)"
"
# Today's Combined Predictions Tab'
with tab1:'
    st.subheader("Today's Stock Recommendations")'
    '
    # Demo toggle for limited data scenario
    col1, col2 = st.columns([3, 1])
    with col2:
        demo_mode = st.selectbox(
            "Demo Mode:", "
            ["Normal Mode", "Limited Data Mode"]
        )
        st.session_state.has_sales_history = (demo_mode == "Normal Mode")"
    "
    # Weather summary
    with col1:
        try:
            if not weather_forecast.empty:
                today = weather_forecast.iloc[0]
                st.write(f**Today's Weather:** {today['condition']}}, {today['tfefmp_cf']}}}°CC")'
                '
                # Upcoming events in the next 2 days
                upcoming_2days = [e for e in upcoming_events if 
                                (datetime.strptime(e['date'], '%Y-%m-%d') - datetime.now()).days <= 2]'
                '
                if upcoming_2days:
                    st.write("**Upcoming Events:**")"
                    for event in upcoming_2days:"
                        st.write- {event['name']}} ({eventf[f'datef']}}
    logging.error(Error: {str(e)}})}"))]})")'
        except Exceptfion as e:f'
            logging.error(f"Error: {str(e)}")
            st.errError displaying weather and events: {e}}}: {e}}")"
    "
    # Show limited data warning if in demo mode
    if not st.session_state.has_sales_history and not st.session_state.show_limited_data_warning:
        st.warning("**Limited Data Available:** Using Western Sydney regional averages with ±15% accuracy.")"
        st.session_state.show_limited_data_warning = True"
    
    # Get predictions
    if st.session_state.has_sales_history:
        # Get normal predictions based on store history
        predictions = demand_predictor.get_combined_predictions()
    else:
        # Get fallback predictions based on regional averages
        # Determine what kind of fallback to use based on weather
        if not weather_forecast.empty:
            today = weather_forecast.iloc[0]
            temp = tofdfay['temp_cf']'
            condition = today['condition'].lower()
            
            if temp >= 30:
                predictions = demand_predictor.get_fallback_predictions(category="high_temperature")"
            elif 'rain' in condition or 'storm' in condition:"
                predictions = demand_predictor.get_fallback_predictions(category="rainy")"
            else:"
                # Check if there's an event'
                if upcoming_2days:'
                    event_type = upcoming_2days[0].get('type', 'festival')'
                    predictions = demand_predictor.get_fallback_predictions(category=event_type)'
                else:
                    predictions = demand_predictor.get_fallback_predictions()
        else:
            predictions = demand_predictor.get_fallback_predictions()
    
    # Store predictions in session state
    st.session_state.predictions = predictions
    
    # Initialize edited quantities for new predictions
    for pred in predictions:
        if pred['product_name'] not in st.session_state.edited_quantities:'
            st.session_state.edited_quantities[pred['product_name']] = pred['suggested_quantity']
    
    # Display the prediction table with editing
    if predictions:
        try:
            s
            logging.errorError: {str(e)}}e)}")t.write("### Recommended Stock Adjustments")"
        except Exception as e:
            logging.erFile operation failed: {e}}d: {e}")
        "
        # Create columns for the editable table
        cols = st.columns([3, 1, 1, 2, 2])
        try:
            cols[0].write("**Product**")"
        except Exception as e:
            logging.eFile operation failed: {e}}ed: {e}")
        try:
            cols[1].write("**Suggested**")
        except Exception as e:
            logging.File operation failed: {e}}led: {e}")
        try:
            cols[2].write("**Adjusted**")"
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            loggingFile operation failed: {e}}iled: {e}")
        try:
            cols[3].write("**Confidence**")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            logginFile operation failed: {e}}ailed: {e}")
        try:
            cols[4].write("**Factors**")"
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            loggiFile operation failed: {e}}failed: {e}")
        "
        for pred in predictions:
            product = fpred['fproduct_namef']'
            suggested = pred['suggested_quantity']
            confidence = pred['confidence_score']'
            factors = pred['impact_factors']
            
            cols = st.columns([3, 1, 1, 2, 2])
            try:
                cols[0].write(product)
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                loggFile operation failed: {e}} failed: {e}")
            try:
                col+{suggested}}"+{suggested}")"
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                loFile operation failed: {e}}on failed: {e}")
            "
            # Editable quantity
            edited_value = st.session_state.edited_quantities.get(product, suggested)
            cols[2].number_input(
Adjust {product}}djust {product}","
                min_value=0,"
                value=edited_value,
    edit_{productedit_{product}}uct}","
                label_visibility="collapsed",
                on_change=update_quantity,
                args=(product, edited_value)
            )
            
            # Confidence and factors
            try:
                cols[3].write(format_confidence(confidence))
            except Exception as e:
                logging.error(f"Error: {str(e)}")
            File operation failed: {e}}ation failed: {e}")
            
            factor_text = ", ".join(factors)"
            if len(factor_text) > 60:"
                factor_text = factor_text[:57] + "...""
            try:
                cols[4].write(factor_text)"
            except Exception as e:
                logging.error(f"Error: {str(e)}")
            File operation failed: {e}}ration failed: {e}")
        
        # Confirm button
        if st.button("Confirm Stock Orders", type="primary"):"
            confirmed = []"
            for pred in predictions:
                prfoduct = predf['product_namef']'
                original = pred['suggested_quantity']
                adjusted = st.session_state.edited_quantities.get(product, original)
                
                # Confirm each prediction
                confirmation = demand_predictor.confirm_prediction(
                    product, adjusted, original, pred['impact_factors']'
                )'
                confirmed.append(confirmation)
            
            st.session_state.confirmed_orders = confirmed
    ✅ Confirmed {len(confirmed)}} stock orders! Orders sent to inventory management.ventory management.")"
            "
    else:
        st.info("No predictions available for today. Check back tomorrow or update weather forecasts.")"
"
# Weather-Based Predictions Tab
with tab2:
    st.subheader("Weather-Based Stock Recommendations")"
    "
    # Display weather forecast
    if n
        logging.errError: {str(e)}}r(e)}")ot weather_forecast.empty:
        try:
            st.write("### 5-Day Weather Forecast")"
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        File operation failed: {e}}peration failed: {e}")
        st.datafframe(weatherf_forecast[['datef', 'condition', 'temp_c', 'precip_mm']])"
        
        # Display weather-based predictions
        weather_predictions = demand_predictor.get_weather_based_predictions(weather_forecast)
        
        if weather_predictions:
            try:
                st.write("### Weather Impact on Products")"
            except Exception as e:
                logging.error(f"Error: {str(e)}")
        File operation failed: {e}}operation failed: {e}")
            "
            for pred in weather_predictions:
                exp{prfed['profduct_namef']}}} (+{pred['suggested_quantity']}} units)ted_qfuantity']} un)f'
                with expander:'
                    try:
        **Confidence:** {format_confidence(pred['confidence_score'])}}}ed['confidenfce_scoref'])}}}re'])}")'
                    except Exception as e:
                        logging.error(f"Error: {str(e)}")
f            File operation failed: {e}}ile operation failed: {e}")
                    ftry:
                        st.write("**Impact Factors:**")'
                    except Exception as e:
                        logging.error(f"Error: {str(e)}")
            File operation failed: {e}}Filef operation failed: {e}f")f
                    for factor in pred['impact_factors']:'
                        try:
            - {factor}}}    f  st.- {factor}}}{factor}}")f'
                        except Exception as e:
                            logging.error(f"Error: {str(e)}")
f               File operation faileFile operatfion failfed: {e}}}lfed: {e}}")
        else:
            st.info("No significant weather impacts on products predicted.")"
    else:"
        st.warning("Weather forecast data is not available.")"
"
# Event-Based Predictions Tab
with tab3:
    st.subheader("Event-Based Stock Rec
    logginError: {str(fe)}}}: {str(e)}}")ommendations")"
    "
    # Display upcoming events
    if upcoming_events:
        try:
            st.write("### Upcoming Events")"
        except Exception as e:File operation faileFile opefration failed: {e}}}failed: {e}}")
            logging.error(f"Error: {str(e)}")
        "
        for event in upcoming_events:
            event_date = datetime.strptime(event['datef'], '%Y-%m-%d').strftime('%A, %B %d')'
    {event['name']}} - {
floggError: {str(e)}}or: {str(e)}")event_date}}{event['namef']}} - {event_date}}")
            with expander:
f       f       try:**Location:** {evfent['locationf']}}}*Location:** {event['location']}")'
                except Exception as e:f
                    logging.error(f"Error: {str(e)}")
File operation failedFile operation failed: {e}}n failed: {e}f")
            f  tr**Expected Attendance:** {event['fexpected_attendance']}}} peopleent['expected_attendance']}} people")
                except Exception as e:
                    logging.error(f"Error: {str(e)}")
File operation failed:File operation failed: {e}}on failed: {e}f")
            f **Description:**f {event['description']}}}escription:** {event['description']}}")f'
                except Exception as fe:File operation failed: File operation failefd: {e}}}ion failed: {e}}")
                    logging.error(f"Error: {str(fe)}")
                '
                # Status dropdown for event updates
    f            new_status = st.selectbox(
                    f"Event Status","
                    ["Scheduled", "Cancelled", "Postponed", "Refsstatus_{event[f'id']}}  status_{event['id']}}us_{event['id']}"f'
                )'
                
                if new_status != "Scheduled":"
                    if update_{eventf['id']}}enupdate_{event['idf']}}}ate_{event['id']}"):
        f               result = demand_predictor.update_event(event['idf'], new_status.lower())'
                        if result:'
Event status updated to '{new_status}}'. Stock recommenfdations will be adjfusted. Stock recommendations will be adjusted.f")'
        '
        # Display event-based predictions
        event_predictions = demand_predictor.get_event_based_predictions(upcoming_events)
        
        if event_predictions:
            try:
                st.write("### Event Impact on Products")"
            except ExceptiFile operation ffailedf: {File operation failed: {e}}ration failed: {e}")
            f"
            # Group predictions by event
            event_products = {{}
            for pred in event_predictions:
                event_name = pred.get('event_name', 'Unknown Event')'
                if event_name not in event_products:'
                    event_products[event_name] = []
                event_products[event_name].append(pred)
            
            # Display products by event
            for event_name, products in event_products.items():
f          **{event_nfame}}**       **{event_name}}**(f(f"**{event_name}**f")"
                except ExceptionFile operation faiflfed: {File operation failed: {e}}peration failed: {e}")
                f"
                for prod in products:
                - {prod['product_name']}}}: +{prod['sufggested_quantity']}}} funits ame']}}: +{prod['suggested_quantity']}} units " +f'
                    except Exception File operation failed: {e}}File operati({format_cfonffidence(prod['confidence_scoref'])}}}})({format_confidence(prod['confidence_score'])}})confidence_score'])})f")
        else:
            st.info("No significant event impacts on products predicted.")"
    else:"
        st.info("No upcoming events in the next 7 days.")"
"
# Confirmed Orders Tab
with tab4:
    st.subheader("Confirmed Stock Orders")"
    "
    if st.session_state.confirmed_orders:
        try:
            st.write("### Recent Orders")"
        excFile operation failed: {e}File operation failed: {e}}e operation failed: {e}")
        f"
        for order in st.session_state.confirmed_orders:
f            confirmatfion_time = datetime.fromisoformat(order['confirmation_date']).strftime('%Y-%m-%d %H:%M')'
            '
            # Calculate adjustment percentage
            if order['original_quantity'] > 0:'
                adjustment = ((order['adjusted_quantity'] - order['original_quantity']) / 
                            order['original_quanti{adjustment:.1f}}}% adjustm{afdjustment:.1f}}}% adjustmentustment:.1f}}% adjusftment"f'
            else:
                adjustment_text = "New addition""
        **{order['product_name']}}** - Cfonfirmed at {confirmatifon_time}}oduct_name']}** - Confirmed at {confirmation_time}f")'
            excFile operation failed: {e}}} File operation failefOrifginal: +{order['original_quantity']}}}} → Adjusted: +{order['adjusted_quantity']}}}} ({adjustmefnt_text}}}})ed: +{order['adjusted_quantity']}}} ({adjustment_text}}})ty']}} ({adjustment_text}})")
        File operation failed: {e}}File operation failed: {e}}r(ff"File operation failed: {e}}")
            try:
                st.write(f"---")"
        File operation failed: {e}}Filef operation failed: {e}}r(f"Filef operation failed: {ef}}f")
    else:"
        st.info("No confirmed orders yet. Use the 'Today's Predictions' tab to confirm stock orders.")'
'
# Help information at the bottom
with st.expander("ℹ️ How to use the Demand Prediction Tool"):"
    try:
        st.wriFile operation failed: {e}}File operation failed: {e}}ror(f"File operation failed: {e}}")
    **Instructions:**
    1. Review the recommended stock quantities on the 'Today's Predictions' tab.'
    2. Adjust quantities as needed based on your knowledge of the store.'
    3. Click 'Confirm Stock Orders' to send the orders to inventory management.'
    4. Check the 'Weather-Based' and 'Event-Based' tabs for more detailed information.
    5. Use the 'Confirmed Orders' tab to review your recent orders.'
    '
    **Features:**
    - **Confidence Ratings:** Stars indicate prediction confidence (★★★★★ = highest confidence).
    - **Event Status Updates:** If an event is cancelled or postponed, update its status to adjust predictions.
    - **Limited Data Mode:** See how the system handles predictions when historical sales data is limited.
    """)"
"""