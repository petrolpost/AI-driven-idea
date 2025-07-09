"""Utility functions for Interactive Data Dashboard.

This module provides various utility functions for data processing,
validation, formatting, and other common operations.
"""

import logging
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import streamlit as st
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype

# Configure logging
logger = logging.getLogger(__name__)


# Data Validation Utilities
def validate_dataframe(df: pd.DataFrame, min_rows: int = 1, min_cols: int = 1) -> bool:
    """Validate DataFrame meets minimum requirements.
    
    Args:
        df: DataFrame to validate
        min_rows: Minimum number of rows required
        min_cols: Minimum number of columns required
        
    Returns:
        True if valid, False otherwise
    """
    try:
        if df is None or df.empty:
            return False
        
        if len(df) < min_rows:
            logger.warning(f"DataFrame has {len(df)} rows, minimum {min_rows} required")
            return False
        
        if len(df.columns) < min_cols:
            logger.warning(f"DataFrame has {len(df.columns)} columns, minimum {min_cols} required")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating DataFrame: {str(e)}")
        return False


def validate_column_exists(df: pd.DataFrame, column: str) -> bool:
    """Check if column exists in DataFrame.
    
    Args:
        df: DataFrame to check
        column: Column name to validate
        
    Returns:
        True if column exists, False otherwise
    """
    return column in df.columns


def validate_numeric_column(df: pd.DataFrame, column: str) -> bool:
    """Check if column contains numeric data.
    
    Args:
        df: DataFrame to check
        column: Column name to validate
        
    Returns:
        True if column is numeric, False otherwise
    """
    if not validate_column_exists(df, column):
        return False
    
    return is_numeric_dtype(df[column])


def validate_categorical_column(df: pd.DataFrame, column: str) -> bool:
    """Check if column contains categorical data.
    
    Args:
        df: DataFrame to check
        column: Column name to validate
        
    Returns:
        True if column is categorical, False otherwise
    """
    if not validate_column_exists(df, column):
        return False
    
    return df[column].dtype in ['object', 'category'] or df[column].dtype.name == 'string'


def validate_datetime_column(df: pd.DataFrame, column: str) -> bool:
    """Check if column contains datetime data.
    
    Args:
        df: DataFrame to check
        column: Column name to validate
        
    Returns:
        True if column is datetime, False otherwise
    """
    if not validate_column_exists(df, column):
        return False
    
    return is_datetime64_any_dtype(df[column])


# Data Type Detection and Conversion
def detect_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """Detect and categorize column types.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary mapping column names to types
    """
    column_types = {}
    
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            if df[col].dtype in ['int64', 'int32', 'int16', 'int8']:
                column_types[col] = 'integer'
            else:
                column_types[col] = 'float'
        elif is_datetime64_any_dtype(df[col]):
            column_types[col] = 'datetime'
        elif df[col].dtype == 'bool':
            column_types[col] = 'boolean'
        elif df[col].dtype == 'category':
            column_types[col] = 'category'
        else:
            # Try to detect if it's a potential datetime or numeric column
            sample_values = df[col].dropna().head(100)
            
            if _is_potential_datetime(sample_values):
                column_types[col] = 'potential_datetime'
            elif _is_potential_numeric(sample_values):
                column_types[col] = 'potential_numeric'
            else:
                column_types[col] = 'text'
    
    return column_types


def _is_potential_datetime(series: pd.Series) -> bool:
    """Check if series could be converted to datetime."""
    try:
        # Try to parse a sample of values
        sample = series.head(10).astype(str)
        datetime_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
            r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
        ]
        
        for pattern in datetime_patterns:
            if sample.str.match(pattern).any():
                return True
        
        # Try pandas to_datetime
        pd.to_datetime(sample.head(5), errors='raise')
        return True
        
    except:
        return False


def _is_potential_numeric(series: pd.Series) -> bool:
    """Check if series could be converted to numeric."""
    try:
        # Try to convert a sample to numeric
        sample = series.head(10)
        pd.to_numeric(sample, errors='raise')
        return True
    except:
        return False


