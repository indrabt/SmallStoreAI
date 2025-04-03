import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import uuid
import os
import json

class InventoryManager:
    """
    Handles inventory management operations including:
    - Tracking current inventory
    - Managing stock levels
    - Providing analytics on inventory performance
    - Generating stock alerts
    """
    
    def __init__(self, data_file="data/inventory.json"):
        """Initialize the inventory manager with data file path"""
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file exists, create if it doesn't"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        if not os.path.exists(self.data_file):
            # Create initial data with sample inventory
            initial_data = {
                "inventory": self._generate_sample_inventory(),
                "categories": [
                    "Fruits & Vegetables", 
                    "Dairy & Eggs", 
                    "Meat & Seafood", 
                    "Bakery", 
                    "Beverages",
                    "Snacks & Confectionery",
                    "Canned & Packaged",
                    "Frozen Foods",
                    "Household & Cleaning"
                ],
                "transactions": []
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _generate_sample_inventory(self):
        """Generate sample inventory data for first-time setup"""
        sample_inventory = [
            {
                "id": str(uuid.uuid4()),
                "name": "Apples - Royal Gala",
                "category": "Fruits & Vegetables",
                "supplier": "Local Organic Farms",
                "quantity": 50,
                "reorder_point": 15,
                "cost_price": 1.25,
                "selling_price": 2.99,
                "last_updated": (datetime.now() - timedelta(days=2)).isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Milk - Full Cream 2L",
                "category": "Dairy & Eggs",
                "supplier": "Penrith Dairy Co-op",
                "quantity": 30,
                "reorder_point": 10,
                "cost_price": 2.50,
                "selling_price": 4.20,
                "last_updated": (datetime.now() - timedelta(days=1)).isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Bread - Multigrain Loaf",
                "category": "Bakery",
                "supplier": "Penrith Bakehouse",
                "quantity": 15,
                "reorder_point": 5,
                "cost_price": 2.00,
                "selling_price": 4.50,
                "last_updated": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Eggs - Free Range Dozen",
                "category": "Dairy & Eggs",
                "supplier": "Happy Hens Farm",
                "quantity": 25,
                "reorder_point": 8,
                "cost_price": 3.50,
                "selling_price": 6.99,
                "last_updated": (datetime.now() - timedelta(days=3)).isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Bananas",
                "category": "Fruits & Vegetables",
                "supplier": "Local Organic Farms",
                "quantity": 40,
                "reorder_point": 12,
                "cost_price": 0.75,
                "selling_price": 1.99,
                "last_updated": (datetime.now() - timedelta(days=1)).isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Bottled Water 24-Pack",
                "category": "Beverages",
                "supplier": "National Distributors",
                "quantity": 20,
                "reorder_point": 5,
                "cost_price": 6.00,
                "selling_price": 9.99,
                "last_updated": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Chicken Breast - 500g",
                "category": "Meat & Seafood",
                "supplier": "NSW Poultry",
                "quantity": 10,
                "reorder_point": 4,
                "cost_price": 7.50,
                "selling_price": 12.99,
                "last_updated": (datetime.now() - timedelta(days=2)).isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Pasta Sauce - Tomato & Basil",
                "category": "Canned & Packaged",
                "supplier": "National Distributors",
                "quantity": 35,
                "reorder_point": 10,
                "cost_price": 1.80,
                "selling_price": 3.49,
                "last_updated": (datetime.now() - timedelta(days=4)).isoformat()
            }
        ]
        return sample_inventory
    
    def _load_data(self):
        """Load inventory data from file"""
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def _save_data(self, data):
        """Save inventory data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_total_items(self):
        """Get total number of unique inventory items"""
        data = self._load_data()
        return len(data['inventory'])
    
    def get_categories(self):
        """Get list of product categories"""
        data = self._load_data()
        return data['categories']
    
    def get_current_inventory(self):
        """Get current inventory as a pandas DataFrame"""
        data = self._load_data()
        df = pd.DataFrame(data['inventory'])
        
        if not df.empty:
            # Convert to proper types and format
            df['last_updated'] = pd.to_datetime(df['last_updated']).dt.strftime('%Y-%m-%d %H:%M')
            df['profit_margin'] = ((df['selling_price'] - df['cost_price']) / df['selling_price'] * 100).round(1)
            df['inventory_value'] = (df['quantity'] * df['cost_price']).round(2)
            
            # Add status column
            df['status'] = df.apply(
                lambda x: 'Low' if x['quantity'] <= x['reorder_point'] else 'OK', 
                axis=1
            )
            
            # Reorder columns for display
            display_cols = [
                'id', 'name', 'category', 'supplier', 'quantity', 'status',
                'reorder_point', 'cost_price', 'selling_price', 'profit_margin',
                'inventory_value', 'last_updated'
            ]
            
            # Ensure all columns exist
            existing_cols = [col for col in display_cols if col in df.columns]
            return df[existing_cols]
        
        return pd.DataFrame()
    
    def filter_inventory(self, inventory_df, search_term="", categories=None):
        """Filter inventory by search term and categories"""
        if inventory_df.empty:
            return inventory_df
            
        filtered_df = inventory_df.copy()
        
        # Apply search filter
        if search_term:
            search_term = search_term.lower()
            filtered_df = filtered_df[
                filtered_df['name'].str.lower().str.contains(search_term) | 
                filtered_df['supplier'].str.lower().str.contains(search_term)
            ]
        
        # Apply category filter
        if categories and len(categories) > 0:
            filtered_df = filtered_df[filtered_df['category'].isin(categories)]
        
        return filtered_df
    
    def get_low_stock_count(self):
        """Get count of items with stock below reorder point"""
        inventory_df = self.get_current_inventory()
        if inventory_df.empty:
            return 0
            
        return len(inventory_df[inventory_df['quantity'] <= inventory_df['reorder_point']])
    
    def get_stock_alerts(self):
        """Get alerts for low stock items"""
        inventory_df = self.get_current_inventory()
        if inventory_df.empty:
            return []
            
        low_stock = inventory_df[inventory_df['quantity'] <= inventory_df['reorder_point']]
        
        alerts = []
        for _, item in low_stock.iterrows():
            alert = {
                'id': item['id'],
                'name': item['name'],
                'current_stock': item['quantity'],
                'reorder_point': item['reorder_point'],
                'supplier': item['supplier'],
                'message': f"Low stock alert: Only {item['quantity']} units remaining (reorder point: {item['reorder_point']})"
            }
            alerts.append(alert)
        
        return alerts
    
    def add_inventory_item(self, name, category, supplier, quantity, cost_price, selling_price):
        """Add a new inventory item"""
        data = self._load_data()
        
        new_item = {
            "id": str(uuid.uuid4()),
            "name": name,
            "category": category,
            "supplier": supplier,
            "quantity": quantity,
            "reorder_point": max(1, int(quantity * 0.2)),  # Default reorder point to 20% of initial quantity
            "cost_price": cost_price,
            "selling_price": selling_price,
            "last_updated": datetime.now().isoformat()
        }
        
        data['inventory'].append(new_item)
        self._save_data(data)
        
        return new_item
    
    def update_inventory_item(self, item_id, **kwargs):
        """Update an existing inventory item"""
        data = self._load_data()
        
        for i, item in enumerate(data['inventory']):
            if item['id'] == item_id:
                # Update only provided fields
                for key, value in kwargs.items():
                    if key in item:
                        item[key] = value
                
                # Update last_updated timestamp
                item['last_updated'] = datetime.now().isoformat()
                
                data['inventory'][i] = item
                self._save_data(data)
                return item
        
        return None  # Item not found
    
    def update_stock_quantity(self, item_id, quantity_change, transaction_type="adjustment"):
        """Update stock quantity with transaction logging"""
        data = self._load_data()
        
        for i, item in enumerate(data['inventory']):
            if item['id'] == item_id:
                old_quantity = item['quantity']
                item['quantity'] = max(0, old_quantity + quantity_change)
                item['last_updated'] = datetime.now().isoformat()
                
                # Log transaction
                transaction = {
                    "id": str(uuid.uuid4()),
                    "item_id": item_id,
                    "item_name": item['name'],
                    "transaction_type": transaction_type,
                    "quantity_change": quantity_change,
                    "old_quantity": old_quantity,
                    "new_quantity": item['quantity'],
                    "timestamp": datetime.now().isoformat()
                }
                
                data['transactions'].append(transaction)
                data['inventory'][i] = item
                self._save_data(data)
                return item
        
        return None  # Item not found
    
    def delete_inventory_item(self, item_id):
        """Delete an inventory item"""
        data = self._load_data()
        
        for i, item in enumerate(data['inventory']):
            if item['id'] == item_id:
                deleted_item = data['inventory'].pop(i)
                self._save_data(data)
                return deleted_item
        
        return None  # Item not found
    
    def get_inventory_value_by_category(self):
        """Get inventory value summary by category"""
        inventory_df = self.get_current_inventory()
        if inventory_df.empty:
            return pd.DataFrame()
            
        category_value = inventory_df.groupby('category')['inventory_value'].sum().reset_index()
        category_value = category_value.sort_values('inventory_value', ascending=False)
        
        return category_value.set_index('category')
    
    def get_inventory_trends(self):
        """Get inventory trends over time"""
        # In a real app, this would pull from historical data
        # For demo purposes, we'll create synthetic trend data based on current inventory
        
        inventory_df = self.get_current_inventory()
        if inventory_df.empty:
            return None
            
        # Get categories and create trend data
        categories = inventory_df['category'].unique()
        
        # Create date range for the past 30 days
        date_range = pd.date_range(end=datetime.now(), periods=30, freq='D')
        
        # Create a dictionary for the trend data
        trend_data = {}
        
        # Add inventory value for each category with slight variations
        for category in categories:
            base_value = inventory_df[inventory_df['category'] == category]['inventory_value'].sum()
            
            # Create variations of this value for the trend
            np.random.seed(hash(category) % 10000)  # Consistent seed for each category
            variations = np.random.normal(0, base_value * 0.1, len(date_range))
            trend_data[category] = [max(0, base_value + var) for var in variations]
        
        # Create DataFrame with date as index
        trend_df = pd.DataFrame(trend_data, index=date_range)
        
        return trend_df
    
    def get_stock_turnover_rate(self):
        """Get stock turnover rate by category"""
        # In a real app, this would be calculated from sales and inventory history
        # For demo purposes, we'll create synthetic turnover data
        
        inventory_df = self.get_current_inventory()
        if inventory_df.empty:
            return None
            
        # Group by category
        category_df = inventory_df.groupby('category').agg({
            'inventory_value': 'sum'
        }).reset_index()
        
        # Add synthetic turnover rate
        np.random.seed(42)  # For consistent results
        category_df['turnover_rate'] = np.random.uniform(2, 8, len(category_df))
        
        return category_df.set_index('category')['turnover_rate']
    
    def get_days_of_supply(self):
        """Get estimated days of supply by category"""
        # In a real app, this would be calculated from sales velocity and current inventory
        # For demo purposes, we'll create synthetic data
        
        inventory_df = self.get_current_inventory()
        if inventory_df.empty:
            return None
            
        # Group by category
        category_df = inventory_df.groupby('category').agg({
            'inventory_value': 'sum'
        }).reset_index()
        
        # Add synthetic days of supply
        np.random.seed(42)  # For consistent results
        category_df['days_of_supply'] = np.random.uniform(5, 30, len(category_df))
        
        return category_df.set_index('category')['days_of_supply']
