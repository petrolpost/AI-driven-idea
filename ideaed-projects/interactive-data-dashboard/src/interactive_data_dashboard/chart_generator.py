"""Chart generation module for Interactive Data Dashboard.

This module provides comprehensive chart generation capabilities using Plotly
for creating interactive and customizable visualizations.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import streamlit as st

from .config import get_config, ChartTheme

# Configure logging
logger = logging.getLogger(__name__)
config = get_config()


class ChartGenerator:
    """Comprehensive chart generation class using Plotly."""
    
    def __init__(self):
        """Initialize the ChartGenerator with configuration settings."""
        self.config = get_config()
        self.default_theme = self.config.charts.default_theme.value
        self.default_height = self.config.charts.height
        self.default_width = self.config.charts.width
        self.margin = self.config.charts.margin_dict
        self.enable_animations = self.config.charts.enable_animations
        
        # Color palettes
        self.color_palettes = {
            'default': px.colors.qualitative.Set1,
            'pastel': px.colors.qualitative.Pastel,
            'bold': px.colors.qualitative.Bold,
            'vivid': px.colors.qualitative.Vivid,
            'safe': px.colors.qualitative.Safe,
            'prism': px.colors.qualitative.Prism,
            'dark24': px.colors.qualitative.Dark24,
            'light24': px.colors.qualitative.Light24
        }
        
        logger.info(f"ChartGenerator initialized with theme={self.default_theme}, size={self.default_width}x{self.default_height}")
    
    def create_scatter_plot(self, df: pd.DataFrame, x: str, y: str, 
                           color: Optional[str] = None, size: Optional[str] = None,
                           title: Optional[str] = None, **kwargs) -> go.Figure:
        """Create an interactive scatter plot.
        
        Args:
            df: Input DataFrame
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color encoding
            size: Column name for size encoding
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating scatter plot: x={x}, y={y}, color={color}, size={size}")
            
            # Validate columns
            self._validate_columns(df, [x, y] + [col for col in [color, size] if col is not None])
            
            # Create the plot
            fig = px.scatter(
                df, x=x, y=y, color=color, size=size,
                title=title or f"{y} vs {x}",
                template=self.default_theme,
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating scatter plot: {str(e)}")
            raise
    
    def create_line_plot(self, df: pd.DataFrame, x: str, y: str,
                        color: Optional[str] = None, title: Optional[str] = None,
                        **kwargs) -> go.Figure:
        """Create an interactive line plot.
        
        Args:
            df: Input DataFrame
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color encoding (multiple lines)
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating line plot: x={x}, y={y}, color={color}")
            
            # Validate columns
            self._validate_columns(df, [x, y] + ([color] if color else []))
            
            # Create the plot
            fig = px.line(
                df, x=x, y=y, color=color,
                title=title or f"{y} over {x}",
                template=self.default_theme,
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating line plot: {str(e)}")
            raise
    
    def create_bar_chart(self, df: pd.DataFrame, x: str, y: str,
                        color: Optional[str] = None, orientation: str = 'v',
                        title: Optional[str] = None, **kwargs) -> go.Figure:
        """Create an interactive bar chart.
        
        Args:
            df: Input DataFrame
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color encoding
            orientation: 'v' for vertical, 'h' for horizontal
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating bar chart: x={x}, y={y}, color={color}, orientation={orientation}")
            
            # Validate columns
            self._validate_columns(df, [x, y] + ([color] if color else []))
            
            # Create the plot
            fig = px.bar(
                df, x=x, y=y, color=color,
                orientation=orientation,
                title=title or f"{y} by {x}",
                template=self.default_theme,
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating bar chart: {str(e)}")
            raise
    
    def create_histogram(self, df: pd.DataFrame, x: str, bins: Optional[int] = None,
                        color: Optional[str] = None, title: Optional[str] = None,
                        **kwargs) -> go.Figure:
        """Create an interactive histogram.
        
        Args:
            df: Input DataFrame
            x: Column name for the variable
            bins: Number of bins (auto if None)
            color: Column name for color encoding
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating histogram: x={x}, bins={bins}, color={color}")
            
            # Validate columns
            self._validate_columns(df, [x] + ([color] if color else []))
            
            # Create the plot
            fig = px.histogram(
                df, x=x, color=color, nbins=bins,
                title=title or f"Distribution of {x}",
                template=self.default_theme,
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating histogram: {str(e)}")
            raise
    
    def create_box_plot(self, df: pd.DataFrame, x: Optional[str] = None, y: str = None,
                       color: Optional[str] = None, title: Optional[str] = None,
                       **kwargs) -> go.Figure:
        """Create an interactive box plot.
        
        Args:
            df: Input DataFrame
            x: Column name for categories (optional)
            y: Column name for values
            color: Column name for color encoding
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating box plot: x={x}, y={y}, color={color}")
            
            # Validate columns
            columns_to_validate = [col for col in [x, y, color] if col is not None]
            self._validate_columns(df, columns_to_validate)
            
            # Create the plot
            fig = px.box(
                df, x=x, y=y, color=color,
                title=title or f"Box Plot of {y or 'Values'}",
                template=self.default_theme,
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating box plot: {str(e)}")
            raise
    
    def create_violin_plot(self, df: pd.DataFrame, x: Optional[str] = None, y: str = None,
                          color: Optional[str] = None, title: Optional[str] = None,
                          **kwargs) -> go.Figure:
        """Create an interactive violin plot.
        
        Args:
            df: Input DataFrame
            x: Column name for categories (optional)
            y: Column name for values
            color: Column name for color encoding
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating violin plot: x={x}, y={y}, color={color}")
            
            # Validate columns
            columns_to_validate = [col for col in [x, y, color] if col is not None]
            self._validate_columns(df, columns_to_validate)
            
            # Create the plot
            fig = px.violin(
                df, x=x, y=y, color=color,
                title=title or f"Violin Plot of {y or 'Values'}",
                template=self.default_theme,
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating violin plot: {str(e)}")
            raise
    
    def create_pie_chart(self, df: pd.DataFrame, values: str, names: str,
                        title: Optional[str] = None, **kwargs) -> go.Figure:
        """Create an interactive pie chart.
        
        Args:
            df: Input DataFrame
            values: Column name for values
            names: Column name for labels
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating pie chart: values={values}, names={names}")
            
            # Validate columns
            self._validate_columns(df, [values, names])
            
            # Aggregate data if needed
            df_agg = df.groupby(names)[values].sum().reset_index()
            
            # Create the plot
            fig = px.pie(
                df_agg, values=values, names=names,
                title=title or f"Distribution of {values} by {names}",
                template=self.default_theme,
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating pie chart: {str(e)}")
            raise
    
    def create_heatmap(self, df: pd.DataFrame, x: str, y: str, z: str,
                      title: Optional[str] = None, **kwargs) -> go.Figure:
        """Create an interactive heatmap.
        
        Args:
            df: Input DataFrame
            x: Column name for x-axis
            y: Column name for y-axis
            z: Column name for values (color intensity)
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating heatmap: x={x}, y={y}, z={z}")
            
            # Validate columns
            self._validate_columns(df, [x, y, z])
            
            # Create pivot table for heatmap
            pivot_df = df.pivot_table(values=z, index=y, columns=x, aggfunc='mean')
            
            # Create the plot
            fig = px.imshow(
                pivot_df,
                title=title or f"Heatmap of {z}",
                template=self.default_theme,
                aspect='auto',
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating heatmap: {str(e)}")
            raise
    
    def create_correlation_heatmap(self, df: pd.DataFrame, columns: Optional[List[str]] = None,
                                  title: Optional[str] = None, **kwargs) -> go.Figure:
        """Create a correlation heatmap for numeric columns.
        
        Args:
            df: Input DataFrame
            columns: List of columns to include (all numeric if None)
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating correlation heatmap for columns: {columns}")
            
            # Select numeric columns
            if columns is None:
                numeric_df = df.select_dtypes(include=[np.number])
            else:
                self._validate_columns(df, columns)
                numeric_df = df[columns].select_dtypes(include=[np.number])
            
            if numeric_df.empty:
                raise ValueError("No numeric columns found for correlation analysis")
            
            # Calculate correlation matrix
            corr_matrix = numeric_df.corr()
            
            # Create the heatmap
            fig = px.imshow(
                corr_matrix,
                title=title or "Correlation Matrix",
                template=self.default_theme,
                color_continuous_scale='RdBu_r',
                aspect='auto',
                **kwargs
            )
            
            # Add correlation values as text
            fig.update_traces(
                text=np.around(corr_matrix.values, decimals=2),
                texttemplate="%{text}",
                textfont={"size": 10}
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating correlation heatmap: {str(e)}")
            raise
    
    def create_3d_scatter(self, df: pd.DataFrame, x: str, y: str, z: str,
                         color: Optional[str] = None, size: Optional[str] = None,
                         title: Optional[str] = None, **kwargs) -> go.Figure:
        """Create a 3D scatter plot.
        
        Args:
            df: Input DataFrame
            x: Column name for x-axis
            y: Column name for y-axis
            z: Column name for z-axis
            color: Column name for color encoding
            size: Column name for size encoding
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating 3D scatter plot: x={x}, y={y}, z={z}, color={color}, size={size}")
            
            # Validate columns
            self._validate_columns(df, [x, y, z] + [col for col in [color, size] if col is not None])
            
            # Create the plot
            fig = px.scatter_3d(
                df, x=x, y=y, z=z, color=color, size=size,
                title=title or f"3D Scatter: {x}, {y}, {z}",
                template=self.default_theme,
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating 3D scatter plot: {str(e)}")
            raise
    
    def create_sunburst_chart(self, df: pd.DataFrame, path: List[str], values: str,
                             title: Optional[str] = None, **kwargs) -> go.Figure:
        """Create a sunburst chart for hierarchical data.
        
        Args:
            df: Input DataFrame
            path: List of column names representing hierarchy levels
            values: Column name for values
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating sunburst chart: path={path}, values={values}")
            
            # Validate columns
            self._validate_columns(df, path + [values])
            
            # Create the plot
            fig = px.sunburst(
                df, path=path, values=values,
                title=title or "Sunburst Chart",
                template=self.default_theme,
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating sunburst chart: {str(e)}")
            raise
    
    def create_treemap(self, df: pd.DataFrame, path: List[str], values: str,
                      title: Optional[str] = None, **kwargs) -> go.Figure:
        """Create a treemap for hierarchical data.
        
        Args:
            df: Input DataFrame
            path: List of column names representing hierarchy levels
            values: Column name for values
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating treemap: path={path}, values={values}")
            
            # Validate columns
            self._validate_columns(df, path + [values])
            
            # Create the plot
            fig = px.treemap(
                df, path=path, values=values,
                title=title or "Treemap",
                template=self.default_theme,
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating treemap: {str(e)}")
            raise
    
    def create_parallel_coordinates(self, df: pd.DataFrame, dimensions: List[str],
                                   color: Optional[str] = None,
                                   title: Optional[str] = None, **kwargs) -> go.Figure:
        """Create a parallel coordinates plot.
        
        Args:
            df: Input DataFrame
            dimensions: List of column names for dimensions
            color: Column name for color encoding
            title: Chart title
            **kwargs: Additional Plotly arguments
            
        Returns:
            Plotly Figure object
        """
        try:
            logger.info(f"Creating parallel coordinates: dimensions={dimensions}, color={color}")
            
            # Validate columns
            self._validate_columns(df, dimensions + ([color] if color else []))
            
            # Create the plot
            fig = px.parallel_coordinates(
                df, dimensions=dimensions, color=color,
                title=title or "Parallel Coordinates",
                template=self.default_theme,
                **kwargs
            )
            
            # Apply default styling
            self._apply_default_styling(fig)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating parallel coordinates: {str(e)}")
            raise
    
    def create_subplot_grid(self, figures: List[go.Figure], rows: int, cols: int,
                           subplot_titles: Optional[List[str]] = None,
                           title: Optional[str] = None) -> go.Figure:
        """Create a grid of subplots.
        
        Args:
            figures: List of Plotly figures
            rows: Number of rows
            cols: Number of columns
            subplot_titles: List of subplot titles
            title: Main title
            
        Returns:
            Combined Plotly Figure object
        """
        try:
            logger.info(f"Creating subplot grid: {rows}x{cols} with {len(figures)} figures")
            
            # Create subplots
            fig = make_subplots(
                rows=rows, cols=cols,
                subplot_titles=subplot_titles
            )
            
            # Add traces from each figure
            for i, source_fig in enumerate(figures):
                row = (i // cols) + 1
                col = (i % cols) + 1
                
                if row <= rows and col <= cols:
                    for trace in source_fig.data:
                        fig.add_trace(trace, row=row, col=col)
            
            # Update layout
            fig.update_layout(
                title=title or "Subplot Grid",
                template=self.default_theme,
                height=self.default_height * rows,
                width=self.default_width,
                margin=self.margin
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating subplot grid: {str(e)}")
            raise
    
    def _validate_columns(self, df: pd.DataFrame, columns: List[str]) -> None:
        """Validate that columns exist in DataFrame.
        
        Args:
            df: Input DataFrame
            columns: List of column names to validate
            
        Raises:
            ValueError: If any column is missing
        """
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Columns not found in DataFrame: {missing_columns}")
    
    def _apply_default_styling(self, fig: go.Figure) -> None:
        """Apply default styling to a Plotly figure.
        
        Args:
            fig: Plotly Figure object to style
        """
        fig.update_layout(
            height=self.default_height,
            width=self.default_width,
            margin=self.margin,
            template=self.default_theme,
            showlegend=True,
            hovermode='closest'
        )
        
        # Configure animations
        if not self.enable_animations:
            fig.layout.transition = {'duration': 0}
        
        # Update hover information
        fig.update_traces(
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         '%{xaxis.title.text}: %{x}<br>' +
                         '%{yaxis.title.text}: %{y}<br>' +
                         '<extra></extra>'
        )
    
    def apply_custom_theme(self, fig: go.Figure, theme: Union[str, ChartTheme]) -> go.Figure:
        """Apply a custom theme to a figure.
        
        Args:
            fig: Plotly Figure object
            theme: Theme name or ChartTheme enum
            
        Returns:
            Updated Figure object
        """
        try:
            if isinstance(theme, ChartTheme):
                theme_name = theme.value
            else:
                theme_name = theme
            
            fig.update_layout(template=theme_name)
            logger.info(f"Applied theme: {theme_name}")
            
            return fig
            
        except Exception as e:
            logger.error(f"Error applying theme: {str(e)}")
            return fig
    
    def export_chart(self, fig: go.Figure, filename: str, format: str = 'png',
                    width: Optional[int] = None, height: Optional[int] = None,
                    scale: Optional[int] = None) -> bytes:
        """Export chart to various formats.
        
        Args:
            fig: Plotly Figure object
            filename: Output filename
            format: Export format ('png', 'jpg', 'svg', 'pdf', 'html')
            width: Image width (uses config default if None)
            height: Image height (uses config default if None)
            scale: Image scale factor (uses config default if None)
            
        Returns:
            Exported chart as bytes
        """
        try:
            export_width = width or self.config.charts.export_width
            export_height = height or self.config.charts.export_height
            export_scale = scale or self.config.charts.export_scale
            
            if format.lower() == 'html':
                return fig.to_html().encode('utf-8')
            elif format.lower() in ['png', 'jpg', 'jpeg', 'svg', 'pdf']:
                return fig.to_image(
                    format=format,
                    width=export_width,
                    height=export_height,
                    scale=export_scale
                )
            else:
                raise ValueError(f"Unsupported export format: {format}")
                
        except Exception as e:
            logger.error(f"Error exporting chart: {str(e)}")
            raise
    
    @st.cache_data(ttl=3600)
    def create_cached_chart(_self, chart_type: str, df: pd.DataFrame, **kwargs) -> go.Figure:
        """Create and cache charts for better performance.
        
        Note: The _self parameter is used to avoid hashing the ChartGenerator instance.
        """
        chart_methods = {
            'scatter': _self.create_scatter_plot,
            'line': _self.create_line_plot,
            'bar': _self.create_bar_chart,
            'histogram': _self.create_histogram,
            'box': _self.create_box_plot,
            'violin': _self.create_violin_plot,
            'pie': _self.create_pie_chart,
            'heatmap': _self.create_heatmap,
            'correlation': _self.create_correlation_heatmap,
            '3d_scatter': _self.create_3d_scatter,
            'sunburst': _self.create_sunburst_chart,
            'treemap': _self.create_treemap,
            'parallel': _self.create_parallel_coordinates
        }
        
        if chart_type not in chart_methods:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        return chart_methods[chart_type](df, **kwargs)


# Utility functions
def get_available_chart_types() -> List[str]:
    """Get list of available chart types.
    
    Returns:
        List of chart type names
    """
    return [
        'scatter', 'line', 'bar', 'histogram', 'box', 'violin',
        'pie', 'heatmap', 'correlation', '3d_scatter', 'sunburst',
        'treemap', 'parallel'
    ]


def get_chart_requirements(chart_type: str) -> Dict[str, Any]:
    """Get requirements for a specific chart type.
    
    Args:
        chart_type: Type of chart
        
    Returns:
        Dictionary with chart requirements
    """
    requirements = {
        'scatter': {'required': ['x', 'y'], 'optional': ['color', 'size']},
        'line': {'required': ['x', 'y'], 'optional': ['color']},
        'bar': {'required': ['x', 'y'], 'optional': ['color', 'orientation']},
        'histogram': {'required': ['x'], 'optional': ['color', 'bins']},
        'box': {'required': ['y'], 'optional': ['x', 'color']},
        'violin': {'required': ['y'], 'optional': ['x', 'color']},
        'pie': {'required': ['values', 'names'], 'optional': []},
        'heatmap': {'required': ['x', 'y', 'z'], 'optional': []},
        'correlation': {'required': [], 'optional': ['columns']},
        '3d_scatter': {'required': ['x', 'y', 'z'], 'optional': ['color', 'size']},
        'sunburst': {'required': ['path', 'values'], 'optional': []},
        'treemap': {'required': ['path', 'values'], 'optional': []},
        'parallel': {'required': ['dimensions'], 'optional': ['color']}
    }
    
    return requirements.get(chart_type, {'required': [], 'optional': []})


def suggest_chart_type(df: pd.DataFrame, x: Optional[str] = None, 
                      y: Optional[str] = None) -> List[str]:
    """Suggest appropriate chart types based on data characteristics.
    
    Args:
        df: Input DataFrame
        x: X-axis column (optional)
        y: Y-axis column (optional)
        
    Returns:
        List of suggested chart types
    """
    suggestions = []
    
    # Get column types
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Basic suggestions based on data types
    if len(numeric_cols) >= 2:
        suggestions.extend(['scatter', 'correlation'])
    
    if len(numeric_cols) >= 1:
        suggestions.extend(['histogram', 'box'])
    
    if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
        suggestions.extend(['bar', 'violin'])
    
    if len(categorical_cols) >= 1:
        suggestions.append('pie')
    
    if len(datetime_cols) >= 1 and len(numeric_cols) >= 1:
        suggestions.append('line')
    
    if len(numeric_cols) >= 3:
        suggestions.extend(['3d_scatter', 'parallel'])
    
    # Column-specific suggestions
    if x and y:
        x_type = 'numeric' if x in numeric_cols else 'categorical' if x in categorical_cols else 'datetime'
        y_type = 'numeric' if y in numeric_cols else 'categorical' if y in categorical_cols else 'datetime'
        
        if x_type == 'numeric' and y_type == 'numeric':
            suggestions.insert(0, 'scatter')
        elif x_type == 'categorical' and y_type == 'numeric':
            suggestions.insert(0, 'bar')
        elif x_type == 'datetime' and y_type == 'numeric':
            suggestions.insert(0, 'line')
    
    # Remove duplicates while preserving order
    return list(dict.fromkeys(suggestions))