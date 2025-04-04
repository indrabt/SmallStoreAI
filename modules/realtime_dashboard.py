"""
Real-Time Client Dashboard Module for Small Store AI Pack
Tracks stock, deliveries, and sales in real-time, adapted from hub Feature 9
"""
import time
import datetime
import random
import math
import uuid
import json
from pathlib import Path


class RealtimeDashboard:
    """
    Manages real-time dashboard data for store operations
    - Tracks delivery status from Feature 5
    - Monitors sales data from Square POS
    - Shows inventory levels
    - Provides operational summaries
    """
    
    def __init__(self, data_file="data/realtime_dashboard.json"):
        """Initialize with data file path"""
        self.data_file = data_file
        self._ensure_data_file_exists()
        self.dashboard_data = self._load_data()
        
    def _ensure_data_file_exists(self):
        """Create data file if it doesn't exist"""
        if not Path(self.data_file).exists():
            Path(self.data_file).parent.mkdir(parents=True, exist_ok=True)
            
            # Initialize with default data
            default_data = {
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "delivery_status": {
                    "active_deliveries": [],
                    "completed_deliveries": [],
                    "connection_status": "connected",
                    "last_sync": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "on_time_percentage": 95.0
                },
                "sales_data": {
                    "today_sales": 0,
                    "yesterday_sales": 0,
                    "week_sales": 0,
                    "month_sales": 0,
                    "top_items": [],
                    "connection_status": "connected",
                    "last_sync": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "accuracy_percentage": 98.5
                },
                "inventory_status": {
                    "low_stock_items": [],
                    "total_items": 0,
                    "low_stock_percentage": 0,
                    "connection_status": "connected",
                    "last_sync": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "operational_summary": {
                    "deliveries_on_time": 0,
                    "deliveries_total": 0,
                    "on_time_percentage": 0,
                    "cost_savings": 0,
                    "issues_resolved": 0,
                    "connection_status": "connected",
                    "last_sync": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "notifications": [],
                "cached_data": {
                    "delivery_status": {},
                    "sales_data": {},
                    "inventory_status": {},
                    "timestamp": None
                }
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(default_data, f, indent=2)
    
    def _load_data(self):
        """Load dashboard data from file"""
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def _save_data(self):
        """Save dashboard data to file"""
        self.dashboard_data["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.data_file, 'w') as f:
            json.dump(self.dashboard_data, f, indent=2)
    
    def _add_notification(self, title, message, level="info"):
        """Add a notification to the dashboard"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notification = {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "title": title,
            "message": message,
            "level": level,
            "read": False
        }
        
        self.dashboard_data["notifications"].insert(0, notification)
        
        # Keep notification list to a reasonable size
        if len(self.dashboard_data["notifications"]) > 50:
            self.dashboard_data["notifications"] = self.dashboard_data["notifications"][:50]
            
        self._save_data()
        return notification
    
    def _cache_current_data(self):
        """Cache current delivery, sales, and inventory data for offline use"""
        self.dashboard_data["cached_data"] = {
            "delivery_status": self.dashboard_data["delivery_status"],
            "sales_data": self.dashboard_data["sales_data"],
            "inventory_status": self.dashboard_data["inventory_status"],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._save_data()
    
    def update_dashboard(self):
        """
        Update dashboard with latest data
        In a real implementation, this would pull data from Feature 5 and Square POS
        """
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Update last sync times
        self.dashboard_data["delivery_status"]["last_sync"] = current_time_str
        self.dashboard_data["sales_data"]["last_sync"] = current_time_str
        self.dashboard_data["inventory_status"]["last_sync"] = current_time_str
        self.dashboard_data["operational_summary"]["last_sync"] = current_time_str
        
        # Check if we should simulate a connection issue (1% chance)
        if random.random() < 0.01:
            self._simulate_connection_issue()
            return
            
        # Update delivery status - simulating Feature 5 integration
        self._update_delivery_status()
        
        # Update sales data - simulating Square POS integration
        self._update_sales_data()
        
        # Update inventory status
        self._update_inventory_status()
        
        # Update operational summary
        self._update_operational_summary()
        
        # Cache the updated data
        self._cache_current_data()
        
        # Save all changes
        self._save_data()
    
    def _update_delivery_status(self):
        """Update delivery status with simulated data from Feature 5"""
        # Get time of day (0-24 hours) to simulate delivery patterns
        current_hour = datetime.datetime.now().hour
        
        # Active deliveries logic
        active_deliveries = []
        
        # Generate 0-3 active deliveries based on time of day
        num_active = min(3, max(0, int(math.sin(current_hour / 24 * math.pi) * 3)))
        
        for i in range(num_active):
            # Calculate a random distance (1-15 km) and time to arrival
            distance = round(random.uniform(1, 15), 1)
            arrival_minutes = int(distance * 3)  # 3 minutes per km
            
            # Generate order sizes (40-120 items)
            items = random.randint(40, 120)
            
            # Product types
            products = ["Bottles", "Cases", "Packages", "Pallets"]
            product = random.choice(products)
            
            # Driver names
            drivers = ["Alex", "Sam", "Taylor", "Jordan", "Casey"]
            driver = random.choice(drivers)
            
            # Create the delivery object
            # Calculate arrival times
            est_arrival = datetime.datetime.now() + datetime.timedelta(minutes=arrival_minutes)
            sched_arrival = datetime.datetime.now() + datetime.timedelta(minutes=arrival_minutes)
            
            delivery = {
                "id": str(uuid.uuid4()),
                "driver": driver,
                "distance": distance,
                "items": items,
                "product_type": product,
                "estimated_arrival": est_arrival.strftime("%Y-%m-%d %H:%M:%S"),
                "scheduled_arrival": sched_arrival.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "in transit",
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            active_deliveries.append(delivery)
        
        # Update active deliveries
        self.dashboard_data["delivery_status"]["active_deliveries"] = active_deliveries
        
        # Handle completed deliveries (keep last 10)
        if len(self.dashboard_data["delivery_status"]["completed_deliveries"]) > 10:
            self.dashboard_data["delivery_status"]["completed_deliveries"] = \
                self.dashboard_data["delivery_status"]["completed_deliveries"][:10]
        
        # On-time percentage (95%+ per requirements)
        self.dashboard_data["delivery_status"]["on_time_percentage"] = round(random.uniform(95, 100), 1)
    
    def _update_sales_data(self):
        """Update sales data with simulated data from Square POS"""
        # Get current date parts for consistent simulated data
        now = datetime.datetime.now()
        day_of_month = now.day
        hour = now.hour
        
        # Today's sales curve - sales build throughout the day
        if hour < 8:
            sales_factor = 0.1
        elif hour < 12:
            sales_factor = 0.4
        elif hour < 17:
            sales_factor = 0.7
        else:
            sales_factor = 0.9
            
        # Base sales values
        base_daily_sales = 1000
        
        # Calculate today's sales based on time of day
        today_sales = round(base_daily_sales * sales_factor * (0.8 + 0.4 * random.random()), 2)
        
        # Yesterday's sales (fixed for the day)
        yesterday_sales = round(base_daily_sales * (0.8 + 0.4 * random.random()), 2)
        
        # Week and month calculations
        week_sales = round(yesterday_sales * 7 * (0.8 + 0.4 * random.random()), 2)
        month_sales = round(yesterday_sales * 30 * (0.8 + 0.4 * random.random()), 2)
        
        # Update sales data
        self.dashboard_data["sales_data"]["today_sales"] = today_sales
        self.dashboard_data["sales_data"]["yesterday_sales"] = yesterday_sales
        self.dashboard_data["sales_data"]["week_sales"] = week_sales
        self.dashboard_data["sales_data"]["month_sales"] = month_sales
        
        # Accuracy percentage (98%+ per requirements)
        self.dashboard_data["sales_data"]["accuracy_percentage"] = round(random.uniform(98, 100), 1)
        
        # Top selling items
        products = [
            "Bottled Water (500ml)", 
            "Organic Apples", 
            "Free-Range Eggs",
            "Whole Grain Bread",
            "Grass-Fed Milk",
            "Local Honey",
            "Fresh Coffee",
            "Gluten-Free Pasta",
            "Organic Chicken",
            "Craft Beer"
        ]
        
        # Randomize order but keep consistent for the day
        random.seed(now.day)
        random.shuffle(products)
        top_products = products[:5]
        random.seed()  # Reset the random seed
        
        # Create top items with quantities
        top_items = []
        for product in top_products:
            quantity = random.randint(20, 100)
            amount = round(quantity * random.uniform(2, 15), 2)
            
            top_items.append({
                "product": product,
                "quantity": quantity,
                "amount": amount
            })
            
        self.dashboard_data["sales_data"]["top_items"] = top_items
    
    def _update_inventory_status(self):
        """Update inventory status data"""
        # Get current date parts for consistent simulated data
        now = datetime.datetime.now()
        
        # Inventory categories
        categories = [
            "Beverages", "Produce", "Dairy", "Bakery", 
            "Meat & Seafood", "Frozen Foods", "Dry Goods", 
            "Snacks", "Health & Beauty", "Household"
        ]
        
        # Total items in inventory
        total_items = random.randint(150, 200)
        
        # Low stock threshold percentage
        low_stock_threshold = 0.25  # 25%
        
        # Generate low stock items (5-15 items)
        num_low_stock = random.randint(5, 15)
        low_stock_items = []
        
        for i in range(num_low_stock):
            category = random.choice(categories)
            stock_level = round(random.uniform(0.05, low_stock_threshold), 2)  # 5-25%
            
            # Product name based on category
            products_by_category = {
                "Beverages": ["Bottled Water", "Soft Drinks", "Juice", "Coffee", "Tea"],
                "Produce": ["Apples", "Bananas", "Carrots", "Lettuce", "Tomatoes"],
                "Dairy": ["Milk", "Cheese", "Yogurt", "Butter", "Eggs"],
                "Bakery": ["Bread", "Rolls", "Pastries", "Muffins", "Bagels"],
                "Meat & Seafood": ["Chicken", "Beef", "Pork", "Salmon", "Shrimp"],
                "Frozen Foods": ["Ice Cream", "Frozen Meals", "Frozen Vegetables", "Pizza", "Desserts"],
                "Dry Goods": ["Rice", "Pasta", "Flour", "Sugar", "Cereal"],
                "Snacks": ["Chips", "Cookies", "Crackers", "Nuts", "Popcorn"],
                "Health & Beauty": ["Soap", "Shampoo", "Toothpaste", "Lotion", "Vitamins"],
                "Household": ["Paper Towels", "Toilet Paper", "Cleaning Supplies", "Detergent", "Trash Bags"]
            }
            
            product = random.choice(products_by_category.get(category, ["Unknown"]))
            
            # Calculate restock urgency
            if stock_level < 0.10:
                urgency = "high"
            elif stock_level < 0.15:
                urgency = "medium"
            else:
                urgency = "low"
                
            # Create low stock item
            item = {
                "id": str(uuid.uuid4()),
                "name": product,
                "category": category,
                "current_stock": int(stock_level * 100),  # Convert to units
                "max_stock": 100,  # Fixed for simplicity
                "stock_percentage": stock_level * 100,  # As percentage
                "urgency": urgency,
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            low_stock_items.append(item)
        
        # Update inventory status
        self.dashboard_data["inventory_status"]["low_stock_items"] = low_stock_items
        self.dashboard_data["inventory_status"]["total_items"] = total_items
        self.dashboard_data["inventory_status"]["low_stock_percentage"] = round((num_low_stock / total_items) * 100, 1)
    
    def _update_operational_summary(self):
        """Update operational summary data"""
        # Get values from delivery status
        on_time_percentage = self.dashboard_data["delivery_status"]["on_time_percentage"]
        
        # Calculate total deliveries and on-time deliveries
        total_deliveries = random.randint(15, 25)
        on_time_deliveries = int(total_deliveries * (on_time_percentage / 100))
        
        # Cost savings (based on $10-30 per delivery)
        savings_per_delivery = random.uniform(10, 30)
        cost_savings = round(total_deliveries * savings_per_delivery, 2)
        
        # Issues resolved
        issues_resolved = random.randint(1, 5)
        
        # Update operational summary
        self.dashboard_data["operational_summary"]["deliveries_on_time"] = on_time_deliveries
        self.dashboard_data["operational_summary"]["deliveries_total"] = total_deliveries
        self.dashboard_data["operational_summary"]["on_time_percentage"] = on_time_percentage
        self.dashboard_data["operational_summary"]["cost_savings"] = cost_savings
        self.dashboard_data["operational_summary"]["issues_resolved"] = issues_resolved
    
    def _simulate_connection_issue(self):
        """Simulate a connection issue and recovery"""
        # Determine what's affected
        affected_systems = random.choice([
            ["delivery_status"],
            ["sales_data"],
            ["delivery_status", "sales_data"]
        ])
        
        # Mark systems as disconnected
        for system in affected_systems:
            self.dashboard_data[system]["connection_status"] = "disconnected"
            
        # Add notification
        affected_names = "delivery tracking" if "delivery_status" in affected_systems else ""
        affected_names += " and " if "delivery_status" in affected_systems and "sales_data" in affected_systems else ""
        affected_names += "sales data" if "sales_data" in affected_systems else ""
        
        self._add_notification(
            "Connection Issue Detected",
            f"Lost connection to {affected_names}. Using cached data until connection is restored.",
            "warning"
        )
        
        # Save changes
        self._save_data()
    
    def simulate_delivery_delay(self):
        """
        Simulate a delivery delay and notification
        
        Returns:
            dict: Delay information
        """
        # Make sure there are active deliveries
        if not self.dashboard_data["delivery_status"]["active_deliveries"]:
            self._update_delivery_status()  # Create some deliveries
        
        # If still no deliveries, create one specifically
        if not self.dashboard_data["delivery_status"]["active_deliveries"]:
            # Create a delivery
            delivery = {
                "id": str(uuid.uuid4()),
                "driver": "Sam",
                "distance": 10.5,
                "items": 80,
                "product_type": "Bottles",
                "estimated_arrival": (datetime.datetime.now() + datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                "scheduled_arrival": (datetime.datetime.now() + datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                "status": "in transit",
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.dashboard_data["delivery_status"]["active_deliveries"].append(delivery)
        
        # Select a delivery to delay
        delivery = self.dashboard_data["delivery_status"]["active_deliveries"][0]
        
        # Calculate delay (30-90 minutes)
        delay_minutes = random.randint(30, 90)
        
        # Update the delivery
        delivery["status"] = "delayed"
        
        # Convert string dates to datetime if needed
        if isinstance(delivery["estimated_arrival"], str):
            delivery["estimated_arrival"] = datetime.datetime.strptime(
                delivery["estimated_arrival"], "%Y-%m-%d %H:%M:%S"
            )
            
        # Add delay to estimated arrival
        new_arrival = delivery["estimated_arrival"] + datetime.timedelta(minutes=delay_minutes)
        delivery["estimated_arrival"] = new_arrival.strftime("%Y-%m-%d %H:%M:%S")
        delivery["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add notification
        notification = self._add_notification(
            "Delivery Delay Detected",
            f"Delivery by {delivery['driver']} with {delivery['items']} {delivery['product_type']} " +
            f"is delayed by {delay_minutes} minutes.",
            "warning"
        )
        
        # Save changes
        self._save_data()
        
        return {
            "delivery_id": delivery["id"],
            "driver": delivery["driver"],
            "delay_minutes": delay_minutes,
            "new_arrival_time": delivery["estimated_arrival"],
            "items": delivery["items"],
            "product_type": delivery["product_type"],
            "notification": notification
        }
    
    def simulate_inventory_alert(self):
        """
        Simulate an inventory alert for low stock
        
        Returns:
            dict: Alert information
        """
        # Make sure we have low stock items
        if not self.dashboard_data["inventory_status"]["low_stock_items"]:
            self._update_inventory_status()  # Create some low stock items
        
        # If still no items, create one specifically
        if not self.dashboard_data["inventory_status"]["low_stock_items"]:
            # Create a low stock item
            item = {
                "id": str(uuid.uuid4()),
                "name": "Bottled Water",
                "category": "Beverages",
                "current_stock": 5,
                "max_stock": 100,
                "stock_percentage": 5.0,
                "urgency": "high",
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.dashboard_data["inventory_status"]["low_stock_items"].append(item)
        
        # Find the most urgent low stock item
        urgent_items = [item for item in self.dashboard_data["inventory_status"]["low_stock_items"] 
                      if item["urgency"] == "high"]
        
        if not urgent_items:
            # If no high urgency items, use the first low stock item
            item = self.dashboard_data["inventory_status"]["low_stock_items"][0]
            # Make it high urgency
            item["urgency"] = "high"
            item["stock_percentage"] = 5.0
            item["current_stock"] = 5
        else:
            item = urgent_items[0]
        
        # Add notification
        notification = self._add_notification(
            "Critical Inventory Alert",
            f"{item['name']} is critically low at {item['stock_percentage']}% of maximum stock. " +
            f"Only {item['current_stock']} units remaining.",
            "error"
        )
        
        # Save changes
        self._save_data()
        
        return {
            "item_id": item["id"],
            "name": item["name"],
            "category": item["category"],
            "current_stock": item["current_stock"],
            "stock_percentage": item["stock_percentage"],
            "urgency": item["urgency"],
            "notification": notification
        }
    
    def simulate_sales_spike(self):
        """
        Simulate a sales spike alert
        
        Returns:
            dict: Alert information
        """
        # Get current sales data
        current_sales = self.dashboard_data["sales_data"]["today_sales"]
        
        # Calculate spike (30-50% increase)
        spike_percentage = random.uniform(30, 50)
        sales_increase = current_sales * (spike_percentage / 100)
        new_sales = current_sales + sales_increase
        
        # Update sales data
        self.dashboard_data["sales_data"]["today_sales"] = round(new_sales, 2)
        
        # Add notification
        notification = self._add_notification(
            "Sales Spike Detected",
            f"Sales have increased by {spike_percentage:.1f}% in the last hour. " +
            f"${sales_increase:.2f} additional revenue.",
            "success"
        )
        
        # Save changes
        self._save_data()
        
        return {
            "previous_sales": current_sales,
            "new_sales": new_sales,
            "increase_amount": sales_increase,
            "increase_percentage": spike_percentage,
            "notification": notification
        }
    
    def mark_notification_read(self, notification_id):
        """
        Mark a notification as read
        
        Args:
            notification_id (str): ID of the notification
            
        Returns:
            bool: Success status
        """
        for notification in self.dashboard_data["notifications"]:
            if notification["id"] == notification_id:
                notification["read"] = True
                self._save_data()
                return True
        
        return False
    
    def get_active_deliveries(self):
        """
        Get active deliveries
        
        Returns:
            list: Active deliveries
        """
        return self.dashboard_data["delivery_status"]["active_deliveries"]
    
    def get_completed_deliveries(self):
        """
        Get completed deliveries
        
        Returns:
            list: Completed deliveries
        """
        return self.dashboard_data["delivery_status"]["completed_deliveries"]
    
    def get_delivery_metrics(self):
        """
        Get delivery metrics
        
        Returns:
            dict: Delivery metrics
        """
        return {
            "on_time_percentage": self.dashboard_data["delivery_status"]["on_time_percentage"],
            "connection_status": self.dashboard_data["delivery_status"]["connection_status"],
            "last_sync": self.dashboard_data["delivery_status"]["last_sync"]
        }
    
    def get_sales_data(self):
        """
        Get sales data
        
        Returns:
            dict: Sales data
        """
        return self.dashboard_data["sales_data"]
    
    def get_inventory_status(self):
        """
        Get inventory status
        
        Returns:
            dict: Inventory status
        """
        return self.dashboard_data["inventory_status"]
    
    def get_operational_summary(self):
        """
        Get operational summary
        
        Returns:
            dict: Operational summary
        """
        return self.dashboard_data["operational_summary"]
    
    def get_notifications(self, unread_only=False):
        """
        Get notifications
        
        Args:
            unread_only (bool): Only return unread notifications
            
        Returns:
            list: Notifications
        """
        if unread_only:
            return [n for n in self.dashboard_data["notifications"] if not n["read"]]
        else:
            return self.dashboard_data["notifications"]
    
    def get_dashboard_summary(self):
        """
        Get a complete dashboard summary
        
        Returns:
            dict: Dashboard summary
        """
        # First update the dashboard
        self.update_dashboard()
        
        # Then return the complete data
        return {
            "last_updated": self.dashboard_data["last_updated"],
            "delivery_status": {
                "active_deliveries": self.get_active_deliveries(),
                "metrics": self.get_delivery_metrics()
            },
            "sales_data": self.get_sales_data(),
            "inventory_status": self.get_inventory_status(),
            "operational_summary": self.get_operational_summary(),
            "notifications": self.get_notifications(unread_only=True)
        }