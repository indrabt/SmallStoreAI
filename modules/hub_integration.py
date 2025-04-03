import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import uuid
import os
import json
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class LogisticsHubIntegration:
    """
    Handles integration with the smart logistics hub including:
    - Route optimization
    - Predictive resilience analysis
    - Multi-modal logistics orchestration
    - Real-time client dashboard integration
    - Ecosystem partnership management
    """
    
    def __init__(self, data_file="data/logistics_hub.json"):
        """Initialize the logistics hub integration with data file path"""
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file exists, create if it doesn't"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        if not os.path.exists(self.data_file):
            # Create initial data with sample logistics hub data
            initial_data = {
                "routes": self._generate_sample_routes(),
                "resilience_data": self._generate_sample_resilience_data(),
                "logistics_options": self._generate_sample_logistics_options(),
                "partnerships": self._generate_sample_partnerships(),
                "dashboard_data": {},
                "history": []
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _generate_sample_routes(self):
        """Generate sample route data for first-time setup"""
        # Base locations around Penrith
        base_locations = [
            {"name": "Penrith CBD", "address": "High St, Penrith NSW 2750", "coordinates": {"lat": -33.751, "lon": 150.694}},
            {"name": "Glenmore Park", "address": "Glenmore Pkwy, Glenmore Park NSW 2745", "coordinates": {"lat": -33.784, "lon": 150.670}},
            {"name": "Emu Plains", "address": "Great Western Hwy, Emu Plains NSW 2750", "coordinates": {"lat": -33.747, "lon": 150.661}},
            {"name": "Jamisontown", "address": "Mulgoa Rd, Jamisontown NSW 2750", "coordinates": {"lat": -33.766, "lon": 150.682}},
            {"name": "South Penrith", "address": "York Rd, South Penrith NSW 2750", "coordinates": {"lat": -33.764, "lon": 150.698}},
            {"name": "Cranebrook", "address": "Borrowdale Way, Cranebrook NSW 2749", "coordinates": {"lat": -33.724, "lon": 150.710}},
            {"name": "Cambridge Park", "address": "Oxford St, Cambridge Park NSW 2747", "coordinates": {"lat": -33.742, "lon": 150.734}},
            {"name": "Kingswood", "address": "The Northern Rd, Kingswood NSW 2747", "coordinates": {"lat": -33.760, "lon": 150.722}},
            {"name": "Werrington", "address": "Dunheved Rd, Werrington NSW 2747", "coordinates": {"lat": -33.742, "lon": 150.748}}
        ]
        
        # Sample drivers
        drivers = ["Mike Smith", "Sarah Johnson", "David Chen", "Emma Wong", "James Taylor"]
        
        # Sample vehicles
        vehicles = ["Van #1", "Van #2", "Truck #1", "Hybrid Vehicle", "Electric Van"]
        
        # Generate routes
        routes = []
        
        for i in range(3):  # 3 sample routes
            # Select locations for this route (4-6 stops)
            np.random.seed(i)  # For consistent demo data
            num_stops = np.random.randint(4, 7)
            route_stops = np.random.choice(base_locations, num_stops, replace=False).tolist()
            
            # Calculate estimated time (5-15 minutes per stop plus base time)
            base_time = 30  # Base route time in minutes
            per_stop_time = np.random.uniform(5, 15, num_stops)
            estimated_time = int(base_time + per_stop_time.sum())
            
            # Calculate total distance (2-5 km per stop plus base distance)
            base_distance = 5  # Base route distance in km
            per_stop_distance = np.random.uniform(2, 5, num_stops)
            total_distance = round(base_distance + per_stop_distance.sum(), 1)
            
            # Assign driver and vehicle
            driver = drivers[i % len(drivers)]
            vehicle = vehicles[i % len(vehicles)]
            
            # Add delivery windows to stops
            for stop in route_stops:
                # Morning or afternoon window
                if np.random.random() < 0.5:
                    window_start = np.random.randint(8, 12)
                    window_end = window_start + np.random.randint(1, 3)
                    stop['delivery_window'] = f"{window_start}:00 AM - {window_end}:00 PM"
                else:
                    window_start = np.random.randint(1, 5)
                    window_end = window_start + np.random.randint(1, 3)
                    stop['delivery_window'] = f"{window_start}:00 PM - {window_end}:00 PM"
            
            # Create route
            route = {
                "id": f"R-{i+1}",
                "vehicle": vehicle,
                "driver": driver,
                "estimated_time": estimated_time,
                "total_distance": total_distance,
                "stop_count": num_stops,
                "stops": route_stops,
                "status": "planned",
                "created_at": (datetime.now() - timedelta(hours=np.random.randint(1, 24))).isoformat(),
                "optimized": True,
                "distance_saved": round(np.random.uniform(1.5, 4.0), 1),
                "optimization_score": round(np.random.uniform(7.5, 9.5), 1)
            }
            
            routes.append(route)
        
        return routes
    
    def _generate_sample_resilience_data(self):
        """Generate sample resilience data for first-time setup"""
        # Sample risk factors
        risk_factors = [
            {
                "factor": "Weather Disruption",
                "severity": "Medium",
                "description": "Potential heavy rainfall forecasted for next week that may affect local deliveries",
                "probability": 0.6,
                "impact_score": 7,
                "mitigation_strategies": [
                    "Pre-stock high-demand items",
                    "Schedule deliveries earlier in the week",
                    "Ensure backup transport options"
                ]
            },
            {
                "factor": "Supplier Capacity",
                "severity": "Low",
                "description": "Minor capacity constraints with dairy supplier due to seasonal fluctuations",
                "probability": 0.3,
                "impact_score": 4,
                "mitigation_strategies": [
                    "Increase order frequency with smaller volumes",
                    "Temporarily diversify dairy sourcing"
                ]
            },
            {
                "factor": "Transport Cost Increase",
                "severity": "High",
                "description": "Expected fuel price increase of 10% next month affecting delivery costs",
                "probability": 0.9,
                "impact_score": 8,
                "mitigation_strategies": [
                    "Optimize delivery routes further",
                    "Consider shared logistics with nearby businesses",
                    "Temporarily increase local sourcing"
                ]
            },
            {
                "factor": "Labor Shortage",
                "severity": "Medium",
                "description": "Seasonal labor shortages expected during upcoming holiday period",
                "probability": 0.7,
                "impact_score": 6,
                "mitigation_strategies": [
                    "Pre-arrange temporary staff",
                    "Schedule deliveries during off-peak hours",
                    "Simplify receiving processes"
                ]
            }
        ]
        
        # Sample backup suppliers
        backup_suppliers = {
            "Penrith Dairy Co-op": [
                {
                    "name": "Western Sydney Dairy",
                    "distance": 15.2,
                    "reliability_score": 8.5,
                    "cost_difference": "+5%"
                },
                {
                    "name": "Blue Mountains Dairy",
                    "distance": 22.8,
                    "reliability_score": 9.2,
                    "cost_difference": "+8%"
                }
            ],
            "Local Organic Farms": [
                {
                    "name": "Richmond Fresh Produce",
                    "distance": 18.5,
                    "reliability_score": 8.8,
                    "cost_difference": "+3%"
                },
                {
                    "name": "Hawkesbury Valley Farms",
                    "distance": 25.3,
                    "reliability_score": 9.0,
                    "cost_difference": "+7%"
                }
            ],
            "NSW Poultry": [
                {
                    "name": "Windsor Poultry Farms",
                    "distance": 30.2,
                    "reliability_score": 8.6,
                    "cost_difference": "+2%"
                }
            ]
        }
        
        # Create resilience data
        resilience_data = {
            "last_updated": datetime.now().isoformat(),
            "overall_risk_score": 6.2,
            "high_risk_suppliers": 1,
            "medium_risk_suppliers": 2,
            "risk_mitigations": 10,
            "risk_factors": risk_factors,
            "backup_suppliers": backup_suppliers
        }
        
        return resilience_data
    
    def _generate_sample_logistics_options(self):
        """Generate sample logistics options for first-time setup"""
        options = [
            {
                "id": "option-1",
                "name": "Standard Delivery",
                "type": "road",
                "cost": 250.00,
                "time": 48,
                "carbon_footprint": 180,
                "reliability_score": 8.5,
                "details": "Standard road delivery using existing contracted carriers",
                "suitable_for": ["Regular restocking", "Non-perishable goods"]
            },
            {
                "id": "option-2",
                "name": "Express Delivery",
                "type": "road",
                "cost": 350.00,
                "time": 24,
                "carbon_footprint": 200,
                "reliability_score": 9.0,
                "details": "Priority road delivery for urgent restocking needs",
                "suitable_for": ["Urgent orders", "Perishable goods"]
            },
            {
                "id": "option-3",
                "name": "Multi-Modal Delivery",
                "type": "multi-modal",
                "cost": 300.00,
                "time": 36,
                "carbon_footprint": 140,
                "reliability_score": 8.8,
                "details": "Combination of rail and last-mile delivery for reduced emissions",
                "suitable_for": ["Large orders", "Environmental focus"]
            },
            {
                "id": "option-4",
                "name": "Local Courier Network",
                "type": "local",
                "cost": 275.00,
                "time": 30,
                "carbon_footprint": 120,
                "reliability_score": 8.2,
                "details": "Delivery through local courier partners for medium-sized orders",
                "suitable_for": ["Medium orders", "Supporting local businesses"]
            },
            {
                "id": "option-5",
                "name": "Green Delivery",
                "type": "green",
                "cost": 320.00,
                "time": 40,
                "carbon_footprint": 90,
                "reliability_score": 8.0,
                "details": "Low-emission vehicles and optimized routes for minimal environmental impact",
                "suitable_for": ["Environmental focus", "Regular restocking"]
            }
        ]
        
        return options
    
    def _generate_sample_partnerships(self):
        """Generate sample partnerships for first-time setup"""
        partnerships = [
            {
                "id": "partner-1",
                "name": "Western Sydney Logistics",
                "type": "Transport Provider",
                "services": "Road freight, storage, cross-docking",
                "integration_status": "Active",
                "contact": "John Smith | john@wsl.com.au | +61 2 5555 1234",
                "partnership_since": (datetime.now() - timedelta(days=180)).isoformat(),
                "service_level": 9.2,
                "cost_savings": "12%"
            },
            {
                "id": "partner-2",
                "name": "EcoDelivery Sydney",
                "type": "Green Logistics",
                "services": "Electric vehicle delivery, carbon offset logistics",
                "integration_status": "Pending",
                "contact": "Emma Green | emma@ecodelivery.com.au | +61 2 5555 4321",
                "partnership_since": None,
                "service_level": None,
                "cost_savings": "Estimated 5%"
            },
            {
                "id": "partner-3",
                "name": "Penrith Courier Collective",
                "type": "Last-Mile Delivery",
                "services": "Rapid local delivery, returns management",
                "integration_status": "Active",
                "contact": "Michael Wong | operations@penrithcouriers.com.au | +61 2 5555 5678",
                "partnership_since": (datetime.now() - timedelta(days=90)).isoformat(),
                "service_level": 8.8,
                "cost_savings": "8%"
            },
            {
                "id": "partner-4",
                "name": "NSW Cold Chain Solutions",
                "type": "Temperature-Controlled Logistics",
                "services": "Refrigerated transport, cold storage",
                "integration_status": "Not Integrated",
                "contact": "Sarah Johnson | sarah@nswcoldchain.com.au | +61 2 5555 8765",
                "partnership_since": None,
                "service_level": None,
                "cost_savings": "Estimated 15%"
            }
        ]
        
        return partnerships
    
    def _load_data(self):
        """Load logistics hub data from file"""
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def _save_data(self, data):
        """Save logistics hub data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_supplier_data(self):
        """Load supplier data from file"""
        supplier_file = "data/suppliers.json"
        
        if not os.path.exists(supplier_file):
            return {"suppliers": []}
            
        with open(supplier_file, 'r') as f:
            return json.load(f)
    
    def get_optimized_routes(self):
        """Get optimized delivery routes"""
        data = self._load_data()
        return data['routes']
    
    def get_total_routes(self):
        """Get total number of routes"""
        data = self._load_data()
        return len(data['routes'])
    
    def get_avg_distance_saved(self):
        """Get average distance saved by route optimization"""
        data = self._load_data()
        routes = data['routes']
        
        if not routes:
            return 0
        
        total_saved = sum(route.get('distance_saved', 0) for route in routes)
        return total_saved / len(routes)
    
    def get_fuel_savings(self):
        """Get estimated fuel savings from route optimization"""
        # Rough estimate based on distance saved
        avg_distance_saved = self.get_avg_distance_saved()
        total_routes = self.get_total_routes()
        
        # Assume $0.20 per km fuel cost for delivery vehicles
        fuel_cost_per_km = 0.20
        
        # Calculate monthly savings (assume each route is run 4 times per month)
        monthly_savings = avg_distance_saved * total_routes * 4 * fuel_cost_per_km
        
        return monthly_savings
    
    def get_route_map(self):
        """Generate a map visualization of optimized routes"""
        data = self._load_data()
        routes = data['routes']
        
        if not routes:
            return None
        
        # Create a new figure with a specific size
        fig = Figure(figsize=(10, 6))
        ax = fig.subplots()
        
        # Store points
        store_lat, store_lon = -33.753, 150.695  # Penrith store location
        
        # Add store location (center)
        ax.scatter(store_lon, store_lat, color='red', s=100, marker='*')
        ax.annotate('Your Store', (store_lon, store_lat), fontsize=12, color='red',
                   xytext=(5, 5), textcoords='offset points')
        
        # Route colors
        colors = ['green', 'blue', 'purple', 'orange', 'brown']
        
        # Plot each route
        for i, route in enumerate(routes):
            route_color = colors[i % len(colors)]
            
            # Extract stops
            stops = route['stops']
            
            # Start at store
            route_lats = [store_lat]
            route_lons = [store_lon]
            
            # Add each stop
            for stop in stops:
                lat = stop['coordinates']['lat']
                lon = stop['coordinates']['lon']
                route_lats.append(lat)
                route_lons.append(lon)
                
                # Plot stop
                ax.scatter(lon, lat, color=route_color, s=80, alpha=0.7, marker='o')
                ax.annotate(stop['name'], (lon, lat), fontsize=9,
                           xytext=(5, 5), textcoords='offset points')
            
            # Return to store
            route_lats.append(store_lat)
            route_lons.append(store_lon)
            
            # Plot route line
            ax.plot(route_lons, route_lats, color=route_color, linestyle='-', linewidth=2, alpha=0.6,
                   label=f"Route {route['id']} ({route['driver']})")
        
        # Add legend
        ax.legend(loc='upper right', fontsize=9)
        
        # Set title and labels
        ax.set_title('Optimized Delivery Routes')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        
        # Adjust plot limits
        all_lats = [stop['coordinates']['lat'] for route in routes for stop in route['stops']]
        all_lons = [stop['coordinates']['lon'] for route in routes for stop in route['stops']]
        
        if all_lats and all_lons:
            min_lat, max_lat = min(all_lats), max(all_lats)
            min_lon, max_lon = min(all_lons), max(all_lons)
            
            # Include store location in bounds calculation
            min_lat = min(min_lat, store_lat)
            max_lat = max(max_lat, store_lat)
            min_lon = min(min_lon, store_lon)
            max_lon = max(max_lon, store_lon)
            
            # Add padding (5% of range)
            lat_padding = (max_lat - min_lat) * 0.1
            lon_padding = (max_lon - min_lon) * 0.1
            
            ax.set_xlim(min_lon - lon_padding, max_lon + lon_padding)
            ax.set_ylim(min_lat - lat_padding, max_lat + lat_padding)
        
        fig.tight_layout()
        return fig
    
    def dispatch_route(self, route_id):
        """Dispatch a planned route"""
        data = self._load_data()
        
        # Find the route
        for i, route in enumerate(data['routes']):
            if route['id'] == route_id:
                # Update status
                data['routes'][i]['status'] = "dispatched"
                data['routes'][i]['dispatched_at'] = datetime.now().isoformat()
                
                # Log the event
                event = {
                    "event_type": "route_dispatched",
                    "route_id": route_id,
                    "timestamp": datetime.now().isoformat(),
                    "details": {
                        "driver": route['driver'],
                        "vehicle": route['vehicle'],
                        "stop_count": route['stop_count']
                    }
                }
                
                data['history'].append(event)
                self._save_data(data)
                return True
        
        return False  # Route not found
    
    def get_resilience_insights(self):
        """Get supply chain resilience insights"""
        data = self._load_data()
        return data['resilience_data']
    
    def get_risk_map(self):
        """Generate a risk map visualization"""
        data = self._load_data()
        resilience_data = data['resilience_data']
        supplier_data = self._load_supplier_data()
        
        if not resilience_data or not supplier_data['suppliers']:
            return None
        
        # Create a new figure
        fig = Figure(figsize=(10, 6))
        ax = fig.subplots()
        
        # Store location
        store_lat, store_lon = -33.753, 150.695  # Penrith store location
        ax.scatter(store_lon, store_lat, color='red', s=100, marker='*')
        ax.annotate('Your Store', (store_lon, store_lat), fontsize=12, color='red',
                   xytext=(5, 5), textcoords='offset points')
        
        # Map suppliers with risk levels
        for supplier in supplier_data['suppliers']:
            if 'coordinates' in supplier:
                lat = supplier['coordinates']['latitude']
                lon = supplier['coordinates']['longitude']
                name = supplier['name']
                
                # Determine risk level (for demo purposes)
                # In a real app, this would come from actual risk assessment
                risk_level = "Low"
                if "Dairy" in name or "Poultry" in name:  # Match high-risk suppliers from resilience data
                    risk_level = "High"
                elif "Bakery" in name or "Organic" in name:
                    risk_level = "Medium"
                
                # Set color based on risk
                if risk_level == "High":
                    color = 'red'
                    size = 100
                elif risk_level == "Medium":
                    color = 'orange'
                    size = 80
                else:
                    color = 'green'
                    size = 60
                
                # Plot supplier
                ax.scatter(lon, lat, color=color, s=size, alpha=0.7, marker='o')
                ax.annotate(f"{name} ({risk_level} risk)", (lon, lat), fontsize=9,
                           xytext=(5, 5), textcoords='offset points')
                
                # Draw connecting line to store
                ax.plot([store_lon, lon], [store_lat, lat], color=color, 
                       linestyle='--', linewidth=1, alpha=0.5)
        
        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='*', color='w', markerfacecolor='red', markersize=15, label='Your Store'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Low Risk Supplier'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Medium Risk Supplier'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='High Risk Supplier')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        # Set title and labels
        ax.set_title('Supply Chain Risk Map')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        
        # Adjust plot limits
        fig.tight_layout()
        return fig
    
    def get_backup_suppliers(self):
        """Get backup supplier recommendations"""
        data = self._load_data()
        resilience_data = data['resilience_data']
        
        return resilience_data.get('backup_suppliers', {})
    
    def get_logistics_options(self):
        """Get available logistics options"""
        data = self._load_data()
        return data['logistics_options']
    
    def get_recommended_logistics_option(self):
        """Get the recommended logistics option based on current needs"""
        data = self._load_data()
        options = data['logistics_options']
        
        if not options:
            return None
        
        # In a real app, this would use more sophisticated logic
        # For demo, recommend option with best balance of cost and carbon footprint
        
        # Calculate a score for each option (lower is better)
        for option in options:
            # Normalize scores (lower is better)
            cost_score = option['cost'] / 300  # Normalize around $300
            time_score = option['time'] / 36   # Normalize around 36 hours
            carbon_score = option['carbon_footprint'] / 150  # Normalize around 150kg
            
            # Weight factors
            cost_weight = 0.4
            time_weight = 0.3
            carbon_weight = 0.3
            
            # Calculate overall score (lower is better)
            option['_score'] = (cost_score * cost_weight + 
                               time_score * time_weight + 
                               carbon_score * carbon_weight)
        
        # Find option with lowest score
        recommended = min(options, key=lambda x: x['_score'])
        
        # Remove temporary score
        for option in options:
            if '_score' in option:
                del option['_score']
        
        return recommended
    
    def apply_logistics_option(self, option_name):
        """Apply a selected logistics option"""
        data = self._load_data()
        
        # Find the option
        selected_option = next((o for o in data['logistics_options'] if o['name'] == option_name), None)
        
        if not selected_option:
            return False
        
        # Log the selection
        event = {
            "event_type": "logistics_option_selected",
            "option_id": selected_option['id'],
            "option_name": selected_option['name'],
            "timestamp": datetime.now().isoformat(),
            "details": {
                "cost": selected_option['cost'],
                "time": selected_option['time'],
                "carbon_footprint": selected_option['carbon_footprint']
            }
        }
        
        data['history'].append(event)
        self._save_data(data)
        
        return True
    
    def get_partnerships(self):
        """Get ecosystem partnerships"""
        data = self._load_data()
        return data['partnerships']
    
    def integrate_partner(self, partner_id):
        """Initiate or update partner integration"""
        data = self._load_data()
        
        # Find the partner
        for i, partner in enumerate(data['partnerships']):
            if partner['id'] == partner_id:
                # Update status
                if partner['integration_status'] == "Not Integrated":
                    data['partnerships'][i]['integration_status'] = "Pending"
                elif partner['integration_status'] == "Pending":
                    data['partnerships'][i]['integration_status'] = "Active"
                    data['partnerships'][i]['partnership_since'] = datetime.now().isoformat()
                    # Assign random service level if becoming active
                    data['partnerships'][i]['service_level'] = round(np.random.uniform(8.0, 9.5), 1)
                
                # Log the event
                event = {
                    "event_type": "partner_integration_updated",
                    "partner_id": partner_id,
                    "partner_name": partner['name'],
                    "timestamp": datetime.now().isoformat(),
                    "details": {
                        "new_status": data['partnerships'][i]['integration_status']
                    }
                }
                
                data['history'].append(event)
                self._save_data(data)
                return True
        
        return False  # Partner not found
