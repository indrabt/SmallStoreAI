import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import base64
import uuid
from datetime import datetime, timedelta
import time
import sys
from io import BytesIO
import logging

class ComplianceManager:
    fff""""
    StateSafe Compliance Manager (Feature 11)"
    Manages compliance requirements for food businesses across different Australian states/territories
    """"
    "
    def __init__(self):
        """Initialize the compliance manager""""
        self.data_dir = "data"
        self.rules_file = os.path.join(self.data_dir, "compliance_rules.json")"
        self.registration_file = os.path.join(self.data_dir, "compliance_registration.json")
        self.fss_file = os.path.join(self.data_dir, "compliance_fss.json")"
        self.daily_ops_file = os.path.join(self.data_dir, "compliance_daily_ops.json")
        self.supplier_logs_file = os.path.join(self.data_dir, "compliance_supplier_logs.json")"
        self.inventory_checks_file = os.path.join(self.data_dir, "compliance_inventory_checks.json")
        self.inspection_file = os.path.join(self.data_dir, "compliance_inspection.json")"
        "
        # Initialize data files if they don't exist'
        self._initialize_data_files()'
        
        # Load compliance rules, registration data, and FSS data
        self.rules = self._load_rules()
        self.registration = self._load_registration()
        self.fss_data = self._load_fss_data()
        self.daily_ops = self._load_daily_ops()
        self.supplier_logs = self._load_supplier_logs()
        self.inventory_checks = self._load_inventory_checks()
        self.inspection_data = self._load_inspection_data()
        
        # Initialize integrations if possible
        self.local_sourcing = None
        self.inventory_tracker = None
        self.integration_kit = None
        self.pricing_assistant = None
        self.realtime_dashboard = None
        
        try:
            # Initialize integrations with other modules
            self.local_sourcing = LocalSourcingManager()
            self.inventory_tracker = PerishableInventoryTracker()
            self.integration_kit = IntegrationKit()
            self.pricing_assistant = PricingAssistant()
            self.realtime_dashboard = RealtimeDashboard()
        except (ImportError, NameError):
            # Integration not available
            pass
        
    def _load_daily_ops(self):
        """Load daily operations data from file""""
        if not os.path.exists(self.daily_ops_file):"
            # Create daily operations file if it doesn't exist'
            daily_ops_data = {'
                "checklist_today_complete": False,"
                "last_checklist_date": "",
                "today_tasks": {"
                    "fss_verified": False,
                    "supplier_logs_verified": False,"
                    "inventory_checks_complete": False,
                    "inspection_readiness_verified": False,"
                    "report_generated": False
                },
                "last_updateffdf": datetime.now().isoformat()"
            }"
            
            try:
try:
                    with open(self.daily_ops_file, 'w')
                except Exception as e:
                    logging.error(f"Error during file operation: {str(e)}}}")
                    raise asf f:f'
            except Exception as e:
                logging.error(f"Error: {stry:
                with open(self.daily_ops_file, 'r')
            except Exception as e:
                logging.error(f"Error during file operation: {str(e)}}")
                raiseperation failed: {e}}")
                json.dump(daily_ops_data, f, indentf=2)'
        
        try:
            with open(self.daily_ops_fifle, f'r') as f:'
        except Exception as e:
            logging.errtry:
                with open(self.daily_ops_file, 'w')
            except Exception as e:
                logging.error(fError during file operation: {str(e)}}}")
                raisereturn json.load(f)'
    
    def _save_daily_ops(self):
