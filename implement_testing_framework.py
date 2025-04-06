#!/usr/bin/env python3
"""
Testing framework implementation for SmallStoreAI repository.
This script creates a basic testing structure and implements unit tests for core functionality.
"""

import os
import sys
import shutil
from pathlib import Path

def create_test_directory(directory):
    """Create a tests directory structure."""
    tests_dir = os.path.join(directory, 'tests')
    os.makedirs(tests_dir, exist_ok=True)
    
    # Create __init__.py to make the tests directory a package
    init_path = os.path.join(tests_dir, '__init__.py')
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write('# Tests package for SmallStoreAI\n')
    
    # Create subdirectories for different test types
    unit_tests_dir = os.path.join(tests_dir, 'unit')
    integration_tests_dir = os.path.join(tests_dir, 'integration')
    fixtures_dir = os.path.join(tests_dir, 'fixtures')
    
    os.makedirs(unit_tests_dir, exist_ok=True)
    os.makedirs(integration_tests_dir, exist_ok=True)
    os.makedirs(fixtures_dir, exist_ok=True)
    
    # Create __init__.py files for subdirectories
    for subdir in [unit_tests_dir, integration_tests_dir, fixtures_dir]:
        with open(os.path.join(subdir, '__init__.py'), 'w', encoding='utf-8') as f:
            f.write(f'# {os.path.basename(subdir)} package for SmallStoreAI tests\n')
    
    print(f"Created test directory structure at {tests_dir}")
    return tests_dir, unit_tests_dir, integration_tests_dir, fixtures_dir

def create_test_fixtures(fixtures_dir):
    """Create test fixtures for common test scenarios."""
    # Create sample inventory data
    inventory_fixture = os.path.join(fixtures_dir, 'inventory_data.py')
    with open(inventory_fixture, 'w', encoding='utf-8') as f:
        f.write("""# Sample inventory data for testing
SAMPLE_INVENTORY = [
    {
        "id": "item1",
        "name": "Test Product 1",
        "category": "Grocery",
        "price": 9.99,
        "cost": 5.50,
        "quantity": 100,
        "reorder_point": 20,
        "supplier": "Test Supplier"
    },
    {
        "id": "item2",
        "name": "Test Product 2",
        "category": "Dairy",
        "price": 4.99,
        "cost": 2.75,
        "quantity": 50,
        "reorder_point": 10,
        "supplier": "Test Supplier"
    },
    {
        "id": "item3",
        "name": "Test Product 3",
        "category": "Produce",
        "price": 2.99,
        "cost": 1.50,
        "quantity": 75,
        "reorder_point": 15,
        "supplier": "Another Supplier",
        "expiry_date": "2025-12-31"
    }
]
""")
    
    # Create sample supplier data
    supplier_fixture = os.path.join(fixtures_dir, 'supplier_data.py')
    with open(supplier_fixture, 'w', encoding='utf-8') as f:
        f.write("""# Sample supplier data for testing
SAMPLE_SUPPLIERS = [
    {
        "id": "supplier1",
        "name": "Test Supplier",
        "contact": "test@supplier.com",
        "phone": "555-1234",
        "address": "123 Test St, Test City",
        "categories": ["Grocery", "Dairy"],
        "lead_time_days": 3
    },
    {
        "id": "supplier2",
        "name": "Another Supplier",
        "contact": "info@anothersupplier.com",
        "phone": "555-5678",
        "address": "456 Test Ave, Test City",
        "categories": ["Produce"],
        "lead_time_days": 1
    }
]
""")
    
    # Create sample weather data
    weather_fixture = os.path.join(fixtures_dir, 'weather_data.py')
    with open(weather_fixture, 'w', encoding='utf-8') as f:
        f.write("""# Sample weather data for testing
SAMPLE_WEATHER_FORECAST = [
    {
        "date": "2025-04-07",
        "condition": "Sunny",
        "temperature": 25,
        "precipitation": 0
    },
    {
        "date": "2025-04-08",
        "condition": "Partly Cloudy",
        "temperature": 22,
        "precipitation": 10
    },
    {
        "date": "2025-04-09",
        "condition": "Rain",
        "temperature": 18,
        "precipitation": 80
    }
]
""")
    
    # Create mock configuration
    config_fixture = os.path.join(fixtures_dir, 'mock_config.py')
    with open(config_fixture, 'w', encoding='utf-8') as f:
        f.write("""# Mock configuration for testing
import os

# Mock database configuration
MOCK_DB_CONFIG = {
    "host": "localhost",
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
""")
    
    # Create a helper module for tests
    test_utils = os.path.join(fixtures_dir, 'test_utils.py')
    with open(test_utils, 'w', encoding='utf-8') as f:
        f.write("""# Utility functions for tests
import os
import json
import tempfile
from contextlib import contextmanager

@contextmanager
def temp_file_with_content(content, suffix='.json'):
    \"\"\"Create a temporary file with the given content.\"\"\"
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        yield path
    finally:
        os.unlink(path)

def create_test_json_file(data):
    \"\"\"Create a temporary JSON file with the given data.\"\"\"
    with temp_file_with_content(json.dumps(data)) as path:
        return path

class MockResponse:
    \"\"\"Mock response object for API testing.\"\"\"
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code
        self.text = json.dumps(json_data)
    
    def json(self):
        return self.json_data
""")
    
    print(f"Created test fixtures in {fixtures_dir}")
    return True

