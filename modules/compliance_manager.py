import streamlit as st
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime, timedelta
import time


class ComplianceManager:
    """
    StateSafe Compliance Manager (Feature 11)
    Manages compliance requirements for food businesses across different Australian states/territories
    """
    
    def __init__(self):
        """Initialize the compliance manager"""
        self.data_dir = "data"
        self.rules_file = os.path.join(self.data_dir, "compliance_rules.json")
        self.registration_file = os.path.join(self.data_dir, "compliance_registration.json")
        self.fss_file = os.path.join(self.data_dir, "compliance_fss.json")
        
        # Initialize data files if they don't exist
        self._initialize_data_files()
        
        # Load compliance rules, registration data, and FSS data
        self.rules = self._load_rules()
        self.registration = self._load_registration()
        self.fss_data = self._load_fss_data()
        
    def _initialize_data_files(self):
        """Initialize data files if they don't exist"""
        # Create compliance rules file if it doesn't exist
        if not os.path.exists(self.rules_file):
            rules = {
                "NSW": {
                    "name": "New South Wales",
                    "legislation": ["Food Act 2003", "Food Standards Code", "Standard 3.2.2A"],
                    "fss_required": True,
                    "fss_certification_period_years": 5,
                    "registration_fee": 0,
                    "registration_required": True,
                    "notification_required": True,
                    "notification_api": "NSW Food Authority",
                    "notification_method": "API"
                },
                "VIC": {
                    "name": "Victoria",
                    "legislation": ["Food Act 1984", "Food Standards Code"],
                    "fss_required": True,
                    "fss_certification_period_years": 5,
                    "registration_fee": 300,
                    "registration_required": True,
                    "notification_required": True,
                    "notification_api": "VIC Health",
                    "notification_method": "Manual Payment"
                },
                "QLD": {
                    "name": "Queensland",
                    "legislation": ["Food Act 2006", "Food Standards Code"],
                    "fss_required": True,
                    "fss_certification_period_years": 2,
                    "registration_fee": 150,
                    "registration_required": True,
                    "notification_required": True,
                    "notification_api": "QLD Health",
                    "notification_method": "Email"
                },
                "SA": {
                    "name": "South Australia",
                    "legislation": ["Food Act 2001", "Food Standards Code"],
                    "fss_required": False,
                    "fss_certification_period_years": 0,
                    "registration_fee": 120,
                    "registration_required": True,
                    "notification_required": True,
                    "notification_api": "SA Health",
                    "notification_method": "Email"
                },
                "WA": {
                    "name": "Western Australia",
                    "legislation": ["Food Act 2008", "Food Standards Code"],
                    "fss_required": False,
                    "fss_certification_period_years": 0,
                    "registration_fee": 140,
                    "registration_required": True,
                    "notification_required": True,
                    "notification_api": "WA Health",
                    "notification_method": "Form"
                },
                "TAS": {
                    "name": "Tasmania",
                    "legislation": ["Food Act 2003", "Food Standards Code"],
                    "fss_required": False,
                    "fss_certification_period_years": 0,
                    "registration_fee": 100,
                    "registration_required": True,
                    "notification_required": True,
                    "notification_api": "TAS Health",
                    "notification_method": "Email"
                },
                "NT": {
                    "name": "Northern Territory",
                    "legislation": ["Food Act 2004", "Food Standards Code"],
                    "fss_required": False,
                    "fss_certification_period_years": 0,
                    "registration_fee": 90,
                    "registration_required": True,
                    "notification_required": True,
                    "notification_api": "NT Health",
                    "notification_method": "Email"
                },
                "ACT": {
                    "name": "Australian Capital Territory",
                    "legislation": ["Food Act 2001", "Food Standards Code"],
                    "fss_required": False,
                    "fss_certification_period_years": 0,
                    "registration_fee": 110,
                    "registration_required": True,
                    "notification_required": True,
                    "notification_api": "ACT Health",
                    "notification_method": "Online Form"
                }
            }
            
            with open(self.rules_file, 'w') as f:
                json.dump(rules, f, indent=2)
        
        # Create registration data file if it doesn't exist
        if not os.path.exists(self.registration_file):
            registration_data = {
                "registered": False,
                "state": "",
                "business_name": "",
                "business_address": "",
                "business_phone": "",
                "registration_date": "",
                "registration_expiry": "",
                "confirmation_code": "",
                "registration_status": "Not Registered",
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.registration_file, 'w') as f:
                json.dump(registration_data, f, indent=2)
        
        # Create FSS data file if it doesn't exist
        if not os.path.exists(self.fss_file):
            fss_data = {
                "assigned": False,
                "fss_name": "",
                "fss_certification_date": "",
                "fss_expiry_date": "",
                "fss_certificate_number": "",
                "compliant": False,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.fss_file, 'w') as f:
                json.dump(fss_data, f, indent=2)
    
    def _load_rules(self):
        """Load compliance rules from file"""
        with open(self.rules_file, 'r') as f:
            return json.load(f)
    
    def _load_registration(self):
        """Load registration data from file"""
        with open(self.registration_file, 'r') as f:
            return json.load(f)
    
    def _load_fss_data(self):
        """Load FSS data from file"""
        with open(self.fss_file, 'r') as f:
            return json.load(f)
    
    def _save_registration(self):
        """Save registration data to file"""
        # Update last updated timestamp
        self.registration["last_updated"] = datetime.now().isoformat()
        
        with open(self.registration_file, 'w') as f:
            json.dump(self.registration, f, indent=2)
    
    def _save_fss_data(self):
        """Save FSS data to file"""
        # Update last updated timestamp
        self.fss_data["last_updated"] = datetime.now().isoformat()
        
        with open(self.fss_file, 'w') as f:
            json.dump(self.fss_data, f, indent=2)
    
    def get_states_list(self):
        """Get list of Australian states/territories"""
        return list(self.rules.keys())
    
    def get_state_rules(self, state_code):
        """Get compliance rules for a specific state"""
        if state_code in self.rules:
            return self.rules[state_code]
        return None
    
    def register_business(self, state, business_name, business_address, business_phone):
        """Register business with local council"""
        if state not in self.rules:
            return {
                "success": False,
                "message": f"Invalid state code: {state}"
            }
        
        # Simulate API call to register business with local council
        # In production, this would be a real API call
        time.sleep(1)  # Simulate API call delay
        
        state_rules = self.rules[state]
        fee = state_rules["registration_fee"]
        
        # Update registration data
        self.registration["registered"] = True
        self.registration["state"] = state
        self.registration["business_name"] = business_name
        self.registration["business_address"] = business_address
        self.registration["business_phone"] = business_phone
        self.registration["registration_date"] = datetime.now().isoformat()
        
        # Set registration expiry date (1 year from now)
        expiry_date = datetime.now() + timedelta(days=365)
        self.registration["registration_expiry"] = expiry_date.isoformat()
        
        # Generate fake confirmation code
        confirmation_code = f"{state}-{int(time.time())}"
        self.registration["confirmation_code"] = confirmation_code
        
        # Set registration status based on fee
        if fee > 0:
            self.registration["registration_status"] = "Pending Payment"
        else:
            self.registration["registration_status"] = "Registered"
        
        # Save registration data
        self._save_registration()
        
        # Return registration result
        return {
            "success": True,
            "message": "Business registered successfully" if fee == 0 else f"Registration pending payment of ${fee}",
            "confirmation_code": confirmation_code,
            "fee": fee,
            "expiry_date": expiry_date.isoformat()
        }
    
    def complete_payment(self):
        """Complete registration payment"""
        if not self.registration["registered"]:
            return {
                "success": False,
                "message": "Business not registered yet"
            }
        
        if self.registration["registration_status"] != "Pending Payment":
            return {
                "success": False,
                "message": "No payment pending"
            }
        
        # Update registration status
        self.registration["registration_status"] = "Registered"
        
        # Save registration data
        self._save_registration()
        
        # Return payment result
        return {
            "success": True,
            "message": "Payment completed successfully",
            "confirmation_code": self.registration["confirmation_code"]
        }
    
    def get_staff_list(self):
        """Get list of staff for FSS assignment (simulate integration with Feature 8)"""
        # In production, this would be a real API call to Feature 8
        # For demonstration, return dummy data
        return [
            {
                "id": "staff-001",
                "name": "Jane Doe",
                "position": "Manager",
                "fss_certified": True,
                "fss_expiry": (datetime.now() + timedelta(days=365*3)).isoformat(),
                "fss_certificate": "FSS-001-NSW"
            },
            {
                "id": "staff-002",
                "name": "John Smith",
                "position": "Assistant Manager",
                "fss_certified": True,
                "fss_expiry": (datetime.now() + timedelta(days=180)).isoformat(),
                "fss_certificate": "FSS-002-NSW"
            },
            {
                "id": "staff-003",
                "name": "Alex Johnson",
                "position": "Supervisor",
                "fss_certified": False,
                "fss_expiry": None,
                "fss_certificate": None
            }
        ]
    
    def assign_fss(self, staff_id, staff_name, fss_certificate, fss_expiry):
        """Assign Food Safety Supervisor"""
        # Update FSS data
        self.fss_data["assigned"] = True
        self.fss_data["fss_name"] = staff_name
        self.fss_data["fss_certification_date"] = datetime.now().isoformat()
        self.fss_data["fss_expiry_date"] = fss_expiry
        self.fss_data["fss_certificate_number"] = fss_certificate
        self.fss_data["compliant"] = True
        
        # Save FSS data
        self._save_fss_data()
        
        # Return assignment result
        return {
            "success": True,
            "message": f"{staff_name} assigned as Food Safety Supervisor",
            "expiry_date": fss_expiry
        }
    
    def get_compliance_status(self):
        """Get overall compliance status"""
        status = {
            "registration_compliant": False,
            "fss_compliant": False,
            "overall_compliant": False,
            "alerts": [],
            "state": self.registration["state"],
            "business_name": self.registration["business_name"]
        }
        
        # Check registration compliance
        if self.registration["registered"] and self.registration["registration_status"] == "Registered":
            status["registration_compliant"] = True
        else:
            status["alerts"].append("Business not registered with local council")
        
        # Check FSS compliance
        if self.registration["state"] in self.rules:
            state_rules = self.rules[self.registration["state"]]
            
            # Check if FSS is required for this state
            if state_rules["fss_required"]:
                if self.fss_data["assigned"] and self.fss_data["compliant"]:
                    # Check if FSS certification is still valid
                    fss_expiry = datetime.fromisoformat(self.fss_data["fss_expiry_date"])
                    if fss_expiry > datetime.now():
                        status["fss_compliant"] = True
                    else:
                        status["alerts"].append("FSS certification expired")
                else:
                    status["alerts"].append("Food Safety Supervisor not assigned")
            else:
                # FSS not required in this state
                status["fss_compliant"] = True
        
        # Determine overall compliance
        status["overall_compliant"] = status["registration_compliant"] and status["fss_compliant"]
        
        return status