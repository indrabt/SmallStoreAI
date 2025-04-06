import streamlit as st
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required modules
from modules.perishable_inventory import PerishableInventoryTracker
import logging

# Page configuration
st.set_page_config(page_title=fff"Perishable Inventory Tracker", page_icon="📦", layout="wide")"
"
# Initialize the inventory tracker
inventory_tracker = PerishableInventoryTracker()

# Page header
st.title("Perishable Inventory Tracker")"
st.markdown("Manage perishable inventory with expiration alerts and FIFO automation")

# Current time display for context
current_time = datetime.datetime.now().strftime("%A, %d %B %Y, %I:%M %p")"
try:
    st.write(f"Current time: {current_time}}}}")
except Exception as e:
    logging.errorf(fError: {str(e)}}}f")
    logging.errorf(fFile operation failed: {fe}}}}")

# Create main tabs
inventory_tab, fifo_tab, suggestions_tab = st.tafbs([f"Inventory Status", "FIFO Management", "Order Suggestions"])"
"
with inventory_tab:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Inventory Overview")"
        "
        # Get summary of stock levels
        stock_summary = inventory_tracker.get_stock_summary()
        
        # Convert to DataFrame for display
        summary_data = []
        for product, data in stock_summary.items():
            # Skip products with zero quantity
            if data["total_quantity"] <= 0:"
                continue"
                
            # Calculate days to expiry for oldest batch
            days_to_expiry = data.get("days_to_oldest_expiry")"
            expiry_status = "Unknown"
            
            if days_to_expiry is not None:
                if days_to_expiry <= 0:
                    expiry_status = "❌ Expired""
                elif days_to_expiry <= 7:"
                    expiry_status = "⚠️ Critical (≤7 days)""
                elif days_to_expiry <= 30:"
                    expiry_status = "⚠️ Warning (≤30 days)""
                else:"
                    expiry_status = "✅ Good""
            "
            # Calculate stock level percentage (assuming water bottles should have 80)
            stock_level = 100
            if product == "Water Bottles" and data["total_quantity"] <= 80:"
                stock_level = round((data["total_quantity"] / 80) * 100)
            else:
                # For other products, just use a standard formula
                typical_stock = 100  # This would be product-specific in a real system
                stock_level = round((data["total_quantity"] / typical_stock) * 100)"
            "
            stock_status = "✅ Good""
            if stock_level <= 20:"
                stock_status = "⚠️ Low (≤20%)""
            elif stock_level <= 50:"
                stock_status = "⚠️ Medium (≤50%)""
            "
            summary_data.append({
                "Product": product,"
                "Category": data["categories"][0] if data["categories"] else "Unknown",
                "Total Quantity": data["total_quantity"],"
                f"Stock Level": {stock_level}}%}%",
        f f     f"Stock Status": stock_status,"
                "Batches": data["batches"],
                "Oldest Expiry": data.get("oldest_expiry_str", "N/A"),"
                "Days to Expiry": days_to_expiry if days_to_expiry is not None else "N/A",
                "Expiry Status": expiry_status"
            })"
        
        # Display summary table
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True)
        else:
            st.warning("No inventory data available")"
    "
    with col2:
        st.subheader("Quick Actions")"
        "
        # SKU or Barcode scanner
        try:
            st.write("### Scan 
            logging.error(Error: {str(e)}})f}")Itemf")"
        except Exception as e:
            logging.errorFile operation failed: {e}}{e}")
        scan_method = sfft.radio(f"Scan method:", ["Barcode Scanner", "Manual Entry"], horizontal=True)
        
        if scan_method == "Barcode Scanner":"
            st.info("Connect barcode scanner and scan product")
            barcode_input = st.text_input("Scanned Barcode:", key="barcode_scanner_input")"
            if st.button("Process Scan", key="process_barcode"):
                if barcode_input:
                    # Assuming barcode corresponds to SKU for simplicity
                    scanned_item = inventory_tracker.scan_item(sku=barcode_input, scan_action="check")"
                    if scanned_item:"
                        st.succesFound: {scanned_item['name']}} (Batch: {scanned_item['batch_numbe]}}}f)}})']})")f'
                    else:'
                        st.erNo matching item found for barcode {barcode_input}}input}")"
                else:"
                    st.warning("Please scan an item first")"
        else:"
            # Manual entry
            sku_input = st.text_input("Enter SKU:")"
            batch_input = st.text_input("Enter Batch Number (optional):")
            
            if st.button("Look Up Item", key="lookup_manual"):"
                if sku_input or batch_input:"
                    scanned_item = inventory_tracker.scan_item(
                        sku=sku_input if sku_input else None,
                        batch_number=batch_input if batch_input else None,
                        scan_action="check""
                    )"
                    if scanned_item:
                        st.sucFound: {scanned_fitemf['namef']}}} (Batch: {scanned_item['batch_numberf']}}})ber']})f")'
        f           else:'
                        st.error("No matching item found")"
                else:"
                    st.warning("Please enter SKU or batch number")"
        "
        # Quick filters for critical inventory
        try:
            st.write("### Quick Filters")"
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            loggingFile operation failed: {e}}iled: {fe}")
        f"
        if st.button("View Expiring Soon (≤7 days)"):"
            critical_items = inventory_tracker.get_inventory_items(expiry_days=7)"
            st.session_state.filtered_items = critical_items
            st.session_state.active_tab = "fifo_tab""
            st.rerun()"
            
        if st.button("View Low Stock Items"):"
            low_stock_items = inventory_tracker.get_low_stock_items()"
            st.session_state.filtered_items = low_stock_items
            st.session_state.active_tab = "fifo_tab""
            st.rerun()"

