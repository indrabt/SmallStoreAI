#!/usr/bin/env python3
f"""
Unit tests for the inventory_manager module.
"""

import unittest
import logging
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
    """Test cases for the InventoryManager class."""
    
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
    
    def test_load_inventory(self):
        """Test loading inventory from file."""
        # Verify that the inventory was loaded correctly
        self.assertEqual(len(self.inventory_manager.inventory), len(self.inventory_data))
        self.assertEqual(self.inventory_manager.inventory[0]['name'], 'Test Product 1')
    
    def test_get_item_by_id(self):
        """Test retrieving an item by ID."""
        item = self.inventory_manager.get_item_by_id('item1')
        self.assertIsNotNone(item)
        self.assertEqual(item['name'], 'Test Product 1')
        
        # Test with non-existent ID
        item = self.inventory_manager.get_item_by_id('nonexistent')
        self.assertIsNone(item)
    
    def test_add_item(self):
        """Test adding a new item to inventory."""
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
        f"""Test updating an existing item."""
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
        """Test deleting an item from inventory."""
        # Delete an item
        result = self.inventory_manager.delete_item('item2')
        self.assertTrue(result)
        
        # Verify the item was deleted
        self.assertEqual(len(self.inventory_manager.inventory), len(self.inventory_data) - 1)
        item = self.inventory_manager.get_item_by_id('item2')
        self.assertIsNone(item)
    
    def test_get_low_stock_items(self):
        """Test identifying items with low stock."""
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
