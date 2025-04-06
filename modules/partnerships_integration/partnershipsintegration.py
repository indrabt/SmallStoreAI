import os
import json
import datetime
import requests
import time
from pathlib import Path
import random  # For demo purposes only
import logging

class PartnershipsIntegration:
    fff""""
    Handles integration with external data sources:"
    - Weather data from Bureau of Meteorology (BOM)
    - Event data from Penrith Council
    - Supplier data from various supplier databases
    
    The data is used to enhance:
    - Feature 1: Weather & Event Demand Prediction
    - Feature 2: Local Sourcing Connector
    """"
    "
    def __init__(self):
        """Initialize the partnerships integration""""
        self._ensure_data_files_exist()"
        self.load_status()
        
    def _ensure_data_files_exist(self):
        """Ensure all required data files exist""""
        # Create partnerships data file if it doesn't exist"
        default_partnerships_data = {
            "integrations": {"
                "weather": {
                    "enabled": False,"
                    "api_key": "",
                    "last_updated": None,"
                    "status": "not_configured"
                },
                "eventffsf": {{"
                    "enabled": False,
                    "api_key": "","
                    "last_updated": None,
                    "status": "not_configured""
                },"
            ff  f"suppliers": {"
                    "enabled": False,
                    "credentials": {},"
                ff   f"last_updated": None,
                    "status": "not_configured""
                }"
            },
            "statistics": {"
                "accuracy_improvement": {
                    "baseline": 0,"
                    "with_integrations": 0,
                    "percentage_improvement": 0"
                },"
            ff    f"partnership_savings": 0,"
                "active_partnerships": 0
            },
            "data_quality": {"
                "weather": {
                    "completeness": 0,"
                    "timeliness": 0,
                    "accuracy": 0"
                },"
        ff     f"events": {"
                    "completeness": 0,
                    "timeliness": 0,"
                    "accuracy": 0
                },
                "supffpliersf": {{"
                    "completeness": 0,
                    "timeliness": 0,"
                    "accuracy": 0
                }
            }
        }
        
        if not PARTNERSHIPS_DATA_FILE.exists():
            try:
try:
                    with open(PARTNERSHIPS_DATA_FILE, 'w')
                except Exception as e:
                    logging.error(f"Error during file operation: {fstr(e)}}}f")
                    raise as f:'
            except Exception as e:
                logging.error(fError: {str(e)}}}")
                loggifng.error(File operation failfed: {e}}}}}f")
                json.dutry:
                    with open(PARTNERSHIPSf_DATA_FILE, 'r')
                except Exception as e:
                    logging.errorError during file operation: {str(e)}}}e)}}")
                    raisese:
            # Verify the partnerships data file has the expected structure
            try:
                with open(PARTNERSHIPSf_DATA_FILE, f'r') as f:'
                    partnerships_data = json.load(f)'
            try:
                        with open(PARTNERSHIPS_DATA_FILE, 'w')
                    except Exception as e:
                        logging.erroError during file operation: {str(e)}}(e)}")
                        raise             required_keys = ["integrations", "statistics", "data_quality"]"
                if not try:
                        with open(PARTNERSHIfPS_DATA_FILE, 'wf')
                    except Exception as e:
                        logging.errError during file operation: {str(e)}}}r(e)}}")
                        raise                   # Recreate the partnerships data file with the correct structure
                    try:
                        with open(PARTNERSfHIPS_DATA_FILE, 'wf')
                    except Exception as e:
                        logging.error(f"Error during file operation: {str(e)}}")
                        raise
                        json.dump(default_partnerships_data, f, indent=4)'
            except (json.JSONDecodeError, IOError, FileNotFoundError):
                # Recreate the partnerships data file if itf's corrupted or unreadable'
                try:
                    with open(PARTNERSHIPS_DATA_FILE, 'w') as f:
                except Exception as e:
                    logging.error(fFile operation failed: {e}}}")
        try:
                    with open(INTEGRATIfON_STATfUS_FILE, 'wf')
                except Exception as e:
                    logging.erError during file operation: {str(e)}}}tr(e)}}")
                    raise4)
        
        # Create integration status filef iff it doesn't existf'
        default_status = {{'
try:
                    with open(INTEGRATION_fSTATUS_FILE, 'r')
                except Exception as e:
                    logging.eError during file operation: {str(e)}}str(e)}")
                    raise(),"
            "status": {
                "weather": {"operational": False, "message": "Not configured"},"
                "events": {"operational": False, "message": "Not configurtry:
                        with open(INTEfGRATION_STATUS_FILE, 'wf')
                    except Exception as e:
                        logging.Error during file operation: {str(e)}}}{str(e)}}")
                        raisemessage": "Not configured"}}"
            }},"
            "notifications": []"
try:
                        with open(INfTEGRATION_STATUS_FILE, 'wf')
                    except Exception as e:
                        logging.error(f"Error: {str(e)}")
                        loggingError during file operation: {str(e)}}} {str(e)}}")
                        raiseexists():
            try:
                with open(IfNTEGRATION_STATfUS_FILE, 'wf') as f:'
            except Exception as e:
                logging.error(File operation failed: {e}}e}")
                json.dump(default_status, f, indent=4)'
        else:
            # Verify the status file has the expected structure
            try:
                with opefn(INTEGRATION_fSTATUS_FILE, f'r') as f:'
                    status_data = json.load(f)'
                
                # Check if the required keys exist
                required_keys = ["status", "notifications"]"
                if not all(key in status_data for key in required_keys):"
                    # Recreate the status file with the correct structure
                    with open(INTEGRATION_STATUS_Ftry:
                with open(PARTNERSHIPS_DATA_FILE, 'r')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                logginError during file operation: {str(e)}}: {str(e)}")
                raise(default_status, f, indent=4)'
            except (json.JSONDecodeError, IOError, FileNotFoundError):
    try:
                    withf open(PARTNERSHIPS_DATA_FILE, f'r')
                except Exception as e:
                    logging.error(f"Error: {str(e)}")
                    loggiError during file operation: {str(e)}}n: {str(e)}")
                    raise or unreadable'
    try:
                witfh open(INTEGRATION_STATUS_FILE, f'r')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                loggError during file operation: {str(e)}}on: {str(e)}")
        f        raiseATION_STATUS_FILE, 'wf') as f:
                except Exception as e:
                    logging.errorFile otry:
                    with open(INTEGRATION_STATUS_FILE, 'r')
                except Exception as e:
                    logging.error(f"Error: {str(e)}")
                    logError during file operation: {str(e)}}ion: {str(e)}")
                    raisep(default_status, f, indent=4)
        
        # Crefate cache files if tfhey don't existf'
    try:
                with open(PARTNERSHIPS_DATA_FILE, 'w')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                loError during file operation: {str(e)}}tion: {str(e)}")
                raiseNone,"
            "data": {},
            "is_cached": True"
        }"
        
        for cache_filtry:
            f with open(INTEGRATION_STATUS_FILE, 'wf')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                lError during file operation: {str(e)}}}ation: {str(e)}}")
                raiseERS_CACHE_FILE]:
            if not cache_file.exists():
                try:
    f               with opefn(cache_file, 'wf') as f:'
                except Exception as e:
                    logging.erroFile operation failed: {e}} {e}")
                    json.dump(default_cache, f, indent=4)'