def convert_column_types(df: pd.DataFrame, conversions: Dict[str, str]) -> pd.DataFrame:
    """Convert column types based on specifications.
    
    Args:
        df: DataFrame to convert
        conversions: Dictionary mapping column names to target types
        
    Returns:
        DataFrame with converted types
    """
    df_converted = df.copy()
    
    for col, target_type in conversions.items():
        if col not in df_converted.columns:
            logger.warning(f"Column '{col}' not found in DataFrame")
            continue
        
        try:
            if target_type == 'numeric':
                df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
            elif target_type == 'datetime':
                df_converted[col] = pd.to_datetime(df_converted[col], errors='coerce')
            elif target_type == 'category':
                df_converted[col] = df_converted[col].astype('category')
            elif target_type == 'string':
                df_converted[col] = df_converted[col].astype('string')
            elif target_type == 'boolean':
                df_converted[col] = df_converted[col].astype('bool')
            
            logger.info(f"Converted column '{col}' to {target_type}")
            
        except Exception as e:
            logger.error(f"Error converting column '{col}' to {target_type}: {str(e)}")
    
    return df_converted


# Data Formatting Utilities
def format_number(value: Union[int, float], precision: int = 2, 
                 use_thousands_separator: bool = True) -> str:
    """Format numeric values for display.
    
    Args:
        value: Numeric value to format
        precision: Number of decimal places
        use_thousands_separator: Whether to use thousands separator
        
    Returns:
        Formatted string
    """
    try:
        if pd.isna(value):
            return "N/A"
        
        if use_thousands_separator:
            return f"{value:,.{precision}f}"
        else:
            return f"{value:.{precision}f}"
            
    except (ValueError, TypeError):
        return str(value)


def format_percentage(value: Union[int, float], precision: int = 1) -> str:
    """Format value as percentage.
    
    Args:
        value: Numeric value (0-1 range)
        precision: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    try:
        if pd.isna(value):
            return "N/A"
        
        return f"{value * 100:.{precision}f}%"
        
    except (ValueError, TypeError):
        return str(value)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    try:
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(np.floor(np.log(size_bytes) / np.log(1024)))
        p = np.power(1024, i)
        s = round(size_bytes / p, 2)
        
        return f"{s} {size_names[i]}"
        
    except (ValueError, TypeError, OverflowError):
        return str(size_bytes)


def format_duration(seconds: Union[int, float]) -> str:
    """Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    try:
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
            
    except (ValueError, TypeError):
        return str(seconds)


