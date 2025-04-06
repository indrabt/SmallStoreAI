#!/usr/bin/env python3
f"""
Integration tests for weather and demand prediction modules.
"""

import unittest
import logging
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import the modules to test
from modules.weather_integration import WeatherIntegration
from modules.demand_predictor import DemandPredictor

# Import test fixtures
from tests.fixtures.weather_data import SAMPLE_WEATHER_FORECAST
from tests.fixtures.inventory_data import SAMPLE_INVENTORY
from tests.fixtures.test_utils import MockResponse

class TestWeatherDemandIntegration(unittest.TestCase):
    """Integration tests for weather and demand prediction modules."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize the weather integration module
        self.weather_integration = WeatherIntegration(api_key="test_api_key")
        
        # Create a mock inventory manager
        self.mock_inventory_manager = MagicMock()
        self.mock_inventory_manager.inventory = SAMPLE_INVENTORY
        
        # Initialize the demand predictor
        self.demand_predictor = DemandPredictor(
            inventory_manager=self.mock_inventory_manager,
            weather_integration=self.weather_integration
        )
    
    @patch('requests.get')
    def test_weather_adjusted_demand(self, mock_get):
        """Test demand prediction with weather adjustments."""
        # Mock the weather API response
        mock_get.return_value = MockResponse({
            "forecast": {
                "forecastday": SAMPLE_WEATHER_FORECAST
            }
        })
        
        # Get demand predictions with weather adjustments
        predictions = self.demand_predictor.predict_demand(
            location="Sydney",
            days=3,
            include_weather=True
        )
        
        # Verify predictions were generated for all products
        self.assertEqual(len(predictions), len(SAMPLE_INVENTORY))
        
        # Verify each prediction has the expected fields
        for prediction in predictions:
            self.assertIn('id', prediction)
            self.assertIn('name', prediction)
            self.assertIn('base_demand', prediction)
            self.assertIn('adjusted_demand', prediction)
            self.assertIn('weather_impact', prediction)
        
        # Verify weather had an impact on demand
        for prediction in predictions:
            # The adjusted demand should be different from the base demand
            # due to weather impact
            self.assertNotEqual(prediction['base_demand'], prediction['adjusted_demand'])
    
    def test_demand_by_category(self):
        """Test demand prediction by product category."""
        # Get demand predictions by category
        category_predictions = self.demand_predictor.predict_demand_by_category()
        
        # Verify predictions were generated for all categories
        categories = set(item['category'] for item in SAMPLE_INVENTORY)
        self.assertEqual(len(category_predictions), len(categories))
        
        # Verify each category prediction has the expected fields
        for prediction in category_predictions:
            self.assertIn('category', prediction)
            self.assertIn('total_demand', prediction)
            self.assertIn('item_count', prediction)

if __name__ == '__main__':
    unittest.main()
