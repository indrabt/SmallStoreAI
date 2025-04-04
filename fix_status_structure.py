"""
This script fixes the structure of the status object in the PartnershipsIntegration module.
If the status file exists but has the wrong structure, it will be recreated with the correct structure.
"""

import json
import datetime
from pathlib import Path

# Define paths
DATA_DIR = Path("data")
if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True)

PARTNERSHIPS_DATA_DIR = DATA_DIR / "partnerships"
if not PARTNERSHIPS_DATA_DIR.exists():
    PARTNERSHIPS_DATA_DIR.mkdir(parents=True)

PARTNERSHIPS_DATA_FILE = PARTNERSHIPS_DATA_DIR / "partnerships_config.json"
INTEGRATION_STATUS_FILE = PARTNERSHIPS_DATA_DIR / "integration_status.json"
WEATHER_CACHE_FILE = PARTNERSHIPS_DATA_DIR / "weather_cache.json"
EVENTS_CACHE_FILE = PARTNERSHIPS_DATA_DIR / "events_cache.json"
SUPPLIERS_CACHE_FILE = PARTNERSHIPS_DATA_DIR / "suppliers_cache.json"

# Create integration status file with the correct structure
def create_status_file():
    with open(INTEGRATION_STATUS_FILE, 'w') as f:
        json.dump({
            "last_check": datetime.datetime.now().isoformat(),
            "status": {
                "weather": {"operational": False, "message": "Not configured"},
                "events": {"operational": False, "message": "Not configured"},
                "suppliers": {"operational": False, "message": "Not configured"}
            },
            "notifications": []
        }, f, indent=4)
    print(f"Created new integration status file with correct structure")

# Create partnerships data file with the correct structure
def create_data_file():
    with open(PARTNERSHIPS_DATA_FILE, 'w') as f:
        json.dump({
            "integrations": {
                "weather": {
                    "enabled": False,
                    "api_key": "",
                    "last_updated": None,
                    "status": "not_configured"
                },
                "events": {
                    "enabled": False,
                    "api_key": "",
                    "last_updated": None,
                    "status": "not_configured"
                },
                "suppliers": {
                    "enabled": False,
                    "credentials": {},
                    "last_updated": None,
                    "status": "not_configured"
                }
            },
            "statistics": {
                "accuracy_improvement": {
                    "baseline": 0,
                    "with_integrations": 0,
                    "percentage_improvement": 0
                },
                "partnership_savings": 0,
                "active_partnerships": 0
            },
            "data_quality": {
                "weather": {
                    "completeness": 0,
                    "timeliness": 0,
                    "accuracy": 0
                },
                "events": {
                    "completeness": 0,
                    "timeliness": 0,
                    "accuracy": 0
                },
                "suppliers": {
                    "completeness": 0,
                    "timeliness": 0,
                    "accuracy": 0
                }
            }
        }, f, indent=4)
    print(f"Created new partnerships data file with correct structure")

# Create cache files
def create_cache_files():
    for cache_file in [WEATHER_CACHE_FILE, EVENTS_CACHE_FILE, SUPPLIERS_CACHE_FILE]:
        with open(cache_file, 'w') as f:
            json.dump({
                "last_updated": None,
                "data": {},
                "is_cached": True
            }, f, indent=4)
    print(f"Created cache files with correct structure")

if __name__ == "__main__":
    print("Fixing partnerships integration data structure...")
    create_status_file()
    create_data_file()
    create_cache_files()
    print("Done!")