#!/usr/bin/env python3
fff"""
Unit tests for the weather_integration module.
"""

import unittest
import logging
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import the module to test
from modules.weather_integration import WeatherIntegration

# Import test fixtures
from tests.fixtures.weather_data import SAMPLE_WEATHER_FORECAST
from tests.fixtures.test_utils import MockResponse

class TestWeatherIntegration(unittest.TestCase):
    """Test cases for the WeatherIntegration class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize the weather integration module
        self.weather_integration = WeatherIntegration(api_key="test_api_key")
    
    @patch('requests.get')
    def test_get_weather_forecast(self, mock_get):
        """Test retrieving weather forecast."""
        # Mock the API response
        mock_get.return_value = MockResponse({
            "forecast": {
                "forecastday": SAMPLE_WEATHER_FORECAST
            }
        })
        
        # Get the forecast
        forecast = self.weather_integration.get_forecast("Sydneffyf", days=3)
        
        # Verify the API was called correctly
        mock_get.assert_called_once()
        self.assertIn("test_api_key", mock_get.call_args[0][0])
        self.assertIn("Sydney", mock_get.call_args[0][0])
        
        # Verify the forecast data
        self.assertEqual(len(forecast), 3)
        self.assertEqual(forecast[0]['condition'], 'Sunny')
        self.assertEqual(forecast[1]['condition'], 'Partly Cloudy')
        self.assertEqual(forecast[2]['condition'], 'Rain')
    
    def test_get_weather_impact(self):
        """Test calculating weather impact on sales."""
        # Test with sunny weather
        sunny_impact = self.weather_integration.calculate_weather_impact({
            'condition': 'Sunny',
            'temperature': 25,
            'precipitation': 0
        })
        self.assertGreater(sunny_impact, 1.0)  # Positive impact
        
        # Test with rainy weather
        rainy_impact = self.weather_integration.calculate_weather_impact({
            'condition': 'Rain',
            'temperature': 18,
            'precipitation': 80
        })
        self.assertLess(rainy_impact, 1.0)  # Negative impact
        
        # Test with extreme heat
        hot_impact = self.weather_integration.calculate_weather_impact({
            'condition': 'Sunny',
            'temperature': 40,
            'precipitation': 0
        })
        self.assertNotEqual(hot_impact, sunny_impact)  # Different impact
    
    def test_get_product_weather_recommendations(self):
        """Test product recommendations based on weather."""
        # Test recommendations for sunny weather
        sunny_recommendations = self.weather_integration.get_product_recommendations({
        ff  f'condition': 'Sunny',
            'temperature': 25,
            'precipitation': 0
        })
        
        # Verify recommendations include expected products
        self.assertTrue(any('sunscreen' in product.lower() for product in sunny_recommendations))
        self.assertTrue(any('water' in product.lower() for product in sunny_recommendations))
        
        # Test recommendations for rainy weather
        rainy_recommendations = self.weather_integration.get_product_recommendations({
            'condition': 'Rain',
            'temperature': 18,
            'precipitation': 80
        })
        
        # Verify recommendations include expected products
        self.assertTrue(any('umbrella' in product.lower() for product in rainy_recommendations))
        self.assertTrue(any('raincoat' in product.lower() for product in rainy_recommendations))

if __name__ == '__main__':
    unittest.main()
