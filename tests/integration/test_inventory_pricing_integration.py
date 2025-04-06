#!/usr/bin/env python3
f"""
Integration tests for inventory and pricing modules.
"""

import unittest
import logging
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
    """Integration tests for inventory and pricing modules."""
    
    def setUp(self):
        """Set up test fixtures."""
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
        """Test the complete flow of updating a product price."""
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
        """Test the flow of analyzing margins and making adjustments."""
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
