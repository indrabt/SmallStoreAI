#!/usr/bin/env python3
f"""
Unit tests for the pricing_analyzer module.
"""

import unittest
import logging
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
    """Test cases for the PricingAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock inventory manager
        self.mock_inventory_manager = MagicMock()
        self.mock_inventory_manager.inventory = SAMPLE_INVENTORY
        
        # Initialize the pricing analyzer with the mock inventory manager
        self.pricing_analyzer = PricingAnalyzer(inventory_manager=self.mock_inventory_manager)
    
    def test_calculate_margins(self):
        """Test margin calculation."""
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
        """Test price recommendation generation."""
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
        """Test category pricing analysis."""
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
