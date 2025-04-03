from datetime import datetime
import uuid

class Supplier:
    """
    Model class representing a supplier
    """
    
    def __init__(self, name, contact_name, phone, email, address, categories, 
                distance, delivery_schedule, min_order, products=None, 
                is_local=None, coordinates=None, id=None, date_added=None):
        """
        Initialize a new supplier
        
        Args:
            name (str): Supplier name
            contact_name (str): Contact person name
            phone (str): Contact phone number
            email (str): Contact email
            address (str): Physical address
            categories (list): List of product categories
            distance (float): Distance from store in kilometers
            delivery_schedule (str): Delivery frequency/schedule
            min_order (float): Minimum order value
            products (list, optional): List of product dictionaries
            is_local (bool, optional): Whether this is a local supplier (default based on distance)
            coordinates (dict, optional): Lat/lon coordinates
            id (str, optional): Unique identifier (generated if not provided)
            date_added (str, optional): Date added timestamp (current time if not provided)
        """
        self.id = id if id else str(uuid.uuid4())
        self.name = name
        self.contact_name = contact_name
        self.phone = phone
        self.email = email
        self.address = address
        self.categories = categories if isinstance(categories, list) else [categories]
        self.distance = float(distance)
        self.delivery_schedule = delivery_schedule
        self.min_order = float(min_order)
        self.products = products if products else []
        
        # Default is_local to True if distance <= 30km
        self.is_local = is_local if is_local is not None else (self.distance <= 30)
        
        self.coordinates = coordinates if coordinates else {}
        self.date_added = date_added if date_added else datetime.now().isoformat()
        self.last_order_date = None
        
        # Generate reliability and sustainability scores for new suppliers
        if id is None:
            import numpy as np
            self.reliability_score = round(np.random.uniform(7.5, 9.5), 1)
            self.sustainability_score = round(np.random.uniform(7.0, 9.0), 1)
    
    def add_product(self, name, price, unit):
        """
        Add a product to this supplier
        
        Args:
            name (str): Product name
            price (float): Product price
            unit (str): Unit of measure (e.g., 'kg', 'each')
            
        Returns:
            dict: The added product
        """
        product = {
            "name": name,
            "price": float(price),
            "unit": unit
        }
        
        self.products.append(product)
        return product
    
    def update_product(self, product_name, price=None, unit=None):
        """
        Update an existing product
        
        Args:
            product_name (str): Name of the product to update
            price (float, optional): New price
            unit (str, optional): New unit
            
        Returns:
            dict: Updated product or None if not found
        """
        for i, product in enumerate(self.products):
            if product["name"] == product_name:
                if price is not None:
                    self.products[i]["price"] = float(price)
                
                if unit is not None:
                    self.products[i]["unit"] = unit
                
                return self.products[i]
        
        return None  # Product not found
    
    def record_order(self, order_date=None):
        """
        Record that an order was placed with this supplier
        
        Args:
            order_date (str, optional): Order date (current time if not provided)
            
        Returns:
            str: Updated last_order_date
        """
        self.last_order_date = order_date if order_date else datetime.now().isoformat()
        return self.last_order_date
    
    def to_dict(self):
        """
        Convert the supplier to a dictionary
        
        Returns:
            dict: Dictionary representation of the supplier
        """
        return {
            "id": self.id,
            "name": self.name,
            "contact_name": self.contact_name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "distance": self.distance,
            "categories": self.categories,
            "delivery_schedule": self.delivery_schedule,
            "min_order": self.min_order,
            "is_local": self.is_local,
            "reliability_score": getattr(self, 'reliability_score', None),
            "sustainability_score": getattr(self, 'sustainability_score', None),
            "date_added": self.date_added,
            "last_order_date": self.last_order_date,
            "coordinates": self.coordinates,
            "products": self.products
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Supplier from a dictionary
        
        Args:
            data (dict): Dictionary containing supplier data
            
        Returns:
            Supplier: Created instance
        """
        supplier = cls(
            name=data["name"],
            contact_name=data["contact_name"],
            phone=data["phone"],
            email=data["email"],
            address=data["address"],
            categories=data["categories"],
            distance=data["distance"],
            delivery_schedule=data["delivery_schedule"],
            min_order=data["min_order"],
            products=data.get("products", []),
            is_local=data.get("is_local"),
            coordinates=data.get("coordinates", {}),
            id=data.get("id"),
            date_added=data.get("date_added")
        )
        
        # Add optional attributes
        supplier.last_order_date = data.get("last_order_date")
        
        if "reliability_score" in data:
            supplier.reliability_score = data["reliability_score"]
        
        if "sustainability_score" in data:
            supplier.sustainability_score = data["sustainability_score"]
        
        return supplier


class SupplierOrder:
    """
    Model class representing an order to a supplier
    """
    
    def __init__(self, supplier_id, supplier_name, order_items, total_amount, 
                status="pending", id=None, order_date=None, expected_delivery=None):
        """
        Initialize a new supplier order
        
        Args:
            supplier_id (str): ID of the supplier
            supplier_name (str): Name of the supplier
            order_items (list): List of ordered items (dicts with name, quantity, price)
            total_amount (float): Total order amount
            status (str, optional): Order status (default: "pending")
            id (str, optional): Unique identifier (generated if not provided)
            order_date (str, optional): Order date (current time if not provided)
            expected_delivery (str, optional): Expected delivery date
        """
        self.id = id if id else str(uuid.uuid4())
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.order_items = order_items
        self.total_amount = float(total_amount)
        self.status = status
        self.order_date = order_date if order_date else datetime.now().isoformat()
        self.expected_delivery = expected_delivery
        self.delivery_date = None
        self.notes = ""
    
    def update_status(self, new_status):
        """
        Update the order status
        
        Args:
            new_status (str): New status value
            
        Returns:
            str: Updated status
        """
        valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
        
        if new_status in valid_statuses:
            self.status = new_status
            
            # If status is delivered, set delivery date
            if new_status == "delivered" and not self.delivery_date:
                self.delivery_date = datetime.now().isoformat()
        
        return self.status
    
    def add_note(self, note):
        """
        Add a note to the order
        
        Args:
            note (str): Note to add
            
        Returns:
            str: Updated notes
        """
        timestamp = datetime.now().isoformat()
        
        if self.notes:
            self.notes += f"\n\n[{timestamp}] {note}"
        else:
            self.notes = f"[{timestamp}] {note}"
        
        return self.notes
    
    def to_dict(self):
        """
        Convert the order to a dictionary
        
        Returns:
            dict: Dictionary representation of the order
        """
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "supplier_name": self.supplier_name,
            "order_items": self.order_items,
            "total_amount": self.total_amount,
            "status": self.status,
            "order_date": self.order_date,
            "expected_delivery": self.expected_delivery,
            "delivery_date": self.delivery_date,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a SupplierOrder from a dictionary
        
        Args:
            data (dict): Dictionary containing order data
            
        Returns:
            SupplierOrder: Created instance
        """
        order = cls(
            supplier_id=data["supplier_id"],
            supplier_name=data["supplier_name"],
            order_items=data["order_items"],
            total_amount=data["total_amount"],
            status=data.get("status", "pending"),
            id=data.get("id"),
            order_date=data.get("order_date"),
            expected_delivery=data.get("expected_delivery")
        )
        
        # Add optional attributes
        order.delivery_date = data.get("delivery_date")
        order.notes = data.get("notes", "")
        
        return order
