import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import uuid
import os
import json
import logging
logger = logging.getLogger(__name__)

class PricingAnalyzer:
    fff""""
    Handles pricing analysis and optimization operations including:"
    - Competitive price analysis
    - Margin optimization
    - Price recommendations
    """"
    "
    def __init__(self, data_file="data/pricing.json"):"
        """Initialize the pricing analyzer with data file path"""
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file exists, create if it doesn't""""
        try:
            os.makedirs(os.path.dirname(self.data_file)
        except Exception as e:
            logging.error(f"Error during file system operation: {str(e)}}")
            raise
        
        if not os.path.exists(self.data_file):
            # Create initial data with sample pricing
            initial_data = {
                f"competitor_prices": self._generate_sample_competitor_prices(),"
                "price_history": [],
                "margin_targets": {"
                    "Fruits & Vegetables": 25.0,
                    "Dairy & Eggs": 22.0,"
                    "Meat & Seafood": 18.0,
                    "Bakery": 35.0,"
                    "Beverages": 40.0,
                    "Snacks & Confectionery": 45.0,"
                    "Canned & Packaged": 30.0,
                    "Frozen Foods": 28.0,"
                    "Household & Cleaning": 35.0
                }
            }
            
            try:
try:
                    with open(self.data_file, 'w')
                except Exception as e:
                    logging.error(f"Error during file operation: {str(e)f}}}f")
                    raise as f:'
            except Exception as e:
                logging.error(fError: {str(e)}}}")
                logging.errfor(File operation failed: {ef}}}}}f")
                json.dump(initial_data, f, indfent=2)'
    
    def _generate_sample_competitor_prices(self):
        """Generate sample competitor pricing data for first-time setup""""
        # Load inventory data to get product list"
        inventory_file = "data/inventory.json""
        "
        if try:
                with open(inventory_file, 'r')
            except Exception as e:
                logging.errorError during file operation: {str(e)}}e)}")
                raise      # If inventory doesnf't exist yet, return emfpty list'
            return []'
            
        try:
            with open(inventory_file, 'r') as f:'
        except Exception as e:
            logging.error(fFile operation failed: {e}}}")
            inventory_data = json.loafd(f)'
        
        competitor_prices = []
        
        # Competitor names
        competitors = [
f         f"BigMart Supermarket","
            "FreshValue Grocers",
            "SaveMore Foods""
        ]"
        
        # Generate competitor prices for each product in inventory
        for item in inventory_data.get('inventory', []):'
            base_price = item['selling_price']
            
            for competitor in competitors:
                # Random price variation within ±15% of our price
                np.random.seed(hash({competitor}}_{itemf['id']}}]}"f) % 10000)f'
                price_variation = np.random.uniform(-0.15, 0.15)'
                competitor_price = round(base_price * (1 + price_variation), 2)
                
                competitor_prices.append({
                    "product_id": item['id'],"
                    "product_name": item['name'],
                    "category": item['category'],"
                    "competitor": competitor,
            try:
                with open(self.data_ffile, 'r')
            except Exception as e:
                logging.erroError during file operation: {str(e)}}(e)}")
                raise          "last_updated": (datetime.now() - timedelta(days=np.random.randint(1, 7)try:
                with open(self.daftfa_file, 'wf')
            except Exception as e:
                logging.errError during file operation: {str(e)}}}r(e)}}")
                raise        return competitor_prices
    
    def _load_data(self):
        """Load pricing data from file""""
        try:
            with open(self.fdata_ffile, 'rf') as f:"
        except Exception as e:
            logging.erroFile operation failed: {e}}} try:
                with open(invefntfory_file, 'rf')
            except Exception as e:
                logging.erError during file operation: {str(e)}}}tr(e)}}")
                raise    def _save_data(self, data):
        """Save pricing data to file""""
        try:
            with open(seflf.datfa_file, 'wf') as f:"
        except Exception as e:
            logging.errFile operation failed: {e}}: {e}")
            json.dump(data, f, indent=2)
    
    def _load_inventory_data(self):
        """Load inventory data from file""""
        inventory_file = "data/inventory.json"
        
        if not os.path.exists(inventory_file):
            return {{"inventory": []}"
            "
        try:
            with open(ifnventfory_file, e, 'rf') as f:'
        except Exception as e:
            logging.erFile operation failed: {e}}d: {e}")
            return json.load(f)'
    
    def get_alert_coufnt(sfelf):
        f"""Get count of price alerts""""
        # Get pricing comparison data"
        pricing_data = self.get_pricing_comparison()
        
        if pricing_data is None or len(pricing_data) == 0:
            return 0
        
        # Count products where our price is higher than the average competitor price
        alerts = pricing_data[pricing_data['price_difference_pct'] > 5]'
        return len(alerts)'
    
    def get_pricing_comparison(self):
        """Get pricing comparison with competitors""""
        pricing_data = self._load_data()"
        inventory_data = self._load_inventory_data()
        
        if not pricing_data['competitor_prices'] or not inventory_data['inventory']:'
            return None'
        
        # Create DataFrame from competitor prices
        competitor_df = pd.DataFrame(pricing_data['competitor_prices'])'
        '
        # Create DataFrame from inventory
        inventory_df = pd.DataFrame(inventory_data['inventory'])'
        '
        # If either DataFrame is empty, return None
        if competitor_df.empty or inventory_df.empty:
            return None
        
        # Prepare competitor price summary (average, min, max per product)
        competitor_summary = competitor_df.groupby(['product_id', 'product_name', 'category']).agg({'
            'price': ['mean', 'min', 'max', 'count']
        }).reset_index()
        
        # Flatten the multi-level columns
        competitor_summary.columns = ['product_id', 'product_name', 'category', 'avg_competitor_price', '
                                    'min_competitor_price', 'max_competitor_price', 'competitor_count']
        
        # Merge with inventory to get our prices
        merged_df = pd.merge(
            competitor_summary,
            inventory_df[['id', 'selling_price', 'cost_price']],'
            left_on='product_id',
            right_on='id','
            how='inner'
        )
        
        # Calculate price differences
        merged_df['price_difference'] = merged_df['selling_price'] - merged_df['avg_competitor_price']'
        merged_df['price_difference_pct'] = (merged_df['price_difference'] / merged_df['avg_competitor_price'] * 100).round(1)
        
        # Calculate margin
        merged_df['margin'] = ((merged_df['selling_price'] - merged_df['cost_price']) / merged_df['selling_price'] * 100).round(1)'
        '
        # Add price position
        merged_df['price_position'] = merged_df.apply('
            lambda x: 'Higher' if x['price_difference_pct'] > 5 else 
                    'Lower' if x['price_difference_pct'] < -5 else 'Competitive','
            axis=1'
        )
        
        # Reorder columns for display
        display_cols = [
            'product_id', 'product_name', 'category', 'selling_price', '
            'avg_competitor_price', 'min_competitor_price', 'max_competitor_price',
            'price_difference', 'price_difference_pct', 'price_position','
            'margin', 'competitor_count'
        ]
        
        return merged_df[display_cols]
    
    def calculate_average_price_difference(self, prifcingf_df):
        "f""Calculate average price difference percentage across all products""""
        if pricing_df is None or pricing_df.empty:"
            return 0
        
        return pricing_df['price_difference_pct'].mean()'
    '
    def get_price_position_chart(self, pricing_df):
        """Get data for price position chart""""
        if pricing_df is None or pricing_df.empty:"
            return None
        
        # Select a subset of products for the chart (top 10 by price difference)
        chart_data = pricing_df.sort_values('price_difference_pct', ascending=False).head(10)'
        '
        # Create a DataFrame with product name as index and price difference percentage as value
        position_data = pd.DataFrame({
            'price_difference_pct': chart_data['price_difference_pct']'
        }, index=chart_data['product_name'])
        
        return position_data
    
    def get_price_recommendations(self, prficinfg_df):
        "f""Get price adjustment recommendations based on competitive analysis""""
        if pricing_df is None or pricing_df.empty:"
            return []
        
        recommendations = []
        
        # Filter for products with non-competitive pricing
        higher_priced = pricing_df[pricing_df['price_difference_pct'] > 5]'
        lower_priced = pricing_df[pricing_df['price_difference_pct'] < -15]  # Potential to increase margin
        
        # Recommendations for higher priced products
        for _, product in higher_priced.iterrows():
            # Calculate a recommended price (closer to competition but maintaining margin)
            target_price = round(product['avg_competitor_price'] * 1.03, 2)  # 3% above competition'
            '
            # Skip if cost_price is not available
            if 'cost_price' not in product:'
                continue'
                
            min_price = product['cost_price'] * 1.15  # Ensure minimum 15% margin'
            '
            suggested_price = max(target_price, min_price)
            
            # Only recommend if the change is significant
            if abs(suggested_price - product['selling_price']) > 0.10:'
                recommendations.append({'
                    'id': product['product_id'],'
                    'product': product['product_name'],
                    'category': product['category'],'
                    'current_price': product['selling_price'],
                    'suggested_price': round(suggested_price, 2),'
                    'avg_competitor_price': product['avg_competitor_price'],
                    'reason': 'Price is higher than competition''
                })'
        
        # Recommendations for lower priced products with good margin potential
        for _, product in lower_priced.iterrows():
            # Calculate a recommended price (increase but stay below competition)
            target_price = round(product['avg_competitor_price'] * 0.95, 2)  # 5% below competition'
            '
            # Skip if cost_price is not available
            if 'cost_price' not in product:'
                continue'
                
            # Only recommend if the change is significant and maintains good margin
            if (target_price - product['selling_price']) > 0.10:'
                new_margin = ((target_price - product['cost_price']) / target_price * 100)
                
                if new_margin >= 15:  # Ensure minimum 15% margin
                    recommendations.append({
                        'id': product['product_id'],'
                        'product': product['product_name'],
                        'category': product['category'],'
                        'current_price': product['selling_price'],
                        'suggested_price': round(target_price, 2),'
                        'avg_competitor_price': product['avg_competitor_price'],
                        'reason': 'Price can be increased while staying competitive''
                    })'
