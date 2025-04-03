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
                "orders": []
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
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