def create_unit_tests(unit_tests_dir, module_name):
    """Create unit tests for a specific module."""
    # Determine the appropriate test file name
    test_file = os.path.join(unit_tests_dir, f"test_{module_name}.py")
    
    # Create different test templates based on the module
    if module_name == "inventory_manager":
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("""#!/usr/bin/env python3
\"\"\"
Unit tests for the inventory_manager module.
\"\"\"

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import the module to test
from modules.inventory_manager import InventoryManager

# Import test fixtures
from tests.fixtures.inventory_data import SAMPLE_INVENTORY
from tests.fixtures.test_utils import temp_file_with_content

class TestInventoryManager(unittest.TestCase):
    \"\"\"Test cases for the InventoryManager class.\"\"\"
    
    def setUp(self):
        \"\"\"Set up test fixtures.\"\"\"
        # Create a temporary inventory file
        self.inventory_data = SAMPLE_INVENTORY
        self.inventory_json = json.dumps(self.inventory_data)
        
        # Create a mock inventory file path
        with temp_file_with_content(self.inventory_json) as path:
            self.inventory_file = path
            # Initialize the inventory manager with the test file
            self.inventory_manager = InventoryManager(inventory_file=self.inventory_file)
    
    def test_load_inventory(self):
        \"\"\"Test loading inventory from file.\"\"\"
        # Verify that the inventory was loaded correctly
        self.assertEqual(len(self.inventory_manager.inventory), len(self.inventory_data))
        self.assertEqual(self.inventory_manager.inventory[0]['name'], 'Test Product 1')
    
    def test_get_item_by_id(self):
        \"\"\"Test retrieving an item by ID.\"\"\"
        item = self.inventory_manager.get_item_by_id('item1')
        self.assertIsNotNone(item)
        self.assertEqual(item['name'], 'Test Product 1')
        
        # Test with non-existent ID
        item = self.inventory_manager.get_item_by_id('nonexistent')
        self.assertIsNone(item)
    
    def test_add_item(self):
        \"\"\"Test adding a new item to inventory.\"\"\"
        new_item = {
            "id": "item4",
            "name": "Test Product 4",
            "category": "Beverages",
            "price": 3.99,
            "cost": 2.00,
            "quantity": 30,
            "reorder_point": 5,
            "supplier": "Test Supplier"
        }
        
        # Add the item
        result = self.inventory_manager.add_item(new_item)
        self.assertTrue(result)
        
        # Verify the item was added
        self.assertEqual(len(self.inventory_manager.inventory), len(self.inventory_data) + 1)
        
        # Retrieve the added item
        added_item = self.inventory_manager.get_item_by_id('item4')
        self.assertIsNotNone(added_item)
        self.assertEqual(added_item['name'], 'Test Product 4')
    
    def test_update_item(self):
        \"\"\"Test updating an existing item.\"\"\"
        # Update an item
        updated_item = {
            "id": "item1",
            "name": "Updated Product 1",
            "category": "Grocery",
            "price": 10.99,
            "cost": 6.00,
            "quantity": 90,
            "reorder_point": 25,
            "supplier": "Test Supplier"
        }
        
        result = self.inventory_manager.update_item(updated_item)
        self.assertTrue(result)
        
        # Verify the item was updated
        item = self.inventory_manager.get_item_by_id('item1')
        self.assertEqual(item['name'], 'Updated Product 1')
        self.assertEqual(item['price'], 10.99)
    
    def test_delete_item(self):
        \"\"\"Test deleting an item from inventory.\"\"\"
        # Delete an item
        result = self.inventory_manager.delete_item('item2')
        self.assertTrue(result)
        
        # Verify the item was deleted
        self.assertEqual(len(self.inventory_manager.inventory), len(self.inventory_data) - 1)
        item = self.inventory_manager.get_item_by_id('item2')
        self.assertIsNone(item)
    
    def test_get_low_stock_items(self):
        \"\"\"Test identifying items with low stock.\"\"\"
        # Modify an item to have low stock
        item = self.inventory_manager.get_item_by_id('item1')
        item['quantity'] = 10  # Below reorder point of 20
        self.inventory_manager.update_item(item)
        
        # Get low stock items
        low_stock = self.inventory_manager.get_low_stock_items()
        self.assertEqual(len(low_stock), 1)
        self.assertEqual(low_stock[0]['id'], 'item1')

if __name__ == '__main__':
    unittest.main()
""")
    elif module_name == "pricing_analyzer":
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("""#!/usr/bin/env python3
\"\"\"
Unit tests for the pricing_analyzer module.
\"\"\"

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import the module to test
from modules.pricing_analyzer import PricingAnalyzer

# Import test fixtures
from tests.fixtures.inventory_data import SAMPLE_INVENTORY

class TestPricingAnalyzer(unittest.TestCase):
    \"\"\"Test cases for the PricingAnalyzer class.\"\"\"
    
    def setUp(self):
        \"\"\"Set up test fixtures.\"\"\"
        # Create a mock inventory manager
        self.mock_inventory_manager = MagicMock()
        self.mock_inventory_manager.inventory = SAMPLE_INVENTORY
        
        # Initialize the pricing analyzer with the mock inventory manager
        self.pricing_analyzer = PricingAnalyzer(inventory_manager=self.mock_inventory_manager)
    
    def test_calculate_margins(self):
        \"\"\"Test margin calculation.\"\"\"
        # Calculate margins for all products
        margins = self.pricing_analyzer.calculate_margins()
        
        # Verify margins are calculated correctly
        self.assertEqual(len(margins), len(SAMPLE_INVENTORY))
        
        # Check specific margin calculations
        # Margin = (price - cost) / price * 100
        expected_margin_1 = (9.99 - 5.50) / 9.99 * 100  # ~44.94%
        self.assertAlmostEqual(margins[0]['margin'], expected_margin_1, places=2)
        
        expected_margin_2 = (4.99 - 2.75) / 4.99 * 100  # ~44.89%
        self.assertAlmostEqual(margins[1]['margin'], expected_margin_2, places=2)
    
    def test_get_price_recommendations(self):
        \"\"\"Test price recommendation generation.\"\"\"
        # Mock competitor prices
        competitor_prices = {
            'Test Product 1': 11.99,
            'Test Product 2': 4.49,
            'Test Product 3': 3.49
        }
        
        # Patch the method that would normally fetch competitor prices
        with patch.object(self.pricing_analyzer, 'get_competitor_prices', return_value=competitor_prices):
            recommendations = self.pricing_analyzer.get_price_recommendations()
            
            # Verify recommendations are generated for all products
            self.assertEqual(len(recommendations), len(SAMPLE_INVENTORY))
            
            # Check specific recommendations
            # Product 1 is priced lower than competitor, should recommend increase
            self.assertGreater(recommendations[0]['suggested_price'], SAMPLE_INVENTORY[0]['price'])
            
            # Product 2 is priced higher than competitor, should recommend decrease
            self.assertLess(recommendations[1]['suggested_price'], SAMPLE_INVENTORY[1]['price'])
            
            # Product 3 is priced lower than competitor, should recommend increase
            self.assertGreater(recommendations[2]['suggested_price'], SAMPLE_INVENTORY[2]['price'])
    
    def test_analyze_category_pricing(self):
        \"\"\"Test category pricing analysis.\"\"\"
        # Analyze pricing by category
        category_analysis = self.pricing_analyzer.analyze_category_pricing()
        
        # Verify analysis includes all categories
        categories = set(item['category'] for item in SAMPLE_INVENTORY)
        self.assertEqual(len(category_analysis), len(categories))
        
        # Check that each category has the correct metrics
        for category in category_analysis:
            self.assertIn('category', category)
            self.assertIn('avg_price', category)
            self.assertIn('avg_margin', category)
            self.assertIn('item_count', category)

if __name__ == '__main__':
    unittest.main()
""")
    elif module_name == "weather_integration":
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("""#!/usr/bin/env python3
\"\"\"
Unit tests for the weather_integration module.
\"\"\"

import unittest
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
    \"\"\"Test cases for the WeatherIntegration class.\"\"\"
    
    def setUp(self):
        \"\"\"Set up test fixtures.\"\"\"
        # Initialize the weather integration module
        self.weather_integration = WeatherIntegration(api_key="test_api_key")
    
    @patch('requests.get')
    def test_get_weather_forecast(self, mock_get):
        \"\"\"Test retrieving weather forecast.\"\"\"
        # Mock the API response
        mock_get.return_value = MockResponse({
            "forecast": {
                "forecastday": SAMPLE_WEATHER_FORECAST
            }
        })
        
        # Get the forecast
        forecast = self.weather_integration.get_forecast("Sydney", days=3)
        
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
        \"\"\"Test calculating weather impact on sales.\"\"\"
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
        \"\"\"Test product recommendations based on weather.\"\"\"
        # Test recommendations for sunny weather
        sunny_recommendations = self.weather_integration.get_product_recommendations({
            'condition': 'Sunny',
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
""")
    else:
        # Generic test template for other modules
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(f"""#!/usr/bin/env python3
\"\"\"
Unit tests for the {module_name} module.
\"\"\"

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import the module to test
try:
    from modules.{module_name} import *
except ImportError:
    print(f"Could not import {module_name} module. Make sure it exists and is importable.")
    sys.exit(1)

class Test{module_name.title().replace('_', '')}(unittest.TestCase):
    \"\"\"Test cases for the {module_name} module.\"\"\"
    
    def setUp(self):
        \"\"\"Set up test fixtures.\"\"\"
        # Initialize any objects needed for testing
        pass
    
    def test_example(self):
        \"\"\"Example test case.\"\"\"
        # Replace with actual tests for the module
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
""")
    
    print(f"Created unit test for {module_name} at {test_file}")
    return True