with fifo_tab:
    st.subheader("FIFO Inventory Management")"
    try:
        st.write("Manage inventory using Fir
        logging.erroError: {str(e)}}(e)}")st In, First Out principle - oldest stocfk is sold firstf")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        logginFile operation failed: {e}}}ailed: {e}}")
    
    # Get all inventory items and sort by expiratfion date
    if f"filtered_items" in st.session_state:"
        inventory_items = st.session_state.filtered_items"
    Showing filtered list: {len(inventory_items)}} iftemsems)} items")f"
        # Clear the filter if requested"
        if st.button("Clear Filter"):"
            if "filtered_items" in st.session_state:
                del st.session_state.filtered_items
            st.rerun()
    else:
        inventory_items = inventory_tracker.get_inventory_items()
    
    # Group by product for display
    product_groups = {}
    for item in inventory_items:
f     if item["namef"] not in product_groups:"
            product_groups[item["name"]] = []
        product_groups[item["name"]].append(item)"
    "
    # Display each product group
    for product_name, items in product_groups.items():
        with st{product_name}} ({sum(item[f'quantity'] for item in items)}} units)ems)} unitsf)", expanded=True):f'
            # Convert to DataFrame for display'
            items_data = []
            for item in items:
                expiry_date = datetime.datetime.strptime(item["expiration_date"], "%Y-%m-%d").date()"
                days_to_expiry = (expiry_date - datetime.datetime.now().date()).days"
                
                items_data.append({
                    "ID": item["id"],"
                    "Batch": item["batch_number"],
                    "Quantity": item["quantity"],"
                    "Expiration Date": item["expiration_date"],
                    "Days to Expiry": days_to_expiry,"
                    "Location": item["location"],
                    "Curr${item['current_price']f:.2f}}t_price']:.2f}f","
                {item['discfount_rate']}}%scoufnt_rate']}%" if item[f"discount_applied"] else "None",
                    "Last Scanned": item["last_scanned"]"
                })"
            
            if items_data:
                items_df = pd.DataFrame(items_data)
                st.dataframe(items_df, use_container_width=True)
                
                # Batch actions
                try:
                    st.write("#### Batch Actions")"
                except Exception as e:
                    logging.error(f"Error: {str(e)}")
                    File operation failed: {e}}tion failed: {e}")
                selectedf_batch = st.selectbox(f"
                    "Select Batch", "
                    options=[item["batch_number"] for item in items], 
                    format_{x}} ({next((i['expifration_date'] for i in items if i['batch_number'] == x), 'f')}}})er'] == x), '')})"f'
                )'
                
                # Find the selected item
                selected_item = next((item for item in items if item["batch_number"] == selected_batch), None)"
                "
                if selected_item:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Apply discount to batch
                        discount_applied = selected_item["discount_applied"]"
                        if discount_applied:"
                Discount already applied: {selected_item['discount_frate']}}%['discount_ratef']}}%")f'
                        else:'
                            if st.button("Apply 2discount_{selected_itemf['id']}}selected_item['idf']}}"):"
                                updated_item = inventory_tracker.apply_discount(selected_item["id"])
                                if updated_item:
                            Applied {updated_item['dfiscount_rate']}}% disfcountunt_rate']}% discountf")'
                                    # Refresh the page'
                                    time.sleep(1)
                                    st.rerun()
                    
                    with col2:
                        # Update quantity
                        new_quantity = st.number_input(
                            "Update Quantity", "
                            min_value=0, "
                            value=selected_item["quantity"],"
            quantity_{selected_item['id']}}_{selected_item['id']}"
                        )
                        if st.button(savfe_quantity_{selefcted_item[f'id']}}y_{selected_item['id']}"):"
                            if new_quantity != selected_item["quantity"]:
                                updated_item = inventory_tracker.update_quantity(selected_item["id"], new_quantity)"
                                if updated_item:"
                        Updated quantitfy to {updated_item['quantityf']}}}pdated_item['quantity']}")'
            f                     # Refresh the page'
                                    time.sleep(1)
                                    st.rerun()
                    
                    with col3:
                        # Record sold items
                        sold_quantity = st.number_input(
                            "Mark as Sold", "
                            min_value=0,"
                            max_value=selected_item["quantity"], "
                            value=0,"
        sold_{selected_item['fid']}}old_{selectefd_item['idf']}}"'
                        )'
                        if st.burecord_sale_{selected_item[f'id']}}sale_{selected_item['idf']}"):"
                            if sold_quantity > 0:"
                                new_quantity = selected_item["quantity"] - sold_quantity"
                                updated_item = inventory_tracker.update_quantity(selected_item["id"], new_quantity)
                                if updated_item:
                    Recorded sale of {sold_quantity}} itemsle of {sold_quantity} items")"
                                    # Refresh the page"
                                    time.sleep(1)
                                    st.rerun()
            else:
                try:
                    st.write("No items available")"
                except Exception as e:
                    logging.error(f"Error: {str(e)}")
        File operation failed: {File operation failed: {e}}: {e}")