# Data Summary Utilities
def get_column_summary(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """Get comprehensive summary of a column.
    
    Args:
        df: DataFrame containing the column
        column: Column name to summarize
        
    Returns:
        Dictionary with column summary statistics
    """
    if column not in df.columns:
        return {"error": f"Column '{column}' not found"}
    
    series = df[column]
    summary = {
        "name": column,
        "dtype": str(series.dtype),
        "count": len(series),
        "non_null_count": series.count(),
        "null_count": series.isnull().sum(),
        "null_percentage": (series.isnull().sum() / len(series)) * 100,
        "unique_count": series.nunique(),
        "memory_usage": series.memory_usage(deep=True)
    }
    
    # Type-specific statistics
    if is_numeric_dtype(series):
        summary.update({
            "min": series.min(),
            "max": series.max(),
            "mean": series.mean(),
            "median": series.median(),
            "std": series.std(),
            "q25": series.quantile(0.25),
            "q75": series.quantile(0.75),
            "skewness": series.skew(),
            "kurtosis": series.kurtosis()
        })
    elif is_datetime64_any_dtype(series):
        summary.update({
            "min_date": series.min(),
            "max_date": series.max(),
            "date_range": series.max() - series.min()
        })
    else:
        # Categorical/text columns
        value_counts = series.value_counts()
        summary.update({
            "most_frequent": value_counts.index[0] if len(value_counts) > 0 else None,
            "most_frequent_count": value_counts.iloc[0] if len(value_counts) > 0 else 0,
            "least_frequent": value_counts.index[-1] if len(value_counts) > 0 else None,
            "least_frequent_count": value_counts.iloc[-1] if len(value_counts) > 0 else 0
        })
    
    return summary


def detect_outliers(series: pd.Series, method: str = 'iqr', 
                   threshold: float = 1.5) -> Tuple[pd.Series, Dict[str, Any]]:
    """Detect outliers in a numeric series.
    
    Args:
        series: Numeric series to analyze
        method: Method to use ('iqr', 'zscore', 'modified_zscore')
        threshold: Threshold for outlier detection
        
    Returns:
        Tuple of (outlier_mask, outlier_info)
    """
    if not is_numeric_dtype(series):
        raise ValueError("Series must be numeric for outlier detection")
    
    series_clean = series.dropna()
    
    if method == 'iqr':
        Q1 = series_clean.quantile(0.25)
        Q3 = series_clean.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        outlier_mask = (series < lower_bound) | (series > upper_bound)
        
        info = {
            "method": "IQR",
            "threshold": threshold,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "Q1": Q1,
            "Q3": Q3,
            "IQR": IQR
        }
        
    elif method == 'zscore':
        z_scores = np.abs((series_clean - series_clean.mean()) / series_clean.std())
        outlier_mask = pd.Series(False, index=series.index)
        outlier_mask.loc[z_scores.index] = z_scores > threshold
        
        info = {
            "method": "Z-Score",
            "threshold": threshold,
            "mean": series_clean.mean(),
            "std": series_clean.std()
        }
        
    elif method == 'modified_zscore':
        median = series_clean.median()
        mad = np.median(np.abs(series_clean - median))
        modified_z_scores = 0.6745 * (series_clean - median) / mad
        outlier_mask = pd.Series(False, index=series.index)
        outlier_mask.loc[modified_z_scores.index] = np.abs(modified_z_scores) > threshold
        
        info = {
            "method": "Modified Z-Score",
            "threshold": threshold,
            "median": median,
            "mad": mad
        }
        
    else:
        raise ValueError(f"Unknown outlier detection method: {method}")
    
    info["outlier_count"] = outlier_mask.sum()
    info["outlier_percentage"] = (outlier_mask.sum() / len(series)) * 100
    
    return outlier_mask, info


# File Utilities
def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Get comprehensive file information.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with file information
    """
    try:
        path = Path(file_path)
        
        if not path.exists():
            return {"error": "File does not exist"}
        
        stat = path.stat()
        
        return {
            "name": path.name,
            "stem": path.stem,
            "suffix": path.suffix,
            "size_bytes": stat.st_size,
            "size_formatted": format_file_size(stat.st_size),
            "created": datetime.fromtimestamp(stat.st_ctime),
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "accessed": datetime.fromtimestamp(stat.st_atime),
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
            "absolute_path": str(path.absolute())
        }
        
    except Exception as e:
        return {"error": str(e)}


def safe_filename(filename: str) -> str:
    """Create a safe filename by removing/replacing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename
    """
    # Remove or replace invalid characters
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    safe_name = safe_name.strip(' .')
    
    # Ensure it's not empty
    if not safe_name:
        safe_name = "untitled"
    
    # Limit length
    if len(safe_name) > 255:
        name, ext = os.path.splitext(safe_name)
        safe_name = name[:255-len(ext)] + ext
    
    return safe_name


# Streamlit Utilities
def create_download_button(data: Union[str, bytes], filename: str, 
                          mime_type: str, label: str = "Download") -> None:
    """Create a Streamlit download button.
    
    Args:
        data: Data to download
        filename: Suggested filename
        mime_type: MIME type of the data
        label: Button label
    """
    st.download_button(
        label=label,
        data=data,
        file_name=safe_filename(filename),
        mime=mime_type
    )


def display_dataframe_info(df: pd.DataFrame, title: str = "DataFrame Information") -> None:
    """Display comprehensive DataFrame information in Streamlit.
    
    Args:
        df: DataFrame to display information for
        title: Section title
    """
    st.subheader(title)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Rows", f"{len(df):,}")
    
    with col2:
        st.metric("Columns", len(df.columns))
    
    with col3:
        memory_usage = df.memory_usage(deep=True).sum()
        st.metric("Memory Usage", format_file_size(memory_usage))
    
    with col4:
        missing_cells = df.isnull().sum().sum()
        total_cells = len(df) * len(df.columns)
        missing_pct = (missing_cells / total_cells) * 100 if total_cells > 0 else 0
        st.metric("Missing Data", f"{missing_pct:.1f}%")


def create_column_selector(df: pd.DataFrame, label: str, 
                          column_types: Optional[List[str]] = None,
                          key: Optional[str] = None) -> Optional[str]:
    """Create a column selector widget.
    
    Args:
        df: DataFrame to select columns from
        label: Widget label
        column_types: Filter by column types (e.g., ['numeric', 'categorical'])
        key: Widget key
        
    Returns:
        Selected column name or None
    """
    available_columns = df.columns.tolist()
    
    if column_types:
        filtered_columns = []
        for col in available_columns:
            if 'numeric' in column_types and is_numeric_dtype(df[col]):
                filtered_columns.append(col)
            elif 'categorical' in column_types and validate_categorical_column(df, col):
                filtered_columns.append(col)
            elif 'datetime' in column_types and is_datetime64_any_dtype(df[col]):
                filtered_columns.append(col)
        
        available_columns = filtered_columns
    
    if not available_columns:
        st.warning(f"No columns available for {label}")
        return None
    
    return st.selectbox(label, options=available_columns, key=key)


def create_multi_column_selector(df: pd.DataFrame, label: str,
                                column_types: Optional[List[str]] = None,
                                key: Optional[str] = None) -> List[str]:
    """Create a multi-column selector widget.
    
    Args:
        df: DataFrame to select columns from
        label: Widget label
        column_types: Filter by column types
        key: Widget key
        
    Returns:
        List of selected column names
    """
    available_columns = df.columns.tolist()
    
    if column_types:
        filtered_columns = []
        for col in available_columns:
            if 'numeric' in column_types and is_numeric_dtype(df[col]):
                filtered_columns.append(col)
            elif 'categorical' in column_types and validate_categorical_column(df, col):
                filtered_columns.append(col)
            elif 'datetime' in column_types and is_datetime64_any_dtype(df[col]):
                filtered_columns.append(col)
        
        available_columns = filtered_columns
    
    if not available_columns:
        st.warning(f"No columns available for {label}")
        return []
    
    return st.multiselect(label, options=available_columns, key=key)


# Performance Utilities
def measure_execution_time(func):
    """Decorator to measure function execution time."""
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        logger.info(f"Function '{func.__name__}' executed in {execution_time:.3f} seconds")
        
        return result
    
    return wrapper


def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame memory usage by downcasting numeric types.
    
    Args:
        df: DataFrame to optimize
        
    Returns:
        Optimized DataFrame
    """
    df_optimized = df.copy()
    
    # Optimize numeric columns
    for col in df_optimized.select_dtypes(include=['int64']).columns:
        df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
    
    for col in df_optimized.select_dtypes(include=['float64']).columns:
        df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
    
    # Convert object columns to category if beneficial
    for col in df_optimized.select_dtypes(include=['object']).columns:
        if df_optimized[col].nunique() / len(df_optimized) < 0.5:  # Less than 50% unique values
            df_optimized[col] = df_optimized[col].astype('category')
    
    # Log memory savings
    original_memory = df.memory_usage(deep=True).sum()
    optimized_memory = df_optimized.memory_usage(deep=True).sum()
    savings = original_memory - optimized_memory
    savings_pct = (savings / original_memory) * 100
    
    logger.info(f"Memory optimization: {format_file_size(savings)} saved ({savings_pct:.1f}%)")
    
    return df_optimized


# Error Handling Utilities
class DataProcessingError(Exception):
    """Custom exception for data processing errors."""
    pass


class ChartGenerationError(Exception):
    """Custom exception for chart generation errors."""
    pass


def handle_errors(func):
    """Decorator for consistent error handling."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            st.error(f"An error occurred: {str(e)}")
            return None
    
    return wrapper


# Constants
SUPPORTED_FILE_TYPES = {
    '.csv': 'CSV',
    '.xlsx': 'Excel',
    '.xls': 'Excel',
    '.json': 'JSON',
    '.parquet': 'Parquet',
    '.feather': 'Feather',
    '.pkl': 'Pickle',
    '.pickle': 'Pickle'
}

CHART_COLOR_PALETTES = {
    'Default': 'plotly',
    'Viridis': 'viridis',
    'Plasma': 'plasma',
    'Inferno': 'inferno',
    'Magma': 'magma',
    'Cividis': 'cividis',
    'Blues': 'blues',
    'Reds': 'reds',
    'Greens': 'greens',
    'Rainbow': 'rainbow'
}

DATE_FORMATS = [
    '%Y-%m-%d',
    '%m/%d/%Y',
    '%d/%m/%Y',
    '%Y/%m/%d',
    '%m-%d-%Y',
    '%d-%m-%Y',
    '%Y-%m-%d %H:%M:%S',
    '%m/%d/%Y %H:%M:%S',
    '%d/%m/%Y %H:%M:%S'
]