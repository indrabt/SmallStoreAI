import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

def format_currency(value, include_symbol=True, decimal_places=2):
    """
    Format a numeric value as currency
    
    Args:
        value (float): The numeric value to format
        include_symbol (bool): Whether to include the $ symbol
        decimal_places (int): Number of decimal places to include
        
    Returns:
        str: Formatted currency string
    """
    if pd.isna(value):
        return "N/A"
    
    formatted = f"{abs(value):.{decimal_places}f}"
    
    if include_symbol:
        return f"${formatted}" if value >= 0 else f"-${formatted}"
    else:
        return formatted if value >= 0 else f"-{formatted}"

def calculate_percentage_change(old_value, new_value):
    """
    Calculate percentage change between two values
    
    Args:
        old_value (float): The original value
        new_value (float): The new value
        
    Returns:
        float: Percentage change (positive for increase, negative for decrease)
    """
    if old_value == 0:
        return float('inf') if new_value > 0 else float('-inf') if new_value < 0 else 0
    
    return ((new_value - old_value) / abs(old_value)) * 100

def parse_date(date_str, format=None):
    """
    Parse a date string into a datetime object
    
    Args:
        date_str (str): The date string to parse
        format (str, optional): Format string for parsing. If None, try common formats.
        
    Returns:
        datetime: Parsed datetime object or None if parsing fails
    """
    if not date_str:
        return None
    
    if format:
        try:
            return datetime.strptime(date_str, format)
        except ValueError:
            pass
    
    # Try common formats
    formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None

def extract_numbers(text):
    """
    Extract numeric values from a text string
    
    Args:
        text (str): The text to extract numbers from
        
    Returns:
        list: List of extracted numbers as floats
    """
    if not text:
        return []
    
    # Find all numbers (including decimals)
    numbers = re.findall(r'-?\d+\.?\d*', text)
    return [float(num) for num in numbers]

def generate_date_ranges(start_date, end_date, interval='day'):
    """
    Generate a list of date ranges between start and end dates
    
    Args:
        start_date (datetime): Start date
        end_date (datetime): End date
        interval (str): Interval type - 'day', 'week', 'month', or 'year'
        
    Returns:
        list: List of date range tuples (start, end)
    """
    if not start_date or not end_date:
        return []
    
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    ranges = []
    current = start_date
    
    while current <= end_date:
        if interval == 'day':
            range_end = datetime(current.year, current.month, current.day, 23, 59, 59)
            next_date = current + timedelta(days=1)
        elif interval == 'week':
            # Get the end of the week (Sunday)
            days_to_sunday = 6 - current.weekday()
            range_end = datetime(current.year, current.month, 
                                (current + timedelta(days=days_to_sunday)).day, 23, 59, 59)
            next_date = current + timedelta(days=7)
        elif interval == 'month':
            # Get the end of the month
            if current.month == 12:
                range_end = datetime(current.year, 12, 31, 23, 59, 59)
                next_date = datetime(current.year + 1, 1, 1)
            else:
                next_month = current.month + 1
                range_end = datetime(current.year, current.month, 
                                   (datetime(current.year, next_month, 1) - timedelta(days=1)).day, 
                                   23, 59, 59)
                next_date = datetime(current.year, next_month, 1)
        elif interval == 'year':
            range_end = datetime(current.year, 12, 31, 23, 59, 59)
            next_date = datetime(current.year + 1, 1, 1)
        else:
            # Default to daily if interval not recognized
            range_end = datetime(current.year, current.month, current.day, 23, 59, 59)
            next_date = current + timedelta(days=1)
        
        # Cap the end date at the overall end date
        range_end = min(range_end, end_date)
        
        ranges.append((current, range_end))
        current = next_date
        
        # Break if we're past the end date
        if current > end_date:
            break
    
    return ranges

def filter_outliers(data, column, method='iqr', threshold=1.5):
    """
    Filter outliers from a pandas DataFrame
    
    Args:
        data (DataFrame): The DataFrame to filter
        column (str): The column to check for outliers
        method (str): Method to use - 'iqr' (interquartile range) or 'std' (standard deviation)
        threshold (float): Threshold for filtering (1.5 for IQR, 3.0 for std dev)
        
    Returns:
        DataFrame: DataFrame with outliers removed
    """
    if data.empty:
        return data
    
    if method == 'iqr':
        # IQR method
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    
    elif method == 'std':
        # Standard deviation method
        mean = data[column].mean()
        std = data[column].std()
        
        lower_bound = mean - threshold * std
        upper_bound = mean + threshold * std
        
        return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    
    else:
        # Return original data if method not recognized
        return data
