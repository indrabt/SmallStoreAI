import json
import datetime
import os
import random  # For demo data generation
from datetime import timedelta

class PerishableInventoryTracker:
    """
    Handles perishable inventory tracking including:
    - Expiration date monitoring
    - FIFO (First In, First Out) inventory management
    - Automatic price discounting for near-expiry items
    - Integration with Square POS API (simulated)
    - Email alerts for critical expiration thresholds
    """
    
    def __init__(self, data_file="data/perishable_inventory.json"):
        """Initialize the perishable inventory tracker with data file path"""
        self.data_file = data_file
        self._ensure_data_file_exists()
        self.inventory_data = self._load_data()
        
    def _ensure_data_file_exists(self):
        """Ensure the data file exists, create if it doesn't"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            # Create a sample inventory data structure
            sample_data = {
                "inventory_items": self._generate_sample_inventory(),
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "settings": {
                    "expiry_thresholds": {
                        "warning": 30,  # days
                        "critical": 7,  # days
                        "discount_threshold": 7  # days
                    },
                    "discount_rates": {
                        "default": 20,  # percent
                        "critical": 40  # percent
                    },
                    "notification_emails": ["manager@smallstore.com"],
                    "scan_accuracy_threshold": 85  # percent
                }
            }
            with open(self.data_file, 'w') as file:
                json.dump(sample_data, file, indent=4)
    
    def _generate_sample_inventory(self):
        """Generate sample perishable inventory for demonstration"""
        today = datetime.datetime.now()
        
        # Create some sample product categories
        categories = ["Dairy", "Produce", "Bakery", "Beverages", "Meat", "Prepared Foods"]
        
        # Sample products with expiration characteristics
        sample_products = [
            {"name": "Water Bottles", "category": "Beverages", "shelf_life_days": 365, "current_stock": 80},
            {"name": "Milk", "category": "Dairy", "shelf_life_days": 10, "current_stock": 45},
            {"name": "Yogurt", "category": "Dairy", "shelf_life_days": 30, "current_stock": 65},
            {"name": "Bread", "category": "Bakery", "shelf_life_days": 7, "current_stock": 30},
            {"name": "Apples", "category": "Produce", "shelf_life_days": 14, "current_stock": 120},
            {"name": "Bananas", "category": "Produce", "shelf_life_days": 7, "current_stock": 75},
            {"name": "Chicken Breast", "category": "Meat", "shelf_life_days": 5, "current_stock": 25},
            {"name": "Prepared Salad", "category": "Prepared Foods", "shelf_life_days": 3, "current_stock": 15}
        ]
        
        inventory_items = []
        
        # Generate multiple batches for each product with different expiration dates
        for product in sample_products:
            # Create 2-3 batches per product
            num_batches = random.randint(2, 3)
            total_stock = product["current_stock"]
            
            for i in range(num_batches):
                # Distribute stock among batches
                if i == num_batches - 1:
                    batch_stock = total_stock
                else:
                    batch_stock = random.randint(1, total_stock - (num_batches - i - 1))
                    total_stock -= batch_stock
                
                # Vary expiration dates
                if i == 0:
                    # Oldest batch
                    days_old = random.randint(int(product["shelf_life_days"] * 0.5), 
                                           int(product["shelf_life_days"] * 0.8))
                    expiration_date = (today + timedelta(days=product["shelf_life_days"] - days_old))
                elif i == 1:
                    # Middle batch
                    expiration_date = (today + timedelta(days=int(product["shelf_life_days"] * 0.7)))
                else:
                    # Newest batch
                    expiration_date = (today + timedelta(days=product["shelf_life_days"]))
                
                received_date = expiration_date - timedelta(days=product["shelf_life_days"])
                
                # Generate a random SKU
                sku = f"{product['category'][:3].upper()}{random.randint(1000, 9999)}"
                
                inventory_items.append({
                    "id": f"{product['name'].lower().replace(' ', '_')}_{i+1}",
                    "name": product["name"],
                    "category": product["category"],
                    "sku": sku,
                    "batch_number": f"B{(today - timedelta(days=random.randint(5, 30))).strftime('%Y%m%d')}-{random.randint(1, 999):03d}",
                    "quantity": batch_stock,
                    "unit": "each",
                    "received_date": received_date.strftime("%Y-%m-%d"),
                    "expiration_date": expiration_date.strftime("%Y-%m-%d"),
                    "original_price": round(random.uniform(1.5, 15.99), 2),
                    "current_price": round(random.uniform(1.5, 15.99), 2),
                    "discount_applied": False,
                    "discount_rate": 0,
                    "last_scanned": (today - timedelta(days=random.randint(0, 5))).strftime("%Y-%m-%d"),
                    "location": random.choice(["Front Shelf", "Back Storage", "Display Case", "Refrigerator"]),
                    "notes": ""
                })
                
                # Make sure water bottles match the example
                if product["name"] == "Water Bottles" and i == 0:
                    inventory_items[-1]["quantity"] = 80
                    inventory_items[-1]["expiration_date"] = (today + timedelta(days=30)).strftime("%Y-%m-%d")
        
        return inventory_items
    
    def _load_data(self):
        """Load inventory data from file"""
        with open(self.data_file, 'r') as file:
            return json.load(file)
    
    def _save_data(self):
        """Save inventory data to file"""
        self.inventory_data["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.data_file, 'w') as file:
            json.dump(self.inventory_data, file, indent=4)
    
    def get_inventory_items(self, category=None, expiry_days=None, low_stock=False):
        """
        Get inventory items with optional filtering
        
        Args:
            category (str, optional): Filter by category
            expiry_days (int, optional): Filter by items expiring within X days
            low_stock (bool, optional): Filter to show only low stock items
            
        Returns:
            list: Filtered inventory items
        """
        items = self.inventory_data["inventory_items"]
        today = datetime.datetime.now().date()
        
        if category:
            items = [item for item in items if item["category"] == category]
            
        if expiry_days is not None:
            items = [item for item in items if 
                    (datetime.datetime.strptime(item["expiration_date"], "%Y-%m-%d").date() - today).days <= expiry_days]
            
        if low_stock:
            # Group by product name and check if any product is low in total stock
            product_totals = {}
            for item in self.inventory_data["inventory_items"]:
                name = item["name"]
                if name not in product_totals:
                    product_totals[name] = 0
                product_totals[name] += item["quantity"]
            
            # Assume low stock is 20% of typical stock for that product
            # (This would be more sophisticated in a real implementation)
            low_stock_items = set()
            for item in self.inventory_data["inventory_items"]:
                name = item["name"]
                # Just an example threshold calculation
                if name == "Water Bottles" and product_totals[name] <= 80 * 0.2:  # 20% of 80
                    low_stock_items.add(name)
                elif product_totals[name] <= 30:  # Generic low threshold
                    low_stock_items.add(name)
            
            items = [item for item in items if item["name"] in low_stock_items]
        
        # Sort by expiration date (oldest first) to enforce FIFO
        return sorted(items, key=lambda x: x["expiration_date"])
    
    def get_expiring_items(self, days_threshold=None):
        """
        Get items expiring within specified days
        
        Args:
            days_threshold (int, optional): Days threshold, defaults to warning threshold in settings
            
        Returns:
            list: Items expiring within threshold
        """
        if days_threshold is None:
            days_threshold = self.inventory_data["settings"]["expiry_thresholds"]["warning"]
            
        return self.get_inventory_items(expiry_days=days_threshold)
    
    def get_critical_items(self):
        """
        Get items at critical expiration threshold
        
        Returns:
            list: Items at critical expiration threshold
        """
        critical_days = self.inventory_data["settings"]["expiry_thresholds"]["critical"]
        return self.get_inventory_items(expiry_days=critical_days)
    
    def get_low_stock_items(self):
        """
        Get items with low stock levels
        
        Returns:
            list: Items with low stock
        """
        return self.get_inventory_items(low_stock=True)
    
    def apply_discount(self, item_id, custom_discount=None):
        """
        Apply a discount to a nearly expired item
        
        Args:
            item_id (str): ID of the item to discount
            custom_discount (int, optional): Custom discount percentage, defaults to settings
            
        Returns:
            dict: Updated item information
        """
        for i, item in enumerate(self.inventory_data["inventory_items"]):
            if item["id"] == item_id:
                discount_rate = custom_discount or self.inventory_data["settings"]["discount_rates"]["default"]
                
                # For critical items, use the critical discount rate
                days_to_expiry = (datetime.datetime.strptime(item["expiration_date"], "%Y-%m-%d").date() - 
                                 datetime.datetime.now().date()).days
                if days_to_expiry <= self.inventory_data["settings"]["expiry_thresholds"]["critical"]:
                    discount_rate = self.inventory_data["settings"]["discount_rates"]["critical"]
                
                # Apply discount
                self.inventory_data["inventory_items"][i]["original_price"] = item["current_price"]
                self.inventory_data["inventory_items"][i]["current_price"] = round(
                    item["current_price"] * (1 - discount_rate/100), 2)
                self.inventory_data["inventory_items"][i]["discount_applied"] = True
                self.inventory_data["inventory_items"][i]["discount_rate"] = discount_rate
                
                # Simulate updating Square POS
                self._update_square_pos(item_id, self.inventory_data["inventory_items"][i])
                
                self._save_data()
                return self.inventory_data["inventory_items"][i]
                
        return None
    
    def scan_item(self, item_id=None, sku=None, batch_number=None, scan_action="check"):
        """
        Scan an item via barcode or manual entry
        
        Args:
            item_id (str, optional): ID of the item
            sku (str, optional): SKU code of the item
            batch_number (str, optional): Batch number of the item
            scan_action (str): Action to perform ('check', 'sold', 'adjust')
            
        Returns:
            dict: Scanned item information or None if not found
        """
        found_item = None
        
        # Find the item
        for i, item in enumerate(self.inventory_data["inventory_items"]):
            if ((item_id and item["id"] == item_id) or 
                (sku and item["sku"] == sku) or 
                (batch_number and item["batch_number"] == batch_number)):
                
                found_item = item
                found_idx = i
                break
                
        if not found_item:
            return None
            
        # Update last scanned timestamp
        self.inventory_data["inventory_items"][found_idx]["last_scanned"] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Perform action based on scan_action
        if scan_action == "sold":
            # Deduct one unit as sold
            if self.inventory_data["inventory_items"][found_idx]["quantity"] > 0:
                self.inventory_data["inventory_items"][found_idx]["quantity"] -= 1
                
        elif scan_action == "adjust":
            # This would open a quantity adjustment dialog in the UI
            pass
        
        self._save_data()
        return self.inventory_data["inventory_items"][found_idx]
    
    def update_quantity(self, item_id, new_quantity):
        """
        Update the quantity of an item
        
        Args:
            item_id (str): ID of the item
            new_quantity (int): New quantity value
            
        Returns:
            dict: Updated item information or None if not found
        """
        for i, item in enumerate(self.inventory_data["inventory_items"]):
            if item["id"] == item_id:
                self.inventory_data["inventory_items"][i]["quantity"] = new_quantity
                self._save_data()
                
                # Simulate updating Square POS
                self._update_square_pos(item_id, self.inventory_data["inventory_items"][i])
                
                return self.inventory_data["inventory_items"][i]
                
        return None
    
    def get_stock_summary(self):
        """
        Get a summary of stock levels by product
        
        Returns:
            dict: Summary of stock levels by product
        """
        summary = {}
        
        for item in self.inventory_data["inventory_items"]:
            name = item["name"]
            if name not in summary:
                summary[name] = {
                    "total_quantity": 0,
                    "batches": 0,
                    "oldest_expiry": None,
                    "newest_expiry": None,
                    "categories": set(),
                    "locations": set()
                }
            
            summary[name]["total_quantity"] += item["quantity"]
            summary[name]["batches"] += 1
            summary[name]["categories"].add(item["category"])
            summary[name]["locations"].add(item["location"])
            
            expiry_date = datetime.datetime.strptime(item["expiration_date"], "%Y-%m-%d").date()
            
            if summary[name]["oldest_expiry"] is None or expiry_date < summary[name]["oldest_expiry"]:
                summary[name]["oldest_expiry"] = expiry_date
                
            if summary[name]["newest_expiry"] is None or expiry_date > summary[name]["newest_expiry"]:
                summary[name]["newest_expiry"] = expiry_date
        
        # Convert sets to lists for JSON serialization
        for name in summary:
            summary[name]["categories"] = list(summary[name]["categories"])
            summary[name]["locations"] = list(summary[name]["locations"])
            
            # Convert dates to strings
            if summary[name]["oldest_expiry"]:
                days_to_oldest_expiry = (summary[name]["oldest_expiry"] - datetime.datetime.now().date()).days
                summary[name]["oldest_expiry_str"] = summary[name]["oldest_expiry"].strftime("%Y-%m-%d")
                summary[name]["days_to_oldest_expiry"] = days_to_oldest_expiry
                
            if summary[name]["newest_expiry"]:
                days_to_newest_expiry = (summary[name]["newest_expiry"] - datetime.datetime.now().date()).days
                summary[name]["newest_expiry_str"] = summary[name]["newest_expiry"].strftime("%Y-%m-%d")
                summary[name]["days_to_newest_expiry"] = days_to_newest_expiry
        
        return summary
    
    def _send_expiry_alert(self, items):
        """
        Simulate sending expiry alerts to configured emails
        
        Args:
            items (list): Items that need attention
            
        Returns:
            bool: Whether alert was sent
        """
        # In a real implementation, this would send actual emails
        print(f"ALERT: {len(items)} items require attention")
        for email in self.inventory_data["settings"]["notification_emails"]:
            print(f"Email alert would be sent to: {email}")
        
        return True
    
    def _update_square_pos(self, item_id, item_data):
        """
        Simulate updating the Square POS with inventory changes
        
        Args:
            item_id (str): ID of the item
            item_data (dict): Updated item data
            
        Returns:
            bool: Whether update was successful
        """
        # In a real implementation, this would make API calls to Square
        print(f"Square POS would be updated for item {item_id}")
        print(f"New price: ${item_data['current_price']}")
        print(f"New quantity: {item_data['quantity']}")
        
        return True
    
    def update_next_order_quantity(self, product_name, new_quantity):
        """
        Update the suggested next order quantity for a product
        
        Args:
            product_name (str): Name of the product
            new_quantity (int): Suggested quantity for next order
            
        Returns:
            dict: Updated order suggestion information
        """
        if "order_suggestions" not in self.inventory_data:
            self.inventory_data["order_suggestions"] = {}
            
        self.inventory_data["order_suggestions"][product_name] = {
            "suggested_quantity": new_quantity,
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "notes": "Adjusted based on expiration tracking"
        }
        
        self._save_data()
        return self.inventory_data["order_suggestions"][product_name]
    
    def get_next_order_suggestions(self):
        """
        Get suggestions for next order quantities
        
        Returns:
            dict: Order suggestions by product
        """
        if "order_suggestions" not in self.inventory_data:
            self.inventory_data["order_suggestions"] = {}
            
        return self.inventory_data["order_suggestions"]