"""
Waste Management Lite Module
Tracks waste through donations and overstock, and provides suggestions for order adjustments
"""

import datetime
import json
import os
import uuid
import math

class WasteManagement:
    """
    Waste Management Lite system that tracks donation/waste data and provides 
    order adjustment recommendations
    """
    
    def __init__(self, data_file="data/waste_management.json"):
        """Initialize the waste management system with data file path"""
        self.data_file = data_file
        self._ensure_data_file_exists()
        self._load_data()
        
    def _ensure_data_file_exists(self):
        """Ensure the data file exists, create if it doesn't"""
        if not os.path.exists(os.path.dirname(self.data_file)):
            os.makedirs(os.path.dirname(self.data_file))
            
        if not os.path.exists(self.data_file):
            # Create initial data structure
            initial_data = {
                "donation_logs": [],
                "order_adjustments": [],
                "waste_metrics": {
                    "total_donated": 0,
                    "total_wasted": 0,
                    "cost_savings": 0,
                    "donations_by_recipient": {},
                    "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "settings": {
                    "donation_recipients": [
                        "Food Bank",
                        "Local Shelter",
                        "Community Center",
                        "Staff Take-Home",
                        "Other"
                    ],
                    "notification_emails": [],
                    "square_pos_integration": True
                }
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _load_data(self):
        """Load waste management data from file"""
        with open(self.data_file, 'r') as f:
            self.waste_data = json.load(f)
    
    def _save_data(self):
        """Save waste management data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.waste_data, f, indent=2)
            
    def get_donation_recipients(self):
        """
        Get list of donation recipients
        
        Returns:
            list: List of recipient names
        """
        return self.waste_data["settings"]["donation_recipients"]
    
    def add_donation_recipient(self, recipient_name):
        """
        Add new donation recipient
        
        Args:
            recipient_name (str): Name of recipient organization
            
        Returns:
            bool: Success status
        """
        if recipient_name not in self.waste_data["settings"]["donation_recipients"]:
            self.waste_data["settings"]["donation_recipients"].append(recipient_name)
            self._save_data()
            return True
        return False
        
    def log_donation(self, product_name, quantity, recipient, unit_cost=None, reason="Near expiry", notes=""):
        """
        Log a donation of products
        
        Args:
            product_name (str): Name of the product donated
            quantity (int): Number of units donated
            recipient (str): Name of the recipient organization
            unit_cost (float, optional): Cost per unit
            reason (str, optional): Reason for donation/waste
            notes (str, optional): Additional notes
            
        Returns:
            dict: Created donation log
        """
        # Calculate cost if provided
        total_cost = 0
        if unit_cost:
            total_cost = unit_cost * quantity
            
        # Create donation log
        donation = {
            "id": str(uuid.uuid4()),
            "product_name": product_name,
            "quantity": quantity,
            "recipient": recipient,
            "unit_cost": unit_cost,
            "total_cost": total_cost,
            "reason": reason,
            "notes": notes,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "logged_by": "Staff",  # In a real app, this would be the logged-in user
            "synced_to_square": False
        }
        
        # Add to logs
        self.waste_data["donation_logs"].append(donation)
        
        # Update metrics
        self.waste_data["waste_metrics"]["total_donated"] += quantity
        self.waste_data["waste_metrics"]["cost_savings"] += total_cost
        
        # Update donations by recipient
        if recipient not in self.waste_data["waste_metrics"]["donations_by_recipient"]:
            self.waste_data["waste_metrics"]["donations_by_recipient"][recipient] = 0
        self.waste_data["waste_metrics"]["donations_by_recipient"][recipient] += quantity
        
        # Update timestamp
        self.waste_data["waste_metrics"]["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self._save_data()
        
        # Simulate Square POS sync
        self._sync_with_square(donation)
        
        return donation
    
    def log_waste(self, product_name, quantity, unit_cost=None, reason="Expired", notes=""):
        """
        Log product waste
        
        Args:
            product_name (str): Name of the product wasted
            quantity (int): Number of units wasted
            unit_cost (float, optional): Cost per unit
            reason (str, optional): Reason for waste
            notes (str, optional): Additional notes
            
        Returns:
            dict: Created waste log
        """
        # Calculate cost if provided
        total_cost = 0
        if unit_cost:
            total_cost = unit_cost * quantity
            
        # Create waste log
        waste_log = {
            "id": str(uuid.uuid4()),
            "product_name": product_name,
            "quantity": quantity,
            "unit_cost": unit_cost,
            "total_cost": total_cost,
            "reason": reason,
            "notes": notes,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "logged_by": "Staff",  # In a real app, this would be the logged-in user
            "synced_to_square": False
        }
        
        # Add to logs (we reuse the donation logs array but with null recipient)
        waste_log["recipient"] = None
        self.waste_data["donation_logs"].append(waste_log)
        
        # Update metrics
        self.waste_data["waste_metrics"]["total_wasted"] += quantity
        
        # Update timestamp
        self.waste_data["waste_metrics"]["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self._save_data()
        
        # Simulate Square POS sync
        self._sync_with_square(waste_log)
        
        return waste_log
    
    def get_all_logs(self):
        """
        Get all donation and waste logs
        
        Returns:
            list: All donation and waste logs
        """
        return sorted(self.waste_data["donation_logs"], 
                     key=lambda x: datetime.datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"), 
                     reverse=True)
    
    def get_logs_by_product(self, product_name):
        """
        Get logs for a specific product
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            list: Logs for the specified product
        """
        return [log for log in self.waste_data["donation_logs"] if log["product_name"] == product_name]
    
    def get_waste_metrics(self):
        """
        Get waste management metrics
        
        Returns:
            dict: Waste management metrics
        """
        return self.waste_data["waste_metrics"]
    
    def create_order_adjustment(self, product_name, current_order_quantity, suggested_adjustment_percent, reason):
        """
        Create order adjustment recommendation
        
        Args:
            product_name (str): Product name
            current_order_quantity (int): Current order quantity
            suggested_adjustment_percent (float): Suggested adjustment percentage (negative for decrease)
            reason (str): Reason for adjustment
            
        Returns:
            dict: Created order adjustment
        """
        # Calculate suggested new quantity
        new_quantity = current_order_quantity * (1 + (suggested_adjustment_percent / 100))
        new_quantity = math.ceil(new_quantity)  # Round up to nearest whole number
        
        # Create adjustment
        adjustment = {
            "id": str(uuid.uuid4()),
            "product_name": product_name,
            "current_quantity": current_order_quantity,
            "adjustment_percent": suggested_adjustment_percent,
            "suggested_quantity": new_quantity,
            "reason": reason,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending",  # pending, approved, rejected
            "approved_by": None,
            "applied": False
        }
        
        # Add to adjustments
        self.waste_data["order_adjustments"].append(adjustment)
        self._save_data()
        
        return adjustment
    
    def get_order_adjustments(self, status=None):
        """
        Get order adjustment recommendations
        
        Args:
            status (str, optional): Filter by status (pending, approved, rejected)
            
        Returns:
            list: Order adjustments
        """
        adjustments = self.waste_data["order_adjustments"]
        
        if status:
            adjustments = [adj for adj in adjustments if adj["status"] == status]
            
        return sorted(adjustments, 
                     key=lambda x: datetime.datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"), 
                     reverse=True)
    
    def update_adjustment_status(self, adjustment_id, new_status, approved_by=None):
        """
        Update status of order adjustment
        
        Args:
            adjustment_id (str): ID of adjustment to update
            new_status (str): New status (approved, rejected)
            approved_by (str, optional): Name of person who approved/rejected
            
        Returns:
            dict: Updated adjustment or None if not found
        """
        for i, adj in enumerate(self.waste_data["order_adjustments"]):
            if adj["id"] == adjustment_id:
                self.waste_data["order_adjustments"][i]["status"] = new_status
                
                if approved_by:
                    self.waste_data["order_adjustments"][i]["approved_by"] = approved_by
                    
                self._save_data()
                return self.waste_data["order_adjustments"][i]
                
        return None
    
    def mark_adjustment_applied(self, adjustment_id):
        """
        Mark order adjustment as applied
        
        Args:
            adjustment_id (str): ID of adjustment
            
        Returns:
            dict: Updated adjustment or None if not found
        """
        for i, adj in enumerate(self.waste_data["order_adjustments"]):
            if adj["id"] == adjustment_id:
                self.waste_data["order_adjustments"][i]["applied"] = True
                self.waste_data["order_adjustments"][i]["applied_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_data()
                return self.waste_data["order_adjustments"][i]
                
        return None
    
    def analyze_product_waste(self, product_name, days=30):
        """
        Analyze waste data for a product and suggest order adjustments
        
        Args:
            product_name (str): Product name
            days (int, optional): Number of days to analyze
            
        Returns:
            dict: Analysis results and suggestions
        """
        # Get logs for the product within the specified date range
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        
        product_logs = [
            log for log in self.waste_data["donation_logs"] 
            if log["product_name"] == product_name and log["timestamp"][:10] >= cutoff_date
        ]
        
        # Calculate metrics
        total_quantity = sum(log["quantity"] for log in product_logs)
        donated_quantity = sum(log["quantity"] for log in product_logs if log["recipient"])
        wasted_quantity = sum(log["quantity"] for log in product_logs if not log["recipient"])
        
        total_cost = sum(log["total_cost"] for log in product_logs if "total_cost" in log)
        
        # Determine if order adjustment is needed
        needs_adjustment = total_quantity > 0
        suggested_adjustment_percent = 0
        
        if needs_adjustment:
            # Simple algorithm: suggest reducing by roughly the percentage wasted/donated
            # In a real implementation, this would be more sophisticated
            if wasted_quantity > 0:
                # More waste than donations suggests larger reduction
                suggested_adjustment_percent = -10
            elif donated_quantity > 0:
                # More donations suggest smaller reduction
                suggested_adjustment_percent = -5
        
        return {
            "product_name": product_name,
            "days_analyzed": days,
            "total_quantity": total_quantity,
            "donated_quantity": donated_quantity,
            "wasted_quantity": wasted_quantity,
            "total_cost": total_cost,
            "needs_adjustment": needs_adjustment,
            "suggested_adjustment_percent": suggested_adjustment_percent,
            "reason": f"Based on {days} days of waste tracking data"
        }
    
    def get_summary(self):
        """
        Get a summary of waste management data
        
        Returns:
            dict: Summary data
        """
        # Get overall metrics
        metrics = self.waste_data["waste_metrics"]
        
        # Get recent logs (last 7 days)
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        recent_logs = [
            log for log in self.waste_data["donation_logs"] 
            if log["timestamp"][:10] >= cutoff_date
        ]
        
        # Get pending adjustments
        pending_adjustments = self.get_order_adjustments(status="pending")
        
        # Summary stats for recent activity
        recent_donated = sum(log["quantity"] for log in recent_logs if log["recipient"])
        recent_wasted = sum(log["quantity"] for log in recent_logs if not log["recipient"])
        
        # Group by product
        product_summary = {}
        for log in recent_logs:
            product = log["product_name"]
            if product not in product_summary:
                product_summary[product] = {
                    "donated": 0,
                    "wasted": 0,
                    "total": 0
                }
            
            product_summary[product]["total"] += log["quantity"]
            
            if log["recipient"]:
                product_summary[product]["donated"] += log["quantity"]
            else:
                product_summary[product]["wasted"] += log["quantity"]
        
        return {
            "total_donated": metrics["total_donated"],
            "total_wasted": metrics["total_wasted"],
            "cost_savings": metrics["cost_savings"],
            "recent_donated": recent_donated,
            "recent_wasted": recent_wasted,
            "pending_adjustments": len(pending_adjustments),
            "product_summary": product_summary,
            "as_of": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _sync_with_square(self, log_entry):
        """
        Simulate syncing waste/donation data with Square POS
        
        Args:
            log_entry (dict): Log entry to sync
            
        Returns:
            bool: Success status
        """
        # This would make actual API calls to Square in a real implementation
        print(f"Syncing with Square POS: {log_entry['product_name']} x {{log_entry[}"quantity']}")
        
        # Find and update the log entry
        for i, log in enumerate(self.waste_data["donation_logs"]):
            if log["id"] == log_entry["id"]:
                self.waste_data["donation_logs"][i]["synced_to_square"] = True
                self._save_data()
                break
                
        return True