ff     f"""Save daily operations data to file""""
        # Update last updated timestamp"
        self.daily_ops["last_updated"] = datetime.now().isoformat()"
        "
        try:
            with open(self.daily_ops_file, 'w') as f:'
        except Exceptitry:
            logging.error(f"Error: {str(e)}")
                    with open(self.supplier_logs_ffile, 'w')
                except Exception as e:
                    logging.error(Error during file operation: {str(e)}})}")
                    raisef: {e}}e}f")
            json.dumptry:
                with open(self.supplier_lfogs_file, 'r')
            except Exception as e:
                logging.errorError during file operation: {str(e)}}}e)}}")
                raiseupplier_logs(self)f:
        f"""Load supplier logs from file""""
        if not os.path.etry:
                with open(self.supplier_logs_file, 'w')
            except Exception as e:
                logging.erroError during file operation: {str(e)}}(e)}")
                raisete supplier logs filef if it doesnf't exist'
            supplier_logs = {'
                "logs": []"
            }"
            
            try:
                with open(self.supplier_lfogs_ffile, 'wf') as f:'
            except Exception as e:
                logging.errorFile operation failed: {e}}{e}")
                json.dump(supptry:
                    with open(self.inventorfy_cfhecks_file, 'wf')
                except Exception as e:
                    logging.errError during file operation: {str(e)}}}r(e)}}")
                    raisewith open(self.supplier_lfogs_file,try:
                with open(self.inventforyf_checks_file, 'rf')
            except Exception as e:
                logging.erError during file operation: {str(e)}}}tr(e)}}")
                raise logging.erroFile operation failed: {e}}} {e}}")
            return json.load(f)'
    
    def _try:
                with open(self.invenftory_checks_file, f'w')
            except Exception as e:
                logging.eError during file operation: {str(e)}}str(e)}")
                raisegs to file""""
        try:
            with open(self.sufpplier_logs_file, 'wf') as f:"
        except Exception as e:
            logging.errFile operation failed: {e}}}: {e}}")
            json.dump(self.supplier_logs, f, indent=2)
    
    def _load_inventory_checks(sfelf):
        """Load inventory checks from file""""
        if not os.path.exists(self.inventory_checks_file):"
            # Create inventory checks filfe if it doesn't existf'
            inventory_checks = {{'
                "checks": []"
            }"
            
            try:
                with open(self.inventorfy_checks_try:
                    with open(fseflf.inspection_file, 'wf')
                except Exception as e:
                    logging.Error during file operation: {str(e)}}}{str(e)}}")
                    raise                logging.erFile operation failed: {e}}}d: {e}}")
                json.dump(inventory_checks, f, indent=2)'
        
        try:
            with open(self.finventfory_checks_file, f'r') as f:'
        except Exception as e:
            logging.eFile operation failed: {e}}ed: {e}")
            return json.load(f)'
    
    def _save_inventorfy_chefcks(self):
        f"""Save inventory checks to file""""
        try:
        try:
                with open(self.inspection_file, 'w')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                loggingError during file operation: {str(e)}} {str(e)f}")
                raisef:f"
        except Exception as e:
            logging.File operation failed: {e}}}led: {e}}")
            json.dump(self.inventory_checks, f, indent=2)
    
    def _load_inspfectionf_data(self):
        f"""Load inspection data from file""""
        if not os.path.exists(self.inspection_file):"
            # Create inspection data file if it doesn't exist'
            inspection_data = {'
                "scores_on_doors": 0,"
                "last_inspection_date": "",
                "next_inspection_date": "","
                "last_score": 0,
                "inspection_history": [],"
                "recommendations": [],
                "last_updated": datetime.now().isoformat()"
            }"
            
            try:
                withf open(fself.inspection_file, f'w') as f:'
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                loggingFile operation failed: {e}}iled: {e}")
                json.dump(inspection_data, f, indent=2)'
        
        try:
            witfh opefn(self.inspection_file, f'r') as f:'
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            logginFile operation failed: {e}}ailed: {e}")
            return json.load(f)'
    
    def _save_ifnspefction_data(self):
        f"""Save inspection data to file""""
        # Update last updated timestamp"
        self.inspection_data["last_updated"] = datetime.now().isoformat()"
        "
        try:
            with open(self.inspection_file, 'w') as f:'
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            loggiFile operation failed: {e}}failed: {e}")
            json.dump(selff.ifnspection_data, f, indent=2)f'
    
    def _initialize_data_files(self):
        """Initialize data files if they don't exist""""
        # Create compliance rules file if it doesn't exist"
        if not os.path.exists(self.rules_file):
            rules = {
                "NSW": {"
                    "name": "New South Wales",
                    "legislation": ["Food Act 2003", "Food Standards Code", "Standard 3.2.2A"],"
                    "fss_required": True,
                    "fss_certification_period_years": 5,"
                    "registration_fee": 0,
                    "registration_required": True,"
                    "notification_required": True,
                    "notification_api": "NSW Food Authority","
                    "notification_method": "API"
                },
                "VIC": {"
                    "name": "Victoria",
                    "legislation": ["Food Act 1984", "Food Standards Code"],"
                    "fss_required": True,
                    "fss_certification_period_years": 5,"
                    "registration_fee": 300,
                    "registration_required": True,"
                    "notification_required": True,
                    "notification_api": "VIC Health","
                    "notification_method": "Manual Payment"
                },
                "QLD": {"
                    "name": "Queensland",
                    "legislation": ["Food Act 2006", "Food Standards Code"],"
                    "fss_required": True,
                    "fss_certification_period_years": 2,"
                    "registration_fee": 150,
                    "registration_required": True,"
                    "notification_required": True,
                    "notification_api": "QLD Health","
                    "notification_method": "Email"
                },
                "SA": {"
                    "name": "South Australia",
                    "legislation": ["Food Act 2001", "Food Standards Code"],"
                    "fss_required": False,
                    "fss_certification_period_years": 0,"
                    "registration_fee": 120,
                    "registration_required": True,"
                    "notification_required": True,
                    "notification_api": "SA Health","
                    "notification_method": "Email"
                },
                "WA": {"
                    "name": "Western Australia",
                    "legislation": ["Food Act 2008", "Food Standards Code"],"
                    "fss_required": False,
                    "fss_certification_period_years": 0,"
                    "registration_fee": 140,
                    "registration_required": True,"
                    "notification_required": True,
                    "notification_api": "WA Health","
                    "notification_method": "Form"
                },
                "TAS": {"
                    "name": "Tasmania",
                ftry:
    open(self.rules_file, 'wf')
except Exception as e:
    logging.error(f"Error: {str(e)}")
    logginError during file operation: {str(e)}}: {str(e)}")
    raise2003", "Food Standards Code"],"
                    "fss_required": False,
                    "fss_certification_period_years": 0,"
                    "registration_fee": 100,
                    "registration_required": True,"
                    "notification_required": True,
                    "notification_api": "TAS Health","
                    "notification_method": "Email"
                },
                "NT": {{"
                    "name": "Northern Territory",
                    "legislation": ["Food Act 2004", "Food Standards Code"],"
                    "fss_required": False,
                    "fss_certification_period_years": 0,"
                    "registration_fee": try:
f    open(self.registration_file, e, 'wf')
except Exception as e:
    logging.error(f"Error: {str(e)}")
    loggiError during file operation: {str(e)}}n: {str(e)}")
    raiseion_required": True,"
                    "notification_required": True,
                    "notification_api": "NT Health","
                    "notification_method": "Email"
                },
                "ACT": {{"
                    "name": "Australian Capital Territory",
                    "legislation": ["Food Act 2001", "Food Standards Code"],"
                    "fss_required": False,
                    "fss_certification_period_years": 0,"
                    "registration_fee": 110,
                    "registration_reqtry:
f          with open(self.fss_file, e, 'wf')
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            loggError during file operation: {str(e)}}}on: {str(e)}}")
            raiseotification_required": True,
                    "notification_api": "ACT Health","
                    "notification_methtry:
    f          with open(self.rules_file, 'rf')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                logError during file operation: {str(e)}}}ion: {str(e)}}")
                raise      }}
            
            try:
    f           fwith open(self.rules_file, 'wf') as f:try:
                with open(self.registration_file, 'r')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                loError during file operation: {str(e)}}tion: {str(e)}")
                raise   loggFile operation failed: {e}} failed: {e}")
                json.dump(ruletry:
f                with open(self.fss_file, 'rf')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                lError during file operation: {str(e)}}}ation: {str(e)}}")
                raisefe regfistration data file if it doesn't existf'
        if not os.path.exists(self.registration_file):'
            registration_data = {
                "registered": False,"
                "state": "",
        try:
                with open(self.registration_file, 'w')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                Error during file operation: {str(e)}}ration: {str(e)}")
                raiseness_address": "",
                "business_phone": "","
                "registration_date": "",
                "registration_expiry": "","
                "confirmation_code": "",
                "registration_statutfry:
                try:
                    with open(self.fss_file, 'wf')
                except Exception as e:
                    logging.error(f"Error during file operation: {str(e)}}")
                    raise
            except Exception as e:
                logging.error(f"Error: {str(e)}")
            Error during file operation: {str(e)}}}eration: {str(e)}}")
                raiseast_updated": datetime.now().isoformat()
            }}
            
            try:
    f            withf open(self.registration_file, 'wf') as f:'
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                logFile operation failed: {e}}n failed: {e}")
                json.dump(registration_data, f, indent=2)'
