import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import uuid
import os
import json
import requests

class WeatherIntegration:
    """
    Handles weather data integration and weather-based inventory recommendations:
    - Fetches weather forecast for the local area
    - Analyzes historical weather impacts on sales
    - Provides weather-based stocking recommendations
    """
    
    def __init__(self, location="Penrith, Australia", data_file="data/weather.json"):
        """Initialize the weather integration with location and data file path"""
        self.location = location
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file exists, create if it doesn't"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        if not os.path.exists(self.data_file):
            # Create initial data with sample weather impact data
            initial_data = {
                "location": self.location,
                "weather_impacts": self._generate_sample_weather_impacts(),
                "recent_forecasts": [],
                "recommendations_history": []
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _generate_sample_weather_impacts(self):
        """Generate sample weather impact data for first-time setup"""
        # Sample weather conditions
        conditions = [
            "sunny", "clear", "partly cloudy", "cloudy", 
            "overcast", "mist", "fog", "light rain", 
            "moderate rain", "heavy rain", "thunderstorm"
        ]
        
        # Sample product categories
        categories = [
            "Fruits & Vegetables", "Dairy & Eggs", "Meat & Seafood", 
            "Bakery", "Beverages", "Snacks & Confectionery", 
            "Frozen Foods", "Household & Cleaning"
        ]
        
        # Generate impact data
        impacts = []
        
        for condition in conditions:
            for category in categories:
                # Different impacts based on weather condition and category
                if "rain" in condition or condition == "thunderstorm":
                    if category in ["Fruits & Vegetables", "Bakery"]:
                        impact_value = np.random.uniform(-15, -5)
                    elif category in ["Frozen Foods", "Snacks & Confectionery"]:
                        impact_value = np.random.uniform(5, 15)
                    else:
                        impact_value = np.random.uniform(-5, 5)
                
                elif condition in ["sunny", "clear"]:
                    if category in ["Beverages", "Fruits & Vegetables", "Snacks & Confectionery"]:
                        impact_value = np.random.uniform(10, 20)
                    elif category == "Frozen Foods":
                        impact_value = np.random.uniform(15, 25)
                    else:
                        impact_value = np.random.uniform(0, 10)
                
                else:  # Cloudy, mist, fog, partly cloudy, overcast
                    impact_value = np.random.uniform(-5, 5)
                
                impacts.append({
                    "weather_condition": condition,
                    "category": category,
                    "sales_impact_percentage": round(impact_value, 1)
                })
        
        # Add temperature impacts
        temp_ranges = [
            {"min": 0, "max": 10, "label": "cold"},
            {"min": 10, "max": 20, "label": "cool"},
            {"min": 20, "max": 30, "label": "warm"},
            {"min": 30, "max": 45, "label": "hot"}
        ]
        
        for temp_range in temp_ranges:
            for category in categories:
                if temp_range["label"] == "hot":
                    if category in ["Beverages", "Frozen Foods", "Ice Cream"]:
                        impact_value = np.random.uniform(20, 35)
                    elif category in ["Bakery", "Chocolate"]:
                        impact_value = np.random.uniform(-15, -5)
                    else:
                        impact_value = np.random.uniform(-5, 5)
                
                elif temp_range["label"] == "cold":
                    if category in ["Beverages", "Frozen Foods", "Ice Cream"]:
                        impact_value = np.random.uniform(-20, -10)
                    elif category in ["Bakery", "Soups", "Hot Beverages"]:
                        impact_value = np.random.uniform(10, 20)
                    else:
                        impact_value = np.random.uniform(-5, 5)
                
                else:  # cool or warm
                    impact_value = np.random.uniform(-5, 10)
                
                impacts.append({
                    "temp_min": temp_range["min"],
                    "temp_max": temp_range["max"],
                    "temp_label": temp_range["label"],
                    "category": category,
                    "sales_impact_percentage": round(impact_value, 1)
                })
        
        return impacts
    
    def _load_data(self):
        """Load weather data from file"""
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def _save_data(self, data):
        """Save weather data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_inventory_data(self):
        """Load inventory data from file"""
        inventory_file = "data/inventory.json"
        
        if not os.path.exists(inventory_file):
            return {"inventory": []}
            
        with open(inventory_file, 'r') as f:
            return json.load(f)
    
    def get_forecast(self):
        """
        Get weather forecast for the location
        
        For demo purposes, this generates synthetic weather data
        In a real application, this would call a weather API
        """
        # Check if we have a recent forecast stored
        data = self._load_data()
        
        # Get the current time
        now = datetime.now()
        
        # Generate dates for the next 5 days
        dates = [(now + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)]
        
        # Generate weather conditions based on seasonal patterns for Penrith, Australia
        # In a real app, this would be an actual API call
        
        # Current month (1-12)
        month = now.month
        
        # Season probability weights (Southern Hemisphere)
        # Penrith has hot summers (Dec-Feb), mild winters (Jun-Aug)
        if month in [12, 1, 2]:  # Summer
            condition_weights = {
                "Sunny": 0.5, 
                "Partly cloudy": 0.3, 
                "Cloudy": 0.1, 
                "Light rain": 0.07, 
                "Thunderstorm": 0.03
            }
            temp_range = (25, 40)  # Summer temps
            precip_range = (0, 15)
            
        elif month in [3, 4, 5]:  # Autumn
            condition_weights = {
                "Sunny": 0.4, 
                "Partly cloudy": 0.3, 
                "Cloudy": 0.2, 
                "Light rain": 0.1
            }
            temp_range = (15, 25)  # Autumn temps
            precip_range = (0, 10)
            
        elif month in [6, 7, 8]:  # Winter
            condition_weights = {
                "Sunny": 0.3, 
                "Partly cloudy": 0.3, 
                "Cloudy": 0.3, 
                "Light rain": 0.1
            }
            temp_range = (5, 18)  # Winter temps
            precip_range = (0, 8)
            
        else:  # Spring (9, 10, 11)
            condition_weights = {
                "Sunny": 0.4, 
                "Partly cloudy": 0.3, 
                "Cloudy": 0.2, 
                "Light rain": 0.08,
                "Thunderstorm": 0.02
            }
            temp_range = (15, 28)  # Spring temps
            precip_range = (0, 12)
        
        # Generate conditions based on weights
        conditions = []
        for _ in range(5):
            condition = np.random.choice(
                list(condition_weights.keys()),
                p=list(condition_weights.values())
            )
            conditions.append(condition)
        
        # Generate temperatures with a slight trend
        base_temp = np.random.uniform(temp_range[0], temp_range[1])
        temps = []
        for i in range(5):
            # Add some day-to-day variation
            variation = np.random.uniform(-3, 3)
            day_temp = base_temp + variation + (i * np.random.uniform(-1, 1))
            # Ensure temperature stays in reasonable range
            day_temp = max(min(day_temp, temp_range[1] + 3), temp_range[0] - 3)
            temps.append(round(day_temp, 1))
        
        # Generate precipitation amounts
        precips = []
        for condition in conditions:
            if condition == "Sunny" or condition == "Partly cloudy":
                precip = 0
            elif condition == "Cloudy":
                precip = np.random.uniform(0, 1) if np.random.random() < 0.3 else 0
            elif condition == "Light rain":
                precip = np.random.uniform(1, 5)
            elif condition == "Thunderstorm":
                precip = np.random.uniform(5, 20)
            else:
                precip = 0
            
            precips.append(round(precip, 1))
        
        # Create forecast DataFrame
        forecast = pd.DataFrame({
            'date': dates,
            'condition': conditions,
            'temp_c': temps,
            'precip_mm': precips
        })
        
        # Store forecast in data file
        data['recent_forecasts'] = forecast.to_dict('records')
        self._save_data(data)
        
        return forecast
    
    def get_weather_sales_impact(self):
        """Get historical weather impact on sales data"""
        # For demo purposes, create a DataFrame showing sales impact by temperature/condition
        data = self._load_data()
        impacts = data['weather_impacts']
        
        # Create a pivot table from the impact data
        impact_df = pd.DataFrame(impacts)
        
        # Categorize data for plotting
        weather_impact = {}
        
        # Process condition-based impacts
        condition_impacts = impact_df[impact_df['weather_condition'].notna()]
        
        for category in condition_impacts['category'].unique():
            if category not in weather_impact:
                weather_impact[category] = {}
            
            category_data = condition_impacts[condition_impacts['category'] == category]
            
            for _, row in category_data.iterrows():
                condition = row['weather_condition'].capitalize()
                impact = row['sales_impact_percentage']
                weather_impact[category][condition] = impact
        
        # Process temperature-based impacts
        temp_impacts = impact_df[impact_df['temp_label'].notna()]
        
        for category in temp_impacts['category'].unique():
            if category not in weather_impact:
                weather_impact[category] = {}
            
            category_data = temp_impacts[temp_impacts['category'] == category]
            
            for _, row in category_data.iterrows():
                temp_label = row['temp_label'].capitalize()
                impact = row['sales_impact_percentage']
                weather_impact[category][f"Temp: {temp_label}"] = impact
        
        # Convert to DataFrame for chart
        impact_chart_df = pd.DataFrame(weather_impact)
        
        return impact_chart_df
    
    def get_stocking_recommendations(self, weather_data):
        """
        Get product stocking recommendations based on weather forecast
        
        Args:
            weather_data: DataFrame with columns 'date', 'condition', 'temp_c', 'precip_mm'
            
        Returns:
            Dictionary of recommendations by category
        """
        if weather_data is None or weather_data.empty:
            return {}
        
        data = self._load_data()
        impacts = data['weather_impacts']
        inventory_data = self._load_inventory_data()
        
        # Convert impacts to DataFrame for easier filtering
        impact_df = pd.DataFrame(impacts)
        
        # Initialize recommendations
        recommendations = {}
        
        # Process each day's weather
        for _, day in weather_data.iterrows():
            weather_condition = day['condition'].lower()
            temp_c = day['temp_c']
            
            # Find relevant impact data based on condition
            condition_matches = impact_df[impact_df['weather_condition'].notna()]
            condition_matches = condition_matches[condition_matches['weather_condition'].str.lower() == weather_condition]
            
            # Find relevant impact data based on temperature
            temp_matches = impact_df[impact_df['temp_label'].notna()]
            temp_matches = temp_matches[
                (temp_matches['temp_min'] <= temp_c) & 
                (temp_matches['temp_max'] > temp_c)
            ]
            
            # Combine impacts
            combined_impacts = {}
            
            for _, impact in condition_matches.iterrows():
                category = impact['category']
                if category not in combined_impacts:
                    combined_impacts[category] = []
                
                combined_impacts[category].append(impact['sales_impact_percentage'])
            
            for _, impact in temp_matches.iterrows():
                category = impact['category']
                if category not in combined_impacts:
                    combined_impacts[category] = []
                
                combined_impacts[category].append(impact['sales_impact_percentage'])
            
            # Calculate average impact per category
            avg_impacts = {
                category: sum(impacts) / len(impacts) 
                for category, impacts in combined_impacts.items()
            }
            
            # Add recommendations based on impacts
            for category, impact in avg_impacts.items():
                # Get inventory items for this category
                category_items = [
                    item for item in inventory_data['inventory'] 
                    if item['category'] == category
                ]
                
                if not category_items:
                    continue
                
                if category not in recommendations:
                    recommendations[category] = []
                
                for item in category_items:
                    # Calculate adjustment percentage based on impact
                    adjustment_percentage = round(impact, 1)
                    
                    # Create recommendation text
                    if adjustment_percentage > 5:
                        rec_text = f"Increase stock by {adjustment_percentage}% due to {weather_condition} weather"
                    elif adjustment_percentage < -5:
                        rec_text = f"Decrease stock by {abs(adjustment_percentage)}% due to {weather_condition} weather"
                    else:
                        rec_text = f"Maintain normal stock levels ({weather_condition} weather has minimal impact)"
                    
                    # Check if this item is already in recommendations
                    existing_item = next(
                        (r for r in recommendations[category] if r['id'] == item['id']), 
                        None
                    )
                    
                    if existing_item:
                        # Update existing recommendation if new adjustment is stronger
                        if abs(adjustment_percentage) > abs(existing_item['adjustment_percentage']):
                            existing_item['adjustment_percentage'] = adjustment_percentage
                            existing_item['recommendation'] = rec_text
                    else:
                        # Add new recommendation
                        recommendations[category].append({
                            'id': item['id'],
                            'name': item['name'],
                            'adjustment_percentage': adjustment_percentage,
                            'recommendation': rec_text
                        })
        
        return recommendations
    
    def apply_recommendations_to_inventory(self, recommendations):
        """
        Apply weather-based recommendations to inventory planning
        
        Args:
            recommendations: Dictionary of recommendations by category
            
        Returns:
            Boolean indicating success
        """
        if not recommendations:
            return False
        
        inventory_data = self._load_inventory_data()
        weather_data = self._load_data()
        
        # Flatten recommendations into a list
        all_recs = []
        for category, items in recommendations.items():
            for item in items:
                all_recs.append({
                    'category': category,
                    **item
                })
        
        # Record the application of recommendations
        application_record = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'recommendations': all_recs
        }
        
        weather_data['recommendations_history'].append(application_record)
        self._save_data(weather_data)
        
        # Note: In a real application, this would actually update order quantities or forecasts
        # For this demo, we just record that recommendations were applied
        
        return True
