"""Tests for the main dashboard application.

This module contains comprehensive tests for the Interactive Data Dashboard,
including data processing, chart generation, and UI components.
"""

import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from io import StringIO
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from interactive_data_dashboard.main import (
    DataProcessor,
    ChartGenerator,
    CONFIG
)


class TestDataProcessor:
    """Test cases for DataProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'numeric_col': [1, 2, 3, 4, 5],
            'categorical_col': ['A', 'B', 'A', 'C', 'B'],
            'float_col': [1.1, 2.2, 3.3, 4.4, 5.5],
            'string_numbers': ['10', '20', '30', '40', '50'],
            'mixed_col': ['text', '100', 'more_text', '200', 'final_text']
        })
        
        self.data_with_nulls = pd.DataFrame({
            'col1': [1, 2, None, 4, 5],
            'col2': ['A', None, 'C', 'D', None],
            'col3': [1.1, 2.2, 3.3, None, 5.5]
        })
    
    def test_get_data_summary_basic(self):
        """Test basic data summary generation."""
        summary = DataProcessor.get_data_summary(self.sample_data)
        
        assert summary['shape'] == (5, 5)
        assert len(summary['columns']) == 5
        assert 'numeric_col' in summary['columns']
        assert 'dtypes' in summary
        assert 'missing_values' in summary
        assert 'memory_usage' in summary
    
    def test_get_data_summary_empty_dataframe(self):
        """Test data summary with empty dataframe."""
        empty_df = pd.DataFrame()
        summary = DataProcessor.get_data_summary(empty_df)
        
        assert summary == {}
    
    def test_get_data_summary_numeric_summary(self):
        """Test numeric summary in data summary."""
        summary = DataProcessor.get_data_summary(self.sample_data)
        
        assert 'numeric_summary' in summary
        numeric_summary = summary['numeric_summary']
        assert 'numeric_col' in numeric_summary
        assert 'float_col' in numeric_summary
        
        # Check if statistics are calculated correctly
        assert numeric_summary['numeric_col']['mean'] == 3.0
        assert numeric_summary['numeric_col']['count'] == 5.0
    
    def test_get_data_summary_categorical_summary(self):
        """Test categorical summary in data summary."""
        summary = DataProcessor.get_data_summary(self.sample_data)
        
        assert 'categorical_summary' in summary
        categorical_summary = summary['categorical_summary']
        assert 'categorical_col' in categorical_summary
        
        # Check value counts
        cat_counts = categorical_summary['categorical_col']
        assert cat_counts['A'] == 2
        assert cat_counts['B'] == 2
        assert cat_counts['C'] == 1
    
    def test_clean_data_basic(self):
        """Test basic data cleaning."""
        cleaned_df = DataProcessor.clean_data(self.sample_data.copy())
        
        # Should not change the original data structure
        assert cleaned_df.shape == self.sample_data.shape
        assert list(cleaned_df.columns) == list(self.sample_data.columns)
    
    def test_clean_data_convert_string_numbers(self):
        """Test conversion of string numbers to numeric."""
        cleaned_df = DataProcessor.clean_data(self.sample_data.copy())
        
        # string_numbers should be converted to numeric
        assert pd.api.types.is_numeric_dtype(cleaned_df['string_numbers'])
        assert cleaned_df['string_numbers'].iloc[0] == 10
        assert cleaned_df['string_numbers'].iloc[4] == 50
    
    def test_clean_data_remove_empty_rows_columns(self):
        """Test removal of completely empty rows and columns."""
        df_with_empty = self.sample_data.copy()
        df_with_empty['empty_col'] = None
        df_with_empty.loc[len(df_with_empty)] = [None] * len(df_with_empty.columns)
        
        cleaned_df = DataProcessor.clean_data(df_with_empty)
        
        # Empty column should be removed
        assert 'empty_col' not in cleaned_df.columns
        # Empty row should be removed
        assert len(cleaned_df) == len(self.sample_data)
    
    def test_clean_data_empty_dataframe(self):
        """Test cleaning empty dataframe."""
        empty_df = pd.DataFrame()
        cleaned_df = DataProcessor.clean_data(empty_df)
        
        assert cleaned_df.empty
    
    def test_filter_data_range_filter(self):
        """Test range filtering."""
        filters = {
            'numeric_col': {
                'type': 'range',
                'value': [2, 4]
            }
        }
        
        filtered_df = DataProcessor.filter_data(self.sample_data, filters)
        
        assert len(filtered_df) == 3  # Values 2, 3, 4
        assert filtered_df['numeric_col'].min() == 2
        assert filtered_df['numeric_col'].max() == 4
    
    def test_filter_data_categorical_filter(self):
        """Test categorical filtering."""
        filters = {
            'categorical_col': {
                'type': 'categorical',
                'value': ['A', 'B']
            }
        }
        
        filtered_df = DataProcessor.filter_data(self.sample_data, filters)
        
        assert len(filtered_df) == 4  # All A and B values
        assert set(filtered_df['categorical_col'].unique()) == {'A', 'B'}
    
    def test_filter_data_multiple_filters(self):
        """Test multiple filters applied together."""
        filters = {
            'numeric_col': {
                'type': 'range',
                'value': [2, 4]
            },
            'categorical_col': {
                'type': 'categorical',
                'value': ['A', 'B']
            }
        }
        
        filtered_df = DataProcessor.filter_data(self.sample_data, filters)
        
        # Should have rows where numeric_col is 2-4 AND categorical_col is A or B
        assert len(filtered_df) == 2  # Rows with values (2,'B') and (3,'A')
    
    def test_filter_data_nonexistent_column(self):
        """Test filtering with non-existent column."""
        filters = {
            'nonexistent_col': {
                'type': 'range',
                'value': [1, 5]
            }
        }
        
        filtered_df = DataProcessor.filter_data(self.sample_data, filters)
        
        # Should return original dataframe unchanged
        pd.testing.assert_frame_equal(filtered_df, self.sample_data)
    
    @patch('streamlit.cache_data')
    def test_load_csv_data_success(self, mock_cache):
        """Test successful CSV loading."""
        # Mock the cache decorator to return the function unchanged
        mock_cache.return_value = lambda func: func
        
        # Create a mock file object
        csv_content = "col1,col2\n1,A\n2,B\n3,C"
        mock_file = StringIO(csv_content)
        mock_file.name = "test.csv"
        
        with patch('pandas.read_csv') as mock_read_csv:
            expected_df = pd.DataFrame({
                'col1': [1, 2, 3],
                'col2': ['A', 'B', 'C']
            })
            mock_read_csv.return_value = expected_df
            
            result_df = DataProcessor.load_csv_data(mock_file)
            
            pd.testing.assert_frame_equal(result_df, expected_df)
            mock_read_csv.assert_called_once_with(mock_file)


class TestChartGenerator:
    """Test cases for ChartGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'x_numeric': [1, 2, 3, 4, 5],
            'y_numeric': [2, 4, 6, 8, 10],
            'category': ['A', 'B', 'A', 'C', 'B'],
            'size_col': [10, 20, 30, 40, 50]
        })
        
        self.chart_generator = ChartGenerator()
    
    def test_create_scatter_plot_basic(self):
        """Test basic scatter plot creation."""
        fig = self.chart_generator.create_scatter_plot(
            self.sample_data, 'x_numeric', 'y_numeric'
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert fig.data[0].type == 'scatter'
        assert fig.layout.xaxis.title.text == 'x_numeric'
        assert fig.layout.yaxis.title.text == 'y_numeric'
    
    def test_create_scatter_plot_with_color(self):
        """Test scatter plot with color grouping."""
        fig = self.chart_generator.create_scatter_plot(
            self.sample_data, 'x_numeric', 'y_numeric', color='category'
        )
        
        assert isinstance(fig, go.Figure)
        # Should have multiple traces for different categories
        assert len(fig.data) >= 1
    
    def test_create_scatter_plot_with_size(self):
        """Test scatter plot with size mapping."""
        fig = self.chart_generator.create_scatter_plot(
            self.sample_data, 'x_numeric', 'y_numeric', size='size_col'
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
    
    def test_create_bar_chart_basic(self):
        """Test basic bar chart creation."""
        fig = self.chart_generator.create_bar_chart(
            self.sample_data, 'category', 'y_numeric'
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert fig.data[0].type == 'bar'
        assert fig.layout.xaxis.title.text == 'category'
        assert fig.layout.yaxis.title.text == 'y_numeric'
    
    def test_create_line_chart_basic(self):
        """Test basic line chart creation."""
        fig = self.chart_generator.create_line_chart(
            self.sample_data, 'x_numeric', 'y_numeric'
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'
    
    def test_create_histogram_basic(self):
        """Test basic histogram creation."""
        fig = self.chart_generator.create_histogram(
            self.sample_data, 'x_numeric'
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert fig.data[0].type == 'histogram'
        assert fig.layout.xaxis.title.text == 'x_numeric'
        assert fig.layout.yaxis.title.text == 'Frequency'
    
    def test_create_histogram_with_bins(self):
        """Test histogram with custom bins."""
        fig = self.chart_generator.create_histogram(
            self.sample_data, 'x_numeric', bins=10
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
    
    def test_create_correlation_heatmap_basic(self):
        """Test correlation heatmap creation."""
        fig = self.chart_generator.create_correlation_heatmap(self.sample_data)
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert fig.data[0].type == 'heatmap'
    
    def test_create_correlation_heatmap_no_numeric_columns(self):
        """Test correlation heatmap with no numeric columns."""
        non_numeric_df = pd.DataFrame({
            'col1': ['A', 'B', 'C'],
            'col2': ['X', 'Y', 'Z']
        })
        
        with patch('streamlit.warning') as mock_warning:
            fig = self.chart_generator.create_correlation_heatmap(non_numeric_df)
            
            assert isinstance(fig, go.Figure)
            assert len(fig.data) == 0  # Empty figure
            mock_warning.assert_called_once()
    
    def test_create_pie_chart_basic(self):
        """Test basic pie chart creation."""
        fig = self.chart_generator.create_pie_chart(
            self.sample_data, 'category'
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert fig.data[0].type == 'pie'
    
    def test_chart_configuration_applied(self):
        """Test that chart configuration from CONFIG is applied."""
        fig = self.chart_generator.create_scatter_plot(
            self.sample_data, 'x_numeric', 'y_numeric'
        )
        
        # Check that height from CONFIG is applied
        assert fig.layout.height == CONFIG['chart_height']
        
        # Check that template from CONFIG is applied
        assert fig.layout.template.layout.template == CONFIG['default_theme']


class TestConfiguration:
    """Test cases for application configuration."""
    
    def test_config_defaults(self):
        """Test that CONFIG has expected default values."""
        assert 'max_upload_size' in CONFIG
        assert 'max_data_points' in CONFIG
        assert 'default_theme' in CONFIG
        assert 'chart_height' in CONFIG
        assert 'chart_width' in CONFIG
        assert 'enable_caching' in CONFIG
        
        # Test default values
        assert isinstance(CONFIG['max_upload_size'], int)
        assert isinstance(CONFIG['max_data_points'], int)
        assert isinstance(CONFIG['chart_height'], int)
        assert isinstance(CONFIG['chart_width'], int)
        assert isinstance(CONFIG['enable_caching'], bool)
    
    def test_config_environment_override(self):
        """Test that environment variables can override config."""
        with patch.dict(os.environ, {'MAX_UPLOAD_SIZE_MB': '500'}):
            # Reload the module to pick up environment changes
            import importlib
            import interactive_data_dashboard.main
            importlib.reload(interactive_data_dashboard.main)
            
            from interactive_data_dashboard.main import CONFIG
            assert CONFIG['max_upload_size'] == 500


class TestIntegration:
    """Integration tests for the dashboard components."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=100),
            'value': np.random.randn(100).cumsum(),
            'category': np.random.choice(['A', 'B', 'C'], 100),
            'size': np.random.randint(10, 100, 100)
        })
    
    def test_data_processing_pipeline(self):
        """Test the complete data processing pipeline."""
        # 1. Get data summary
        summary = DataProcessor.get_data_summary(self.sample_data)
        assert summary['shape'][0] == 100
        assert summary['shape'][1] == 4
        
        # 2. Clean data
        cleaned_data = DataProcessor.clean_data(self.sample_data)
        assert not cleaned_data.empty
        
        # 3. Apply filters
        filters = {
            'value': {
                'type': 'range',
                'value': [-2, 2]
            }
        }
        filtered_data = DataProcessor.filter_data(cleaned_data, filters)
        assert len(filtered_data) <= len(cleaned_data)
    
    def test_chart_generation_pipeline(self):
        """Test the complete chart generation pipeline."""
        chart_generator = ChartGenerator()
        
        # Test different chart types with the same data
        charts = [
            chart_generator.create_scatter_plot(self.sample_data, 'date', 'value'),
            chart_generator.create_line_chart(self.sample_data, 'date', 'value'),
            chart_generator.create_bar_chart(self.sample_data, 'category', 'value'),
            chart_generator.create_histogram(self.sample_data, 'value'),
            chart_generator.create_pie_chart(self.sample_data, 'category')
        ]
        
        for chart in charts:
            assert isinstance(chart, go.Figure)
            assert len(chart.data) > 0
    
    def test_performance_with_large_dataset(self):
        """Test performance with larger datasets."""
        large_data = pd.DataFrame({
            'x': np.random.randn(5000),
            'y': np.random.randn(5000),
            'category': np.random.choice(['A', 'B', 'C', 'D'], 5000)
        })
        
        # Test data processing
        start_time = pd.Timestamp.now()
        summary = DataProcessor.get_data_summary(large_data)
        processing_time = (pd.Timestamp.now() - start_time).total_seconds()
        
        assert processing_time < 5.0  # Should complete within 5 seconds
        assert summary['shape'][0] == 5000
        
        # Test chart generation
        chart_generator = ChartGenerator()
        start_time = pd.Timestamp.now()
        fig = chart_generator.create_scatter_plot(large_data, 'x', 'y')
        chart_time = (pd.Timestamp.now() - start_time).total_seconds()
        
        assert chart_time < 10.0  # Should complete within 10 seconds
        assert isinstance(fig, go.Figure)


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty dataframes."""
        empty_df = pd.DataFrame()
        
        # Data processing should handle empty dataframes gracefully
        summary = DataProcessor.get_data_summary(empty_df)
        assert summary == {}
        
        cleaned_df = DataProcessor.clean_data(empty_df)
        assert cleaned_df.empty
        
        filtered_df = DataProcessor.filter_data(empty_df, {})
        assert filtered_df.empty
    
    def test_invalid_column_names(self):
        """Test handling of invalid column names in chart generation."""
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        chart_generator = ChartGenerator()
        
        # This should not raise an exception, but might create an empty or error chart
        try:
            fig = chart_generator.create_scatter_plot(df, 'nonexistent_col', 'col2')
            # If it doesn't raise an exception, it should return a Figure object
            assert isinstance(fig, go.Figure)
        except Exception as e:
            # If it does raise an exception, it should be handled gracefully
            assert isinstance(e, (KeyError, ValueError))
    
    def test_mixed_data_types(self):
        """Test handling of mixed data types."""
        mixed_df = pd.DataFrame({
            'numeric': [1, 2, 3, 4, 5],
            'text': ['a', 'b', 'c', 'd', 'e'],
            'mixed': [1, 'text', 3.14, None, 'more_text'],
            'dates': pd.date_range('2023-01-01', periods=5)
        })
        
        # Data processing should handle mixed types
        summary = DataProcessor.get_data_summary(mixed_df)
        assert 'dtypes' in summary
        assert len(summary['dtypes']) == 4
        
        # Cleaning should work
        cleaned_df = DataProcessor.clean_data(mixed_df)
        assert not cleaned_df.empty
        assert cleaned_df.shape[1] == 4  # All columns should remain


if __name__ == '__main__':
    pytest.main([__file__, '-v'])