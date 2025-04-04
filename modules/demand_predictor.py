import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import uuid
import os
import json
from .inventory_manager import InventoryManager
from .weather_integration import WeatherIntegration
from .event_recommender import EventRecommender

class DemandPredictor:
    """
    Handles demand prediction based on weather and event data:
    - Analyzes weather impacts on specific products
    - Analyzes event impacts on specific products
    - Provides editable product quantity suggestions
    - Tracks prediction accuracy over time
    """
    
    def __init__(self, data_file="data/demand_predictions.json"):
        """Initialize the demand predictor with data file path"""
        self.data_file = data_file
        self.inventory_manager = InventoryManager()
        self.weather_integration = WeatherIntegration()
        self.event_recommender = EventRecommender()
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file exists, create if it doesn't"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        if not os.path.exists(self.data_file):
            # Create initial data structure
            initial_data = {
                "product_weather_impacts": self._generate_sample_weather_impacts(),
                "product_event_impacts": self._generate_sample_event_impacts(),
                "past_predictions": [],
                "prediction_accuracy": {},
                "default_regional_patterns": self._generate_default_regional_patterns(),
                "confirmed_orders": []
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _generate_sample_weather_impacts(self):
        """Generate sample product-specific weather impact data for first-time setup"""
        # Sample weather impacts on specific products
        impacts = [
            {
                "product_name": "Bottled Water 24-Pack",
                "temperature_impacts": [
                    {"min_temp": 30, "max_temp": 45, "impact_percentage": 100, "base_units": 50},
                    {"min_temp": 25, "max_temp": 30, "impact_percentage": 50, "base_units": 30},
                ],
                "condition_impacts": [
                    {"condition": "Sunny", "impact_percentage": 20, "base_units": 10},
                    {"condition": "Thunderstorm", "impact_percentage": -10, "base_units": -5}
                ],
                "last_analysis": datetime.now().isoformat(),
                "confidence_score": 0.85
            },
            {
                "product_name": "Ice Cream - Vanilla 1L",
                "temperature_impacts": [
                    {"min_temp": 30, "max_temp": 45, "impact_percentage": 120, "base_units": 40},
                    {"min_temp": 25, "max_temp": 30, "impact_percentage": 60, "base_units": 25},
                ],
                "condition_impacts": [
                    {"condition": "Sunny", "impact_percentage": 30, "base_units": 15},
                    {"condition": "Cloudy", "impact_percentage": -15, "base_units": -5}
                ],
                "last_analysis": datetime.now().isoformat(),
                "confidence_score": 0.82
            },
            {
                "product_name": "Umbrellas",
                "temperature_impacts": [],
                "condition_impacts": [
                    {"condition": "Light rain", "impact_percentage": 150, "base_units": 20},
                    {"condition": "Moderate rain", "impact_percentage": 250, "base_units": 30},
                    {"condition": "Heavy rain", "impact_percentage": 350, "base_units": 40},
                    {"condition": "Thunderstorm", "impact_percentage": 300, "base_units": 35}
                ],
                "last_analysis": datetime.now().isoformat(),
                "confidence_score": 0.9
            },
            {
                "product_name": "Soft Drinks 12-Pack",
                "temperature_impacts": [
                    {"min_temp": 30, "max_temp": 45, "impact_percentage": 80, "base_units": 30},
                    {"min_temp": 25, "max_temp": 30, "impact_percentage": 40, "base_units": 20},
                ],
                "condition_impacts": [
                    {"condition": "Sunny", "impact_percentage": 25, "base_units": 10}
                ],
                "last_analysis": datetime.now().isoformat(),
                "confidence_score": 0.78
            },
            {
                "product_name": "BBQ Supplies",
                "temperature_impacts": [
                    {"min_temp": 25, "max_temp": 45, "impact_percentage": 70, "base_units": 15}
                ],
                "condition_impacts": [
                    {"condition": "Sunny", "impact_percentage": 90, "base_units": 20},
                    {"condition": "Partly cloudy", "impact_percentage": 40, "base_units": 10},
                    {"condition": "Light rain", "impact_percentage": -60, "base_units": -15}
                ],
                "last_analysis": datetime.now().isoformat(),
                "confidence_score": 0.81
            }
        ]
        return impacts
    
    def _generate_sample_event_impacts(self):
        """Generate sample product-specific event impact data for first-time setup"""
        # Sample event impacts on specific products
        impacts = [
            {
                "product_name": "Bottled Water 24-Pack",
                "event_impacts": [
                    {"event_type": "festival", "impact_percentage": 120, "base_units": 60},
                    {"event_type": "sports", "impact_percentage": 80, "base_units": 40},
                    {"event_type": "market", "impact_percentage": 50, "base_units": 25}
                ],
                "last_analysis": datetime.now().isoformat(),
                "confidence_score": 0.85
            },
            {
                "product_name": "Snack Chips Large Bag",
                "event_impacts": [
                    {"event_type": "festival", "impact_percentage": 90, "base_units": 30},
                    {"event_type": "sports", "impact_percentage": 100, "base_units": 35},
                    {"event_type": "school_holiday", "impact_percentage": 70, "base_units": 25}
                ],
                "last_analysis": datetime.now().isoformat(),
                "confidence_score": 0.88
            },
            {
                "product_name": "Fresh Sandwiches",
                "event_impacts": [
                    {"event_type": "market", "impact_percentage": 110, "base_units": 40},
                    {"event_type": "fair", "impact_percentage": 80, "base_units": 30}
                ],
                "last_analysis": datetime.now().isoformat(),
                "confidence_score": 0.82
            },
            {
                "product_name": "Juice Boxes 10-Pack",
                "event_impacts": [
                    {"event_type": "school_holiday", "impact_percentage": 130, "base_units": 50},
                    {"event_type": "fair", "impact_percentage": 90, "base_units": 35}
                ],
                "last_analysis": datetime.now().isoformat(),
                "confidence_score": 0.9
            },
            {
                "product_name": "Sunscreen SPF50+",
                "event_impacts": [
                    {"event_type": "festival", "impact_percentage": 150, "base_units": 30},
                    {"event_type": "school_holiday", "impact_percentage": 120, "base_units": 25},
                    {"event_type": "sports", "impact_percentage": 100, "base_units": 20}
                ],
                "last_analysis": datetime.now().isoformat(),
                "confidence_score": 0.87
            }
        ]
        return impacts
    
    def _generate_default_regional_patterns(self):
        """Generate default regional demand patterns for Western Sydney"""
        regional_patterns = {
            "high_temperature_products": [
                {"product": "Bottled Water 24-Pack", "base_units": 80, "error_margin": 0.15},
                {"product": "Ice Cream Assorted", "base_units": 60, "error_margin": 0.15},
                {"product": "Soft Drinks 12-Pack", "base_units": 70, "error_margin": 0.15}
            ],
            "rainy_weather_products": [
                {"product": "Umbrellas", "base_units": 25, "error_margin": 0.15},
                {"product": "Rain Ponchos", "base_units": 20, "error_margin": 0.15}
            ],
            "event_products": {
                "festival": [
                    {"product": "Bottled Water 24-Pack", "base_units": 60, "error_margin": 0.15},
                    {"product": "Snack Chips", "base_units": 45, "error_margin": 0.15},
                    {"product": "Sunscreen", "base_units": 30, "error_margin": 0.15}
                ],
                "school_holiday": [
                    {"product": "Juice Boxes 10-Pack", "base_units": 50, "error_margin": 0.15},
                    {"product": "Snack Packs", "base_units": 55, "error_margin": 0.15},
                    {"product": "Ice Cream Assorted", "base_units": 40, "error_margin": 0.15}
                ]
            }
        }
        return regional_patterns
    
    def _load_data(self):
        """Load prediction data from file"""
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def _save_data(self, data):
        """Save prediction data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_weather_based_predictions(self, weather_forecast=None):
        """
        Get product quantity predictions based on weather forecast
        
        Args:
            weather_forecast (DataFrame, optional): Weather forecast data, if not provided, it will be fetched
            
        Returns:
            list: List of product quantity predictions with confidence scores
        """
        if weather_forecast is None or weather_forecast.empty:
            weather_forecast = self.weather_integration.get_forecast()
            
        if weather_forecast.empty:
            return []
        
        data = self._load_data()
        product_impacts = data["product_weather_impacts"]
        
        predictions = []
        
        # Get first day's weather (for immediate suggestions)
        try:
            first_day = weather_forecast.iloc[0]
            temp_c = first_day['temp_c']
            condition = first_day['condition']
            forecast_date = first_day['date']
        except Exception as e:
            st.error(f"Error processing weather forecast: {e}")
            return []
        
        # Process each product's weather impact
        for product in product_impacts:
            product_name = product["product_name"]
            base_quantity = 0
            impact_reasons = []
            
            # Check temperature impacts
            for temp_impact in product["temperature_impacts"]:
                if temp_impact["min_temp"] <= temp_c <= temp_impact["max_temp"]:
                    base_quantity += temp_impact["base_units"]
                    impact_reasons.append(f"{temp_c}°C temperature ({temp_impact['impact_percentage']}% impact)")
            
            # Check condition impacts
            for cond_impact in product["condition_impacts"]:
                if cond_impact["condition"].lower() in condition.lower():
                    base_quantity += cond_impact["base_units"]
                    impact_reasons.append(f"{condition} conditions ({cond_impact['impact_percentage']}% impact)")
            
            # Only add predictions with some quantity
            if base_quantity > 0:
                predictions.append({
                    "product_name": product_name,
                    "suggested_quantity": int(base_quantity),
                    "confidence_score": product["confidence_score"],
                    "based_on": "Historical weather sales patterns",
                    "impact_factors": impact_reasons,
                    "forecast_date": forecast_date
                })
        
        # Sort predictions by quantity (descending)
        return sorted(predictions, key=lambda x: x["suggested_quantity"], reverse=True)
    
    def get_event_based_predictions(self, upcoming_events=None):
        """
        Get product quantity predictions based on upcoming events
        
        Args:
            upcoming_events (list, optional): List of upcoming events, if not provided, it will be fetched
            
        Returns:
            list: List of product quantity predictions with confidence scores
        """
        if upcoming_events is None:
            upcoming_events = self.event_recommender.get_upcoming_events(days=7)  # Next 7 days
            
        if not upcoming_events:
            return []
        
        data = self._load_data()
        product_impacts = data["product_event_impacts"]
        
        predictions = []
        
        # Process each upcoming event
        for event in upcoming_events:
            event_name = event["name"]
            event_type = event.get("type", "general")
            event_date = event["date"]
            
            # Check if this event is in the next 2 days (for immediate action)
            event_datetime = datetime.strptime(event_date, '%Y-%m-%d')
            if (event_datetime - datetime.now()).days > 2:
                continue
            
            # Process each product's event impact
            for product in product_impacts:
                product_name = product["product_name"]
                
                for event_impact in product["event_impacts"]:
                    if event_impact["event_type"] == event_type:
                        predictions.append({
                            "product_name": product_name,
                            "suggested_quantity": int(event_impact["base_units"]),
                            "confidence_score": product["confidence_score"],
                            "based_on": "Historical event sales patterns",
                            "impact_factors": [f"{event_name} ({event_impact['impact_percentage']}% impact)"],
                            "forecast_date": event_date,
                            "event_name": event_name
                        })
        
        # Sort predictions by quantity (descending)
        return sorted(predictions, key=lambda x: x["suggested_quantity"], reverse=True)
    
    def get_combined_predictions(self):
        """
        Get combined predictions from weather and events
        
        Returns:
            list: List of product quantity predictions with confidence scores
        """
        weather_forecast = self.weather_integration.get_forecast()
        upcoming_events = self.event_recommender.get_upcoming_events(days=7)
        
        weather_predictions = self.get_weather_based_predictions(weather_forecast)
        event_predictions = self.get_event_based_predictions(upcoming_events)
        
        # Combine predictions (add quantities for the same product)
        combined = {}
        
        # Process weather predictions
        for pred in weather_predictions:
            product = pred["product_name"]
            if product not in combined:
                combined[product] = pred.copy()
            else:
                combined[product]["suggested_quantity"] += pred["suggested_quantity"]
                combined[product]["impact_factors"].extend(pred["impact_factors"])
                
                # Update confidence score (take the average)
                scores = [combined[product]["confidence_score"], pred["confidence_score"]]
                combined[product]["confidence_score"] = sum(scores) / len(scores)
        
        # Process event predictions
        for pred in event_predictions:
            product = pred["product_name"]
            if product not in combined:
                combined[product] = pred.copy()
            else:
                combined[product]["suggested_quantity"] += pred["suggested_quantity"]
                combined[product]["impact_factors"].extend(pred["impact_factors"])
                
                # Update confidence score (take the average)
                scores = [combined[product]["confidence_score"], pred["confidence_score"]]
                combined[product]["confidence_score"] = sum(scores) / len(scores)
                
                # Add event information if not already there
                if "event_name" in pred and "event_name" not in combined[product]:
                    combined[product]["event_name"] = pred["event_name"]
        
        # Convert back to list and sort
        combined_list = list(combined.values())
        return sorted(combined_list, key=lambda x: x["suggested_quantity"], reverse=True)
    
    def confirm_prediction(self, product_name, adjusted_quantity, original_quantity, factors):
        """
        Confirm a prediction (after user edits)
        
        Args:
            product_name (str): Name of the product
            adjusted_quantity (int): Quantity after user adjustment
            original_quantity (int): Original suggested quantity
            factors (list): Impact factors for this prediction
            
        Returns:
            dict: Confirmed prediction
        """
        data = self._load_data()
        
        # Create a record of this confirmation
        confirmation = {
            "id": str(uuid.uuid4()),
            "product_name": product_name,
            "original_quantity": original_quantity,
            "adjusted_quantity": adjusted_quantity,
            "adjustment_percentage": ((adjusted_quantity - original_quantity) / original_quantity * 100) if original_quantity else 0,
            "impact_factors": factors,
            "confirmation_date": datetime.now().isoformat(),
            "status": "pending"  # Will be updated when results are tracked
        }
        
        data["confirmed_orders"].append(confirmation)
        self._save_data(data)
        
        return confirmation
    
    def get_fallback_predictions(self, category=None):
        """
        Get fallback predictions based on Western Sydney averages when no sales history is available
        
        Args:
            category (str, optional): Weather or event category to filter by
            
        Returns:
            list: List of product quantity predictions with limited confidence
        """
        data = self._load_data()
        regional_patterns = data["default_regional_patterns"]
        
        predictions = []
        
        if category == "high_temperature":
            products = regional_patterns["high_temperature_products"]
            for product in products:
                predictions.append({
                    "product_name": product["product"],
                    "suggested_quantity": int(product["base_units"]),
                    "confidence_score": 1 - product["error_margin"],
                    "based_on": "Western Sydney regional averages",
                    "impact_factors": ["Limited local sales data available"],
                    "is_fallback": True
                })
        
        elif category == "rainy":
            products = regional_patterns["rainy_weather_products"]
            for product in products:
                predictions.append({
                    "product_name": product["product"],
                    "suggested_quantity": int(product["base_units"]),
                    "confidence_score": 1 - product["error_margin"],
                    "based_on": "Western Sydney regional averages",
                    "impact_factors": ["Limited local sales data available"],
                    "is_fallback": True
                })
                
        elif category in regional_patterns["event_products"]:
            products = regional_patterns["event_products"][category]
            for product in products:
                predictions.append({
                    "product_name": product["product"],
                    "suggested_quantity": int(product["base_units"]),
                    "confidence_score": 1 - product["error_margin"],
                    "based_on": "Western Sydney regional averages",
                    "impact_factors": ["Limited local sales data available"],
                    "is_fallback": True
                })
        
        # Return all fallbacks if no category specified
        if category is None:
            # High temperature products
            for product in regional_patterns["high_temperature_products"]:
                predictions.append({
                    "product_name": product["product"],
                    "suggested_quantity": int(product["base_units"]),
                    "confidence_score": 1 - product["error_margin"],
                    "based_on": "Western Sydney regional averages (high temperature)",
                    "impact_factors": ["Limited local sales data available"],
                    "is_fallback": True
                })
            
            # Rainy weather products
            for product in regional_patterns["rainy_weather_products"]:
                predictions.append({
                    "product_name": product["product"],
                    "suggested_quantity": int(product["base_units"]),
                    "confidence_score": 1 - product["error_margin"],
                    "based_on": "Western Sydney regional averages (rainy weather)",
                    "impact_factors": ["Limited local sales data available"],
                    "is_fallback": True
                })
            
            # Event products
            for event_type, products in regional_patterns["event_products"].items():
                for product in products:
                    predictions.append({
                        "product_name": product["product"],
                        "suggested_quantity": int(product["base_units"]),
                        "confidence_score": 1 - product["error_margin"],
                        "based_on": f"Western Sydney regional averages ({event_type})",
                        "impact_factors": ["Limited local sales data available"],
                        "is_fallback": True
                    })
        
        return predictions
    
    def update_event(self, event_id, status_change):
        """
        Update an event's status (e.g., when an event is cancelled)
        
        Args:
            event_id (str): ID of the event to update
            status_change (str): New status (e.g., 'cancelled', 'postponed')
            
        Returns:
            bool: Whether the update was successful
        """
        # This would call event_recommender.update_event() and then adjust predictions
        # For now, we'll just return True
        return True