def create_integration_tests(integration_tests_dir):
    """Create integration tests for key module interactions."""
    # Create an integration test for inventory and pricing
    inventory_pricing_test = os.path.join(integration_tests_dir, "test_inventory_pricing_integration.py")
    with open(inventory_pricing_test, 'w', encoding='utf-8') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"
Integration tests for inventory and pricing modules.
\"\"\"

import unittest
import sys
import os
import json
import tempfile
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import the modules to test
from modules.inventory_manager import InventoryManager
from modules.pricing_analyzer import PricingAnalyzer
from modules.pricing_assistant import PricingAssistant

# Import test fixtures
from tests.fixtures.inventory_data import SAMPLE_INVENTORY
from tests.fixtures.test_utils import temp_file_with_content

class TestInventoryPricingIntegration(unittest.TestCase):
    \"\"\"Integration tests for inventory and pricing modules.\"\"\"
    
    def setUp(self):
        \"\"\"Set up test fixtures.\"\"\"
        # Create a temporary inventory file
        self.inventory_data = SAMPLE_INVENTORY
        self.inventory_json = json.dumps(self.inventory_data)
        
        # Create a mock inventory file path
        with temp_file_with_content(self.inventory_json) as path:
            self.inventory_file = path
            # Initialize the inventory manager with the test file
            self.inventory_manager = InventoryManager(inventory_file=self.inventory_file)
            
            # Initialize the pricing analyzer with the inventory manager
            self.pricing_analyzer = PricingAnalyzer(inventory_manager=self.inventory_manager)
            
            # Initialize the pricing assistant with both components
            self.pricing_assistant = PricingAssistant(
                inventory_manager=self.inventory_manager,
                pricing_analyzer=self.pricing_analyzer
            )
    
    def test_price_update_flow(self):
        \"\"\"Test the complete flow of updating a product price.\"\"\"
        # Get the original price
        item_id = 'item1'
        original_item = self.inventory_manager.get_item_by_id(item_id)
        original_price = original_item['price']
        
        # Generate a price recommendation
        with patch.object(self.pricing_analyzer, 'get_competitor_prices', return_value={
            'Test Product 1': 11.99,
            'Test Product 2': 4.49,
            'Test Product 3': 3.49
        }):
            recommendations = self.pricing_analyzer.get_price_recommendations()
            
            # Find the recommendation for our item
            item_recommendation = next(r for r in recommendations if r['id'] == item_id)
            new_price = item_recommendation['suggested_price']
            
            # Apply the price update
            self.pricing_assistant.update_price(item_id, new_price)
            
            # Verify the price was updated in the inventory
            updated_item = self.inventory_manager.get_item_by_id(item_id)
            self.assertEqual(updated_item['price'], new_price)
            self.assertNotEqual(updated_item['price'], original_price)
    
    def test_margin_analysis_flow(self):
        \"\"\"Test the flow of analyzing margins and making adjustments.\"\"\"
        # Calculate initial margins
        initial_margins = self.pricing_analyzer.calculate_margins()
        
        # Find the item with the lowest margin
        lowest_margin_item = min(initial_margins, key=lambda x: x['margin'])
        item_id = lowest_margin_item['id']
        
        # Increase the price to improve the margin
        item = self.inventory_manager.get_item_by_id(item_id)
        new_price = item['price'] * 1.1  # 10% increase
        
        self.pricing_assistant.update_price(item_id, new_price)
        
        # Recalculate margins
        updated_margins = self.pricing_analyzer.calculate_margins()
        
        # Find the updated margin for our item
        updated_item_margin = next(m for m in updated_margins if m['id'] == item_id)
        
        # Verify the margin improved
        self.assertGreater(updated_item_margin['margin'], lowest_margin_item['margin'])

