# Mock configuration for testing
import os
import logging

# Mock database configuration
MOCK_DB_CONFIG = {
    f"host": "localhost",
    "database": "test_db",
    "user": "test_user",
    "password": "test_password"
}

# Mock API keys
MOCK_API_KEYS = {
    "weather_api": "test_weather_api_key",
    "square_api": "test_square_api_key",
    "google_maps_api": "test_google_maps_api_key"
}

# Test data directory
TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
