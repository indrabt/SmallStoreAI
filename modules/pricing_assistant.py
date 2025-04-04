import os
import json
import uuid
from datetime import datetime, timedelta
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class PricingAssistant:
    """
    Handles dynamic pricing suggestions and Square POS integration:
    - Calculates optimal prices based on supplier costs, demand, and competitor prices
    - Suggests promotions based on events and inventory status
    - Manages price synchronization with Square POS
    - Tracks price performance metrics
    """
    
    def __init__(self, data_file="data/pricing_assistant.json"):
        """Initialize the pricing assistant with data file path"""
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file exists, create if it doesn't"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        if not os.path.exists(self.data_file):
            # Create initial data with sample pricing
            initial_data = {
                "price_suggestions": self._generate_sample_price_suggestions(),
                "promotions": self._generate_sample_promotions(),
                "price_history": [],
                "promotion_history": [],
                "sync_history": [],
                "pos_settings": {
                    "square_api_enabled": False,
                    "square_api_key": "",
                    "square_location_id": "",
                    "auto_sync": False,
                    "sync_schedule": "10:00",
                    "last_sync": None
                }
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _generate_sample_price_suggestions(self):
        """Generate sample price suggestion data for first-time setup"""
        # Try to load inventory and supplier data
        inventory_data = self._load_inventory_data()
        supplier_data = self._load_supplier_data()
        
        suggestions = []
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # If inventory exists, use actual products
        if inventory_data and 'inventory' in inventory_data and inventory_data['inventory']:
            sample_products = random.sample(inventory_data['inventory'], min(10, len(inventory_data['inventory'])))
            
            for product in sample_products:
                # Find if a supplier exists for this product category
                supplier_cost = None
                supplier_name = None
                supplier_discount = random.uniform(0.05, 0.25)  # Random discount between 5% and 25%
                
                if supplier_data and 'suppliers' in supplier_data:
                    matching_suppliers = [s for s in supplier_data['suppliers'] 
                                         if 'categories' in s and product['category'] in s['categories']]
                    
                    if matching_suppliers:
                        supplier = random.choice(matching_suppliers)
                        supplier_name = supplier['name']
                        
                        # Check if supplier has this product
                        supplier_products = [p for p in supplier.get('products', []) 
                                            if product['name'].lower() in p['name'].lower()]
                        
                        if supplier_products:
                            supplier_cost = supplier_products[0]['price']
                        else:
                            # Simulate a discounted cost
                            supplier_cost = product['cost_price'] * (1 - supplier_discount)
                
                # If no supplier match found, simulate cost
                if not supplier_cost:
                    supplier_cost = product['cost_price'] * (1 - supplier_discount)
                    supplier_name = "Simulated Supplier"
                
                # Calculate competitive price (slightly below current price)
                competitive_price = round(product['selling_price'] * 0.95, 2)
                
                # Competitor price (slightly above competitive price)
                competitor_price = round(competitive_price * 1.05, 2)
                
                # Calculate savings
                supplier_savings = round(((product['cost_price'] - supplier_cost) / product['cost_price']) * 100, 1)
                price_discount = round(((product['selling_price'] - competitive_price) / product['selling_price']) * 100, 1)
                
                suggestions.append({
                    "id": str(uuid.uuid4()),
                    "product_id": product['id'],
                    "product_name": product['name'],
                    "category": product['category'],
                    "current_cost": product['cost_price'],
                    "current_price": product['selling_price'],
                    "supplier_cost": round(supplier_cost, 2),
                    "supplier_name": supplier_name,
                    "competitive_price": competitive_price,
                    "competitor_price": competitor_price,
                    "competitor_name": "Coles",
                    "supplier_savings": supplier_savings,
                    "price_discount": price_discount,
                    "date": current_date,
                    "demand_impact": {
                        "estimated_sales_current": random.randint(50, 100),
                        "estimated_sales_competitive": random.randint(70, 120),
                        "sales_increase_percentage": random.randint(10, 30)
                    },
                    "margin_current": round(((product['selling_price'] - product['cost_price']) / product['selling_price']) * 100, 1),
                    "margin_competitive": round(((competitive_price - supplier_cost) / competitive_price) * 100, 1),
                    "status": "pending",
                    "applied": False,
                    "alert": supplier_savings >= 15 or price_discount >= 10,
                    "alert_type": "savings" if supplier_savings >= 15 else "competitive" if price_discount >= 10 else None
                })
        else:
            # Create generic sample suggestions
            sample_products = [
                {"name": "Bottled Water 24-Pack", "category": "Beverages"},
                {"name": "Organic Apples", "category": "Fruits & Vegetables"},
                {"name": "Whole Milk 2L", "category": "Dairy & Eggs"},
                {"name": "White Bread", "category": "Bakery"},
                {"name": "Potato Chips 175g", "category": "Snacks & Confectionery"}
            ]
            
            for product in sample_products:
                current_cost = round(random.uniform(0.5, 8.0), 2)
                current_price = round(current_cost * random.uniform(1.2, 1.5), 2)
                supplier_cost = round(current_cost * (1 - random.uniform(0.05, 0.25)), 2)
                competitive_price = round(current_price * 0.95, 2)
                competitor_price = round(competitive_price * 1.05, 2)
                
                supplier_savings = round(((current_cost - supplier_cost) / current_cost) * 100, 1)
                price_discount = round(((current_price - competitive_price) / current_price) * 100, 1)
                
                suggestions.append({
                    "id": str(uuid.uuid4()),
                    "product_id": str(uuid.uuid4()),
                    "product_name": product["name"],
                    "category": product["category"],
                    "current_cost": current_cost,
                    "current_price": current_price,
                    "supplier_cost": supplier_cost,
                    "supplier_name": "Sample Supplier",
                    "competitive_price": competitive_price,
                    "competitor_price": competitor_price,
                    "competitor_name": "Coles",
                    "supplier_savings": supplier_savings,
                    "price_discount": price_discount,
                    "date": current_date,
                    "demand_impact": {
                        "estimated_sales_current": random.randint(50, 100),
                        "estimated_sales_competitive": random.randint(70, 120),
                        "sales_increase_percentage": random.randint(10, 30)
                    },
                    "margin_current": round(((current_price - current_cost) / current_price) * 100, 1),
                    "margin_competitive": round(((competitive_price - supplier_cost) / competitive_price) * 100, 1),
                    "status": "pending",
                    "applied": False,
                    "alert": supplier_savings >= 15 or price_discount >= 10,
                    "alert_type": "savings" if supplier_savings >= 15 else "competitive" if price_discount >= 10 else None
                })
        
        return suggestions
    
    def _generate_sample_promotions(self):
        """Generate sample promotions based on upcoming events"""
        # Try to load event data
        event_data = self._load_event_data()
        
        promotions = []
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Define some sample promotion templates
        promotion_templates = [
            {f"name": "{discount}% off {category}", "type": "percent_off", "min_discount": 5, "max_discount": 20},
            {f"name": "Buy One Get One {type} on {category}", "type": "bogo", "types": ["Free", "Half Price", "25% Off"]},
            {f"name": "${amount} off when you spend ${threshold}", "type": "amount_off", "min_amount": 5, "max_amount": 15, "min_threshold": 30, "max_threshold": 75},
            {f"name": "Festival Special: {discount}% off {category}", "type": "event_special", "min_discount": 10, "max_discount": 25}
        ]
        
        # Generate event-based promotions
        if event_data and 'events' in event_data:
            upcoming_events = [e for e in event_data['events'] 
                              if datetime.strptime(e['date'], "%Y-%m-%d") >= datetime.now() 
                              and datetime.strptime(e['date'], "%Y-%m-%d") <= (datetime.now() + timedelta(days=14))]
            
            for event in upcoming_events[:2]:  # Use up to 2 upcoming events
                template = promotion_templates[3]  # Use event special template
                
                # Generate random category based on the event type
                categories = ["Snacks & Confectionery", "Beverages", "Bakery", "Fruits & Vegetables"]
                category = random.choice(categories)
                
                # Generate a discount percentage
                discount = random.randint(template["min_discount"], template["max_discount"])
                
                promotions.append({
                    "id": str(uuid.uuid4()),
                    "name": template["name"].format(discount=discount, category=category),
                    "description": f"Special promotion for {event['name']} on {{event['date']}",
                    "type": "percent_off",
                    "value": discount,
                    "category": category,
                    "start_date": event['date'],
                    "end_date": datetime.strftime(datetime.strptime(event['date'], "%Y-%m-%d") + timedelta(days=1), "%Y-%m-%d"),
                    "applied": False,
                    "status": "pending",
                    "related_event": event['id'],
                    "event_name": event['name'],
                    "estimated_impact": {
                        "sales_increase": random.randint(15, 35),
                        "margin_impact": random.randint(-5, 5),
                        "customer_retention": random.randint(80, 95)
                    },
                    "created_date": current_date
                })
        
        # Generate standard promotions if we have less than 3 promotions
        while len(promotions) < 3:
            template = random.choice(promotion_templates[:3])  # Use non-event templates
            
            if template["type"] == "percent_off":
                # Generate random category
                categories = ["Snacks & Confectionery", "Beverages", "Bakery", "Dairy & Eggs", "Fruits & Vegetables"]
                category = random.choice(categories)
                
                # Generate a discount percentage
                discount = random.randint(template["min_discount"], template["max_discount"])
                
                promotions.append({
                    "id": str(uuid.uuid4()),
                    "name": template["name"].format(discount=discount, category=category),
                    f"description": f"{discount}% discount on all {category} products",
                    "type": "percent_off",
                    "value": discount,
                    "category": category,
                    "start_date": current_date,
                    "end_date": datetime.strftime(datetime.now() + timedelta(days=7), "%Y-%m-%d"),
                    "applied": False,
                    "status": "pending",
                    "related_event": None,
                    "event_name": None,
                    "estimated_impact": {
                        "sales_increase": random.randint(5, 20),
                        "margin_impact": random.randint(-10, 0),
                        "customer_retention": random.randint(60, 85)
                    },
                    "created_date": current_date
                })
            
            elif template["type"] == "bogo":
                # Generate random category
                categories = ["Snacks & Confectionery", "Beverages", "Bakery"]
                category = random.choice(categories)
                
                # Generate type
                bogo_type = random.choice(template["types"])
                
                promotions.append({
                    "id": str(uuid.uuid4()),
                    "name": template["name"].format(type=bogo_type, category=category),
                    f"description": f"Buy one {category} item and get one {bogo_type.lower()}",
                    "type": "bogo",
                    "value": bogo_type,
                    "category": category,
                    "start_date": current_date,
                    "end_date": datetime.strftime(datetime.now() + timedelta(days=7), "%Y-%m-%d"),
                    "applied": False,
                    "status": "pending",
                    "related_event": None,
                    "event_name": None,
                    "estimated_impact": {
                        "sales_increase": random.randint(10, 30),
                        "margin_impact": random.randint(-15, -5),
                        "customer_retention": random.randint(70, 90)
                    },
                    "created_date": current_date
                })
            
            elif template["type"] == "amount_off":
                # Generate amount and threshold
                amount = random.randint(template["min_amount"], template["max_amount"])
                threshold = random.randint(template["min_threshold"], template["max_threshold"])
                
                promotions.append({
                    "id": str(uuid.uuid4()),
                    "name": template["name"].format(amount=amount, threshold=threshold),
                    f"description": f"${amount} off your purchase when you spend ${threshold} or more",
                    "type": "amount_off",
                    "value": amount,
                    "threshold": threshold,
                    "category": "All Categories",
                    "start_date": current_date,
                    "end_date": datetime.strftime(datetime.now() + timedelta(days=7), "%Y-%m-%d"),
                    "applied": False,
                    "status": "pending",
                    "related_event": None,
                    "event_name": None,
                    "estimated_impact": {
                        "sales_increase": random.randint(5, 15),
                        "margin_impact": random.randint(-8, -2),
                        "customer_retention": random.randint(65, 85)
                    },
                    "created_date": current_date
                })
        
        return promotions
    
    def _load_data(self):
        """Load pricing assistant data from file"""
        if not os.path.exists(self.data_file):
            self._ensure_data_file_exists()
            
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def _save_data(self, data):
        """Save pricing assistant data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_inventory_data(self):
        """Load inventory data from file if available"""
        inventory_file = "data/inventory.json"
        
        if os.path.exists(inventory_file):
            try:
                with open(inventory_file, 'r') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def _load_supplier_data(self):
        """Load supplier data from file if available"""
        supplier_file = "data/suppliers.json"
        
        if os.path.exists(supplier_file):
            try:
                with open(supplier_file, 'r') as f:
                    return json.load(f)
            except:
                return None
        return None
        
    def _load_event_data(self):
        """Load event data from file if available"""
        event_file = "data/events.json"
        
        if os.path.exists(event_file):
            try:
                with open(event_file, 'r') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def get_price_suggestions(self, category=None, min_savings=0, status=None):
        """
        Get price suggestions with optional filtering
        
        Args:
            category (str, optional): Filter by product category
            min_savings (float, optional): Filter by minimum supplier savings percentage
            status (str, optional): Filter by status ("pending", "approved", "rejected", "applied")
            
        Returns:
            list: List of matching price suggestions
        """
        data = self._load_data()
        suggestions = data.get('price_suggestions', [])
        
        # Apply filters
        if category:
            suggestions = [s for s in suggestions if s['category'] == category]
        
        if min_savings > 0:
            suggestions = [s for s in suggestions if s['supplier_savings'] >= min_savings]
        
        if status:
            suggestions = [s for s in suggestions if s['status'] == status]
        
        # Sort by savings (highest first)
        suggestions = sorted(suggestions, key=lambda s: s['supplier_savings'], reverse=True)
        
        return suggestions
    
    def get_promotions(self, category=None, active_only=False, event_related=None):
        """
        Get promotions with optional filtering
        
        Args:
            category (str, optional): Filter by product category
            active_only (bool, optional): If True, only return active promotions
            event_related (bool, optional): If True, only event-related; if False, only non-event; if None, all
            
        Returns:
            list: List of matching promotions
        """
        data = self._load_data()
        promotions = data.get('promotions', [])
        
        # Apply filters
        if category:
            promotions = [p for p in promotions if p['category'] == category]
        
        if active_only:
            today = datetime.now().strftime("%Y-%m-%d")
            promotions = [p for p in promotions 
                         if p['start_date'] <= today and p['end_date'] >= today and p['applied']]
        
        if event_related is not None:
            if event_related:
                promotions = [p for p in promotions if p['related_event'] is not None]
            else:
                promotions = [p for p in promotions if p['related_event'] is None]
        
        # Sort by start date (soonest first)
        promotions = sorted(promotions, key=lambda p: p['start_date'])
        
        return promotions
    
    def update_price(self, suggestion_id, new_price):
        """
        Update a price suggestion and optionally apply it to inventory
        
        Args:
            suggestion_id (str): ID of the price suggestion
            new_price (float): New price to apply
            
        Returns:
            dict: Result of the operation
        """
        data = self._load_data()
        
        for i, suggestion in enumerate(data['price_suggestions']):
            if suggestion['id'] == suggestion_id:
                # Store original values
                original_price = suggestion['competitive_price']
                product_id = suggestion['product_id']
                product_name = suggestion['product_name']
                
                # Update suggestion
                data['price_suggestions'][i]['competitive_price'] = new_price
                data['price_suggestions'][i]['status'] = 'approved'
                
                # Record in price history
                history_entry = {
                    "id": str(uuid.uuid4()),
                    "product_id": product_id,
                    "product_name": product_name,
                    "suggestion_id": suggestion_id,
                    "original_price": suggestion['current_price'],
                    "suggested_price": original_price,
                    "applied_price": new_price,
                    "timestamp": datetime.now().isoformat(),
                    "supplier_savings": suggestion['supplier_savings'],
                    "estimated_sales_increase": suggestion['demand_impact']['sales_increase_percentage']
                }
                
                data['price_history'].append(history_entry)
                
                # Save data
                self._save_data(data)
                
                # Try to update inventory price
                inventory_update = self._update_inventory_price(product_id, new_price)
                
                return {
                    "success": True,
                    "product_name": product_name,
                    "new_price": new_price,
                    "inventory_updated": inventory_update['success'],
                    f"message": f"Price updated for {product_name} to ${new_price:.2f}"
                }
        
        return {
            "success": False,
            "message": "Price suggestion not found"
        }
    
    def _update_inventory_price(self, product_id, new_price):
        """
        Update product price in inventory
        
        Args:
            product_id (str): ID of the product to update
            new_price (float): New selling price
            
        Returns:
            dict: Result of the operation
        """
        inventory_file = "data/inventory.json"
        
        if not os.path.exists(inventory_file):
            return {"success": False, "message": "Inventory file not found"}
        
        try:
            with open(inventory_file, 'r') as f:
                inventory_data = json.load(f)
            
            updated = False
            product_name = None
            old_price = 0.0
            
            for i, item in enumerate(inventory_data.get('inventory', [])):
                if item['id'] == product_id:
                    old_price = item['selling_price']
                    inventory_data['inventory'][i]['selling_price'] = new_price
                    product_name = item['name']
                    updated = True
                    break
            
            if updated:
                with open(inventory_file, 'w') as f:
                    json.dump(inventory_data, f, indent=2)
                
                return {
                    "success": True,
                    "product_name": product_name,
                    "old_price": old_price,
                    "new_price": new_price,
                    f"message": f"Updated inventory price for {product_name}"
                }
            else:
                return {
                    "success": False,
                    f"message": f"Product with ID {product_id} not found in inventory"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating inventory: {str(e)}"
            }
    
    def apply_promotion(self, promotion_id, modified_discount=None):
        """
        Apply a promotion
        
        Args:
            promotion_id (str): ID of the promotion to apply
            modified_discount (float, optional): Modified discount value (if changed)
            
        Returns:
            dict: Result of the operation
        """
        data = self._load_data()
        
        for i, promotion in enumerate(data['promotions']):
            if promotion['id'] == promotion_id:
                # Record original values
                original_value = promotion['value']
                
                # Update promotion
                if modified_discount is not None:
                    data['promotions'][i]['value'] = modified_discount
                
                data['promotions'][i]['applied'] = True
                data['promotions'][i]['status'] = 'applied'
                
                # Record in promotion history
                history_entry = {
                    "id": str(uuid.uuid4()),
                    "promotion_id": promotion_id,
                    "promotion_name": promotion['name'],
                    "original_value": original_value,
                    "applied_value": modified_discount if modified_discount is not None else original_value,
                    "category": promotion['category'],
                    "timestamp": datetime.now().isoformat(),
                    "start_date": promotion['start_date'],
                    "end_date": promotion['end_date'],
                    "related_event": promotion['related_event'],
                    "event_name": promotion['event_name']
                }
                
                data['promotion_history'].append(history_entry)
                
                # Save data
                self._save_data(data)
                
                # Simulate POS synchronization
                sync_result = self._sync_with_square_pos(promotion=promotion)
                
                return {
                    "success": True,
                    "promotion_name": promotion['name'],
                    "pos_synced": sync_result['success'],
                    "message": f"Promotion '{promotion['name']}' applied and {sync_result['message']}"
                }
        
        return {
            "success": False,
            "message": "Promotion not found"
        }
    
    def update_promotion(self, promotion_id, **kwargs):
        """
        Update a promotion's details
        
        Args:
            promotion_id (str): ID of the promotion to update
            **kwargs: Fields to update (name, description, value, start_date, end_date)
            
        Returns:
            dict: Result of the operation
        """
        data = self._load_data()
        
        for i, promotion in enumerate(data['promotions']):
            if promotion['id'] == promotion_id:
                # Update provided fields
                for field, value in kwargs.items():
                    if field in promotion:
                        data['promotions'][i][field] = value
                
                # Save data
                self._save_data(data)
                
                return {
                    "success": True,
                    "promotion_id": promotion_id,
                    "message": f"Promotion updated successfully"
                }
        
        return {
            "success": False,
            "message": "Promotion not found"
        }
    
    def create_promotion(self, name, description, promotion_type, value, category, 
                       start_date, end_date, related_event=None, event_name=None):
        """
        Create a new promotion
        
        Args:
            name (str): Promotion name
            description (str): Promotion description
            promotion_type (str): Type of promotion (percent_off, amount_off, bogo)
            value (float/str): Discount value or BOGO type
            category (str): Product category
            start_date (str): Start date (YYYY-MM-DD)
            end_date (str): End date (YYYY-MM-DD)
            related_event (str, optional): Related event ID
            event_name (str, optional): Related event name
            
        Returns:
            dict: Result of the operation
        """
        data = self._load_data()
        
        # Create new promotion
        promotion = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "type": promotion_type,
            "value": value,
            "category": category,
            "start_date": start_date,
            "end_date": end_date,
            "applied": False,
            "status": "pending",
            "related_event": related_event,
            "event_name": event_name,
            "estimated_impact": {
                "sales_increase": random.randint(5, 25),
                "margin_impact": random.randint(-10, 5),
                "customer_retention": random.randint(60, 90)
            },
            "created_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        data['promotions'].append(promotion)
        
        # Save data
        self._save_data(data)
        
        return {
            "success": True,
            "promotion_id": promotion['id'],
            f"message": f"Promotion '{name}' created successfully"
        }
    
    def _sync_with_square_pos(self, product=None, promotion=None):
        """
        Simulate Square POS synchronization
        
        Args:
            product (dict, optional): Product to sync
            promotion (dict, optional): Promotion to sync
            
        Returns:
            dict: Sync result
        """
        data = self._load_data()
        pos_settings = data.get('pos_settings', {})
        
        # Check if Square integration is enabled
        if not pos_settings.get('square_api_enabled', False):
            return {
                "success": True, 
                "synced": False,
                "message": "simulated (Square POS integration not enabled)"
            }
        
        # In a real implementation, this would use the Square API to update prices or promotions
        # For now, we'll just log the sync event
        sync_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "type": "product" if product else "promotion",
            "status": "successful",
            "details": product if product else promotion
        }
        
        data['sync_history'].append(sync_entry)
        pos_settings['last_sync'] = datetime.now().isoformat()
        data['pos_settings'] = pos_settings
        
        # Save data
        self._save_data(data)
        
        return {
            "success": True,
            "synced": True,
            "message": f"successfully synced with Square POS at {{datetime.now().strftime('%H:%M:%S')}"
        }
    
    def update_pos_settings(self, enabled=None, api_key=None, location_id=None, auto_sync=None, sync_schedule=None):
        """
        Update Square POS integration settings
        
        Args:
            enabled (bool, optional): Whether Square API is enabled
            api_key (str, optional): Square API key
            location_id (str, optional): Square location ID
            auto_sync (bool, optional): Whether to auto-sync
            sync_schedule (str, optional): Time to sync (HH:MM)
            
        Returns:
            dict: Result of the operation
        """
        data = self._load_data()
        pos_settings = data.get('pos_settings', {})
        
        # Update provided fields
        if enabled is not None:
            pos_settings['square_api_enabled'] = enabled
        
        if api_key is not None:
            pos_settings['square_api_key'] = api_key
        
        if location_id is not None:
            pos_settings['square_location_id'] = location_id
        
        if auto_sync is not None:
            pos_settings['auto_sync'] = auto_sync
        
        if sync_schedule is not None:
            pos_settings['sync_schedule'] = sync_schedule
        
        data['pos_settings'] = pos_settings
        
        # Save data
        self._save_data(data)
        
        return {
            "success": True,
            "message": "POS settings updated successfully"
        }
    
    def get_pos_settings(self):
        """
        Get Square POS integration settings
        
        Returns:
            dict: POS settings
        """
        data = self._load_data()
        return data.get('pos_settings', {})
    
    def generate_suggestion_impact_chart(self, suggestion_id):
        """
        Generate a chart showing the impact of a price suggestion
        
        Args:
            suggestion_id (str): ID of the price suggestion
            
        Returns:
            Figure: Matplotlib figure with the chart
        """
        data = self._load_data()
        
        # Find the suggestion
        suggestion = None
        for s in data['price_suggestions']:
            if s['id'] == suggestion_id:
                suggestion = s
                break
        
        if not suggestion:
            return None
        
        # Create figure
        fig = Figure(figsize=(10, 6))
        ax = fig.subplots()
        
        # Prepare data
        current_sales = suggestion['demand_impact']['estimated_sales_current']
        new_sales = suggestion['demand_impact']['estimated_sales_competitive']
        current_revenue = current_sales * suggestion['current_price']
        new_revenue = new_sales * suggestion['competitive_price']
        current_profit = current_sales * (suggestion['current_price'] - suggestion['current_cost'])
        new_profit = new_sales * (suggestion['competitive_price'] - suggestion['supplier_cost'])
        
        # Plot data
        x = np.arange(3)
        width = 0.35
        
        metrics = ['Units Sold', 'Revenue ($)', 'Profit ($)']
        current_values = [current_sales, current_revenue, current_profit]
        new_values = [new_sales, new_revenue, new_profit]
        
        rects1 = ax.bar(x - width/2, current_values, width, label='Current Price')
        rects2 = ax.bar(x + width/2, new_values, width, label='Suggested Price')
        
        # Add labels
        ax.set_title(f'Impact Analysis: {suggestion["product_name"]}')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()
        
        # Add value labels
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{height:.0f}',
                           xy=(rect.get_x() + rect.get_width()/2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom')
        
        autolabel(rects1)
        autolabel(rects2)
        
        # Calculate percentage changes
        pct_changes = [
            (new_sales - current_sales) / current_sales * 100,
            (new_revenue - current_revenue) / current_revenue * 100,
            (new_profit - current_profit) / current_profit * 100
        ]
        
        # Add percentage change annotations
        for i, pct in enumerate(pct_changes):
            color = 'green' if pct >= 0 else 'red'
            ax.annotate(f'{pct:.1f}}%",
                       xy=(i, max(current_values[i], new_values[i])),
                       xytext=(0, 10),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       color=color,
                       fontweight='bold')
        
        fig.tight_layout()
        return fig
    
    def generate_promotion_impact_chart(self, promotion_id):
        """
        Generate a chart showing the estimated impact of a promotion
        
        Args:
            promotion_id (str): ID of the promotion
            
        Returns:
            Figure: Matplotlib figure with the chart
        """
        data = self._load_data()
        
        # Find the promotion
        promotion = None
        for p in data['promotions']:
            if p['id'] == promotion_id:
                promotion = p
                break
        
        if not promotion:
            return None
        
        # Create figure
        fig = Figure(figsize=(10, 6))
        ax = fig.subplots()
        
        # Prepare data
        metrics = ['Sales Increase', 'Margin Impact', 'Customer Retention']
        values = [
            promotion['estimated_impact']['sales_increase'],
            promotion['estimated_impact']['margin_impact'],
            promotion['estimated_impact']['customer_retention']
        ]
        
        colors = ['#2986cc', '#e69138', '#6aa84f']
        
        # Create horizontal bar chart
        bars = ax.barh(metrics, values, color=colors)
        
        # Add labels
        ax.set_title(f'Promotion Impact: {promotion["name"]}')
        ax.set_xlabel('Percentage (%)')
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            label_x_pos = width if width >= 0 else 0
            ax.text(label_x_pos + 1, bar.get_y() + bar.get_height()/2, f'{width}}%", 
                   va='center')
        
        # Add a vertical line at 0 for margin impact
        ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
        
        # Add explanatory text
        fig.text(0.02, 0.02, 
                f"Promotion period: {promotion['start_date']} to {promotion['end_date']}\n"
                f"Category: {promotion['category']}\n"
                f"{'Event: ' + promotion['event_name'] if promotion['event_name'] else 'Standard promotion'}",
                fontsize=8)
        
        fig.tight_layout()
        return fig
    
    def check_for_failed_promotions(self, min_sales=5, hours=48):
        """
        Check for promotions that have low sales performance
        In a real implementation, this would check actual sales data
        
        Args:
            min_sales (int): Minimum expected sales
            hours (int): Hours to wait before suggesting changes
            
        Returns:
            list: List of promotions that need adjustment
        """
        # In a real implementation, this would analyze actual sales data
        # For now, we'll simulate by randomly marking a promotion as underperforming
        data = self._load_data()
        today = datetime.now().strftime("%Y-%m-%d")
        
        active_promotions = [p for p in data['promotions'] 
                           if p['applied'] and p['start_date'] <= today and p['end_date'] >= today]
        
        # Randomly select a promotion to mark as underperforming
        failed_promotions = []
        
        if active_promotions and random.random() < 0.3:  # 30% chance of finding an underperforming promotion
            promotion = random.choice(active_promotions)
            
            # Suggest a higher discount
            current_value = promotion['value']
            suggested_value = min(current_value * 1.5, 
                               50 if promotion['type'] == 'percent_off' else current_value + 5)
            
            failed_promotions.append({
                "promotion_id": promotion['id'],
                "promotion_name": promotion['name'],
                "current_value": current_value,
                "suggested_value": suggested_value,
                "promotion_type": promotion['type'],
                "category": promotion['category'],
                "customer_retention": promotion['estimated_impact']['customer_retention'],
                "message": f"This promotion is underperforming. Consider increasing the discount to {{suggested_value:.0f}%."
            })
        
        return failed_promotions
    
    def generate_square_api_code_sample(self):
        """
        Generate a code sample for Square API integration
        
        Returns:
            str: Python code sample for Square API integration
        """
        code_sample = """
# Square API Code Sample (Implementation)
# This would be used in a production environment

import uuid
from square.client import Client

def update_square_inventory(square_client, item_id, variation_id, new_price_money):
    # Update item price in Square POS
    result = square_client.catalog.upsert_catalog_object(
        body={
            "idempotency_key": str(uuid.uuid4()),
            "object": {
                "type": "ITEM_VARIATION",
                f"id": f"#{variation_id}",
                "item_variation_data": {
                    f"item_id": f"#{item_id}",
                    "pricing_type": "FIXED_PRICING",
                    "price_money": {
                        "amount": int(new_price_money * 100),  # Convert dollars to cents
                        "currency": "AUD"
                    }
                }
            }
        }
    )
    return result.body

def create_square_discount(square_client, name, percentage, category_ids=None):
    # Create a discount in Square POS
    discount_data = {
        "type": "DISCOUNT",
        "id": f"#{str(uuid.uuid4())}",
        "discount_data": {
            "name": name,
            "discount_type": "FIXED_PERCENTAGE",
            "percentage": str(percentage),
            "modifier_type": "MODIFIER"
        }
    }
    
    # Add category restrictions if specified
    if category_ids:
        discount_data["discount_data"]["product_set_data"] = {
            "product_ids_any": category_ids
        }
    
    result = square_client.catalog.upsert_catalog_object(
        body={
            "idempotency_key": str(uuid.uuid4()),
            "object": discount_data
        }
    )
    return result.body
"""
        return code_sample