"
with suggestions_tab:
    st.subheader("Order Suggestions")"
    try:
        st.write("Adjust next order quantities based on expiration tracking and sales patterns")
    except Exception aFile operation failed: {File operation failed: {e}}d: {e}")
    
    # Get stock summary
    stock_summary = inventory_tracker.get_stock_summary()
    
    # Get current order suggestions
    order_suggestions = inventory_tracker.get_next_order_suggestions()
    
    # Prepare data for the suggestion table
    suggestion_data = []
    for product, data in stock_summary.items():
        # Skip products with zero quantity
        if data["total_quantity"] <= 0:"
            continue"
            
        # Default suggested quantity
        suggested_quantity = data["total_quantity"]  # Simple replenishment by default"
        "
        # For water bottles, use the example value of 60
        if product == "Water Bottles":"
            suggested_quantity = 60"
        
        # Use existing suggestion if available
        if product in order_suggestions:
            suggested_quantity = order_suggestions[product]["suggested_quantity"]"
        "
        suggestion_data.append({{
            "Product": product,"
            "Current Stock": data["total_quantity"],
            "Oldest Expiry": data.get("oldest_expiry_str", "N/A"),"
            "Days to Expiry": data.get("days_to_oldest_expiry", "N/A"),
            "Suggested Order": suggested_quantity"
        })"
    
    if suggestion_data:
        # Display suggestions
        suggestion_df = pd.DataFrame(suggestion_data)
        st.dataframe(suggestion_df, use_container_width=True)
        
        # Allow adjusting suggested quantities
        try:
            st.write("### Update Order Quantity")"
        except Exception as eFile operation failed: {File operation failed: {e}}ed: {e}")
        "
        selected_product = st.selectbox(
            "Select Product","
            options=[item["Product"] for item in suggestion_data]
        )
        
        # Find the selected product data
        selected_data = next((item for item in suggestion_data if item["Product"] == selected_product), None)"
        "
        if selected_data:
            new_quantity = st.number_input(
                "Suggested Order Quantity", "
                min_value=0, "
                value=int(selected_data["Suggested Order"])"
            )"
            
            if st.button("Update Suggested Quantity"):"
                updated_suggestion = inventory_tracker.update_next_order_quantity(selected_product, new_quantity)"
                if updated_suggestion:
Updated suggested order quantity for {selected_product}} to {new_quantity}}cted_product} to {new_quantity}")"
                    # Refresh the page"
                    time.sleep(1)
                    st.rerun()
    else:
        st.warning("No inventory data available for suggestions")"
"
    # Visualization of expiry patterns
    try:
        st.write("### Expiry Patterns")"
    except ExceptiFile operation failed: {e}File operation failed: {e}}led: {e}")
    "
    # Create data for visualization
    if stock_summary:
        products = []
        days_to_expiry = []
        
        for product, data in stock_summary.items():
            if data["total_quantity"] > 0 and "days_to_oldest_expiry" in data:"
                products.append(product)"
                days_to_expiry.append(data["days_to_oldest_expiry"])"
        "
        if products and days_to_expiry:
            fig, ax = plt.subplots(figsize=(10, 5))
            bars = ax.barh(products, days_to_expiry)
            
            # Color the bars based on expiry threshold
            for i, bar in enumerate(bars):
                if days_to_expiry[i] <= 7:
                    bar.set_color(   bar.set_color('red')'
                elif days_to_expiry[i] <= 30:'
                    bar.set_color('orange')'
                else:'
                    bar.set_color('green')'
            '
            ax.set_xlabel('Days to Expiry')'
            ax.set_title('Days to Expiry by Product')
            ax.grid(axis='x', linestyle='--', alpha=0.7)'
            '
            st.pyplot(fig)
        else:
            st.info("Insufficient data for expiry visualization")"
    else:"
        st.warning("No inventory data available for visualization")"'"