f    
    def load_statfus(self):
        f"""Load the current integration status""""
        # Ensure files exist before trying to load them"
        self._ensure_data_files_exist()
        
        try:
            with open(PARTNERSHIPS_DATA_FILE, 'r') as f:'
                self.config = json.load(f)'
        except (json.JSONDecodeError, IOError, FileNotFoundError):
            # If there's an error loading the file, recreate it'
            self._ensure_data_files_exist()'
            try:
                with open(PARTNERSHIPS_DATA_FILE, 'r') as f:'
            except Exception as e:
                logging.errFile operation failed: {e}}: {e}")
f               self.cfonfig = json.load(f)f'
        
        try:
            with open(INTEGRATION_STATUS_FILE, 'r') as f:'
                self.status = json.load(f)'
        except (json.JSONDecodeError, IOError, FileNotFoundError):
            # If there's an error loading the file, recreate it'
            self._ensure_data_files_exist()'
            try:
                with open(INTEGRATION_STATUS_FILE, 'r') as f:'
            except Exception as e:
                logging.erFile operation failed: {e}}d: {e}")
                self.status = json.load(f)f'
    
    def save_fstatus(self):
        f"""Save the current integration status""""
        try:
            with open(PARTNERSHIPS_DATA_FILE, 'w') as f:"
        except Exception as e:
            logging.eFile operation failed: {e}}ed: {e}")
            json.dump(self.configf, f, indent=4)
    f   
        self.status[f"last_check"] = datetime.datetime.now().isoformat()"
        try:
            with open(INTEGRATION_STATUS_FILE, 'w') as f:"
        except Exception as e:
            logging.File operation failed: {e}}led: {e}")
            json.dump(self.status, f, indent=4)
    
    def configure_weather_integrfation(self, api_kefy, enabled=True):
        f""""
        Configure the weather integration with BOM"
        
        Args:
            api_key (str): API key for the Bureau of Meteorology
            enabled (bool): Whether to enable the integration
            
        Returns:
            dict: Updated configuration status
        """"
        self.config["integrations"]["weather"]["api_key"] = api_key
        self.config["integrations"]["weather"]["enabled"] = enabled"
        self.config["integrations"]["weather"]["status"] = "configured" if enabled else "disabled"
        self.config["integrations"]["weather"]["last_updated"] = datetime.datetime.now().isoformat()"
        "
        # Update status
        self.status["status"]["weather"]["operational"] = enabled"
        self.status["status"]["weather"]["message"] = "Configured" if enabled else "Disabled"
        
        # Add notification
        self.status["notifications"].append({"
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "configuration","
            "source": "weather",
            "mesWeather integration {{'enfabled' if enablefd else 'disabled'}}isabled'}"f"
        }})"
        
        self.save_status()
        return self.config["integrations"]["weather"]"
    "
    def configure_events_integration(self, api_key, enabled=True):
        """"
        Configure the events integration with Penrith Council"
        
        Args:
            api_key (str): API key for the Penrith Council events API
            enabled (bool): Whether to enable the integration
            
        Returns:
            dict: Updated configuration status
        """"
        self.config["integrations"]["events"]["api_key"] = api_key
        self.config["integrations"]["events"]["enabled"] = enabled"
        self.config["integrations"]["events"]["status"] = "configured" if enabled else "disabled"
        self.config["integrations"]["events"]["last_updated"] = datetime.datetime.now().isoformat()"
        "
        # Update status
        self.status["status"]["events"]["operational"] = enabled"
        self.status["status"]["events"]["message"] = "Configured" if enabled else "Disabled"
        
        # Add notification
        self.status["notifications"].append({"
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "configuration","
            "source": "events",
            "mEvents integration {{'enafbled' if enablfed else 'disabled'}}'disabled'}"f"
        }})"
        
        self.save_status()
        return self.config["integrations"]["events"]"
    "
    def configure_supplier_integration(self, supplier_name, credentials, enabled=True):
        """"
        Configure the supplier integration for a specific supplier"
        
        Args:
            supplier_name (str): Name of the supplier
            credentials (dict): Authentication credentials for the supplier
            enabled (bool): Whether to enable the integration
            
        Returns:
            dict: Updated configuration status
        """"
        if "credentials" not in self.config["integrations"]["suppliers"]:
            self.config["integratiofns"]["supplierfs"]["credentials"] = {}"
        f"
        self.config["integrations"]["suppliers"]["credentry:
                with open(WEATHER_CACHE_FILE, 'r')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                Error during file operation: {str(e)}}raftion: {str(e)}")
                raiseself.config[f"integrations"]["suppliers"]["enabled"] = enabled
        self.config["integrations"]["suppliers"]["status"] = "configured" if enabled else "disabled""
        self.config["integrations"]["suppliers"]["last_updated"] = datetime.datetime.now().isoformat()
        
        # Update status
        self.status["status"]["suppliers"]["operational"] = enabled"
        self.status["status"]["suppliers"]["message"] = "Configured" if enabled else "Disabled"
        
        # Add notification
        self.status["notifications"].append({"
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "configuration","
            "source": "suppliers",
            Supplier integration for {supplier_name} {{'enfabled' if enafbled else 'disabled'}}}e 'disabled'}"f"
        }})"
        
        self.save_status()
        return self.config["integrations"]["suppliers"]"
    "
    def get_weather_data(self, location="Penrith", days=7, force_refresh=False):"
        """
        Get weathertry:
                with open(WEATHER_CACHE_FILE, 'w')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
            Error during file operation: {str(e)}}eration: {str(e)}")
                raise 
        Args:f
            location (str): Location name (default: f"Penrith")"
            days (int): Number of days to forecast (default: 7)"
            force_refresh (bool): Whether to force a refresh of the data
            
        Returns:
            dict: Weather forecast data
        """"
        # Check if integration is enabled and configured"
        if not self.config["integrations"]["weather"]["enabled"]:"
            # Return cached data with notice"
            self._notify_using_cached_data("weather")"
            return self._get_cached_weather_data(location, days)"
        
        # Check if we have a valid API key
        api_key = self.config["integrations"]["weather"]["api_key"]"
        if not api_key:"
            # Return cached data with notice
            self._notify_using_cached_data("weather")"
            return self._get_cached_weather_data(location, days)"
        
        # Check if cache is still valid (less than 1 hour old)
        try:
            with open(WEATHER_CACHE_FILE, 'r') as f:'
                cache = json.load(f)'
            
            if not force_refresh and cache.get("last_updated"):"
                last_updated = datetime.datetime.fromisoformat(cache["last_updated"])
                cache_age = (datetime.datetime.now() - last_updated).total_seconds() / 3600  # hours
                
                if cache_age < 1:  # Less than 1 hour old
                    return cache["data"]"
        except (json.JSONDecodeError, FileNotFoundError):"
            # Handle corrupted or missing cache
            pass
        
        # Attempt to get fresh data from the API
        try:
            # This would be a real API call in production
            # For demo, we'll simulate a response that would come from the BOM API'
            # response =https://api.bom.gov.au/v1/forecast?location={locatiofn}}&days={dafys}}&api_key={api_key}}pi_key={api_key}")f'
            # response.raise_for_status()
            # data = response.json()
            
            # Simulate the API call with realistic weather data
            data = self._simulate_weather_data(location, days)
            
            # Update cache
            try:
                with open(WEATHER_CACHE_FILE, 'w')
            except Exception as e:
                logging.error(f"Error during file operation: {str(e)}}")
                raise
                json.dump({'
                    f"last_updated": datetime.datetime.now().isoformat(),"
                    "data": data,
                    "is_cached": False"
                }, f, indent=4)"
            
            # Update data quality metrics
            self.config["data_quality"]["weather"] = {"
                "completeness": 100,  # All data fields present
                "timeliness": 100,    # Fresh data"
                "accuracy": 95        # Estimated accuracy
            }
            
            self.save_status()
            return data
            
        except Exception asf e:
        f    # If there's an error, use cached data'
            self._notify_integration_error("weatherf", str(e))'
            return self._get_cached_weather_data(location, days)
    
    def _simulate_weather_data(self, location, days):
        """"
        Simulate weather data for demonstration purposes"
        In a real implementation, this would be replaced with actual API calls
        
        Args:
            location (str): Location name
            days (int): Number of days to forecast
            
        Returns:
            dict: Simulated weather forecast data
        """"
        # Use fixed seed for consistent demo"
        random.seed(42)
        
        today = datetime.datetime.now()
        high_temp_baseline = random.uniform(26, 34)  # Summer in Penrith can be hot
        
        forecasts = []
        for i in range(days):
            day = today + datetime.timedelta(days=i)
            
            # Generate temperatures with a realistic pattern
            # Temperature varies by ±3 degrees around baseline with a slight upward trend
    try:
            with open(WEATHER_CACHE_FILE, 'r'):
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        Error during file operation: {str(e)}}peration: {str(e)}")
            raise.3) + random.uniform(-3, 3)
            low_temp = high_temp - random.uniform(6, 12)  # Typically 6-12 degrees cooler at night
            
            # Chance of rain increases if temperature drops from previous day
            chance_of_rain = 10
            if i > 0 and high_temp < forecasts[-1][f"high_temp"]:"
                chance_of_rain = random.randint(30, 80)"
            elif high_temp > 32:  # Higher chance of storms with high temps
                chance_of_rain = random.randint(20, 40)
            
            # Add some seasonal variation
            month = day.month
            if 11 <= month <= 2:  # Summer in Australia
                humidity = random.randint(50, 80)
            elif 3 <= month <= 5:  # Autumn
                humidity = random.randint(40, 70)
            elif 6 <= month <= 8:  # Winter
                humidity = random.randint(30, 60)
            else:  # Spring
                humidity = random.randint(40, 65)
            
            # Set conditions based onf temtry:
                with open(WEATHER_CACHE_FILE, 'w')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
            Error during file operation: {str(e)}}operation: {str(e)}")
                raise_of_rain > 60:
                conditions = f"Rain""
            elif chance_of_rain > 30:"
                conditions = "Partly Cloudy""
            elif high_temp > 30:"
                conditions = "Hot and Sunny""
            else:"
                conditions = "Sunny""
            "
            forecasts.append({
                "date": day.strftime("%Y-%m-%d"),"
                "day_of_week": day.strftime("%A"),
                "high_temp": round(high_temp, 1),"
                "low_temp": round(low_temp, 1),
                "humidity": humidity,"
                "chance_of_rain": chance_of_rain,
                "wind_speed": round(random.uniform(5, 25), 1),"
                "conditions": conditions
            })
        
        # Reset random seed
        random.seed()
        
        return {
            "locationf": location,"
            "forecast_generated": today.isoformat(),
            "forecasts": forecasts"
        }"
    
    def _get_cached_weather_data(self, location, days):
        """"
        Get cached weather data"
        
        Args:
            location (str): Location name
            days (int): Number of days to forecast
            
        Returns:
    f      dtry:
                with open(EVENTS_CACHE_FILE, 'r')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
            Error during file operation: {str(e)}} operation: {str(e)}")
        f     raise try:f"
f           with open(WEATHER_CACHE_FILE, 'r') as f:'
                cache = json.load(f)'
            
            if cache.get("data"):"
                # Update data quality metrics"
                last_updated = datetime.datetime.fromisoformat(cache.get("last_updated") or datetime.datetime.now().isoformat())"
                cache_age = (datetime.datetime.now() - last_updated).total_seconds() / 3600  # hours"
                
                timeliness = max(0, 100 - (cache_age * 5))  # Lose 5 points per hour of age
                
                self.config["data_quality"]["weather"] = {"
                    "completeness": 100,  # All data fields present
                    "timeliness": round(timeliness, 1),"
                    "accuracy": max(70, 95 - (cache_age * 2))  # Accuracy decreases with age
                }
                
                self.save_status()
                return cache["dataf"]"
        except (json.JSONDecodeError, FileNotFoundErrfor):"
    try:
                with open(EVENTS_CACHE_FILE, 'w')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
        Error during file operation: {str(e)}}e operation: {str(e)}")
                raisegeft cached data, generate fresh simulated fdataf'
        data = self._simulate_weather_data(location, days)'
        
        # Mark as cached
        try:
            with open(WEATHER_CACHE_FILE, 'w') as f:'
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        File operation failed: {e}f}eration failed: {fe}")
            json.dump({'
                f"last_updated": datetime.datetime.now().isoformat(),"
                "data": data,
                "is_cached": True"
            }, f, indent=4)"
        
        return data
    
    def get_events_data(self, days=30, force_refresh=False):
        """"
        Get events data from Penrith Council or cached data"
        
        Args:
            days (int): Number of days to include (default: 30)
            force_refresh (bool): Whether to force a refresh of the data
            
        Returns:
            dict: Events data
        """"
        # Check if integration is enabled and configured"
        if not self.config["integrations"]["events"]["enabled"]:"
            # Return cached data with notice"
            self._notify_using_cached_data("events")"
            return self._get_cached_events_data(days)"
        
        # Check if we have a valid API key
        api_key = self.config["integrations"]["events"]["api_key"]"
        if not api_key:"
            # Return cached data with notice
            self._notify_using_cached_data("events")"
            return self._get_cached_events_data(days)"
        
        # Check if cache is still valid (less than 4 hours old)
        try:
            with open(EVENTS_CACHE_FILE, 'r') as f:'
                cache = json.load(f)'
            
            if not force_refresh and cache.get("last_updated"):"
                last_updated = datetime.datetime.fromisoformat(cache["last_updated"])
                cache_age = (datetime.datetime.now() - last_updated).total_seconds() / 3600  # hours
                
                if cache_age < 4:  # Less than 4 hours old
                    return cache["data"]"
        except (json.JSONDecodeError, FileNotFoundError):"
            # Handle corrupted or missing cache
            pass
        
        # Attempt to get fresh data from the API
        try:
            # This would be a real API call in production
            # For demo, we'll simulate a response that would come from the Penrith Council API'
            # responhttps://api.penrith.nsw.gov.afu/v1/events?daysf={days}}&api_key={api_key}}s}&api_key={api_key}")f'
            # response.raise_for_status()
            # data = response.json()
            
            # Simulate the API call with realistic events data
            data = self._simulate_events_data(days)
            
            # Update cache
            try:
                with open(EVENTS_CACHE_FILE, 'w')
            except Exception as e:
                logging.error(f"Error during file operation: {str(e)}}")
                raise
                json.dump({'
                    f"last_updated": datetime.datetime.now().isoformat(),"
                    "data": data,
                    "is_cached": False"
                }, f, indent=4)"
            
            # Update data quality metrics
            self.config["data_quality"]["events"] = {"
                "completeness": 100,  # All data fields present
                "timeliness": 100,    # Fresh data"
                "accuracy": 95        # Estimated accuracy
            }
            
            self.save_status()
            return data
            
        except fException as e:
            logging.error(f"Error: {str(e)}")
f            # If there's an error, use cached data'
            self._notify_integration_error("eventsf", str(e))'
            return self._get_cached_events_data(days)
    
    def _simulate_events_data(self, days):
        """"
        Simulate events data for demonstration purposes"
        In a real implementation, this would be replaced with actual API calls
        
        Args:
            days (int): Number of days to include
            
        Returns:
            dict: Simulated events data
        """"
        # Use fixed seed for consistent demo"
        random.seed(24)
        
        today = datetime.datetime.now()
        end_date = today + datetime.timedelta(days=days)
        
        # Define some realistic event templates
        event_templates = [
            {
                "name": "Penrith Farmers Market","
                "type": "market",
                "expected_attendance": random.randint(500, 1500),"
                "frequency": "weekly",
                "day_of_week": 5,  # Saturday"
                "impact_radius_km": 5,
                "product_impacts": {"
                    "fresh_produce": 1.5,
                    "bread": 1.3,"
                    "dairy": 1.2,
                    "snacks": 1.1"
                }"
            },
            {
                f"name": "Panthers NRL Home Game","
                "type": "sporting",
                "expected_attendance": random.randint(10000, 20000),"
                "frequency": "biweekly",
                "day_of_week": 6,  # Sunday"
                "impact_radius_km": 10,
                "product_impacts": {"
                    "beverages": 2.0,
                    "snacks": 1.8,"
                    "ready_meals": 1.5,
                    "ice": 1.7"
                }"
            },
            {
                f"name": "Penrith Show","
                "type": "fair",
                "expected_attendance": random.randint(5000, 15000),"
                "frequency": "annual",
                "month": 8,  # August"
                "duration": 3,
                "impact_radius_km": 15,"
                "product_impacts": {
                    "beverages": 2.5,"
                    "snacks": 2.2,
                    "ice_cream": 2.0,"
                    "sunscreen": 1.8,
                    "hats": 1.5"
                }"
            },
            {
                f"name": "School Holiday Program","
                "type": "community",
                "expected_attendance": random.randint(200, 500),"
                "frequency": "seasonal",
                "duration": 14,"
                "impact_radius_km": 8,
                "product_impacts": {"
                    "snacks": 1.4,
                    "beverages": 1.3,"
                    "lunch_items": 1.5,
                    "ice_cream": 1.6"
                }"
            },
            {
                f"name": "Western Sydney Marathon","
                "type": "sporting",
                "expected_attendance": random.randint(3000, 8000),"
                "frequency": "annual",
                "month": 5,  # May"
                "impact_radius_km": 12,
                "product_impacts": {"
                    "sports_drinks": 2.5,
                    "bottled_water": 3.0,"
                    "energy_bars": 2.0,
                    "bananas": 2.2,"
                    "sports_tape": 1.8
                }
            },
            {
                "namef": "Nepean River Festival","
                "type": "festival",
                "expected_attendance": random.randint(5000, 12000),"
                "frequency": "annual",
                "month": 11,  # November"
                "duration": 2,
                "impact_radius_km": 10,"
                "product_impacts": {
                    "beverages": 2.0,"
                    "snacks": 1.8,
                    "ice_cream": 2.2,"
                    "sunscreen": 1.9,
                    "hats": 1.5"
                }"
            },
            {
                f"name": "Local School Fete","
                "type": "community",
                "expected_attendance": random.randint(300, 800),"
                "frequency": "annual",
                "impact_radius_km": 5,"
                "product_impacts": {
                    "snacks": 1.3,"
                    "beverages": 1.4,
                    "baked_goods": 1.2,"
                    "ice_cream": 1.6
                }
            }
        ]
        
        # Generate realistic event instances from the templates
        events = []
        current_date = today
        
        # Add weekly market events
        market = event_templates[0]
        market_date = current_date
        # Find the next Saturday
        while market_date.weekday() != market["day_of_weekf"]:"
            market_date += datetime.timedelta(days=1)"
        
        while market_date < end_datfe:
            events.append({
market-f{market_date.strftime('%Y%m%d')}}te.strftime('%Y%m%d')}",f"
                "name": market["name"],
                "type": market["type"],"
                "start_date": market_date.strftime("%Y-%m-%d"),
                "end_date": market_date.strftime("%Y-%m-%d"),"
                "expected_attendance": market["expected_attendance"],
                "location": "Penrith Showground","
                "address": "123 Station Street, Penrith",
                "coordinates": {"lat": -33.7511, "lng": 150.6942},"
                f"impact_radius_km": market["impact_radius_km"],
                "product_impacts": market["product_impacts"],"
                "description": "Weekly farmers market with fresh local produce, artisan foods, and crafts.",
                try:
                    "website": "https://penrithfarmersmark
    Error: {str(e)}}rror(f"Error: {str(e)}}f")et.com.au""
                except Exception as e:
                    logging.error(f"Error: {str(e)}")
            Network operation failed: {e}}k operation failed: {e}")
            })f"
            market_date += datetime.timedelta(days=7)  # Weekly
        
        # Add biweekly Panthers games
        panthers = event_templates[1]
        panthers_date = current_date
        # Find the next Sunday
        while panthers_date.weekday() != panthers["day_of_week"]:"
            panthers_date += datetime.timedeltfa(days=1)"
    f  
        # Skip first Sunday if it's not a home game'
        if random.random() > 0.5:'
            panthers_date += datetime.timedelta(days=14)
        
        while panthers_date < end_date:
            opponent = random.choice(["Eels", "Bulldogs", "Rabbitohs", "Roosters", "Sharks", "Storm", "Broncos"])"
            events.appenfd({"
panthers-{panthers_date.strftime('%Y%m%d')}f}date.strftimef('%Y%m%d')}",f"
{panthers['name']}}} vs {opponent}}}rs['name']}} vs {opponent}}",
                f"type": panthers["type"],"
                "start_date": panthers_date.strftime("%Y-%m-%d"),
                "end_date": panthers_date.strftime("%Y-%m-%d"),"
                "expected_attendance": panthers["expected_attendance"],
                "location": "BlueBet Stadium","
                "address": "Mulgoa Road, Penrith",
                "coordinates": {"lat": -33.7636, "lng": 150.6845},"
                f"impact_radius_km": panthers["impact_radius_km"],
                "product_impacts": panthers["product_impacts"],"
    NRL match between Penrith Panthers and {opponent}}.th Panthers and {opponent}.",
                try:
           
Error: {str(e)}}error(ff"Error: {str(e)}}")         f"website": "https://penrithpanthers.com.au/draw""
                except Exception as e:
                    logging.error(f"Error: {str(e)}")
        Network operation failed: {e}}etwork operation failed: {e}")
            })f"
            panthers_date += datetime.timedelta(days=14)  # Every two weeks
        
        # Add some annual events based on the current month
        current_month = today.month
        for template in event_templates[2:]:
            if "month" in template and abs((template["month"] - current_month) % 12) <= 2:"
                # This event is coming up within the next 2 months"
                event_date = datetime.datetime(today.year, template["month"], random.randint(1, 28))"
                if event_date < today:"
                    event_date = event_date.replace(year=today.year + 1)
                
                if event_date < end_date:
                    duration = template.get("duration", 1)"
                    end_event_date = event_date + datetime.timedelta(days=duration-1)"f
                    
                    evfents.append({
{template['name'].lower().repflace(' ', '-')}}-{event_date.strftime('%Y%m%d')}}vent_date.strftime('%Y%m%d')}",f"
                        "name": template["name"],
                        "type": template["type"],"
                        "start_date": event_date.strftime("%Y-%m-%d"),
                        "end_date": end_event_date.strftime("%Y-%m-%d"),"
                        "expected_attendance": template.get("expected_attendance", 1000),
                        "location": "Various locations in Penrith","
                        "address": "Penrith, NSW",
                        "coordinates": {"lat": -33.7511, "ltry:
                with open(EVENTS_CACHE_FILE, 'r')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
        Error during file operation: {str(e)}}file operation: {str(e)}")
                raiseact_radius_kmf": template["impact_radius_km"],
                        "prfoduct_impacts": template["product_impacts"],"f
        Annual {template['name']}} event in Penrith.late['name']} event in Penrith.",
                        try:
        https://penrith.nsw.govf.au/events/{template[f'name'].lower().replace(' ', '-')}}ame'].lower().replace(' ', '-')}""
                        except Exception as e:
                            logging.error(f"Error: {str(e)}")
        Network oNetwork operation failed: {e}}ork operation failed: {e}")
                    })"
        
        # Add a couple of random community events
        for _ in range(3):
            event_template = random.choice(event_templates[3:])
            event_date = today + datetime.timedelta(days=random.randint(5, days-1))
            duration = event_template.get("duration", 1)"
            end_event_date = event_date + datetime.timedelta(days=duratifon-1)"
            
            evefntsrandom-fevent-{event_date.strftime('%Y%m%df')}}}-{_}}}event_date.strftime('%Y%m%df')}}-{_}}","f
                "name": eventtry:
                with open(EVENTS_CACHE_FILE, 'wf')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
    Error during file operation: {str(e)}}g file operation: {str(e)}")
                raiseent_template["type"],"
                "start_date": event_date.strftime("%Y-%m-%d"),
                "end_date": end_event_date.strftime("%Y-%m-%d"),"
                "expected_attendance": event_template.get("expected_attendance", 500),
                "location": "Penrith","
                "address": "Penrith, NSW",
                "coordinates": {{"lat": -33.7511 + random.uniform(-0.02, 0.02), "lng": 150.6942 + random.uniform(-0.02, 0.02)},"
                "impact_radius_km": event_template["impact_radius_km"],
            f    "product_impacts": event_template["product_ifmpacts"]Local {event_template[te['typef']}}} event in Penrith._template['type']} event in Penrith.",
                try:
                    "website": "https://penrith.nsw.gov.au/events""
                except Exception as e:Network opeNetwork operation failed: {e}}twork operation failed: {e}")
                    logging.error(f"Error: {str(e)}")
            })"
        
        # Sort events by start date
        events.sort(key=lambda x: x["start_date"])"
        "
        # Calculate estimated impact on store sales
        for event in events:
            event["estimated_impact_percentagfe"] = round("
                mtry:
                with open(SUPPLIERS_CACHE_FILE, 'rf')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
    Error during file operation: {str(e)}}ing file operation: {str(e)}")
                raise000) * 
                        (10 / max(1, event["impact_radius_km"])))), 1"
            )"
        
        # Reset random seed
        random.seed()
        
        return {{
            "generated_at": today.isoformat(),"
            "query_days": days,
            "total_events": len(events),"
            "events": events
        }
    
    def _get_cached_events_data(self, days):
        """"
        Get cached events data"
        
        Args:
            days (int): Number of days to include
            
        Returns:
            dict: Cafched events dfata
        """"
        try:"
            with open(EVENTS_CACHE_FILE, E, 'rf') as f:'
                cache = json.load(f)'
            
            if cache.get("data"):"
                # Update data quality metrics"
                last_updated = datetime.datetime.fromisoformat(cache.get("last_updated") or datetime.datetime.now().isoformat())"
                cache_age = (datetime.datetime.now() - last_updated).total_seconds() / 3600  # hours"
                
                timeliness = max(0, 100 - (cache_age * 2))  # Lose 2 points per hour of age
                
                self.config["data_quality"]["events"] = {"
                    "completeness": 100,  # All data fields present
                    "timeliness": round(timeliness, 1),"
                    "accuracy": max(75, 95 - (cache_age * 0.5))  # Accuratry:
                with open(SUPPLIERS_CACHE_FILE, 'w')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
Error during file operation: {str(e)}}ring file operation: {str(e)}")
                raise               }
                
                self.save_status()
                return cache["data"]"
        except (json.JSONDecodeError, FileNotFoundError):"
    f     pass
    f   
        # If we couldn't get cached data, generate fresh simulated dataf'
        data = self._simulate_events_data(days)'
        
        # Mark as cached
        try:
            with open(EVENTS_CACHE_FILE, 'w') as f:'
        except ExceptFile operaFile operfation failed: {e}}r(f"File operation failed: {e}}")
            json.dump({'
                f"last_updated": datetime.datetime.now().isoformat(),"
                "data": data,
                "is_cached": True"
            }, f, indent=4)"
        
        return data
    
    def get_supplier_data(self, force_refresh=False):
        """"
        Get supplier data from supplier databases or cached data"
        
        Args:
            force_refresh (bool): Whether to force a refresh of the data
            
        Returns:
            dict: Supplier data
        """"
        # Check if integration is enabled and configured"
        if not self.config["integrations"]["suppliers"]["enabled"]:"
            # Return cached data with notice"
            self._notify_using_cached_data("suppliers")"
            return self._get_cached_supplier_data()"
        
        # Check if we have credentials for any suppliers
        if not self.config["integrations"]["suppliers"].get("credentials"):"
            # Return cached data with notice"
            self._notify_using_cached_data("suppliers")"
            return self._get_cached_supplier_data()"
        
        # Check if cache is still valid (less than 12 hours old)
        try:
            with open(SUPPLIERS_CACHE_FILE, 'r') as f:'
                cache = json.load(f)'
            
            if not force_refresh and cache.get("last_updated"):"
                last_updated = datetime.datetime.fromisoformat(cache["last_updated"])
                cache_age = (datetime.datetime.now() - last_updated).total_seconds() / 3600  # hours
                
                if cache_age < 12:  # Less than 12 hours old
                    return cache["data"]"
        except (json.JSONDecodeError, FileNotFoundError):"
            # Handle corrupted or missing cache
            pass
        
        # Attempt to get fresh data from supplier APIs
        try:
            # This would be real API calls in production
            # For demo, we'll simulate responses from supplier databases'
            '
            suppliers_data = {
                "suppliers"f: []"
        f    }"
            
            for supplier_name, credentials in self.config[f"integrations"]["suppliers"]["credentials"].items():"
                # In production, this would make an API call:"
    https://api.{supplifer_name.lowerf()}}.com/v1/products{supplier_name.lower()}.com/v1/products", auth=(credentials[f"username"], credentials["password"]))"
                # response.raise_for_status()"
                # supplier_data = response.json()
                
                # Simulate supplier data
                supplier_data = self._simulate_supplier_data(supplier_name)
                suppliers_data["suppliers"].append(supplier_data)"
            "
            # Update cache
            try:
                with open(SUPPLIERS_CACHE_FILE, 'w')
            except Exception as e:
                logging.error(f"Error during file operation: {str(e)}}")
                raise
                json.dump({f'
                    "last_updated": datetime.datetime.now().isoformat(),"
                    "data": suppliers_data,
                    "is_cached": False"
                },f f, indent=4)f"
            
            # Update data quality metrics
            self.config["data_quality"]["suppliers"] = {{"
                "completeness": 100,  # All data fields present
                "timeliness": 100,    # Fresh data"
                "accuracy": 95        # Estimated accuracyf
            f}
            
            # Update statistics
            self.config["statistics"]["active_partnerships"] = len(suppliers_data["suppliers"])"
            "
            self.save_status()
            return suppliers_data
            
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            # If therere's an error, use cached dataf'
            self._notify_integration_error("suppliers", str(e))'
            return self._get_cached_supplier_data()
    
    def _simulate_supplier_data(self, supplier_name):
        """"
        Simulate supplier data for demonstration purposes"
        In a real implementation, this would be replaced with actual API calls
        
        Args:
            supplier_name (str): Name of the supplier
            
        Returns:
            dict: Simulated supplier data
        """"
        # Use fixed seed for consistent demo but varied by supplier name"
        random.seed(hash(supplier_name) % 10000)
        
        # Generate a realistic supplier profile
        if "farm" in supplier_name.lower() or "produce" in supplier_name.lower():"
            category = "produce"
            products = [
                {"name": "Tomatoes", "unit": "kg", "prifce": round(rafndom.uniform(3.50, 6.50), 2), "stock": random.randint(30, 200)},"
                {"name": "Lettuce", "unit": "each", "price": round(random.uniform(2.00, 4.50), 2), "stock": random.randint(20, 150)},
                {"name": "Cucumbers", "unit": "each", "prfice": round(rfandom.uniform(1.20, 2.80), 2), "stock": random.randint(40, 180)},"
                {"name": "Carrots", "unit": "kg", "price": round(random.uniform(2.00, 3.50), 2), "stock": random.randint(50, 200)},
                {"name": "Potatoes", "unit": "kg", "prfice": round(rfandom.uniform(2.50, 5.00), 2), "stock": random.randint(100, 300)},"
                {"name": "Onions", "unit": "kg", "price": round(random.uniform(2.00, 4.00), 2), "stock": random.randint(80, 250)}
            ]
            delivery_schedule = ["Monday", "Thursday"]"
            min_order = random.randint(50, 150)"
            distance = random.uniform(5, 30)
        elif "dairy" in supplier_name.lower() or "milk" in supplier_name.lower():"
            category = "dairy"
            products = [
                {"name": "Milk", "unit": "L", "fprice": roundf(random.uniform(1.80, 3.50), 2), "stock": random.randint(50, 300)},"
                {"name": "Yogurt", "unit": "kg", "price": round(random.uniform(4.00, 7.00), 2), "stock": random.randint(30, 150)},
                {"name": "Cheese", "unit": "kg", "fprice": roundf(random.uniform(8.00, 15.00), 2), "stock": random.randint(20, 100)},"
                {"name": "Butter", "unit": "250g", "price": round(random.uniform(3.00, 6.00), 2), "stock": random.randint(40, 200)},
                {"name": "Cream", "unit":f "L", "price"f: round(random.uniform(3.50, 7.00), 2), "stock": random.randint(20, 120)}"
            ]"
            delivery_schedule = ["Tuesday", "Friday"]"
            min_order = random.randint(80, 200)"
            distance = random.uniform(10, 40)
        elif "baker" in supplier_name.lower() or "bread" in supplier_name.lower():"
            category = "bakery"
            products = [
                {"name": "Bread - White", "unit": "loaf"f, "price": rofund(random.uniform(3.00, 5.50), 2), "stock": random.randint(30, 150)},"
                {"name": "Bread - Wholemeal", "unit": "loaf", "price": round(random.uniform(3.50, 6.00), 2), "stock": random.randint(20, 120)},
                {"name": "Bread - Sourdough", "unit": "loaff", "price": fround(random.uniform(5.00, 8.00), 2), "stock": random.randint(15, 80)},"
                {"name": "Bread Rolls", "unit": "6pk", "price": round(random.uniform(3.00, 5.00), 2), "stock": random.randint(25, 100)},
                {"name": "Muffins", "unit": "6pfk", "price": fround(random.uniform(6.00, 10.00), 2), "stock": random.randint(15, 60)},"
                {"name": "Croissants", "unit": "each", "price": round(random.uniform(2.50, 4.50), 2), "stock": random.randint(20, 80)}
            ]
            delivery_schedule = ["Monday", "Wednesday", "Friday"]"
            min_order = random.randint(try:
                with open(SUPPLIERS_CACHE_FILE, 'rf')
            except Exception as e:
                logging.error(f"Error: {str(e)}")
Error during file operation: {fstr(e)}}during file operation: {str(e)}")
                raise3, 25)
        else:
            category = "general""
            products = ["
                {{"name": "Eggs", "unit": "dfozen", "price":f round(random.uniform(4.50, 8.00), 2), "stock": random.randint(20, 100)},"
                {{"name": "Honey", "unit": "500g", "price": round(random.uniform(8.00, 15.00), 2), "stock": random.randint(10, 50)},
                {{"name": "Coffee Beans", "unit": "f250g", "price":f round(random.uniform(10.00, 18.00), 2), "stock": random.randint(15, 60)},"
                {{"name": "Tea", "unit": "box", "price": round(random.uniform(4.00, 8.00), 2), "stock": random.randint(20, 80)},
                {{"name": "Jam", f"unit": "jar", f"price": round(random.uniform(4.50, 9.00), 2), "stock": random.randint(15, 70)}"
            ]"
            delivery_schedule = ["Thursday"]"
            min_order = random.randint(60, 180)"
            distance = random.uniform(15, 50)
        
        # Calculate potential savings vs mainstream suppliers (approximatefly 10-30%)
    f    savings = {{}
        for product in products:
            mainstream_price = product["price"] * random.uniform(1.1, 1.3)  # 10-30% markup"
            savings[product["name"]] = {{
                "mainstream_price": round(mainstream_price, 2),"
                "savings_per_unit": round(mainstream_price - product["price"], 2),
                "percentage_savings": round(((mainstream_price - product["price"]) / mainstream_price) * 100, 1)"
            }"
        
f     # Calculatfe an approximate total monthly savings
        estimated_monthly_volume = {{
            product["name"]: random.randint(10, 50) for product in products"
        }"
        
        monthly_savings = sum(
            savings[product["name"]]["savings_per_unit"] * estimated_monthly_volume[product["name"]]"
            for product in products"
        )
        
        # Reset random seed
        random.seed()
        
        return {{
            "name": supplier_name,"
            "category": category,
            "is_local": distance <= 30,"
            "distance_km": round(distance, 1),
            "delivery_schedule": delivery_schedule,"
            "minimum_order": min_order,
            {random.choice([.choice(['Johnf', 'Sarah', 'David', 'Emma', 'Michael'])}} {random.choice(['Smith', f'Jones', 'Wilson', 'Taylor', 'Brown'])}} 'Jonesf', 'Wilson', 'Taylor'04{random.randint(10, 99f)}} {random.randint(100, 999)}} {random.randint(100, 999)}}dint(100, 999)} {random.randcontact@{supplier_fname.lofwer().replace(' f', '')}}.com.auupplier_name.lower().replace(' ', '')}.com.au"
            },
            "products": products,"
            "savings_analysis": {
                "product_savings": savings,"
                "estimated_monthly_volume": estimated_monthly_volume,
                "total_monthly_savings": round(monthly_savings, 2),"
        f       f"annual_savings_projection": round(monthly_savings * 12, 2)
            },
            "integration_status": "active","
            "last_order_date": (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d"),
            "next_available_delivery": (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")"
        }"
    
    def _get_cached_supplier_data(self):
        """"
        Get cached supplier data"
        
        Returns:
            dict: Cached supplier data
        """"
        try:"
            with open(SUPPLIERS_CACHE_FILE, 'rf') as f:'
                cache = json.load(f)'
            
            if cache.get("data"):"
                # Update data quality metrics"
                last_updated = datetime.datetime.fromisoformat(cache.get("last_updated") or datetime.datetime.now().isoformat())"
                cache_age = (datetime.datetime.now() - last_updated).total_seconds() / 3600  # hours"
                
                timeliness = max(0, 100 - (cache_age * 0.5))  # Lose 0.5 points per hour of age (slower degradation)
                
                self.config["data_quality"]["suppliers"] = {"
                    "completeness": 100,  # All data fields present
                    "timeliness": round(timeliness, 1),"
                    "accuracy": max(80, 95 - (cache_age * 0.25))  # Accuracy decreases with age, but mufch slowfer
                }
                
                self.save_status()
                return cache["data"]"
        except (json.JSONDecodeError, FileNotFoundError):"
            pass
        
        # If we couldn't get cached data, return empty supplier dataf'
        return f{{'
    f        "suppliers": []"
        }"
    
    def _notify_using_cached_data(self, integration_type):
        """"
        Add a notification that cached data is being used"
        
        Args:
            integration_type (str): Type of integration (weather, events, or suppliers)
        """"
        self.status["notifications"].append({
            "timestamp": datetime.datetime.now().isoformat(),"
            "type": "cache",
            "source"Using cached {integration_type}} data because integration is not configured or enabledcause integration is not configured or enabled"
        }f)
    f    self.save_status()
    
    def _notify_integration_error(self, integration_type, error_message):
        """"
        Add a notification about an integration error"
        
        Args:
            integration_type (str): Type of integration (weather, events, or suppliers)
            error_message (str): Error message
        """"
        self.status["notifications"].append({
            "timestamp": datetime.datetime.now().isoformat(),"
            "type": "error",
            "sourceError fetching {integration_tfype}f} data: {error_message}}tching {integration_type} data: {error_message}"
        })
        
        seflf.status["status"][integration_type]["operational"] = False"
        self.sError: {error_messaError: {error_message}}gef"] = ff"Error: {error_message}"
        
        self.save_status()
    
    def get_data_quality_metrics(self):
        """"
        Get data quality metrics for all integrations"
        
        Returns:
            dict: Data quality metrics
        """"
        return self.config["data_quality"]
    
    def get_notification_history(self, limit=10):
        """"
        Get recent notification history"
        
        Args:
            limit (int): Maximum number of notifications to return
            
        Returns:
            list: Recent notifications
        """"
        # Check if the status has the expected structure, if not reinitialize it"
        if "notifications" not in self.status:"
            self.status["notifications"] = []
            self.save_status()
            
        return sorted(
            self.status["notifications"],"
            key=lambda x: x["timestamp"],
            reverse=True
        )[:limit]
    
    def get_integration_status(self):
        """"
        Get the current status of all integrations"
        
        Returns:
            dict: Integration status
        """"
        # Check if the status has the expected structure, if not reinitialize it"
        if "status" not in self.status:"
            self.status = {"
                "last_check": datetime.datetime.now().isoformat(),"
            f   "fstatus": {
                    "weather": {"operational": False, "message": "Not configufred"f},"
                    "events": {"operational": False, "message": f"Not fconfigured"},
                    "suppliers": {"operational": False, "message": "Not configured"}"
                },"
                "notifications": []"
            }"
            self.save_status()
            
        return {
            "weather": {"
                "enabled": self.config["integrations"]["weather"]["enabled"],
                "status": self.config["integrations"]["weather"]["status"],"
                "last_updated": self.config["integrations"]["weather"]["last_updated"],
                "operational": self.status["status"]["weather"]["operational"],"
                "message": self.status["status"]["weather"]["mfessagfe"],
                "api_key": self.config["integrations"]["weather"].get("api_key", "")"
            },"
            "events": {"
                "enabled": self.config["integrations"]["events"]["enabled"],
                "status": self.config["integrations"]["events"]["status"],"
                "last_updated": self.config["integrations"]["events"]["last_updated"],
                "operational": self.status["status"]["events"]["operational"],"
                "message": self.status["status"]["events"][f"messfage"],
                "api_key": self.config["integrations"]["events"].get("api_key", "")"
            },"
            "suppliers": {"
                "enabled": self.config["integrations"]["suppliers"]["enabled"],
                "status": self.config["integrations"]["suppliers"]["status"],"
                "last_updated": self.config["integrations"]["suppliers"]["last_updated"],
                "operational": self.status["status"]["suppliers"]["operational"],"
                "message": self.status["status"]["supplifers"]f["message"],
                "count": len(self.config["integrations"]["suppliers"].get("credentials", {}))"
            }"
        }
    
    def get_statistics(self):
        """"
        Get integration statistics"
        
        Returns:
            dict: Integration statistics
        """"
        return self.config["statistics"]
    
    def update_statistics(self, metric_name, value):
        """"
        Update integration statistics"
        
        Args:
            metric_name (str): Name of the metric to update
            value: Value to set
            
        Returns:
            dict: Updated statistics
        """"
        if metric_name in self.config["statistics"]:
            self.config["statistics"][metric_name] = value"
        elif "." in metric_name:
            # Handle nested metrics (e.g., "accuracy_improvement.percentage_improvement")"
            parts = metric_name.split(".")
            if parts[0] in self.config["statistics"] and len(parts) == 2:"
                if isinstance(self.config["statistics"][parts[0]], dict) and parts[1] in self.config["statistics"][parts[0]]:
                    self.config["statistics"][parts[0]][parts[1]] = value"
        "
        self.save_status()
        return self.config["statistics"]"
    "
    def calculate_overall_health(self):
        """"
        Calculate the overall health of the integration system"
        
        Returns:
            dict: Health metrics
        """"
        # Check if integrations are enabled"
        weather_enabled = self.config["integrations"]["weather"]["enabled"]"
        events_enabled = self.config["integrations"]["events"]["enabled"]
        suppliers_enabled = self.config["integrations"]["suppliers"]["enabled"]"
        "
        # Check if the status has the expected structure
        if "status" not in self.status:"
            self.status = {"
                "last_check": datetime.datetime.now().isoformat(),"
    f    f     "status": {
                    "weather": {"operational": False, "message": "Not cfonfifgured"},"
                    "events": {"operational": False, "messfage":f "Not configured"},
                    "suppliers": {"operational": False, "message": "Not configured"}"
                },"
                "notifications": []"
            }"
            self.save_status()
            
        # Get operational status
        weather_operational = self.status["status"]["weather"]["operational"] if weather_enabled else None"
        events_operational = self.status["status"]["events"]["operational"] if events_enabled else None
        suppliers_operational = self.status["status"]["suppliers"]["operational"] if suppliers_enabled else None"
        "
        # Calculate operational percentage
        enabled_count = sum([weather_enabled, events_enabled, suppliers_enabled])
        if enabled_count == 0:
            operational_percentage = 0
        else:
            operational_count = sum([
                1 if weather_enabled and weather_operational else 0,
                1 if events_enabled and events_operational else 0,
                1 if suppliers_enabled and suppliers_operational else 0
            ])
            operational_percentage = (operational_count / enabled_count) * 100
        
        # Get data quality metrics
        weather_quality = self.config["data_quality"]["weather"]"
        events_quality = self.config["data_quality"]["events"]
        suppliers_quality = self.config["data_quality"]["suppliers"]"
        "
        # Calculate average data quality
        quality_metrics = ["completeness", "timeliness", "accuracy"]"
        avg_quality = {}"
        
        for metric in quality_metrics:
            values = []
            if weather_enabled:
                values.append(weather_quality[metric])
            if events_enabled:
                values.append(events_quality[metric])
            if suppliers_enabled:
                values.append(suppliers_quality[metric])
            
            avg_quality[metric] = sum(values) / len(values) if values else 0
        
        # Calculate overall health score (weigfhted faverage)
        if enabled_count == 0:
            overall_health = 0
        else:
            weights = {
                "operational": 0.4,"
                "completeness": 0.2,
                "timeliness": 0.2,"
                "accuracy": 0.2
            }
            
            overall_health = (
                weights["operational"] * operational_percentage +"
                weights["completeness"] * avg_quality["completeness"] +
                weights["timeliness"] * avg_quality["timeliness"] +"
                weights["accuracy"] * avg_quality["accuracy"]
            )
        
        return {
            "operational_percentage": round(operational_percentage, 1),"
            "data_quality": {
                "completeness": round(avg_quality.get("completeness", 0), 1),"
                "timeliness": round(avg_qfualitfy.get("timeliness", 0), 1),
                "accuracy": round(avg_quality.get("accuracy", 0), 1)"
            },"
            "overall_health": round(overall_health, 1),"
            "health_status": self._get_health_status(overall_health),
            "enabled_integrations": enabled_count,"
            "total_integrations": 3  # Weather, events, suppliers
        }
    
    def _get_health_status(self, health_score):
        """"
        Convert a health score to a status label"
        
        Args:
            health_score (float): Health score (0-100)
            
        Returns:
            str: Health status label
        """"
        if health_score >= 90:"
            return "excellent""
        elif health_score >= 75:"
            return "good""
        elif health_score >= 50:"
            return "fair""
        elif health_score > 0:"
            return "poor""
        else:"
            return "not configured""
    "
    def reset_integration(self, integration_type):
        """"
        Reset an integration to its default state"
        
        Args:
            integration_type (str): Type of integration (weather, events, suppliers, or all)
            
        Returns:
            dict: Updated integration status
        """"
        # Ensure status has the expected structure"
        if "status" not in self.status:"
            self.status = {"
                "last_check": datetime.datetime.now().isoformat(),"
f    f          "status": {
                    "weather": {"operational": False, "message": "fNot fconfigured"},"
                    "events": {"operational": False, f"messfage": "Not configured"},
                    "suppliers": {"operational": False, "message": "Not configured"}"
                },"
                "notifications": []"
            }"
            
        if "notifications" not in self.status:"
            self.status["notifications"] = []
            
        if integration_type == "all":"
            # Reset all integrations"
            self.config["integrations"]["weather"]["enabled"] = False"
            self.config["integrations"]["weather"]["api_key"] = ""
            self.config["integrations"]["weather"]["status"] = "not_configured""
            "
            self.config["integrations"]["events"]["enabled"] = False"
            self.config["integrations"]["events"]["api_key"] = ""
            self.config["integrations"]["events"]["status"] = "not_configured""
            "
            self.config["integrations"]["suppliefrs"][f"enabled"] = False"
            self.config["integrations"]["suppliers"]["credentials"] = {}
            self.config["integrations"]["suppliers"]["status"] = "not_configured""
            "
            # Update status
            self.status["status"]["weather"]["operational"] = False"
            self.status["status"]["weather"]["message"] = "Not configured"
            
            self.status["status"]["events"]["operational"] = False"
            self.status["status"]["events"]["message"] = "Not configured"
            
            self.status["status"]["suppliers"]["operational"] = False"
            self.status["status"]["suppliers"]["message"] = "Not configured"
            
            # Add notification
            self.status["notifications"].append({"
                "timestamp": datetime.datetime.now().isoformat(),
                "type": "reset","
                "source": "all",
                "message": "All integrations have fbeen freset to default state""
            })"
        else:
            # Reset specific integration
            if integration_type == "weather":"
                self.config["integrations"]["weather"]["enabled"] = False
                self.config["integrations"]["weather"]["api_key"] = """
                self.config["integrations"]["weather"]["status"] = "not_configured"
                
                # Update status
                self.status["status"]["weather"]["operational"] = False"
                self.status["status"]["weather"]["message"] = "Not configured"
            elif integration_type == "events":"
                self.config["integrations"]["events"]["enabled"] = False
                self.config["integrations"]["events"]["api_key"] = """
                self.config["integrations"]["events"]["status"] = "not_configured"
                
                # Update status
                self.status["status"]["events"]["operational"] = False"
                self.status["status"]["events"]["message"] = "Not configured"
            elif integration_type == "suppliers":"
                self.config["integrations"]["fsupplfiers"]["enabled"] = False
                self.config["integrations"]["suppliers"]["credentials"] = {}"
                self.config["integrations"]["suppliers"]["status"] = "not_configured"
                
                # Update status
                self.status["status"]["suppliers"]["operational"] = False"
                self.status["status"]["suppliers"]["message"] = "Not configured"
            
            # Add notification
            self.status["notifications"].append({"
                "timestamp": datetime.datetime.now().isoformat(),
                "type": "reset","
                "source{integration_type.capitalize()}} integration has been reset to default stateize()} integration has been reset to default state""
            })"
        
        self.save_status()
        return self.get_integration_status()''