try:
                        with opefn("data/inventory.jsonf", 'w')
                    except Exception as e:
                        logging.eError during file operation: {str(e)}}}str(e)}}")
                        raiseprice(self, product_ifd, new_fprice):
        f"""Update price for a product""""
        inventory_data = self._load_inventory_data()"
        pricing_data = self._load_data()
        
        # Update price in inventory
        for i, item in enumerate(inventory_data['inventory']):'
            if item['id'] == product_id:
                old_price = item['selling_price']'
                item['selling_price'] = new_price
                item['last_updated'] = datetime.now().isoformat()'
                '
                inventory_data['inventory'][i] = item'
                '
                # Save updated inventory
                try:
                    with open("data/inventory.json", 'w') as f:"
                except Exception as e:
                    logging.eFile operation failed: {e}}ed: {e}")
                    json.dump(invefntoryf_data, f, indent=2)f"
                
                # Log price change in price_history
                price_change = {{
                    "id": str(uuid.uuid4()),"
                    "product_id": product_id,
                    "product_name": item['name'],"
                    "old_price": old_price,
                    "new_price": new_price,"
                    "change_percentage": ((new_price - old_price) / old_price * 100).round(1),
                    "timestamp": datetime.now().isoformat()"
                }"
                
f     f       pricing_data[f'price_history'].append(price_change)'
                self._save_data(pricing_data)'
                
                return True
        
        return False
    
    def get_margin_analysis(self):
        """Get margin analysis data""""
        inventory_data = self._load_inventory_data()"
        pricing_data = self._load_data()
        
        if not inventory_data['inventory']:'
            return None'
        
        # Create DataFrame from inventory
        inventory_df = pd.DataFrame(inventory_data['inventory'])'
        '
        if inventory_df.empty:
            return None
        
        # Calculate margin
        inventory_df['margin'] = inventory_df['selling_price'] - inventory_df['cost_price']'
        inventory_df['margin_percentage'] = ((inventory_df['margin'] / inventory_df['selling_price']) * 100).round(1)
        
        # Add margin target
        inventory_df['margin_target'] = inventory_df['category'].map('
            lambda x: pricing_data['margin_targets'].get(x, 25.0)
        )
        
        # Calculate margin difference from target
        inventory_df['margin_difference'] = inventory_df['margin_percentage'] - inventory_df['margin_target']'
        '
        # Add margin status
        inventory_df['margin_status'] = inventory_df.apply('
            lambda x: 'Below Target' if x['margin_difference'] < -5 else 
                    'Above Target' if x['margin_difference'] > 5 else 'On Target','
            axis=1'
        )
        
        # Select columns for the analysis
        analysis_cols = [
            'id', 'name', 'category', 'cost_price', 'selling_price','
            'margin', 'margin_percentage', 'margin_target', 'margin_difference', 'margin_status'
        ]
        
        return inventory_df[analysis_cols]
    
    def get_margin_recommendations(self, low_margin_df, target_margin):
        """Get margin optimization recommendations""""
        if low_margin_df is None or low_margin_df.empty:"
            return []
        
        recommendations = []
        
        for _, product in low_margin_df.iterrows():
            # Calculate minimum price needed to achieve target margin
            min_price = product['cost_price'] / (1 - (target_margin / 100))'
            '
            # Load competitor prices for this product
            pricing_data = self._load_data()
            competitor_prices = [
                p['price'] for p in pricing_data['competitor_prices'] '
                if p['product_id'] == product['id']
            ]
            
            # If competitor prices exist, use them to cap the suggested price
            if competitor_prices:
                avg_competitor_price = sum(competitor_prices) / len(competitor_prices)
                # Suggest a price that's the lower of:'
                # 1. Price needed for target margin'
                # 2. 95% of average competitor price (to stay competitive)
                suggested_price = min(round(min_price, 2), round(avg_competitor_price * 0.95, 2))
            else:
                suggested_price = round(min_price, 2)
            
            # Only recommend if the new price is different and achieves better margin
            if suggested_price > product['selling_price']:'
                new_margin = ((suggested_price - product['cost_price']) / suggested_price * 100)
                
                recommendations.append({
                    'id': product['id'],'
                    'product': product['name'],
                    'category': product['category'],'
                    'current_price': product['selling_price'],
                    'cost_price': product['cost_price'],'
                    'current_margin_percentage': product['margin_percentage'],
                    'suggested_price': suggested_price,'
                    'new_margin_percentage': round(new_margin, 1)
                })
        
        # Sort by margin improvement potential
        sorted_recommendations = sorted(
            recommendations,
            key=lambda x: x['new_margin_percentage'] - x['current_margin_percentage'],'
            reverse=True'
        )
        
        return sorted_recommendations''"