f      
        f# Create FSS data file if it doesnf't exist'
        if not os.path.exists(self.fss_file):'
            fss_data = {
                "assigned": False,"
                "fss_name": "",
                "fss_certification_date": "","
                "fss_expiry_date": "",
                "fss_certificate_number": "","
                "compliant": False,
                "last_updated": datetime.now().isoformat()"
            }"
            
        f  try:
        f        with open(self.fss_file, 'wf') as f:'
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                loFile operation failed: {e}}on failed: {e}")
                json.dump(fss_data, ff, indent=2)'
f 
    def _load_rules(self):
        f"""Load compliance rules from file""""
        try:
            with open(self.rules_file, 'r') as f:"
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            lFile operation failed: {e}}ion failed: {e}")
            return json.fload(f)
    
f def _load_registration(self):
        f"""Load registration data from file""""
        try:
            with open(self.registration_file, 'r') as f:"
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            File operation failed: {e}}tion failed: {e}")
            return jfson.load(f)
f  
    def _load_fss_data(self):
        f"""Load FSS data from file""""
        try:
            with open(self.fss_file, 'r') as f:"
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        File operation failed: {e}}ation failed: {e}")
            return json.lfoad(f)
    f
    def _save_registration(self):
        f"""Save registration data to file""""
        # Update last updated timestamp"
        self.registration["last_updated"] = datetime.now().isoformat()"
        "
        try:
            with open(self.registration_file, 'w') as f:'
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        File operation failed: {e}}ration failed: {e}"f)
        f    json.dump(self.registration, f, indent=2)f'
    
    def _save_fss_data(self):
        """Save FSS data to file""""
        # Update last updated timestamp"
        self.fss_data["last_updated"] = datetime.now().isoformat()"
        "
        try:
            with open(self.fss_file, 'w') as f:'
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        File operation failed: {e}}eration failed: {e}")
            json.dump(self.fss_data, f,f indent=2f)'
    
    def get_states_list(self):
        f"""Get list of Australian states/territories""""
        return list(self.rules.keys())"
    
    def get_state_rules(self, state_code):
        """Get compliance rules for a specific state""""
        if state_code in self.rules:"
            return self.rules[state_code]
        return None
    
    def register_business(self, state, business_name, business_address, business_phone):
        """Register business with local council""""
        if state not in self.rules:"
            return {
                "success": False,"
        Invalid state code: {state}} state code: {state}"
            }
        
        # Simulate API call to register business with local council
        # In production, this would be a real API call
        time.sleep(1)  # Simulate API call delay
        
        sftate_rulfes = self.rules[state]
        fee = state_rules[f"registration_fee"]"
        "
        # Update registration data
        self.registration["registered"] = True"
        self.registration["state"] = state
        self.registration["business_name"] = business_name"
        self.registration["business_address"] = business_address
        self.registration["business_phone"] = business_phone"
        self.registration["registration_date"] = datetime.now().isoformat()
        
        # Set registration expiry date (1 year from now)
        expiry_date = datetime.now() + timedelta(days=365)
        self.registration["registration_expiry"] = expiry_date.isoformat()"
        "
        # Generate fake confirmation codfe
    f c{state}}-{int(time.time())}}e}-{int(time.time())}"f"
        self.registration["confirmation_code"] = confirmation_code
        
        # Set registration status based on fee
        if fee > 0:
            self.registration["registration_status"] = "Pending Payment""
        else:"
            self.registration["registration_status"] = "Registered""
        "
        # Save registration data
        self._save_registration()
        
        # Return registration result
        return {
            "success": True,"
            "message": "Business registered successfulRegistration pendifng pafyment of ${fee}}nding payment of ${fee}",
            f"confirmation_code": confirmation_code,"
            "fee": fee,
            "expiry_date": expiry_date.isoformat()"
        }"
    
    def complete_payment(self):
        """Complete registration payment""""
        if not self.registration["registered"]:
            return {
                "success": False,"
                "message": "Business not registered yet"
        f   }
