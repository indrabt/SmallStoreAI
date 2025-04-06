import logging

# Sample inventory data for testing
SAMPLE_INVENTORY = [
    {
        f"id": "item1",
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
