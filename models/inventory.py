from datetime import datetime
import uuid

class InventoryItem:
    """
    Model class representing an inventory item
    """
    
    def __init__(self, name, category, supplier, quantity, cost_price, selling_price, 
                reorder_point=None, id=None, last_updated=None):
        """
        Initialize a new inventory item
        
        Args:
            name (str): Product name
            category (str): Product category
            supplier (str): Supplier name
            quantity (int): Current quantity in stock
            cost_price (float): Cost price per unit
            selling_price (float): Selling price per unit
            reorder_point (int, optional): Quantity at which to reorder
            id (str, optional): Unique identifier (generated if not provided)
            last_updated (str, optional): Last update timestamp (current time if not provided)
        """
        self.id = id if id else str(uuid.uuid4())
        self.name = name
        self.category = category
        self.supplier = supplier
        self.quantity = int(quantity)
        self.cost_price = float(cost_price)
        self.selling_price = float(selling_price)
        
        # Set default reorder point to 20% of initial quantity if not provided
        self.reorder_point = int(reorder_point) if reorder_point is not None else max(1, int(quantity * 0.2))
        
        self.last_updated = last_updated if last_updated else datetime.now().isoformat()
    
    @property
    def inventory_value(self):
        """Calculate the current inventory value"""
        return self.quantity * self.cost_price
    
    @property
    def profit_margin(self):
        """Calculate the profit margin percentage"""
        if self.selling_price == 0:
            return 0
        
        return ((self.selling_price - self.cost_price) / self.selling_price) * 100
    
    @property
    def is_low_stock(self):
        """Check if the item is at or below its reorder point"""
        return self.quantity <= self.reorder_point
    
    def update_quantity(self, change_amount):
        """
        Update the quantity and last_updated timestamp
        
        Args:
            change_amount (int): Amount to add (positive) or remove (negative)
            
        Returns:
            int: New quantity
        """
        self.quantity = max(0, self.quantity + change_amount)
        self.last_updated = datetime.now().isoformat()
        return self.quantity
    
    def update_price(self, new_cost_price=None, new_selling_price=None):
        """
        Update pricing information
        
        Args:
            new_cost_price (float, optional): New cost price
            new_selling_price (float, optional): New selling price
            
        Returns:
            tuple: New (cost_price, selling_price)
        """
        if new_cost_price is not None:
            self.cost_price = float(new_cost_price)
        
        if new_selling_price is not None:
            self.selling_price = float(new_selling_price)
        
        self.last_updated = datetime.now().isoformat()
        return (self.cost_price, self.selling_price)
    
    def to_dict(self):
        """
        Convert the item to a dictionary
        
        Returns:
            dict: Dictionary representation of the item
        """
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "supplier": self.supplier,
            "quantity": self.quantity,
            "reorder_point": self.reorder_point,
            "cost_price": self.cost_price,
            "selling_price": self.selling_price,
            "last_updated": self.last_updated
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create an InventoryItem from a dictionary
        
        Args:
            data (dict): Dictionary containing item data
            
        Returns:
            InventoryItem: Created instance
        """
        return cls(
            name=data["name"],
            category=data["category"],
            supplier=data["supplier"],
            quantity=data["quantity"],
            cost_price=data["cost_price"],
            selling_price=data["selling_price"],
            reorder_point=data.get("reorder_point"),
            id=data.get("id"),
            last_updated=data.get("last_updated")
        )


class InventoryTransaction:
    """
    Model class representing an inventory transaction
    """
    
    def __init__(self, item_id, item_name, transaction_type, quantity_change, 
                old_quantity, new_quantity, id=None, timestamp=None):
        """
        Initialize a new inventory transaction
        
        Args:
            item_id (str): ID of the inventory item
            item_name (str): Name of the inventory item
            transaction_type (str): Type of transaction (e.g., 'sale', 'purchase', 'adjustment')
            quantity_change (int): Amount changed (positive for additions, negative for removals)
            old_quantity (int): Quantity before the transaction
            new_quantity (int): Quantity after the transaction
            id (str, optional): Unique identifier (generated if not provided)
            timestamp (str, optional): Transaction timestamp (current time if not provided)
        """
        self.id = id if id else str(uuid.uuid4())
        self.item_id = item_id
        self.item_name = item_name
        self.transaction_type = transaction_type
        self.quantity_change = quantity_change
        self.old_quantity = old_quantity
        self.new_quantity = new_quantity
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()
    
    def to_dict(self):
        """
        Convert the transaction to a dictionary
        
        Returns:
            dict: Dictionary representation of the transaction
        """
        return {
            "id": self.id,
            "item_id": self.item_id,
            "item_name": self.item_name,
            "transaction_type": self.transaction_type,
            "quantity_change": self.quantity_change,
            "old_quantity": self.old_quantity,
            "new_quantity": self.new_quantity,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create an InventoryTransaction from a dictionary
        
        Args:
            data (dict): Dictionary containing transaction data
            
        Returns:
            InventoryTransaction: Created instance
        """
        return cls(
            item_id=data["item_id"],
            item_name=data["item_name"],
            transaction_type=data["transaction_type"],
            quantity_change=data["quantity_change"],
            old_quantity=data["old_quantity"],
            new_quantity=data["new_quantity"],
            id=data.get("id"),
            timestamp=data.get("timestamp")
        )