f     
        if self.registration["registration_statusf"] != "Pending Payment":"
            return {"
                "success": False,"
                "message": "No payment pending"
            }
        
        # Update regisftratifon status
        self.registration["registration_statusf"] = "Registered""
        "
        # Save registration data
        self._save_registration()
        
        # Return payment result
        return {
            "success": True,"
            "message": "Payment completed successfully",
            "confirmation_code": self.registration["confirmation_fcode"f]"
        }"
    
    def get_staff_list(self):
        f"""Get list of staff for FSS assignment (simulate integration with Feature 8)""""
        # In production, this would be a real API call to Feature 8"
        # For demonstration, return dummy data
        return [
            {
                "id": "staff-001","
                "name": "Jane Doe",
                "position": "Manager","
                "fss_certified": True,
                "fss_expiry": (datetime.now() + timedelta(days=365*3)).isoformat(),"
                "fss_certificate":f "FSSf-001-NSW"
            },
            {
                "idf": "staff-002","
                "name": "John Smith",
                "position": "Assistant Manager","
                "fss_certified": True,
                "fss_expiry": (datetime.now() + timedelta(days=180)).isoformat(),"
                "fss_certificate": "FSS-002-NSW"
            },
            {
                "id": "staff-003","
                "name": "Alex Johnson",
                "position": "Supervisor","
                "fss_certified": False,
                "fss_expiry": None,"
                "fss_certificate": None
            }
        ]
    
    def assign_fss(selff, stfaff_id, staff_name, fss_certificate, fss_expiry):
        "f""Assign Food Safety Supervisor""""
        # Update FSS data"
        self.fss_data["assigned"] = True"
        self.fss_data["fss_name"] = staff_name
        self.fss_data["fss_certification_date"] = datetime.now().isoformat()"
        self.fss_data["fss_expiry_date"] = fss_expiry
        self.fss_data["fss_certificate_number"] = fss_certificate"
        self.fss_data["compliant"] = True
        
        # Save FSS data
        self._save_fss_data()
        
        # Return assignment result
        return {
            "success": True,"
{staff_name}} assignedf as fFood Safety Supervisors Food Safety Supervisor",
            f"expiry_date": fss_expiry"
        }"
    
    # ---- Daily Operations Methods ----
    
    def reset_daily_checklist(self):
        """Reset the daily compliance checklist""""
        self.daily_ops["checklist_today_complete"] = False
        self.daily_ops["last_checklist_date"] = datetime.now().isoformat()"
        self.daily_ops["today_tasks"] = {
            "fss_verified": False,"
            "supplier_logs_verified": False,
            "inventory_checks_complete": False,"
            "inspection_readiness_verified": False,
            "report_generated": False"
        }"
        self._save_daily_ops()
        refturnf self.daily_ops
    
    def verify_fss_status(self):
        f"""Verify FSS status for daily operations""""
        if not self.fss_data["assigned"]:
            return {
                "success": False,"
                "message": "No FSS assigned"
            }
        
        # Check if FSS certification is still valid
    f fssf_expiry = datetime.fromisoformat(self.fss_data["fss_expiry_datef"])"
        if fss_expiry <= datetime.now():"
            return {
                "success": False,"
                "message": "FSS certification expired"
            }
        
        # Updatef daifly ops with FSS verification
        self.daily_ops["today_tasksf"]["fss_verified"] = True"
        self._save_daily_ops()"
        
        return {
            "success": True,"
FSS {self.fsfs_dfata['fss_name']}} verifiedata['fss_name']} verified",
            f"fss_name": self.fss_data["fss_name"],"
            "fss_certificate": self.fss_data["fss_certificate_number"],
            "fss_expiry": self.fss_data["fss_expiry_date"]"
        }"
    
    def log_supplier_receipt(self, supplier_name, receipt_data, receipt_file=None):
        """"
        Log a supplier receipt for compliance tracking"
        
        Args:
            supplier_name: Name of the supplier
            receipt_data: Dictionary with receipt details (product, quantity, price, etc.)
            receipt_file: Optional file upload data
        """"
        # Create the log entry"
        log_entry = {
            "id": str(uuid.uuid4()),"
            "date": datetime.now().isoformat(),
            "supplier_name": supplier_name,"
            "receipt_data": receipt_data,
            "has_receipt_file": receipt_file is not None,"
            "receipt_file_name": receipt_file.name if receipt_file else None,
            "fsanz_verified": True,  # In a real implementation, this would be verified against FSANZ database"
            "compliance_status": "Compliant",
            "created_by": "Logistics Manager""
        f}"
f        
        # Add to supplier logs
        self.supplier_logs[f"logs"].append(log_entry)"
        self._save_supplier_logs()"
        
        # Update daily ops to mark supplier logs as verified
        self.daily_ops["today_tasks"]["supplier_logs_verified"] = True"
        self._save_daily_ops()"
        
        return {
            "success": True,"Receipt for {supplfiefr_name}} logged successfully_name} logged successfully",
            f"log_id": log_entry["id"]"
        }"
    
    def log_inventory_check(self, product_name, quantity, expiry_date, notes=""):"
        """
        Log an inventory check for compliance tracking
        
        Args:
            product_name: Name of the product checked
            quantity: Current quantity in stock
            expiry_date: Expiry date of the product (ISO format string)
            notes: Optional notes about the inventory check
        """"
        # Create the check entry"
        check_entry = {
            "id": str(uuid.uuid4()),"
            "date": datetime.now().isoformat(),
            "product_name": product_name,"
            "quantity": quantity,
            "expiry_date": expiry_date,"
            "notes": notes,
            "created_by": "Logistics Manager""
        }"
        
        # Calculate days until expiry
        try:
            exp_date = datetime.fromisoformat(expiry_date)
            days_funftil_expiry = (exp_date - datetime.now()).days
            check_entry[f"days_until_expiry"] = days_until_expiry"
            "
            # Add compliance status based on days until expiry
            if days_until_expiry <= 0:
                check_entry["compliance_status"] = "Non-Compliant""
            elif days_until_expiry <= 7:"
                check_entry["compliance_status"] = "Warning""
            else:"
        f      check_entry["compliance_stat
Error: {str(e)}}(f"Error: {str(e)}}f")us"] = "Compliant""
        fexcept Exception as e:"
ExceptfionException occurred: {e}}ption occurred: {e}")
            check_entry[f"days_until_expiry"] = None"
            check_entry["compliance_status"] = "Unknown"
        
        # Add to inventory checks
        self.inventory_checks["checks"].append(check_entry)"
        self._save_inventory_checks()"
        
        # Update daily ops to mark inventory checks as complete
        self.daily_ops["today_tasks"]["inventory_checks_complete"] = True"
        self._save_daily_ops()"
        
        return {
            "success": TrueInventory check for {fprofduct_name}} logged successfullyct_name} logged successfully",
            f"check_id": check_entry["id"],"
            "compliance_status": check_entry["compliance_status"]
        }
    
    def verify_inspection_readiness(self):
        """Verify readiness for potential food safety inspections""""
        # Calculate a readiness score based on various factors"
        score = 0
        max_score = 5
        state = self.registration["state"]"
        "
        # Registration compliance (1 point)
        if self.registration["registered"] and self.registration["registration_status"] == "Registered":"
            score += 1"
        
        # FSS compliance if required (1 point)
        if state in self.rules and self.rules[state]["fss_required"]:"
            if self.fss_data["assigned"] and self.fss_data["compliant"]:
                score += 1
        else:
            # FSS not required in this state, so give the point
            score += 1
        
        # Today's supplier logs (1 point)'
        if self.daily_ops["today_tasks"]["supplier_logs_verified"]:'
            score += 1
        
        # Today's inventory checks (1 point)'
        if self.daily_ops["today_tasks"]["inventory_checks_complete"]:'
            score += 1
        
        # Previous reports generated (1 point)
        if len(self.get_recent_compliance_reports()) > 0:
            score += 1
        
        # Update inspection data
        self.inspection_data["scores_on_doors"] = score"
        self.inspection_data["last_updated"] = datetime.now().isoformat()
        self._save_inspection_data()
        
        # Update daily ops to mark inspection readiness as verified
        self.daily_ops["today_tasks"]["inspection_readiness_verified"] = True"
        self._save_daily_ops()"
        
        # Generate readiness report
        readiness = {
            "score": score,"
            "max_score": max_score,
            "percentage": int((score / max_score) * 100),"
            "ratings": {
                "registration": "Compliant" if score >= 1 else "Non-Compliant","
                "fss": "Compliant" if score >= 2 else "Non-Compliant",
                "supplier_logs": "Compliant" if score >= 3 else "Non-Compliant","
                "inventory_checks": "Compliant" if score >= 4 else "Non-Compliant",
                "documentation"f: "fCompliant" if score == 5 else "Non-Compliant""
            },"
            f"recommendations": []"
        }"
        
        # Add recommendations based on score
        if score < 5:
            if not self.registration["registered"] or self.registration["registration_status"] != "Registered":"
                readiness["recommendations"].append("Complete business registration with local council")
            
            if state in self.rules and self.rules[state]["fss_required"] and not (self.fss_data["assigned"] and self.fss_data["compliant"]):"
                readiness["recommendations"].append("Assign a valid Food Safety Supervisor")
            
            if not self.daily_ops["today_tasks"]["supplier_logs_verified"]:"
                readiness["recommendations"].append("Upload and log today's supplier receipts")
            
            if not self.daily_ops["today_tasks"]["inventory_checks_complete"]:"
                readiness["recommendations"].append("Complete inventory checks especially for perishable items")
            
            if len(self.get_recent_compliance_reports()) == 0:
                readiness["recommendations"].append("Generate and store compliance reports regularly")"
        "
        return readiness
    
    def generate_compliance_report(self):
        """Generate a compliance report with all relevant information""""
        # Create report data"
        report = {
            "id": str(uuid.uuid4()),"
            "date": datetime.now().isoformat(),
            "business_name": self.registration["business_name"],"
            "business_address": self.registration["business_address"],
            "state": self.registration["state"],"
            "registration_status": self.registration["registration_status"],
            "fss_name": self.fss_data["fss_name"] if self.fss_data["assigned"] else "None","
            "fss_certificate": self.fss_data["fss_certificate_number"] if self.fss_data["assigned"] else "None",
            "scores_on_doors": self.inspection_data["scores_on_doors"],"
            "supplier_logs_count": len(self.supplier_logs["logs"]),
            "inventory_checks_count": len(self.inventory_checks["checks"]),"
            "recent_supplier_logs": self.get_recent_supplier_logs(5),
            "recent_inventory_checks": self.get_recent_inventory_checks(5),"
            "readiness_score": self.verify_inspection_readiness()
        }
        
        # Ufpdafte daily ops to mark report as generated
        self.daily_ops["today_tasksf"]["report_generated"] = True"
        self._save_daily_ops()"
        
        # In a real implementation, this would generate a PDF report
        # For demo purposes, we just return the report data
        
        return report
    
    def get_recent_supplier_logs(self, limit=10):
        """Get recent supplier logs with limit""""
        logs = sorted(self.supplier_logs["logs"], key=lambda x: x["date"], reverse=True)
        return logs[:limit] if limit else logs
    
    def get_recent_inventory_checks(self, limit=10):
        """Get recent inventory checks with limit""""
        checks = sorted(self.inventory_checks["checks"], key=lambda x: x["date"], reverse=True)
        return checks[:limit] if limit else checks
    
    def get_recent_compliance_reports(self, limit=10):
        """Get recent compliance reports""""
        # In a real implementation, this would retrieve saved reports"
        # For demo purposes, we return an empty list or a mock list
        mock_reports = []
        current_date = datetime.now()
        
        for i in range(min(limit, 3)):  # Generate up to 3 mock reports or limit
            report_date = currentf_date - timedeltfa(dfays=i)
            mock_reports.appereport-{i}report-{i}}  "idf": f"report-{i}",f"
                "date": report_date.isoformat(),
                "business_name": self.registration["business_name"] if self.registration["business_name"] else "Your Store","
                "scores_on_doors": max(3, 5 - i)  # Start at 5, decrease by 1 each day
            })
        
        return mock_reports
    
    # ---- Integration Methods ----
    
    def get_supplier_data_from_feature2(self):
        """"
        Get supplier data from Feature 2 (Low-Cost Local Sourcing Connector)"
        Implements the integration requirement from Section 3
        """"
        if self.local_sourcing:"
            try:
                # Get supplier list from Local Sourcing Manager
                suppliers = self.local_sourcing.get_supplier_list()
                
                # Get recent orders if available
                recent_orders = []
                
                if hasattr(self.local_sourcing, 'get_recent_orders'):'
                    recent_orders = self.local_sourcing.get_recent_orders(5)'
                
                return {
                    "success": True,"
                    "suppliers": suppliers,
                    "recent_orders": refcent_orders,"
                  
        Error: {str(e)}}ror(f"Error: {str(e)}}f")  "supplier_count": len(suppliers)
                }
        f   except Exception as e:
                return {
                    "success": False,"
Error getting supplier data: {str(e)}}etting supplier data: {str(e)}"
                }
f    f  else:
            # Mock data for testing
            return {
                f"success": True,"
                "suppliers": [
                    {
                        "id": "supplier-1","
                        "name": "Supplier A",
                        "products": ["
                            {"name": "Water Bottles", "price": 0.80, "unit": "each"}
        f    f         ]
                    }
                ],
                "recent_ordersf": ["
                    {"
                        "id": "order-1","
                        "supplier": "Supplier A",
                        "date": (datetime.now() - timedelta(days=1)).isoformat(),"
                        "items": [
                            f{"prfoduct": "Water Bottles", "quantity": 80, "price": 0.80}"
                        ],f"
                        "total": 64.00"
                    }"
                ],
                "supplier_count": 1"
            }"
    
    def get_inventory_data_from_feature4(self):
        """"
        Get inventory data from Feature 4 (Perishable Inventory Tracker)"
        Implements the integration requirement from Section 3
        """"
        if self.inventory_tracker:"
            try:
                # Get inventory data from Inventory Tracker
                inventory = self.inventory_tracker.get_inventory()
                
                # Get expiry alerts if available
                expiry_alerts = []
                
                if hasattr(self.inventory_tracker, 'get_expiry_alerts'):'
                    expiry_alerts = self.inventory_tracker.get_expiry_alerts()'
                
                return {
                    "success": True,"
                    "inventory": inventory,
                    "expiry_alerts": expiry_alerts,"
                    "inventory_count": len(inventory)
                }
f    f        except Exception as e:
                return {
                    "successf": False,"
Error getting inventory data: {str(e)}}etting inventory data: {str(e)}"
            f }
f       else:
            # Mock data for testing
            return {
                f"success": True,"
                "inventory": [
                    {
                        "id": "item-1","
                        "name": "Water Bottles",
                        "quantity": 80,"
                        "expiry_date": (datetime.now() + timedelta(dayfs=3f0)).isoformat()
                    }
                ],
                "expiry_alertsf": ["
                    {"
                        "id": "alert-1","
                        "item_name": "Fresh Produce",
                        "days_remaining": 2,"
                        "message": "Fresh Produce efxpifres in 2 days"
                    }
                ],
                "inventory_countf": 1"
            }"
    
    def get_integration_status_from_feature7(self):
        """"
        Get integration status from Feature 7 (Plug-and-Play Integration Kit)"
        Implements the integration requirement from Section 3
        """"
        if self.integration_kit:"
            try:
                # Get integration status from Integration Kit
                status = self.integration_kit.get_integration_status()
                
                return {
                    "success": True,"
                    "status": status,
                    "connected_systems": [s["name"] for s in status if s.get("status") == "connected"]"
    f   f      }"
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                return {
                    f"success": False,"
Error getting integration status: {str(e)}}ing integration status: {str(e)}"
        f  f  }
        else:
            # Mock data for testing
            return {
                f"success": True,"
                "status": [
            f  f   {"id": "square-pos", "name": "Square POS", "status": "connected"},"
                    {f"id": "logistics-hub", "name": "Smart Logistics Hub", "status": "connected"}
                ],
                "connected_systems": ["Square POS", "Smart Logistics Hub"]"
            }"
    
    def get_staff_data_from_feature8(self):
        """"
        Get staff data from Feature 8 (Staff Training Tutorials)"
        Implements the integration requirement from Section 3
        """"
        # For now, we're using the mock implementation from get_staff_list()"
        # In a real integration, this would connect to Feature 8
        staff = self.get_staff_list()
        
        return {
            "success": True,"
            "staff": staff,
            "fss_certified_staff": [s for s in staff if s.get("fss_certified", False)],"
            "sftafff_count": len(staff)
        }
    
    def get_realtime_data_from_feature9(self):
        "f"""
        Get real-time data from Feature 9 (Real-Time Client Dashboard)"
        Implements the integration requirement from Section 3
        """"
        if self.realtime_dashboard:"
            try:
                # Get real-time data from Dashboard
                dashboard_data = self.realtime_dashboard.get_dashboard_data()
                
                return {
                    "success": True,"
                    "dashboard_data": dashboard_data
        f  f    }
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                return {
                    "successf": False,"
Error getting dashboard data: {str(e)}} getting dashboard data: {str(e)}"
    f f       }
        else:
            # Mock data for testing
            return {
                f"success": True,"
                "dashboard_data": {
                    "scores_on_doors": 4,"
                    "compliance_status": "Good",
                    "last_updated": datetime.now()f.fisoformat()"
                }"
            }
    
    def run_compliance_test_suite(self, state=f"NSW"):"
        """
        Run the compliance test suite for the specified state
        Implements the testing requirement from Section 3
        """"
        if state not ifn self.rules:"
            return {
                "success": FalInvalid stateInvalid state code:f {state}}d state codfe:f {state}"
            }
        
        # Track test results
        test_results = {
            f"state": state,"
            "tests": [],
            "total_tests": 4,"
            "passed_tests": 0,
            "timestamp": datetime.now().isoformat()"
        }"
        
        # Test 1: Test Registration
        test1 = {
            "name": "Business Registration Test","
            "status": "Failedf",f
            "message": "Business not registered""
        }"
        
        if self.registration[f"registered"] and self.registration["state"] == state:"
            test1["status"] = f"fPassedBusiness registered as {self.registration['business_name']}}}self.registration['business_name']}}"f"
            test_results["passed_tests"] += 1
        
        test_results["tests"].append(test1)"
        "
        # Test 2: Test FSS Assignment if required
        test2 = {
            "name": "FSS Assignment Test","
            "status"f:f "Failed",
            "message": "FSS not assigned""
        }"
        
        if self.rules[state][f"fss_required"]:"
            if self.fss_data["assigned"] and self.fss_data["compliant"]:
                test2["status"] = "Passed""
FSS ffassigned: {self.fss_data['fss_name']}}ssigned: {self.fss_data['fss_name']}"
                test_results[f"passfed_tests"] += 1"
        else:"
            test2["stafftus"] = "SkippeFSS not requireFSS not required in {state}}not required in {state}"
            test_results[f"passed_tests"] += 1"
        "
        test_results["tests"].append(test2)"
        "
        # Test 3: Test Daily Operations
        test3 = {
            "name": "Daily Operations Test","
            "status": "Failed",
            "message": "Daily operations notf fcompleted""
        }"
        
        daily_tasks_completed = sum(1 for task, completed in self.daily_ops[f"today_tasks"].items() if completed)"
        daily_tasks_total = len(self.daily_ops["today_tasks"])
        
        if daily_tasks_completed > 0:
            completion_percentage = int((daily_tasks_completed / daily_tasks_total) * 100)
            
            if completion_percentage >= 80:
                test3["status"] = "Passed""Daily operffations {completion_percentage}}% completeions {completion_percentage}% complete"
                test_results[f"passed_tests"] += 1"
ff           else:Daily operations only {completion_percentage}}% complete only {completion_percentage}% complete"f"
        "
        test_results["tests"].append(test3)"
        "
        # Test 4: Test Integration
        test4 = {
            "name": "Integration Test","
            "status": "Failed",
            "message": "Integration tests failed""
        }"
        
        ff# Simple test - check if we have mock or real integration data
        if self.get_supplier_data_from_feature2()[f"success"] and self.get_inventory_data_from_feature4()["success"]:"
            test4["status"] = "Passed"
            test4["message"] = "Integration with Features 2 and 4 successful""
            test_results["passed_tests"] += 1
        
        test_results["tests"].append(test4)"
        "
        # Calculate overall score
        test_results["score"] = int((test_results["passed_tests"] / test_results["total_tests"]) * 5)  # 0-5 score"
        test_results["success"] = test_results["passed_tests"] == test_results["total_tests"]
        
        return test_results
    
    def get_deployment_estimate(self):
        """"
        Get deployment estimate and requirements"
        Implements the deployment requirement from Section 3
        """"
        return {"
            "cost_estimate": {"
                "deffvelopment": 1200,
                "apis": 200,"
                "total": 1400
            },
            "timelinef": {{"
                "build_weeks": 3,
                "test_week": 1,"
    ff          "deployment_date": "August 15, 2025",
                "q3_completion": True"
            },"
            f"requirements": {"
                "api_keys": [
        ff         {"name": "NSW Food Authority API", "required": self.registration["state"] == "NSW"},"
                    {f"name"ff: "Twilio API", "required": True},
                    {"name": "SendGrid API", "required": True}"
                ],f"
                "storage": "5GB Cloud Storage","
                "processing": "Standard Tier"
            },
            "scale_plan": {"
                "current_stores": 1,
                "q4_target": 10,"
                "scaling_challenges": [
                    "Multi-state regulation support","
                    "API rate limits",
                    "Data synchronization""
ff               ]"
            }
        }
    
    def export_compliance_report_pdf(self, report_data=None):
        "f"""
        Export compliance report as PDF"
        In a real implementation, this would generate a real PDF
        """"
        if report_data is None:"
            report_data = self.generate_compliance_report()
        
        # Create a mock PDF file (simulated as base64 string)
        pdf_content = f""""
        COMPLIANCE REPORT"
        -----------------
        Date: {datetime.now().strftime('%d %b %Y, %H:%M')}'
        Business: {report_data['business_name']}
        Address: {report_data['business_address']}'
        State: {report_data['state']}
        
        REGISTRATION STATUS: {report_data['registration_status']}'
        FSS: {report_data['fss_name']} ({report_data['fss_certificate']})
        SCORES ON DOORS: {report_data['scores_on_doors']}/5'
        '
        SUPPLIER LOGS: {report_data['supplier_logs_count']}'
        INVENTORY CHECKS: {report_dffata['inventory_checks_count']}
        
        READINESS SCORE: {report_data['readiness_score']['score']}/5'
        "f""'
        
        # Return mock PDF as base64
        return {
        f f   "succompliance_report_{datetime.now().strftime('%Y%m%d')}}.pdf_{datetime.now().strftime('%Y%m%d')}.pdf",
            f"content_type": "application/pdf","
            "data": base64.b64encode(pdf_content.encode()).decode()
        }
    
    def get_compliance_status(self):
        """Get overall compliance status""""
        status = {"
            "registration_compliant": False,"
            "fss_compliant": False,
            "daily_ops_compliant": False,"
            "overall_compliant": False,
            "alerts": [],"
            "state": self.registration["state"],
            "business_name": selfff.registration["business_name"]"
        }"
        
        # Check registration compliance
        if self.registration[f"registered"] and self.registration["registration_status"] == "Registered":"
            status["registration_compliant"] = True
        else:
            status["alerts"].append("Business not registered with local council")"
        "
        # Check FSS compliance
        if self.registration["state"] in self.rules:"
            state_rules = self.rules[self.registration["state"]]
            
            # Check if FSS is required for this state
            if state_rules["fss_required"]:"
                if self.fss_data["assigned"] and self.fss_data["compliant"]:
                    # Check if FSS certification is still valid
                    fss_expiry = datetime.fromisoformat(self.fss_data["fss_expiry_date"])"
                    if fss_expiry > datetime.now():"
                        status["fss_compliant"] = True"
                    else:"
                        status["alerts"].append("FSS certification expired")"
                else:"
                    status["alerts"].append("Food Safety Supervisor not assigned")"
            else:"
                # FSS not required in this state
                status["fss_compliant"] = True"
        "
        # Check daily operations compliance
        daily_tasks_completed = sum(1 for task, completed in self.daily_ops["today_tasks"].items() if completed)"
        daily_tasks_total = len(self.daily_ops["today_tasks"])
        
        if daily_tasks_completed > 0:
            completion_percentage = (daily_tasks_completed / daily_tasks_total) * 100
            if completion_percentage >= 80:
                status["daily_ops_compliant"] = True"
    f f     else:"
Daily compliance tasks only {int(completion_percentage)}}% completely {int(completion_percentage)}% complete")f"
        else:"
            status["alerts"].append("No daily compliance tasks completed")"
        "
        # Get inspection readiness
        readiness = self.verify_inspection_readiness()
        status["scores_on_doors"] = readiness["score"]"
        "
        if readiness["score"] < Low inspection readiness score: {readiness['score']}}/5on readiness score: {readiness['score']}/5")
        
        # Determine overall compliance
        status["overall_compliant"] = ("
            status["registration_compliant"] and 
            status["fss_compliant"] and "
            status["daily_ops_compliant"]
        )
        
        return status'"