if __name__ == '__main__':
    unittest.main()
""")
    
    # Create an integration test for weather and demand prediction
    weather_demand_test = os.path.join(integration_tests_dir, "test_weather_demand_integration.py")
    with open(weather_demand_test, 'w', encoding='utf-8') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"
Integration tests for weather and demand prediction modules.
\"\"\"

import unittest
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
    \"\"\"Integration tests for weather and demand prediction modules.\"\"\"
    
    def setUp(self):
        \"\"\"Set up test fixtures.\"\"\"
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
        \"\"\"Test demand prediction with weather adjustments.\"\"\"
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
        \"\"\"Test demand prediction by product category.\"\"\"
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
""")
    
    print(f"Created integration tests in {integration_tests_dir}")
    return True

def create_pytest_config(directory):
    """Create pytest configuration file."""
    pytest_ini = os.path.join(directory, 'pytest.ini')
    with open(pytest_ini, 'w', encoding='utf-8') as f:
        f.write("""[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v
""")
    
    print(f"Created pytest configuration at {pytest_ini}")
    return True

def create_test_requirements(directory):
    """Create test requirements file."""
    test_requirements = os.path.join(directory, 'test_requirements.txt')
    with open(test_requirements, 'w', encoding='utf-8') as f:
        f.write("""# Test dependencies
pytest==7.3.1
pytest-cov==4.1.0
mock==5.0.2
coverage==7.2.7
""")
    
    print(f"Created test requirements at {test_requirements}")
    return True

def implement_testing_framework(directory):
    """Implement a testing framework for the SmallStoreAI repository."""
    # Create the test directory structure
    tests_dir, unit_tests_dir, integration_tests_dir, fixtures_dir = create_test_directory(directory)
    
    # Create test fixtures
    create_test_fixtures(fixtures_dir)
    
    # Create unit tests for key modules
    key_modules = ['inventory_manager', 'pricing_analyzer', 'weather_integration']
    for module in key_modules:
        create_unit_tests(unit_tests_dir, module)
    
    # Create integration tests
    create_integration_tests(integration_tests_dir)
    
    # Create pytest configuration
    create_pytest_config(directory)
    
    # Create test requirements file
    create_test_requirements(directory)
    
    print(f"Successfully implemented testing framework in {directory}")
    return True

def main():
    """Main function to run the testing framework implementation script."""
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Default to the current directory
        directory = os.getcwd()
    
    print(f"Implementing testing framework in {directory}...")
    success = implement_testing_framework(directory)
    
    if success:
        print("Testing framework implementation completed successfully.")
    else:
        print("Failed to implement testing framework.")

if __name__ == "__main__":
    main()
