"""Data processing module for Interactive Data Dashboard.

This module provides comprehensive data processing capabilities including
loading, cleaning, transformation, and analysis of various data formats.
"""

import io
import logging
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype
import streamlit as st

from .config import get_config

# Configure logging
logger = logging.getLogger(__name__)
config = get_config()

# Suppress pandas warnings
warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)
warnings.filterwarnings('ignore', category=UserWarning)


class DataProcessor:
    """Comprehensive data processing class for handling various data operations."""
    
    def __init__(self):
        """Initialize the DataProcessor with configuration settings."""
        self.config = get_config()
        self.supported_formats = self.config.data.supported_file_types
        self.max_file_size = self.config.data.max_file_size_bytes
        self.max_data_points = self.config.data.max_data_points
        self.chunk_size = self.config.data.chunk_size
        self.default_encoding = self.config.data.default_encoding
        self.auto_detect_encoding = self.config.data.auto_detect_encoding
        
        logger.info(f"DataProcessor initialized with max_file_size={self.max_file_size}, max_data_points={self.max_data_points}")
    
    def load_data(self, file_obj: Union[io.BytesIO, io.StringIO, str, Path], 
                  file_type: Optional[str] = None, 
                  **kwargs) -> pd.DataFrame:
        """Load data from various file formats.
        
        Args:
            file_obj: File object, file path, or file content
            file_type: File type (csv, xlsx, json, parquet)
            **kwargs: Additional arguments for pandas readers
            
        Returns:
            pd.DataFrame: Loaded data
            
        Raises:
            ValueError: If file type is not supported or file is too large
            Exception: If data loading fails
        """
        try:
            # Determine file type if not provided
            if file_type is None:
                if hasattr(file_obj, 'name'):
                    file_type = Path(file_obj.name).suffix.lower().lstrip('.')
                else:
                    raise ValueError("File type must be specified when file_obj has no name attribute")
            
            # Validate file type
            if file_type not in self.supported_formats:
                raise ValueError(f"Unsupported file type: {file_type}. Supported types: {self.supported_formats}")
            
            # Check file size if it's a file object with size
            if hasattr(file_obj, 'size') and file_obj.size > self.max_file_size:
                raise ValueError(f"File size ({file_obj.size} bytes) exceeds maximum allowed size ({self.max_file_size} bytes)")
            
            logger.info(f"Loading {file_type} file")
            
            # Load data based on file type
            if file_type == 'csv':
                df = self._load_csv(file_obj, **kwargs)
            elif file_type in ['xlsx', 'xls']:
                df = self._load_excel(file_obj, **kwargs)
            elif file_type == 'json':
                df = self._load_json(file_obj, **kwargs)
            elif file_type == 'parquet':
                df = self._load_parquet(file_obj, **kwargs)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            # Validate loaded data
            if df.empty:
                raise ValueError("Loaded data is empty")
            
            # Limit data points if necessary
            if len(df) > self.max_data_points:
                logger.warning(f"Data has {len(df)} rows, limiting to {self.max_data_points}")
                df = df.head(self.max_data_points)
            
            logger.info(f"Successfully loaded data with shape {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _load_csv(self, file_obj: Union[io.BytesIO, io.StringIO, str, Path], **kwargs) -> pd.DataFrame:
        """Load CSV file with encoding detection and error handling."""
        default_kwargs = {
            'encoding': self.default_encoding,
            'low_memory': False,
            'na_values': ['', 'NA', 'N/A', 'null', 'NULL', 'None', 'none', '-', '--'],
            'keep_default_na': True,
            'skip_blank_lines': True
        }
        default_kwargs.update(kwargs)
        
        try:
            return pd.read_csv(file_obj, **default_kwargs)
        except UnicodeDecodeError:
            if self.auto_detect_encoding:
                logger.info("Attempting to detect file encoding")
                # Try common encodings
                encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                for encoding in encodings:
                    try:
                        if hasattr(file_obj, 'seek'):
                            file_obj.seek(0)
                        default_kwargs['encoding'] = encoding
                        return pd.read_csv(file_obj, **default_kwargs)
                    except UnicodeDecodeError:
                        continue
            raise
    
    def _load_excel(self, file_obj: Union[io.BytesIO, str, Path], **kwargs) -> pd.DataFrame:
        """Load Excel file with sheet detection."""
        default_kwargs = {
            'na_values': ['', 'NA', 'N/A', 'null', 'NULL', 'None', 'none', '-', '--'],
            'keep_default_na': True
        }
        default_kwargs.update(kwargs)
        
        # If no sheet specified, use the first sheet
        if 'sheet_name' not in default_kwargs:
            default_kwargs['sheet_name'] = 0
        
        return pd.read_excel(file_obj, **default_kwargs)
    
    def _load_json(self, file_obj: Union[io.BytesIO, io.StringIO, str, Path], **kwargs) -> pd.DataFrame:
        """Load JSON file with orientation detection."""
        default_kwargs = {
            'orient': 'records',
            'lines': False
        }
        default_kwargs.update(kwargs)
        
        try:
            return pd.read_json(file_obj, **default_kwargs)
        except ValueError:
            # Try different orientations
            orientations = ['records', 'index', 'values', 'columns']
            for orient in orientations:
                try:
                    if hasattr(file_obj, 'seek'):
                        file_obj.seek(0)
                    default_kwargs['orient'] = orient
                    return pd.read_json(file_obj, **default_kwargs)
                except ValueError:
                    continue
            raise
    
    def _load_parquet(self, file_obj: Union[io.BytesIO, str, Path], **kwargs) -> pd.DataFrame:
        """Load Parquet file."""
        return pd.read_parquet(file_obj, **kwargs)
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive data summary statistics.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dict containing summary statistics
        """
        try:
            summary = {
                'shape': df.shape,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'memory_usage': df.memory_usage(deep=True).sum(),
                'missing_values': df.isnull().sum().to_dict(),
                'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
                'duplicate_rows': df.duplicated().sum(),
                'numeric_columns': list(df.select_dtypes(include=[np.number]).columns),
                'categorical_columns': list(df.select_dtypes(include=['object', 'category']).columns),
                'datetime_columns': list(df.select_dtypes(include=['datetime64']).columns),
            }
            
            # Add statistics for numeric columns
            numeric_stats = {}
            for col in summary['numeric_columns']:
                numeric_stats[col] = {
                    'mean': float(df[col].mean()) if not df[col].isnull().all() else None,
                    'median': float(df[col].median()) if not df[col].isnull().all() else None,
                    'std': float(df[col].std()) if not df[col].isnull().all() else None,
                    'min': float(df[col].min()) if not df[col].isnull().all() else None,
                    'max': float(df[col].max()) if not df[col].isnull().all() else None,
                    'unique_values': int(df[col].nunique()),
                    'zeros': int((df[col] == 0).sum()),
                    'outliers': self._detect_outliers(df[col])
                }
            summary['numeric_statistics'] = numeric_stats
            
            # Add statistics for categorical columns
            categorical_stats = {}
            for col in summary['categorical_columns']:
                categorical_stats[col] = {
                    'unique_values': int(df[col].nunique()),
                    'most_frequent': df[col].mode().iloc[0] if not df[col].empty and not df[col].mode().empty else None,
                    'frequency_distribution': df[col].value_counts().head(10).to_dict()
                }
            summary['categorical_statistics'] = categorical_stats
            
            logger.info(f"Generated summary for DataFrame with shape {df.shape}")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating data summary: {str(e)}")
            raise
    
    def _detect_outliers(self, series: pd.Series, method: str = 'iqr') -> int:
        """Detect outliers in a numeric series.
        
        Args:
            series: Numeric pandas Series
            method: Method for outlier detection ('iqr' or 'zscore')
            
        Returns:
            Number of outliers detected
        """
        try:
            if series.isnull().all() or len(series) == 0:
                return 0
            
            if method == 'iqr':
                Q1 = series.quantile(0.25)
                Q3 = series.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = (series < lower_bound) | (series > upper_bound)
                return int(outliers.sum())
            
            elif method == 'zscore':
                z_scores = np.abs((series - series.mean()) / series.std())
                outliers = z_scores > 3
                return int(outliers.sum())
            
            else:
                return 0
                
        except Exception:
            return 0
    
    def clean_data(self, df: pd.DataFrame, 
                   remove_duplicates: bool = True,
                   handle_missing: str = 'drop',
                   missing_threshold: float = 0.5,
                   convert_dtypes: bool = True) -> pd.DataFrame:
        """Clean and preprocess the data.
        
        Args:
            df: Input DataFrame
            remove_duplicates: Whether to remove duplicate rows
            handle_missing: How to handle missing values ('drop', 'fill', 'ignore')
            missing_threshold: Threshold for dropping columns with too many missing values
            convert_dtypes: Whether to optimize data types
            
        Returns:
            Cleaned DataFrame
        """
        try:
            df_cleaned = df.copy()
            original_shape = df_cleaned.shape
            
            logger.info(f"Starting data cleaning for DataFrame with shape {original_shape}")
            
            # Remove completely empty rows and columns
            df_cleaned = df_cleaned.dropna(how='all', axis=0)  # Remove empty rows
            df_cleaned = df_cleaned.dropna(how='all', axis=1)  # Remove empty columns
            
            # Remove columns with too many missing values
            missing_ratio = df_cleaned.isnull().sum() / len(df_cleaned)
            cols_to_drop = missing_ratio[missing_ratio > missing_threshold].index
            if len(cols_to_drop) > 0:
                logger.info(f"Dropping columns with >{missing_threshold*100}% missing values: {list(cols_to_drop)}")
                df_cleaned = df_cleaned.drop(columns=cols_to_drop)
            
            # Handle missing values
            if handle_missing == 'drop':
                df_cleaned = df_cleaned.dropna()
            elif handle_missing == 'fill':
                # Fill numeric columns with median, categorical with mode
                for col in df_cleaned.columns:
                    if is_numeric_dtype(df_cleaned[col]):
                        df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
                    else:
                        mode_val = df_cleaned[col].mode()
                        if not mode_val.empty:
                            df_cleaned[col] = df_cleaned[col].fillna(mode_val.iloc[0])
            
            # Remove duplicates
            if remove_duplicates:
                duplicates_before = df_cleaned.duplicated().sum()
                df_cleaned = df_cleaned.drop_duplicates()
                duplicates_removed = duplicates_before - df_cleaned.duplicated().sum()
                if duplicates_removed > 0:
                    logger.info(f"Removed {duplicates_removed} duplicate rows")
            
            # Convert data types for optimization
            if convert_dtypes:
                df_cleaned = self._optimize_dtypes(df_cleaned)
            
            final_shape = df_cleaned.shape
            logger.info(f"Data cleaning completed. Shape changed from {original_shape} to {final_shape}")
            
            return df_cleaned
            
        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            raise
    
    def _optimize_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimize DataFrame data types to reduce memory usage."""
        try:
            df_optimized = df.copy()
            
            for col in df_optimized.columns:
                col_type = df_optimized[col].dtype
                
                # Optimize numeric columns
                if is_numeric_dtype(df_optimized[col]):
                    if col_type == 'int64':
                        if df_optimized[col].min() >= -128 and df_optimized[col].max() <= 127:
                            df_optimized[col] = df_optimized[col].astype('int8')
                        elif df_optimized[col].min() >= -32768 and df_optimized[col].max() <= 32767:
                            df_optimized[col] = df_optimized[col].astype('int16')
                        elif df_optimized[col].min() >= -2147483648 and df_optimized[col].max() <= 2147483647:
                            df_optimized[col] = df_optimized[col].astype('int32')
                    
                    elif col_type == 'float64':
                        df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
                
                # Convert object columns to category if beneficial
                elif col_type == 'object':
                    unique_ratio = df_optimized[col].nunique() / len(df_optimized[col])
                    if unique_ratio < 0.5:  # If less than 50% unique values
                        df_optimized[col] = df_optimized[col].astype('category')
            
            return df_optimized
            
        except Exception as e:
            logger.warning(f"Error optimizing data types: {str(e)}")
            return df
    
    def filter_data(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to the DataFrame.
        
        Args:
            df: Input DataFrame
            filters: Dictionary of column filters
                    Format: {'column_name': {'type': 'range|categorical|text', 'value': ...}}
            
        Returns:
            Filtered DataFrame
        """
        try:
            df_filtered = df.copy()
            
            for column, filter_config in filters.items():
                if column not in df_filtered.columns:
                    logger.warning(f"Column '{column}' not found in DataFrame")
                    continue
                
                filter_type = filter_config.get('type')
                filter_value = filter_config.get('value')
                
                if filter_type == 'range' and isinstance(filter_value, (list, tuple)) and len(filter_value) == 2:
                    min_val, max_val = filter_value
                    df_filtered = df_filtered[
                        (df_filtered[column] >= min_val) & (df_filtered[column] <= max_val)
                    ]
                
                elif filter_type == 'categorical' and isinstance(filter_value, (list, tuple)):
                    df_filtered = df_filtered[df_filtered[column].isin(filter_value)]
                
                elif filter_type == 'text' and isinstance(filter_value, str):
                    df_filtered = df_filtered[
                        df_filtered[column].astype(str).str.contains(filter_value, case=False, na=False)
                    ]
                
                elif filter_type == 'exact' and filter_value is not None:
                    df_filtered = df_filtered[df_filtered[column] == filter_value]
            
            logger.info(f"Applied filters, resulting shape: {df_filtered.shape}")
            return df_filtered
            
        except Exception as e:
            logger.error(f"Error filtering data: {str(e)}")
            raise
    
    def get_column_info(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Get detailed information about a specific column.
        
        Args:
            df: Input DataFrame
            column: Column name
            
        Returns:
            Dictionary with column information
        """
        try:
            if column not in df.columns:
                raise ValueError(f"Column '{column}' not found in DataFrame")
            
            series = df[column]
            info = {
                'name': column,
                'dtype': str(series.dtype),
                'non_null_count': int(series.count()),
                'null_count': int(series.isnull().sum()),
                'null_percentage': float(series.isnull().sum() / len(series) * 100),
                'unique_count': int(series.nunique()),
                'unique_percentage': float(series.nunique() / len(series) * 100),
                'memory_usage': int(series.memory_usage(deep=True))
            }
            
            # Add type-specific information
            if is_numeric_dtype(series):
                info.update({
                    'min': float(series.min()) if not series.isnull().all() else None,
                    'max': float(series.max()) if not series.isnull().all() else None,
                    'mean': float(series.mean()) if not series.isnull().all() else None,
                    'median': float(series.median()) if not series.isnull().all() else None,
                    'std': float(series.std()) if not series.isnull().all() else None,
                    'skewness': float(series.skew()) if not series.isnull().all() else None,
                    'kurtosis': float(series.kurtosis()) if not series.isnull().all() else None,
                    'zeros_count': int((series == 0).sum()),
                    'outliers_count': self._detect_outliers(series)
                })
            
            elif is_datetime64_any_dtype(series):
                info.update({
                    'min_date': series.min(),
                    'max_date': series.max(),
                    'date_range_days': (series.max() - series.min()).days if not series.isnull().all() else None
                })
            
            else:  # Categorical/Object
                value_counts = series.value_counts()
                info.update({
                    'most_frequent': value_counts.index[0] if not value_counts.empty else None,
                    'most_frequent_count': int(value_counts.iloc[0]) if not value_counts.empty else None,
                    'least_frequent': value_counts.index[-1] if not value_counts.empty else None,
                    'least_frequent_count': int(value_counts.iloc[-1]) if not value_counts.empty else None,
                    'top_values': value_counts.head(10).to_dict()
                })
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting column info for '{column}': {str(e)}")
            raise
    
    def sample_data(self, df: pd.DataFrame, n: Optional[int] = None, 
                   method: str = 'random') -> pd.DataFrame:
        """Sample data from DataFrame.
        
        Args:
            df: Input DataFrame
            n: Number of samples (default: config.data_sample_size)
            method: Sampling method ('random', 'head', 'tail')
            
        Returns:
            Sampled DataFrame
        """
        try:
            if n is None:
                n = min(self.config.data.data_sample_size, len(df))
            
            if n >= len(df):
                return df.copy()
            
            if method == 'random':
                return df.sample(n=n, random_state=42)
            elif method == 'head':
                return df.head(n)
            elif method == 'tail':
                return df.tail(n)
            else:
                raise ValueError(f"Unknown sampling method: {method}")
                
        except Exception as e:
            logger.error(f"Error sampling data: {str(e)}")
            raise
    
    @st.cache_data(ttl=3600)
    def load_and_cache_data(_self, file_obj, file_type: str, **kwargs) -> pd.DataFrame:
        """Load and cache data with Streamlit caching.
        
        Note: The _self parameter is used to avoid hashing the DataProcessor instance.
        """
        return _self.load_data(file_obj, file_type, **kwargs)


# Utility functions
def detect_file_type(filename: str) -> str:
    """Detect file type from filename.
    
    Args:
        filename: Name of the file
        
    Returns:
        File type string
    """
    return Path(filename).suffix.lower().lstrip('.')


def validate_dataframe(df: pd.DataFrame, min_rows: int = 1, min_cols: int = 1) -> bool:
    """Validate DataFrame meets minimum requirements.
    
    Args:
        df: DataFrame to validate
        min_rows: Minimum number of rows required
        min_cols: Minimum number of columns required
        
    Returns:
        True if valid, False otherwise
    """
    return not df.empty and len(df) >= min_rows and len(df.columns) >= min_cols


def get_memory_usage(df: pd.DataFrame) -> Dict[str, Union[int, str]]:
    """Get memory usage information for DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with memory usage information
    """
    memory_bytes = df.memory_usage(deep=True).sum()
    memory_mb = memory_bytes / (1024 * 1024)
    
    return {
        'bytes': memory_bytes,
        'mb': round(memory_mb, 2),
        'formatted': f"{memory_mb:.2f} MB" if memory_mb >= 1 else f"{memory_bytes / 1024:.2f} KB"
    }