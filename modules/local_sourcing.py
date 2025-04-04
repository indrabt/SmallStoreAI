import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import uuid
import os
import json
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class LocalSourcingManager:
    """
    Handles local supplier management and sourcing operations including:
    - Supplier directory management
    - Local sourcing analytics
    - Cost comparisons between local and non-local suppliers
    - Supplier order management and notifications
    - Automated order confirmation via SMS/email
    """
    
    def __init__(self, data_file="data/suppliers.json"):
        """Initialize the local sourcing manager with data file path"""
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file exists, create if it doesn't"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        if not os.path.exists(self.data_file):
            # Create initial data with sample suppliers
            initial_data = {
                "suppliers": self._generate_sample_suppliers(),
                "categories": [
                    "Fruits & Vegetables", 
                    "Dairy & Eggs", 
                    "Meat & Seafood", 
                    "Bakery", 
                    "Beverages",
                    "Snacks & Confectionery",
                    "Organic",
                    "Specialty Foods"
                ],
                "orders": self._load_sample_orders()
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
                
    def _load_sample_orders(self):
        """Load sample orders from a JSON file if available"""
        sample_file = "data/sample_orders.json"
        
        if os.path.exists(sample_file):
            try:
                with open(sample_file, 'r') as f:
                    sample_data = json.load(f)
                return sample_data.get('orders', [])
            except:
                return []
        return []
    
    def _generate_sample_suppliers(self):
        """Generate sample supplier data for first-time setup"""
        suppliers = [
            {
                "id": str(uuid.uuid4()),
                "name": "Local Organic Farms",
                "contact_name": "Sarah Johnson",
                "phone": "+61 2 5555 1234",
                "email": "info@localorganicfarms.com.au",
                "address": "123 Farm Rd, Penrith, NSW 2750",
                "distance": 5.2,
                "categories": ["Fruits & Vegetables", "Organic"],
                "delivery_schedule": "Twice a week",
                "min_order": 50.00,
                "is_local": True,
                "reliability_score": 9.2,
                "sustainability_score": 9.7,
                "date_added": (datetime.now() - timedelta(days=120)).isoformat(),
                "last_order_date": (datetime.now() - timedelta(days=3)).isoformat(),
                "coordinates": {"latitude": -33.751, "longitude": 150.694},
                "products": [
                    {
                        "name": "Organic Apples",
                        "price": 1.20,
                        "unit": "kg"
                    },
                    {
                        "name": "Fresh Carrots",
                        "price": 0.90,
                        "unit": "kg"
                    },
                    {
                        "name": "Mixed Salad Greens",
                        "price": 2.50,
                        "unit": "bunch"
                    }
                ]
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Penrith Dairy Co-op",
                "contact_name": "James Smith",
                "phone": "+61 2 5555 2345",
                "email": "orders@penrithdairy.com.au",
                "address": "45 Dairy Lane, Penrith, NSW 2750",
                "distance": 3.8,
                "categories": ["Dairy & Eggs"],
                "delivery_schedule": "Daily",
                "min_order": 25.00,
                "is_local": True,
                "reliability_score": 9.5,
                "sustainability_score": 8.9,
                "date_added": (datetime.now() - timedelta(days=180)).isoformat(),
                "last_order_date": (datetime.now() - timedelta(days=1)).isoformat(),
                "coordinates": {"latitude": -33.759, "longitude": 150.702},
                "products": [
                    {
                        "name": "Full Cream Milk 2L",
                        "price": 2.40,
                        "unit": "each"
                    },
                    {
                        "name": "Local Yogurt 500g",
                        "price": 3.20,
                        "unit": "each"
                    },
                    {
                        "name": "Block Cheddar 250g",
                        "price": 4.50,
                        "unit": "each"
                    }
                ]
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Penrith Bakehouse",
                "contact_name": "Emma Wong",
                "phone": "+61 2 5555 3456",
                "email": "orders@penrithbakehouse.com.au",
                "address": "78 Main St, Penrith, NSW 2750",
                "distance": 1.2,
                "categories": ["Bakery"],
                "delivery_schedule": "Daily",
                "min_order": 15.00,
                "is_local": True,
                "reliability_score": 9.0,
                "sustainability_score": 8.5,
                "date_added": (datetime.now() - timedelta(days=90)).isoformat(),
                "last_order_date": (datetime.now() - timedelta(days=1)).isoformat(),
                "coordinates": {"latitude": -33.755, "longitude": 150.689},
                "products": [
                    {
                        "name": "Multigrain Loaf",
                        "price": 3.80,
                        "unit": "each"
                    },
                    {
                        "name": "White Bread Rolls 6pk",
                        "price": 3.20,
                        "unit": "each"
                    },
                    {
                        "name": "Sourdough Batard",
                        "price": 5.50,
                        "unit": "each"
                    }
                ]
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Happy Hens Farm",
                "contact_name": "Michael Zhang",
                "phone": "+61 2 5555 4567",
                "email": "info@happyhens.com.au",
                "address": "156 Range Rd, Wallacia, NSW 2745",
                "distance": 12.5,
                "categories": ["Dairy & Eggs", "Organic"],
                "delivery_schedule": "Twice a week",
                "min_order": 30.00,
                "is_local": True,
                "reliability_score": 8.8,
                "sustainability_score": 9.6,
                "date_added": (datetime.now() - timedelta(days=150)).isoformat(),
                "last_order_date": (datetime.now() - timedelta(days=2)).isoformat(),
                "coordinates": {"latitude": -33.867, "longitude": 150.639},
                "products": [
                    {
                        "name": "Free Range Eggs Dozen",
                        "price": 5.20,
                        "unit": "each"
                    },
                    {
                        "name": "Organic Eggs Dozen",
                        "price": 6.50,
                        "unit": "each"
                    }
                ]
            },
            {
                "id": str(uuid.uuid4()),
                "name": "NSW Poultry",
                "contact_name": "David Chen",
                "phone": "+61 2 5555 5678",
                "email": "sales@nswpoultry.com.au",
                "address": "42 Industry Way, Eastern Creek, NSW 2766",
                "distance": 22.8,
                "categories": ["Meat & Seafood"],
                "delivery_schedule": "Twice a week",
                "min_order": 100.00,
                "is_local": True,
                "reliability_score": 8.9,
                "sustainability_score": 7.8,
                "date_added": (datetime.now() - timedelta(days=200)).isoformat(),
                "last_order_date": (datetime.now() - timedelta(days=7)).isoformat(),
                "coordinates": {"latitude": -33.806, "longitude": 150.866},
                "products": [
                    {
                        "name": "Chicken Breast 500g",
                        "price": 7.20,
                        "unit": "each"
                    },
                    {
                        "name": "Whole Chicken 1.5kg",
                        "price": 9.50,
                        "unit": "each"
                    },
                    {
                        "name": "Chicken Thigh Fillets 500g",
                        "price": 6.80,
                        "unit": "each"
                    }
                ]
            },
            {
                "id": str(uuid.uuid4()),
                "name": "National Distributors",
                "contact_name": "Lisa Taylor",
                "phone": "+61 2 8888 1234",
                "email": "orders@nationaldist.com.au",
                "address": "5 Corporate Dr, Homebush, NSW 2140",
                "distance": 45.3,
                "categories": ["Beverages", "Canned & Packaged", "Snacks & Confectionery"],
                "delivery_schedule": "Weekly",
                "min_order": 500.00,
                "is_local": False,
                "reliability_score": 9.7,
                "sustainability_score": 6.5,
                "date_added": (datetime.now() - timedelta(days=365)).isoformat(),
                "last_order_date": (datetime.now() - timedelta(days=5)).isoformat(),
                "coordinates": {"latitude": -33.865, "longitude": 151.082},
                "products": [
                    {
                        "name": "Bottled Water 24-Pack",
                        "price": 8.50,
                        "unit": "each"
                    },
                    {
                        "name": "Pasta Sauce - Tomato & Basil",
                        "price": 2.10,
                        "unit": "each"
                    },
                    {
                        "name": "Potato Chips 175g",
                        "price": 2.80,
                        "unit": "each"
                    }
                ]
            }
        ]
        return suppliers
    
    def _load_data(self):
        """Load supplier data from file"""
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def _save_data(self, data):
        """Save supplier data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_supplier_count(self):
        """Get total number of local suppliers"""
        data = self._load_data()
        return len([s for s in data['suppliers'] if s['is_local']])
    
    def get_suppliers(self):
        """Get list of supplier names"""
        data = self._load_data()
        return [supplier['name'] for supplier in data['suppliers']]
    
    def get_supplier_categories(self):
        """Get list of supplier categories"""
        data = self._load_data()
        return data['categories']
    
    def get_supplier_list(self):
        """Get full supplier list"""
        data = self._load_data()
        return data['suppliers']
    
    def filter_suppliers(self, suppliers, search_term="", categories=None, max_distance=50):
        """Filter suppliers by search term, categories, and distance"""
        if not suppliers:
            return []
            
        filtered_suppliers = suppliers.copy()
        
        # Apply search filter
        if search_term:
            search_term = search_term.lower()
            filtered_suppliers = [
                s for s in filtered_suppliers 
                if search_term in s['name'].lower() or 
                   search_term in s['contact_name'].lower() or
                   any(search_term in product['name'].lower() for product in s['products'])
            ]
        
        # Apply category filter
        if categories and len(categories) > 0:
            filtered_suppliers = [
                s for s in filtered_suppliers 
                if any(category in s['categories'] for category in categories)
            ]
        
        # Apply distance filter
        filtered_suppliers = [s for s in filtered_suppliers if s['distance'] <= max_distance]
        
        # Sort by distance
        filtered_suppliers = sorted(filtered_suppliers, key=lambda s: s['distance'])
        
        return filtered_suppliers
    
    def get_supplier_map(self, suppliers):
        """Generate a map visualization of supplier locations"""
        if not suppliers:
            return None
        
        # Create a new figure with a specific size
        fig = Figure(figsize=(10, 6))
        ax = fig.subplots()
        
        # Store coordinates
        latitudes = []
        longitudes = []
        names = []
        distances = []
        is_local = []
        
        # Add store location (center)
        store_lat = -33.753
        store_lon = 150.695
        ax.scatter(store_lon, store_lat, color='red', s=100, marker='*')
        ax.annotate('Your Store', (store_lon, store_lat), fontsize=12, color='red',
                   xytext=(5, 5), textcoords='offset points')
        
        # Process supplier coordinates
        for supplier in suppliers:
            if 'coordinates' in supplier:
                lat = supplier['coordinates']['latitude']
                lon = supplier['coordinates']['longitude']
                latitudes.append(lat)
                longitudes.append(lon)
                names.append(supplier['name'])
                distances.append(supplier['distance'])
                is_local.append(supplier['is_local'])
        
        # Plot suppliers
        for i, (lon, lat, name, dist, local) in enumerate(zip(longitudes, latitudes, names, distances, is_local)):
            color = 'green' if local else 'blue'
            marker = 'o' if local else 's'
            ax.scatter(lon, lat, color=color, s=80, alpha=0.7, marker=marker)
            ax.annotate(f"{name} ({dist:.1f}km)", (lon, lat), fontsize=10,
                       xytext=(5, 5), textcoords='offset points')
        
        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='*', color='w', markerfacecolor='red', markersize=15, label='Your Store'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Local Supplier'),
            Line2D([0], [0], marker='s', color='w', markerfacecolor='blue', markersize=10, label='Non-Local Supplier')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        # Set title and labels
        ax.set_title('Supplier Locations Map')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        
        # Adjust plot limits to ensure all points are visible with some padding
        if latitudes and longitudes:
            min_lat, max_lat = min(latitudes), max(latitudes)
            min_lon, max_lon = min(longitudes), max(longitudes)
            
            # Include store location in bounds calculation
            min_lat = min(min_lat, store_lat)
            max_lat = max(max_lat, store_lat)
            min_lon = min(min_lon, store_lon)
            max_lon = max(max_lon, store_lon)
            
            # Add padding (5% of range)
            lat_padding = (max_lat - min_lat) * 0.05
            lon_padding = (max_lon - min_lon) * 0.05
            
            ax.set_xlim(min_lon - lon_padding, max_lon + lon_padding)
            ax.set_ylim(min_lat - lat_padding, max_lat + lat_padding)
        
        fig.tight_layout()
        return fig
    
    def add_supplier(self, name, contact_name, phone, email, address, categories, 
                   delivery_schedule, min_order, products):
        """Add a new local supplier"""
        data = self._load_data()
        
        # Generate random coordinates near Penrith for demo purposes
        # In a real app, this would use geocoding based on the address
        np.random.seed(hash(name) % 10000)
        base_lat, base_lon = -33.753, 150.695  # Penrith coordinates
        lat_offset = np.random.uniform(-0.05, 0.05)
        lon_offset = np.random.uniform(-0.05, 0.05)
        
        latitude = base_lat + lat_offset
        longitude = base_lon + lon_offset
        
        # Calculate approximate distance (in km)
        # This is a simplified calculation - real app would use proper geo-distance
        distance = np.sqrt((lat_offset * 111)**2 + (lon_offset * 88)**2)  # rough km conversion
        
        new_supplier = {
            "id": str(uuid.uuid4()),
            "name": name,
            "contact_name": contact_name,
            "phone": phone,
            "email": email,
            "address": address,
            "distance": round(distance, 1),
            "categories": categories,
            "delivery_schedule": delivery_schedule,
            "min_order": float(min_order),
            "is_local": distance <= 30,  # Consider local if within 30km
            "reliability_score": np.random.uniform(7.5, 9.5),  # Demo score
            "sustainability_score": np.random.uniform(7.0, 9.0),  # Demo score
            "date_added": datetime.now().isoformat(),
            "coordinates": {"latitude": latitude, "longitude": longitude},
            "products": products
        }
        
        data['suppliers'].append(new_supplier)
        self._save_data(data)
        
        return new_supplier
    
    def update_supplier(self, supplier_id, **kwargs):
        """Update an existing supplier"""
        data = self._load_data()
        
        for i, supplier in enumerate(data['suppliers']):
            if supplier['id'] == supplier_id:
                # Update only provided fields
                for key, value in kwargs.items():
                    if key in supplier:
                        supplier[key] = value
                
                data['suppliers'][i] = supplier
                self._save_data(data)
                return supplier
        
        return None  # Supplier not found
    
    def delete_supplier(self, supplier_id):
        """Delete a supplier"""
        data = self._load_data()
        
        for i, supplier in enumerate(data['suppliers']):
            if supplier['id'] == supplier_id:
                deleted_supplier = data['suppliers'].pop(i)
                self._save_data(data)
                return deleted_supplier
        
        return None  # Supplier not found
    
    def get_sourcing_analytics(self):
        """Get analytics data about local sourcing"""
        data = self._load_data()
        suppliers = data['suppliers']
        
        if not suppliers:
            return {
                'supplier_count': 0,
                'local_supplier_count': 0,
                'avg_distance': 0,
                'local_product_count': 0,
                'local_sourcing_percentage': 0
            }
        
        local_suppliers = [s for s in suppliers if s['is_local']]
        
        # Count local products
        local_product_count = sum(len(s['products']) for s in local_suppliers)
        total_product_count = sum(len(s['products']) for s in suppliers)
        
        # Calculate local sourcing percentage
        local_sourcing_percentage = (local_product_count / total_product_count * 100) if total_product_count > 0 else 0
        
        # Calculate average distance for local suppliers
        avg_distance = sum(s['distance'] for s in local_suppliers) / len(local_suppliers) if local_suppliers else 0
        
        return {
            'supplier_count': len(suppliers),
            'local_supplier_count': len(local_suppliers),
            'avg_distance': round(avg_distance, 1),
            'local_product_count': local_product_count,
            'local_sourcing_percentage': round(local_sourcing_percentage, 1)
        }
    
    def get_sourcing_by_category(self):
        """Get local sourcing percentage by category"""
        data = self._load_data()
        suppliers = data['suppliers']
        
        if not suppliers:
            return None
        
        # Initialize category counters
        categories = {}
        for category in data['categories']:
            categories[category] = {
                'local_products': 0,
                'total_products': 0
            }
        
        # Count products by category and locality
        for supplier in suppliers:
            for product in supplier['products']:
                # Find which categories this supplier belongs to
                for category in supplier['categories']:
                    if category in categories:
                        categories[category]['total_products'] += 1
                        if supplier['is_local']:
                            categories[category]['local_products'] += 1
        
        # Calculate percentages
        percentages = {}
        for category, counts in categories.items():
            if counts['total_products'] > 0:
                percentages[category] = (counts['local_products'] / counts['total_products'] * 100)
            else:
                percentages[category] = 0
        
        # Convert to DataFrame for charting
        df = pd.DataFrame.from_dict(percentages, orient='index', columns=['local_percentage'])
        df = df.sort_values('local_percentage', ascending=False)
        
        return df
    
    def get_cost_comparison(self):
        """Get cost comparison between local and non-local suppliers"""
        data = self._load_data()
        suppliers = data['suppliers']
        
        if not suppliers:
            return None
        
        # Initialize product comparisons
        products = {}
        
        # Collect prices for products from local and non-local suppliers
        for supplier in suppliers:
            for product in supplier['products']:
                product_name = product['name']
                
                if product_name not in products:
                    products[product_name] = {
                        'local_prices': [],
                        'nonlocal_prices': []
                    }
                
                if supplier['is_local']:
                    products[product_name]['local_prices'].append(product['price'])
                else:
                    products[product_name]['nonlocal_prices'].append(product['price'])
        
        # Calculate average prices
        comparison = {}
        for product_name, prices in products.items():
            if prices['local_prices'] and prices['nonlocal_prices']:
                local_avg = sum(prices['local_prices']) / len(prices['local_prices'])
                nonlocal_avg = sum(prices['nonlocal_prices']) / len(prices['nonlocal_prices'])
                
                comparison[product_name] = {
                    'local': local_avg,
                    'nonlocal': nonlocal_avg,
                    'difference': nonlocal_avg - local_avg,
                    'percentage': ((nonlocal_avg - local_avg) / nonlocal_avg * 100)
                }
        
        # Convert to DataFrame for charting
        if comparison:
            df = pd.DataFrame.from_dict({k: [v['local'], v['nonlocal']] for k, v in comparison.items()},
                                      orient='index', columns=['Local', 'Non-Local'])
            
            # Sort by price difference
            df['Difference'] = df['Non-Local'] - df['Local']
            df = df.sort_values('Difference', ascending=False)
            
            # Take top 10 for charting
            df = df.head(10)
            
            # Drop difference column for chart
            return df[['Local', 'Non-Local']]
        
        return None
    
    def calculate_savings(self):
        """Calculate monthly savings from local sourcing"""
        data = self._load_data()
        suppliers = data['suppliers']
        
        if not suppliers:
            return 0
        
        # Get cost comparison data
        comparison_df = self.get_cost_comparison()
        
        if comparison_df is None or comparison_df.empty:
            return 0
        
        # Calculate total savings across all compared products
        total_savings = (comparison_df['Non-Local'] - comparison_df['Local']).sum()
        
        # Estimate monthly purchase quantity (for demo purposes)
        estimated_quantity = 20
        
        # Calculate monthly savings
        monthly_savings = total_savings * estimated_quantity
        
        return monthly_savings
        
    def get_supplier_by_id(self, supplier_id):
        """Get supplier details by ID"""
        data = self._load_data()
        suppliers = data['suppliers']
        
        for supplier in suppliers:
            if supplier['id'] == supplier_id:
                return supplier
                
        return None
    
    def get_supplier_by_name(self, supplier_name):
        """Get supplier details by name"""
        data = self._load_data()
        suppliers = data['suppliers']
        
        for supplier in suppliers:
            if supplier['name'] == supplier_name:
                return supplier
                
        return None
    
    def get_supplier_products(self, supplier_id=None, supplier_name=None):
        """Get products for a specific supplier"""
        if supplier_id:
            supplier = self.get_supplier_by_id(supplier_id)
        elif supplier_name:
            supplier = self.get_supplier_by_name(supplier_name)
        else:
            return []
            
        if supplier:
            return supplier['products']
        return []
    
    def create_order(self, supplier_id, product_name, quantity, pickup_window_start, pickup_window_end):
        """Create a new order for a supplier"""
        supplier = self.get_supplier_by_id(supplier_id)
        if not supplier:
            return None
            
        # Generate order details
        order_id = str(uuid.uuid4())
        order_date = datetime.now().isoformat()
        
        # Find product details
        product_details = None
        for product in supplier['products']:
            if product['name'] == product_name:
                product_details = product
                break
                
        if not product_details:
            return None
            
        # Calculate order total
        total_amount = product_details['price'] * quantity
        
        # Create order object
        order = {
            "id": order_id,
            "supplier_id": supplier_id,
            "supplier_name": supplier['name'],
            "supplier_contact": {
                "name": supplier['contact_name'],
                "phone": supplier['phone'],
                "email": supplier['email']
            },
            "product": {
                "name": product_name,
                "price": product_details['price'],
                "unit": product_details['unit']
            },
            "quantity": quantity,
            "total_amount": total_amount,
            "pickup_window": {
                "start": pickup_window_start,
                "end": pickup_window_end
            },
            "order_date": order_date,
            "status": "pending",
            "status_history": [
                {
                    "status": "pending",
                    "timestamp": order_date,
                    "note": "Order created"
                }
            ],
            "notification_history": [],
            "driver_assigned": False
        }
        
        # Save order
        data = self._load_data()
        data['orders'].append(order)
        self._save_data(data)
        
        # Update supplier's last_order_date
        for i, s in enumerate(data['suppliers']):
            if s['id'] == supplier_id:
                data['suppliers'][i]['last_order_date'] = order_date
                break
                
        self._save_data(data)
        
        return order
    
    def get_orders(self, status=None):
        """Get all orders, optionally filtered by status"""
        data = self._load_data()
        orders = data['orders']
        
        if status:
            orders = [order for order in orders if order['status'] == status]
            
        # Sort by order date (most recent first)
        orders = sorted(orders, key=lambda o: o['order_date'], reverse=True)
        
        return orders
    
    def get_order_by_id(self, order_id):
        """Get order details by ID"""
        data = self._load_data()
        orders = data['orders']
        
        for order in orders:
            if order['id'] == order_id:
                return order
                
        return None
    
    def update_order_status(self, order_id, new_status, note=None):
        """Update an order's status"""
        data = self._load_data()
        
        for i, order in enumerate(data['orders']):
            if order['id'] == order_id:
                data['orders'][i]['status'] = new_status
                
                # Add status history entry
                status_entry = {
                    "status": new_status,
                    "timestamp": datetime.now().isoformat(),
                    f"note": note if note else f"Status updated to {new_status}"
                }
                
                data['orders'][i]['status_history'].append(status_entry)
                self._save_data(data)
                return data['orders'][i]
                
        return None
    
    def send_order_notification(self, order_id, notification_type="sms"):
        """Send order notification to supplier via SMS or email"""
        order = self.get_order_by_id(order_id)
        if not order:
            return {"success": False, "message": "Order not found"}
            
        # Import notification services
        import os
        from twilio.rest import Client
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        # Create notification message
        message = f"Order #{order_id[:8]}: {order['quantity']} {order['product']['name']}, pickup {order['pickup_window']['start']} - {order['pickup_window']['end']}, Penrith Grocery"
        
        notification_result = {"success": False, "message": "Notification failed"}
        
        # Record notification attempt
        notification_entry = {
            "type": notification_type,
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "status": "pending"
        }
        
        # Attempt notification
        try:
            if notification_type == "sms":
                # Check if we have Twilio credentials
                twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
                twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
                twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
                
                if twilio_account_sid and twilio_auth_token and twilio_phone_number:
                    # Send SMS via Twilio
                    client = Client(twilio_account_sid, twilio_auth_token)
                    
                    client.messages.create(
                        body=message,
                        from_=twilio_phone_number,
                        to=order['supplier_contact']['phone']
                    )
                    
                    notification_result = {"success": True, "message": "SMS sent successfully"}
                    notification_entry["status"] = "sent"
                else:
                    # Simulate success for demo purposes
                    notification_result = {"success": True, "message": "SMS notification simulated (Twilio credentials not found)"}
                    notification_entry["status"] = "simulated"
                    notification_entry["note"] = "Twilio credentials not found"
            
            elif notification_type == "email":
                # Check if we have SendGrid credentials
                sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
                
                if sendgrid_api_key:
                    # Send email via SendGrid
                    sg = SendGridAPIClient(sendgrid_api_key)
                    
                    email_message = Mail(
                        from_email='orders@penrithgrocery.com.au',
                        to_emails=order['supplier_contact']['email'],
                        subject=f"Order #{order_id[:8]} from Penrith Grocery",
                        html_content=f"""
                        <h2>New Order from Penrith Grocery</h2>
                        <p><strong>Order ID:</strong> #{order_id[:8]}</p>
                        <p><strong>Product:</strong> {order['product']['name']}</p>
                        <p><strong>Quantity:</strong> {order['quantity']}</p>
                        <p><strong>Pickup Window:</strong> {order['pickup_window']['start']} - {order['pickup_window']['end']}</p>
                        <p>Please confirm this order by replying to this email or calling (02) 5555-9999.</p>
                        """
                    )
                    
                    sg.send(email_message)
                    
                    notification_result = {"success": True, "message": "Email sent successfully"}
                    notification_entry["status"] = "sent"
                else:
                    # Simulate success for demo purposes
                    notification_result = {"success": True, "message": "Email notification simulated (SendGrid credentials not found)"}
                    notification_entry["status"] = "simulated"
                    notification_entry["note"] = "SendGrid credentials not found"
        
        except Exception as e:
            notification_result = {"success": False, "message": f"Notification failed: {str(e)}"}
            notification_entry["status"] = "failed"
            notification_entry["error"] = str(e)
        
        # Update order's notification history
        data = self._load_data()
        for i, o in enumerate(data['orders']):
            if o['id'] == order_id:
                data['orders'][i]['notification_history'].append(notification_entry)
                self._save_data(data)
                break
                
        return notification_result
    
    def process_supplier_response(self, order_id, response_text):
        """Process a response from a supplier"""
        order = self.get_order_by_id(order_id)
        if not order:
            return {"success": False, "message": "Order not found"}
            
        # Analyze response text for confirmation or rejection
        response_lower = response_text.lower()
        
        if "confirm" in response_lower or "yes" in response_lower or "accept" in response_lower:
            # Order confirmed
            self.update_order_status(
                order_id, 
                "confirmed", 
                f"Supplier confirmed: {response_text}"
            )
            return {"success": True, "message": "Order confirmed", "status": "confirmed"}
            
        elif "cancel" in response_lower or "no" in response_lower or "reject" in response_lower:
            # Order rejected
            self.update_order_status(
                order_id, 
                "rejected", 
                f"Supplier rejected: {response_text}"
            )
            return {"success": True, "message": "Order rejected", "status": "rejected"}
            
        else:
            # Ambiguous response
            self.update_order_status(
                order_id, 
                "pending", 
                f"Received response: {response_text}"
            )
            return {"success": True, "message": "Response recorded, but needs manual review", "status": "pending"}
    
    def assign_driver(self, order_id, driver_name):
        """Assign a driver to an order"""
        data = self._load_data()
        
        for i, order in enumerate(data['orders']):
            if order['id'] == order_id:
                data['orders'][i]['driver_assigned'] = True
                data['orders'][i]['driver'] = {
                    "name": driver_name,
                    "assigned_at": datetime.now().isoformat()
                }
                
                # Add status history entry
                status_entry = {
                    "status": "driver_assigned",
                    "timestamp": datetime.now().isoformat(),
                    "note": f"Driver {driver_name} assigned to order"
                }
                
                data['orders'][i]['status_history'].append(status_entry)
                self._save_data(data)
                return data['orders'][i]
                
        return None
    
    def get_alternative_suppliers(self, product_name, original_supplier_id):
        """Get alternative suppliers for a product when original supplier cancels"""
        data = self._load_data()
        suppliers = data['suppliers']
        
        alternatives = []
        
        for supplier in suppliers:
            # Skip the original supplier
            if supplier['id'] == original_supplier_id:
                continue
                
            # Check if this supplier offers the product
            for product in supplier['products']:
                if product_name.lower() in product['name'].lower():
                    alternatives.append({
                        "supplier": supplier,
                        "product": product
                    })
                    break
        
        # Sort alternatives by reliability score and then by distance
        return sorted(
            alternatives, 
            key=lambda a: (-a['supplier']['reliability_score'], a['supplier']['distance'])
        )
