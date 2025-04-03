import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import uuid
import os
import json
import calendar

class EventRecommender:
    """
    Handles event-based recommendations including:
    - Managing local events calendar
    - Analyzing historical event impacts on sales
    - Providing product recommendations for upcoming events
    """
    
    def __init__(self, data_file="data/events.json"):
        """Initialize the event recommender with data file path"""
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file exists, create if it doesn't"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        if not os.path.exists(self.data_file):
            # Create initial data with sample events
            initial_data = {
                "events": self._generate_sample_events(),
                "event_impacts": self._generate_sample_event_impacts(),
                "recommendation_history": []
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _generate_sample_events(self):
        """Generate sample events for first-time setup"""
        # Current date for reference
        now = datetime.now()
        
        # Sample events for the next 30 days
        events = [
            {
                "id": str(uuid.uuid4()),
                "name": "Penrith Farmers Market",
                "date": (now + timedelta(days=3)).strftime('%Y-%m-%d'),
                "location": "Penrith City Park",
                "description": "Weekly farmers market featuring local produce and handmade goods.",
                "expected_attendance": 500,
                "recurring": "weekly",
                "type": "market",
                "added_by": "system",
                "date_added": now.isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Western Sydney Food Festival",
                "date": (now + timedelta(days=10)).strftime('%Y-%m-%d'),
                "location": "Penrith Panthers Stadium",
                "description": "Annual food festival celebrating the diverse cuisines of Western Sydney.",
                "expected_attendance": 3000,
                "recurring": "annual",
                "type": "festival",
                "added_by": "system",
                "date_added": now.isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Penrith Community Fair",
                "date": (now + timedelta(days=15)).strftime('%Y-%m-%d'),
                "location": "Jamison Park",
                "description": "Annual community fair with rides, games, and food stalls.",
                "expected_attendance": 2000,
                "recurring": "annual",
                "type": "fair",
                "added_by": "system",
                "date_added": now.isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "School Holiday Start",
                "date": (now + timedelta(days=7)).strftime('%Y-%m-%d'),
                "location": "Penrith and surrounding areas",
                "description": "Start of school holidays for local schools.",
                "expected_attendance": 10000,
                "recurring": "seasonal",
                "type": "school_holiday",
                "added_by": "system",
                "date_added": now.isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Nepean River Festival",
                "date": (now + timedelta(days=25)).strftime('%Y-%m-%d'),
                "location": "Nepean River",
                "description": "Celebration of the Nepean River with water activities, food, and entertainment.",
                "expected_attendance": 1500,
                "recurring": "annual",
                "type": "festival",
                "added_by": "system",
                "date_added": now.isoformat()
            }
        ]
        
        return events
    
    def _generate_sample_event_impacts(self):
        """Generate sample event impact data for first-time setup"""
        # Sample product categories
        categories = [
            "Fruits & Vegetables", "Dairy & Eggs", "Meat & Seafood", 
            "Bakery", "Beverages", "Snacks & Confectionery", 
            "Frozen Foods", "Household & Cleaning"
        ]
        
        # Sample event types
        event_types = ["market", "festival", "fair", "school_holiday", "sports", "concert"]
        
        # Generate impact data
        impacts = []
        
        for event_type in event_types:
            for category in categories:
                # Different impacts based on event type and category
                if event_type == "market":
                    if category in ["Fruits & Vegetables", "Bakery", "Snacks & Confectionery"]:
                        impact_value = np.random.uniform(15, 30)
                    else:
                        impact_value = np.random.uniform(5, 15)
                
                elif event_type == "festival" or event_type == "fair":
                    if category in ["Beverages", "Snacks & Confectionery", "Frozen Foods"]:
                        impact_value = np.random.uniform(20, 35)
                    else:
                        impact_value = np.random.uniform(5, 15)
                
                elif event_type == "school_holiday":
                    if category in ["Snacks & Confectionery", "Frozen Foods", "Beverages"]:
                        impact_value = np.random.uniform(25, 40)
                    else:
                        impact_value = np.random.uniform(10, 20)
                
                elif event_type == "sports":
                    if category in ["Beverages", "Snacks & Confectionery"]:
                        impact_value = np.random.uniform(20, 35)
                    else:
                        impact_value = np.random.uniform(0, 10)
                
                elif event_type == "concert":
                    if category in ["Beverages", "Snacks & Confectionery"]:
                        impact_value = np.random.uniform(15, 30)
                    else:
                        impact_value = np.random.uniform(0, 5)
                
                else:
                    impact_value = np.random.uniform(5, 15)
                
                impacts.append({
                    "event_type": event_type,
                    "category": category,
                    "sales_impact_percentage": round(impact_value, 1)
                })
        
        # Add specific product recommendations for certain event types
        product_impacts = [
            {
                "event_type": "market",
                "product": "Reusable Shopping Bags",
                "sales_impact_percentage": 45.0,
                "recommendation_reason": "Shoppers at farmers markets often forget bags"
            },
            {
                "event_type": "market",
                "product": "Fresh Bread",
                "sales_impact_percentage": 35.0,
                "recommendation_reason": "Complements fresh produce purchases"
            },
            {
                "event_type": "festival",
                "product": "Bottled Water",
                "sales_impact_percentage": 60.0,
                "recommendation_reason": "Essential for outdoor festival-goers"
            },
            {
                "event_type": "festival",
                "product": "Sunscreen",
                "sales_impact_percentage": 40.0,
                "recommendation_reason": "Outdoor event necessity often forgotten"
            },
            {
                "event_type": "school_holiday",
                "product": "Juice Boxes",
                "sales_impact_percentage": 50.0,
                "recommendation_reason": "Popular for kids' activities and outings"
            },
            {
                "event_type": "school_holiday",
                "product": "Sandwich Supplies",
                "sales_impact_percentage": 40.0,
                "recommendation_reason": "Increased lunch preparation at home"
            },
            {
                "event_type": "fair",
                "product": "Ice Cream",
                "sales_impact_percentage": 45.0,
                "recommendation_reason": "Popular treat before/after fair attendance"
            },
            {
                "event_type": "sports",
                "product": "Sports Drinks",
                "sales_impact_percentage": 55.0,
                "recommendation_reason": "High demand for hydration before/after events"
            }
        ]
        
        impacts.extend(product_impacts)
        
        return impacts
    
    def _load_data(self):
        """Load event data from file"""
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def _save_data(self, data):
        """Save event data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_inventory_data(self):
        """Load inventory data from file"""
        inventory_file = "data/inventory.json"
        
        if not os.path.exists(inventory_file):
            return {"inventory": []}
            
        with open(inventory_file, 'r') as f:
            return json.load(f)
    
    def get_upcoming_events(self, days=30):
        """Get upcoming events within specified number of days"""
        data = self._load_data()
        events = data['events']
        
        if not events:
            return []
        
        # Current date
        now = datetime.now().date()
        
        # Filter events within the specified days
        upcoming = []
        for event in events:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
            
            if now <= event_date <= (now + timedelta(days=days)):
                upcoming.append(event)
        
        # Sort by date
        upcoming.sort(key=lambda e: e['date'])
        
        return upcoming
    
    def get_event_calendar(self):
        """Get events calendar for the current month"""
        # Get current month and year
        now = datetime.now()
        year = now.year
        month = now.month
        
        # Get all days in the month
        num_days = calendar.monthrange(year, month)[1]
        days = [datetime(year, month, day).strftime('%Y-%m-%d') for day in range(1, num_days + 1)]
        
        # Create a calendar DataFrame
        cal_df = pd.DataFrame(index=days, columns=['Day', 'Events'])
        cal_df['Day'] = [datetime.strptime(day, '%Y-%m-%d').strftime('%a, %b %d') for day in days]
        cal_df['Events'] = ''
        
        # Get events for this month
        data = self._load_data()
        month_events = [
            e for e in data['events'] 
            if datetime.strptime(e['date'], '%Y-%m-%d').month == month and
               datetime.strptime(e['date'], '%Y-%m-%d').year == year
        ]
        
        # Add events to calendar
        for event in month_events:
            event_date = event['date']
            if event_date in cal_df.index:
                if cal_df.at[event_date, 'Events']:
                    cal_df.at[event_date, 'Events'] += f", {event['name']}"
                else:
                    cal_df.at[event_date, 'Events'] = event['name']
        
        # Style the calendar
        cal_df = cal_df.reset_index().rename(columns={'index': 'Date'})
        
        return cal_df
    
    def get_recommendations_for_event(self, event_id):
        """Get product recommendations for a specific event"""
        data = self._load_data()
        inventory_data = self._load_inventory_data()
        
        # Find the event
        event = next((e for e in data['events'] if e['id'] == event_id), None)
        
        if not event:
            return []
        
        # Get event type
        event_type = event.get('type', 'general')
        
        # Find relevant impact data
        impacts = data['event_impacts']
        
        # Filter impacts by event type
        type_impacts = [i for i in impacts if i.get('event_type') == event_type]
        
        # Organize recommendations
        recommendations = []
        
        # Process specific product recommendations
        product_recs = [i for i in type_impacts if 'product' in i]
        for rec in product_recs:
            recommendations.append({
                'product': rec['product'],
                'expected_sales_lift': rec['sales_impact_percentage'],
                'recommendation_reason': rec['recommendation_reason']
            })
        
        # Process category recommendations
        category_impacts = [i for i in type_impacts if 'category' in i]
        
        # Group by category to get average impact
        category_avg_impacts = {}
        for impact in category_impacts:
            category = impact['category']
            impact_value = impact['sales_impact_percentage']
            
            if category not in category_avg_impacts:
                category_avg_impacts[category] = []
            
            category_avg_impacts[category].append(impact_value)
        
        # Calculate average impact per category
        category_avgs = {
            category: sum(impacts) / len(impacts) 
            for category, impacts in category_avg_impacts.items()
        }
        
        # Get inventory items by category
        for category, impact in category_avgs.items():
            # Get top items from this category
            category_items = [
                item for item in inventory_data.get('inventory', []) 
                if item.get('category') == category
            ]
            
            # Sort by some criteria (e.g., profit margin, popularity)
            # For demo, just take the first 2 items if they exist
            top_items = category_items[:2]
            
            for item in top_items:
                recommendations.append({
                    'product': item['name'],
                    'expected_sales_lift': round(impact, 1),
                    'recommendation_reason': f"Popular {category.lower()} item during {event_type.replace('_', ' ')} events"
                })
        
        # Sort by expected impact
        recommendations.sort(key=lambda r: r['expected_sales_lift'], reverse=True)
        
        # Take top 10 recommendations
        return recommendations[:10]
    
    def add_event(self, name, date, location, expected_attendance, description):
        """Add a new event to the calendar"""
        data = self._load_data()
        
        # Convert date to string if it's a date object
        if isinstance(date, (datetime, datetime.date)):
            date_str = date.strftime('%Y-%m-%d')
        else:
            date_str = date
        
        new_event = {
            "id": str(uuid.uuid4()),
            "name": name,
            "date": date_str,
            "location": location,
            "description": description,
            "expected_attendance": expected_attendance,
            "recurring": "one-time",  # Default to one-time event
            "type": "custom",  # Default to custom event type
            "added_by": "user",
            "date_added": datetime.now().isoformat()
        }
        
        data['events'].append(new_event)
        self._save_data(data)
        
        return new_event
    
    def update_event(self, event_id, **kwargs):
        """Update an existing event"""
        data = self._load_data()
        
        for i, event in enumerate(data['events']):
            if event['id'] == event_id:
                # Update provided fields
                for key, value in kwargs.items():
                    if key in event:
                        event[key] = value
                
                data['events'][i] = event
                self._save_data(data)
                return event
        
        return None  # Event not found
    
    def delete_event(self, event_id):
        """Delete an event"""
        data = self._load_data()
        
        for i, event in enumerate(data['events']):
            if event['id'] == event_id:
                deleted_event = data['events'].pop(i)
                self._save_data(data)
                return deleted_event
        
        return None  # Event not found
    
    def apply_event_recommendations(self, event_id):
        """
        Apply event-based recommendations to inventory planning
        
        Args:
            event_id: ID of the event to apply recommendations for
            
        Returns:
            Boolean indicating success
        """
        # Get recommendations for this event
        recommendations = self.get_recommendations_for_event(event_id)
        
        if not recommendations:
            return False
        
        data = self._load_data()
        
        # Find the event
        event = next((e for e in data['events'] if e['id'] == event_id), None)
        
        if not event:
            return False
        
        # Record the application of recommendations
        application_record = {
            'id': str(uuid.uuid4()),
            'event_id': event_id,
            'event_name': event['name'],
            'event_date': event['date'],
            'timestamp': datetime.now().isoformat(),
            'recommendations': recommendations
        }
        
        data['recommendation_history'].append(application_record)
        self._save_data(data)
        
        # Note: In a real application, this would actually update order quantities or forecasts
        # For this demo, we just record that recommendations were applied
        
        return True
