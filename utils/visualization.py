import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
import streamlit as st

def get_color_scale(values, cmap='YlGnBu', reverse=False):
    """
    Generate a color scale based on values
    
    Args:
        values (list/array): Numeric values to map to colors
        cmap (str): Matplotlib colormap name
        reverse (bool): Whether to reverse the color map
        
    Returns:
        list: List of hex color codes
    """
    import matplotlib.cm as cm
    import matplotlib.colors as colors
    
    if not values:
        return []
    
    # Get min and max values
    min_val = min(values)
    max_val = max(values)
    
    # If all values are the same, return a single color
    if min_val == max_val:
        return ['#4CAF50'] * len(values)  # Use primary color
    
    # Normalize values between 0 and 1
    norm = colors.Normalize(vmin=min_val, vmax=max_val)
    
    # Get colormap
    colormap = cm.get_cmap(cmap)
    if reverse:
        colormap = colormap.reversed()
    
    # Convert normalized values to colors
    return [colors.rgb2hex(colormap(norm(val))) for val in values]

def format_chart(fig, title=None, x_label=None, y_label=None, legend=True):
    """
    Apply formatting to a matplotlib figure
    
    Args:
        fig (Figure): Matplotlib figure to format
        title (str): Chart title
        x_label (str): X-axis label
        y_label (str): Y-axis label
        legend (bool): Whether to show the legend
        
    Returns:
        Figure: Formatted figure
    """
    # Get the axes
    ax = fig.axes[0] if fig.axes else None
    
    if not ax:
        return fig
    
    # Apply styling
    if title:
        ax.set_title(title, fontsize=14, pad=10)
    
    if x_label:
        ax.set_xlabel(x_label, fontsize=12, labelpad=10)
    
    if y_label:
        ax.set_ylabel(y_label, fontsize=12, labelpad=10)
    
    # Grid styling
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tick styling
    ax.tick_params(axis='both', labelsize=10)
    
    # Legend styling
    if legend and ax.get_legend():
        ax.legend(fontsize=10, frameon=True, facecolor='white', edgecolor='lightgray')
    
    # Add padding
    fig.tight_layout()
    
    return fig

def create_trend_chart(data, x_column, y_columns, title=None, colors=None):
    """
    Create a line chart for trend visualization
    
    Args:
        data (DataFrame): Data containing x and y columns
        x_column (str): Column name for x-axis
        y_columns (list): List of column names for y-axis
        title (str): Chart title
        colors (list): List of colors for each y column
        
    Returns:
        Figure: Matplotlib figure containing the chart
    """
    if data.empty:
        return None
    
    # Create figure
    fig = Figure(figsize=(10, 5))
    ax = fig.subplots()
    
    # Default colors if not provided
    if not colors:
        colors = ['#4CAF50', '#2196F3', '#FFC107', '#F44336', '#9C27B0']
        colors = colors[:len(y_columns)]
    
    # Plot each y column
    for i, col in enumerate(y_columns):
        color = colors[i % len(colors)]
        ax.plot(data[x_column], data[col], marker='o', markersize=4, linewidth=2, 
               label=col, color=color)
    
    # Format the chart
    return format_chart(fig, title=title, x_label=x_column, y_label='Value')

def create_comparison_chart(data, category_col, value_cols, title=None, horizontal=True):
    """
    Create a bar chart for comparison visualization
    
    Args:
        data (DataFrame): Data containing category and value columns
        category_col (str): Column name for categories
        value_cols (list): List of column names for values to compare
        title (str): Chart title
        horizontal (bool): Whether to create a horizontal bar chart
        
    Returns:
        Figure: Matplotlib figure containing the chart
    """
    if data.empty:
        return None
    
    # Create figure
    fig = Figure(figsize=(10, max(5, len(data) * 0.4)))
    ax = fig.subplots()
    
    # Set default colors
    colors = ['#4CAF50', '#2196F3', '#FFC107', '#F44336', '#9C27B0']
    colors = colors[:len(value_cols)]
    
    # Create positions for the bars
    categories = data[category_col].tolist()
    x = np.arange(len(categories))
    width = 0.8 / len(value_cols)  # Width of bars
    
    # Create bars for each value column
    for i, col in enumerate(value_cols):
        pos = x - 0.4 + (i + 0.5) * width
        
        if horizontal:
            ax.barh(pos, data[col], height=width, label=col, color=colors[i])
        else:
            ax.bar(pos, data[col], width=width, label=col, color=colors[i])
    
    # Set categories
    if horizontal:
        ax.set_yticks(x)
        ax.set_yticklabels(categories)
    else:
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
    
    # Format the chart
    x_label = 'Value' if horizontal else category_col
    y_label = category_col if horizontal else 'Value'
    
    return format_chart(fig, title=title, x_label=x_label, y_label=y_label)

def display_metric_cards(metrics, num_columns=4):
    """
    Display a row of metric cards in Streamlit
    
    Args:
        metrics (list): List of dicts with 'label', 'value', and optionally 'delta' and 'help'
        num_columns (int): Number of columns to display
    """
    # Create columns
    cols = st.columns(num_columns)
    
    # Display metrics in columns
    for i, metric in enumerate(metrics):
        col_idx = i % num_columns
        
        with cols[col_idx]:
            if 'delta' in metric:
                st.metric(
                    label=metric['label'],
                    value=metric['value'],
                    delta=metric['delta'],
                    help=metric.get('help', None)
                )
            else:
                st.metric(
                    label=metric['label'],
                    value=metric['value'],
                    help=metric.get('help', None)
                )

def plot_calendar_heatmap(data, date_column, value_column, title=None):
    """
    Create a calendar heatmap visualization
    
    Args:
        data (DataFrame): Data containing date and value columns
        date_column (str): Column name for dates
        value_column (str): Column name for values
        title (str): Chart title
        
    Returns:
        Figure: Matplotlib figure containing the heatmap
    """
    if data.empty:
        return None
    
    # Ensure date column is datetime
    data = data.copy()
    if not pd.api.types.is_datetime64_dtype(data[date_column]):
        data[date_column] = pd.to_datetime(data[date_column])
    
    # Extract year, month, and day
    data['year'] = data[date_column].dt.year
    data['month'] = data[date_column].dt.month
    data['day'] = data[date_column].dt.day
    
    # Pivot the data for heatmap format
    pivot_data = data.pivot_table(
        index='day', 
        columns='month', 
        values=value_column, 
        aggfunc='mean'
    )
    
    # Create figure
    fig = Figure(figsize=(10, 8))
    ax = fig.subplots()
    
    # Create heatmap
    sns.heatmap(
        pivot_data, 
        ax=ax, 
        cmap='YlGnBu', 
        linewidths=0.5,
        cbar_kws={'label': value_column}
    )
    
    # Set month names for x-axis
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_xticklabels([month_names[m-1] for m in sorted(data['month'].unique())])
    
    # Set title
    if title:
        ax.set_title(title, fontsize=14, pad=10)
    
    fig.tight_layout()
    return fig
