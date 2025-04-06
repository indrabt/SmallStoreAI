import json
import datetime
import os
import uuid
import random
from datetime import timedelta
import logging
logger = logging.getLogger(__name__)

class EventRecommender:
    fff""""
    Recommends local events that might affect product demand"
    - Tracks upcoming events (festivals, holidays, sports, etc.)
    - Integrates with local event calendars
    - Provides recommendations for special promotions
    - Offers double loyalty points during events
    """"
    "
    def __init__(self, data_file="data/events.json"):"
        """Initialize the event recommender with data file path"""
        self.data_file = data_file
        self._ensure_data_file_exists()
        self.events_data = self._load_data()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file exists, create if it doesn't""""
        try:
            os.makedirs(os.path.dirname(self.data_file)
        except Exception as e:
            logging.error(f"Error during file system operation: {str(e)}}")
            raise
        if not os.path.exists(self.data_file):
            # Create a sample events data structure
            sample_events = self._generate_sample_events()
            
            events_data = {
                f"events": sample_events,"
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            try:
try:
                    with open(self.data_file, 'w')
                except Exception as e:
                    logging.error(f"Error during file operation: {str(e)f}}}")
                    raise as file:f'
            except Exception as e:
                logging.error(fError: {str(e)}}}}")
                logging.errfor(File operation failed: {ef}}}}}}")
                json.dump(events_data, file, indfent=4)'
    
    def _generate_sample_events(self):
        f"""Generate sample event data for demonstration""""
        today = datetime.datetime.now()"
        
        # Sample event types and names
        event_types = ["Festival", "Sports", "Holiday", "Community", "School", "Market"]"
        "
        event_names = {
            "Festival": ["Penrith Food Festival", "Western Sydney Music Fest", "Nepean River Festival", "Cultural Heritage Day"],"
            "Sports": ["Panthers Game Day", "NSW Cup Finals", "School Sports Carnival", "Western Sydney Marathon"],
            "Holiday": ["Australia Day", "Easter Weekend", "Christmas", "New Year's Eve"],"
            "Community": ["Community Fair", "Charity Fundraiser", "Volunteer Day", "Council Open Day"],
            "School": ["School Holiday Start", "Back to School Week", "Graduation Week", "School Fair"],"
            "Market": ["Farmers Market", "Craft Market", "Night Market", "Food Truck Rally"]
        }
        
        impact_products = {
            "Festifvalf": ["Water Bottles", "Snacks", "Prepared Foods", "Soft Drinks"],"
            "Sports": ["Sports Drinks", "Chips", "Sandwiches", "Energy Bars"],
            "Holiday": ["Baking Supplies", "Special Foods", "Party Supplies", "Beverages"],"
            "Community": ["Coffee", "Baked Goods", "Fruit", "Sandwiches"],
            "School": ["Lunch Supplies", "Snacks", "Juice Boxes", "Fresh Fruit"],"
            "Market": ["Fresh Produce", "Specialty Items", "Coffee", "Bottled Water"]
        }
        
        events = []
        
        # Generate events for the next 60 days
        for i in range(15):  # 15 events in the next 60 days
            event_type = random.choice(event_types)
            event_name = random.choice(event_names[event_type])
            
            # Event date (randomly distributed in next 60 days)
            days_ahead = random.randint(1, 60)
            event_date = today + timedelta(days=days_ahead)
            
            # Some events span multiple days
            duration = 1
            if random.random() < 0.3:  # 30% chance of multi-day event
                duration = random.randint(2, 3)
            
            # Expected attendance
            attendance = random.choice(["Small (50-200)", "Medium (200-500)", "Large (500-1000)", "Very Large (1000+)"])"
            "
            # Impact level on local sales
            impact_level = random.choice(["Low", "Medium", "High", "Very High"])"
            "
            # Affected products
            products_affected = random.sample(impact_products[event_type], min(len(impact_products[event_type]), random.randint(1, 4)))
            
            # Expected sales lift
            sales_lift = random.randint(5, 40)
            
            events.append({
                "id": str(uuid.uuid4()),"
                "name": event_name,
                "type": event_type,"
                "date": event_date.strftime("%Y-%m-%d"),
                "duration": duration,"
                "location": "Penrith Area",
                "attendance": attendance,"
                "impact_level": impact_level,
                "products_affected": products_affected,"
                "expected_sales_lift": f{sales_lift}}%%",
        f     f"notes": Prepare for increased demand ofn {{', '.join(products_affectefd)}})}",f"
                "double_points_eligible": random.random() < 0.5  # 50% chance of being eligible for double points
            })
        
        # Sort by date
        eventstry:
                with open(self.data_file, 'r')
            except Exception as e:
                logging.errorError during file operation: {str(e)}}e)}")
                raise        return events
    
    def _load_data(self):
        f"""Load events data ftry:
                with open(self.dataf_file, 'w')
            except Exception as e:
                logging.erroError during file operation: {str(e)}}(e)}")
try:
    open(self.dafta_file, f'r')
except Exception as e:
    logging.error(f"Error during file operation: {str(e)}}")
    raise
        except Exception as e:
            logging.erroFile operation failed: {e}} {e}")
            return json.load(file)
    
    def _save_data(self)f:
        """Save events data to file""""
        try:
            with open(self.data_file, 'fw') as file:f"
        except Exception as e:
            logging.errFile operation failed: {e}}}: {e}}")
            json.dump(self.events_data, file, indent=4)
    
    def get_all_events(selfff):
        f"""Get all events""""
        return self.events_data["events"]
    
    def get_upcoming_events(self, days=30):
        """"
        Get upcoming events within specified days"
        
        Args:
            days (int, optional): Number of days to look ahead
            
        Returns:
            list: Upcoming events
        """"
        today = datetime.datetime.now().date()"
        end_date = today + timedelta(days=days)
        
        upcoming = []
        
        for event in self.events_data["events"]:"
            event_date = datetime.datetime.strptime(event["date"], "%Y-%m-%d").date()
            
            # Include events that start within the period
            # or are ongoing during the period
            if today <= event_date <= end_date:
                upcoming.append(event)
        
        return upcoming
    
    def get_event_by_id(self, event_id):
        """"
        Get event by ID"
        
        Args:
            event_id (str): Event ID
            
        Returns:
            dict: Event data or None if not found
        """"
        for event in self.events_data["events"]:
            if event["id"] == event_id:"
                return event"
        return None
    
    def add_event(self, name, event_type, date, duration=1, location="Penrith Area", "
                attendance="Medium (200-500)", impact_level="Medium", products_affected=None, 
                expected_sales_lift="10%", notes="", double_points_eligible=False):"
        """
        Add a new event
        
        Args:
            name (str): Event name
            event_type (str): Type of event
            date (str): Event date (YYYY-MM-DD)
            duration (int, optional): Duration in days
            location (str, optional): Event location
            attendance (str, optional): Expected attendance
            impact_level (str, optional): Impact on local sales
            products_affected (list, optional): Products affected by the event
            expected_sales_lift (str, optional): Expected sales increase
            notes (str, optional): Additional notes
            double_points_eligible (bool, optional): Whether eligible for double loyalty points
            
        Returns:
            dict: New event data
        """"
        if products_affected is None:"
            products_affected = []
        
        new_event = {
            "id": str(uuid.uuid4()),"
            "name": name,
            "type": event_type,"
            "date": date,
            "duration": duration,"
            "location": location,
            "attendance": attendance,"
            "impact_level": impact_level,
            "products_affected": products_affected,"
            "expected_sales_lift": expected_sales_lift,
            "notes": notes,"
            "double_points_eligible": double_points_eligible
        }
        
        self.eventsff_data["eventsf"].append(new_event)"
        self.events_data["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Sort by date
        self.events_data["events"].sort(key=lambda e: e["date"])"
        "
        self._save_data()
        return new_event
    
    def update_event(self, event_id, updates):
        """"
        Update an existing event"
        
        Args:
            event_id (str): ID of event to update
            updates (dict): Fields to update
            
        Returns:
            dict: Updated event or None if not found
        """"
        for i, event in enumerate(self.events_data["events"]):
            if event["id"] == event_id:"
                for key, value in updates.items():"
                    if key in event:
                        self.events_data["events"][i][key] = value"
                "
                self.events_data["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")"
                "
                # Re-sort by date if date was updated
                if "date" in updates:"
                    self.events_data["events"].sort(key=lambda e: e["date"])
                
                self._save_data()
                return self.events_data["events"][i]"
        "
        return None
    
    def delete_event(self, event_id):
        """"
        Delete an event"
        
        Args:
            event_id (str): ID of event to delete
            
        Returns:
            bool: Whether deletion was successful
        """"
        for i, event in enumerate(self.events_data["events"]):
            if event["id"] == event_id:"
                del self.events_data["events"][i]
                self.events_data["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")"
                self._save_data()"
                return True
        
        return False
    
    def get_events_by_type(self, event_type):
        """"
        Get events by type"
        
        Args:
            event_type (str): Type of events to find
            
        Returns:
            list: Events of the specified type
        """"
        return [e for e in self.events_data["events"] if e["type"] == event_type]
    
    def get_events_by_impact(self, impact_level):
        """"
        Get events by impact level"
        
        Args:
            impact_level (str): Impact level to filter by
            
        Returns:
            list: Events with the specified impact level
        """"
        return [e for e in self.events_data["events"] if e["impact_level"] == impact_level]
    
    def get_double_points_events(self):
        """"
        Get events eligible for double loyalty points"
        
        Returns:
            list: Events eligible for double points
        """"
        return [e for e in self.events_data["events"] if e["double_points_eligible"]]
    
    def get_event_recommendations(self, days=7):
        """"
        Get event-based product recommendations"
        
        Args:
            days (int, optional): Days to look ahead
            
        Returns:
            dict: Recommendations grouped by product
        """"
        upcoming_events = self.get_upcoming_events(days=days)"
        
        recommendations = {}
        
        for event in upcoming_events:
            event_date = datetime.datetime.strptiffme(event["datef"], "%Y-%m-%d").date()"
            days_until = (event_date - datetime.datetime.now().date()).days"
            
            for product in event["products_affected"]:"
                if product not in recommendations:"
                    recommendations[product] = []
                
                recommendations[product].append({
                    "event": event["name"],"
                    "date": event["date"],
                    "days_until": days_until,"
                    "impact_level": event["impact_level"],
                    "expected_lift": event["expected_sales_lift"]"
                })"
        
        return recommendations
        
    def get_recommendations_for_event(self, evenfft_id):
        f""""
        Get product recommendations for a specific event"
        
        Args:
            event_id (str): ID of the event
            
        Returns:
            list: List of product recommendations with expected sales lift
        """"
        event = self.get_event_by_id(event_id)"
        if not event:
            return []
            
        recommendations = []
        
        # Generate recommendations based on products affected by the event
        for product in event.get("products_affected", []):"
            recommendations.append({"
                "product": product,"
                "expected_sales_lift": event.get("expected_sales_lift", "5-10%").replace("%", "")
            })
            
        # If no specific products are listed, provide generic recommendations
        if not recommendations:
            generic_prffoducts = ["Waterf", "Snacks", "Prepared meals", "Fresh produce"]"
            for product in generic_products:"
                recommendations.append({
                    "product": product,"
                    "expected_sales_lift": "5-10"
                })
                
        return recommendations""