"""Interactive Data Dashboard - Main Application

A Streamlit-based interactive data visualization dashboard that combines
Pandas for data processing and Plotly for creating interactive charts.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CONFIG = {
    'max_upload_size': int(os.getenv('MAX_UPLOAD_SIZE_MB', 200)),
    'max_data_points': int(os.getenv('MAX_DATA_POINTS', 10000)),
    'default_theme': os.getenv('DEFAULT_THEME', 'plotly_white'),
    'chart_height': int(os.getenv('CHART_HEIGHT', 500)),
    'chart_width': int(os.getenv('CHART_WIDTH', 700)),
    'enable_caching': os.getenv('ENABLE_CACHING', 'true').lower() == 'true',
}


class DataProcessor:
    """Data processing utilities for the dashboard."""
    
    @staticmethod
    @st.cache_data
    def load_csv_data(uploaded_file) -> pd.DataFrame:
        """Load and cache CSV data from uploaded file."""
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error loading CSV file: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive data summary."""
        if df.empty:
            return {}
        
        summary = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
        }
        
        # Numeric columns summary
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            summary['numeric_summary'] = df[numeric_cols].describe().to_dict()
        
        # Categorical columns summary
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            summary['categorical_summary'] = {
                col: df[col].value_counts().head().to_dict()
                for col in categorical_cols
            }
        
        return summary
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Basic data cleaning operations."""
        if df.empty:
            return df
        
        # Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Convert string representations of numbers
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to numeric
                numeric_series = pd.to_numeric(df[col], errors='coerce')
                if not numeric_series.isna().all():
                    df[col] = numeric_series
        
        return df
    
    @staticmethod
    def filter_data(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to the dataframe."""
        filtered_df = df.copy()
        
        for column, filter_config in filters.items():
            if column not in df.columns:
                continue
                
            filter_type = filter_config.get('type')
            filter_value = filter_config.get('value')
            
            if filter_type == 'range' and isinstance(filter_value, (list, tuple)):
                min_val, max_val = filter_value
                filtered_df = filtered_df[
                    (filtered_df[column] >= min_val) & 
                    (filtered_df[column] <= max_val)
                ]
            elif filter_type == 'categorical' and filter_value:
                filtered_df = filtered_df[filtered_df[column].isin(filter_value)]
        
        return filtered_df


class ChartGenerator:
    """Chart generation utilities using Plotly."""
    
    @staticmethod
    def create_scatter_plot(df: pd.DataFrame, x: str, y: str, **kwargs) -> go.Figure:
        """Create an interactive scatter plot."""
        color = kwargs.get('color')
        size = kwargs.get('size')
        title = kwargs.get('title', f'{y} vs {x}')
        
        fig = px.scatter(
            df, x=x, y=y, color=color, size=size,
            title=title,
            template=CONFIG['default_theme'],
            height=CONFIG['chart_height']
        )
        
        fig.update_layout(
            xaxis_title=x,
            yaxis_title=y,
            hovermode='closest'
        )
        
        return fig
    
    @staticmethod
    def create_bar_chart(df: pd.DataFrame, x: str, y: str, **kwargs) -> go.Figure:
        """Create an interactive bar chart."""
        color = kwargs.get('color')
        title = kwargs.get('title', f'{y} by {x}')
        
        fig = px.bar(
            df, x=x, y=y, color=color,
            title=title,
            template=CONFIG['default_theme'],
            height=CONFIG['chart_height']
        )
        
        fig.update_layout(
            xaxis_title=x,
            yaxis_title=y
        )
        
        return fig
    
    @staticmethod
    def create_line_chart(df: pd.DataFrame, x: str, y: str, **kwargs) -> go.Figure:
        """Create an interactive line chart."""
        color = kwargs.get('color')
        title = kwargs.get('title', f'{y} over {x}')
        
        fig = px.line(
            df, x=x, y=y, color=color,
            title=title,
            template=CONFIG['default_theme'],
            height=CONFIG['chart_height']
        )
        
        fig.update_layout(
            xaxis_title=x,
            yaxis_title=y
        )
        
        return fig
    
    @staticmethod
    def create_histogram(df: pd.DataFrame, column: str, **kwargs) -> go.Figure:
        """Create a histogram."""
        bins = kwargs.get('bins', 30)
        title = kwargs.get('title', f'Distribution of {column}')
        
        fig = px.histogram(
            df, x=column, nbins=bins,
            title=title,
            template=CONFIG['default_theme'],
            height=CONFIG['chart_height']
        )
        
        fig.update_layout(
            xaxis_title=column,
            yaxis_title='Frequency'
        )
        
        return fig
    
    @staticmethod
    def create_correlation_heatmap(df: pd.DataFrame, **kwargs) -> go.Figure:
        """Create a correlation heatmap for numeric columns."""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            st.warning("No numeric columns found for correlation analysis.")
            return go.Figure()
        
        corr_matrix = numeric_df.corr()
        
        fig = px.imshow(
            corr_matrix,
            title="Correlation Heatmap",
            template=CONFIG['default_theme'],
            height=CONFIG['chart_height'],
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )
        
        fig.update_layout(
            xaxis_title="Variables",
            yaxis_title="Variables"
        )
        
        return fig
    
    @staticmethod
    def create_pie_chart(df: pd.DataFrame, column: str, **kwargs) -> go.Figure:
        """Create a pie chart for categorical data."""
        value_counts = df[column].value_counts().head(10)  # Top 10 categories
        title = kwargs.get('title', f'Distribution of {column}')
        
        fig = px.pie(
            values=value_counts.values,
            names=value_counts.index,
            title=title,
            template=CONFIG['default_theme'],
            height=CONFIG['chart_height']
        )
        
        return fig


def render_sidebar(df: pd.DataFrame) -> Dict[str, Any]:
    """Render the sidebar with data controls and filters."""
    st.sidebar.header("📊 Dashboard Controls")
    
    controls = {}
    
    if not df.empty:
        st.sidebar.subheader("📈 Chart Configuration")
        
        # Chart type selection
        chart_types = [
            "Scatter Plot", "Bar Chart", "Line Chart", 
            "Histogram", "Correlation Heatmap", "Pie Chart"
        ]
        controls['chart_type'] = st.sidebar.selectbox(
            "Select Chart Type", chart_types
        )
        
        # Column selection based on chart type
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        all_cols = df.columns.tolist()
        
        if controls['chart_type'] in ["Scatter Plot", "Bar Chart", "Line Chart"]:
            controls['x_column'] = st.sidebar.selectbox(
                "X-axis Column", all_cols
            )
            controls['y_column'] = st.sidebar.selectbox(
                "Y-axis Column", numeric_cols if numeric_cols else all_cols
            )
            
            # Optional color grouping
            if categorical_cols:
                controls['color_column'] = st.sidebar.selectbox(
                    "Color Grouping (Optional)", 
                    [None] + categorical_cols
                )
            
            # Optional size for scatter plot
            if controls['chart_type'] == "Scatter Plot" and numeric_cols:
                controls['size_column'] = st.sidebar.selectbox(
                    "Size Column (Optional)", 
                    [None] + numeric_cols
                )
        
        elif controls['chart_type'] == "Histogram":
            controls['hist_column'] = st.sidebar.selectbox(
                "Column for Histogram", numeric_cols if numeric_cols else all_cols
            )
            controls['bins'] = st.sidebar.slider(
                "Number of Bins", 10, 100, 30
            )
        
        elif controls['chart_type'] == "Pie Chart":
            controls['pie_column'] = st.sidebar.selectbox(
                "Column for Pie Chart", categorical_cols if categorical_cols else all_cols
            )
        
        # Data filtering
        st.sidebar.subheader("🔍 Data Filters")
        controls['filters'] = {}
        
        # Numeric filters
        for col in numeric_cols[:3]:  # Limit to first 3 numeric columns
            if df[col].notna().any():
                min_val = float(df[col].min())
                max_val = float(df[col].max())
                
                if min_val != max_val:
                    range_values = st.sidebar.slider(
                        f"{col} Range",
                        min_val, max_val, (min_val, max_val),
                        key=f"filter_{col}"
                    )
                    controls['filters'][col] = {
                        'type': 'range',
                        'value': range_values
                    }
        
        # Categorical filters
        for col in categorical_cols[:2]:  # Limit to first 2 categorical columns
            unique_values = df[col].dropna().unique().tolist()
            if len(unique_values) > 1 and len(unique_values) <= 20:
                selected_values = st.sidebar.multiselect(
                    f"Filter {col}",
                    unique_values,
                    default=unique_values,
                    key=f"filter_cat_{col}"
                )
                if selected_values != unique_values:
                    controls['filters'][col] = {
                        'type': 'categorical',
                        'value': selected_values
                    }
    
    return controls


def render_data_overview(df: pd.DataFrame) -> None:
    """Render data overview section."""
    if df.empty:
        return
    
    st.subheader("📋 Data Overview")
    
    # Basic info in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Rows", f"{df.shape[0]:,}")
    
    with col2:
        st.metric("Columns", df.shape[1])
    
    with col3:
        missing_count = df.isnull().sum().sum()
        st.metric("Missing Values", f"{missing_count:,}")
    
    with col4:
        memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
        st.metric("Memory Usage", f"{memory_mb:.1f} MB")
    
    # Data preview
    with st.expander("📊 Data Preview", expanded=False):
        st.dataframe(df.head(100), use_container_width=True)
    
    # Data types and statistics
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("📈 Numeric Summary"):
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                st.dataframe(numeric_df.describe(), use_container_width=True)
            else:
                st.info("No numeric columns found.")
    
    with col2:
        with st.expander("📝 Column Information"):
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.astype(str),
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum(),
                'Unique Values': [df[col].nunique() for col in df.columns]
            })
            st.dataframe(col_info, use_container_width=True)


def render_chart(df: pd.DataFrame, controls: Dict[str, Any]) -> None:
    """Render the selected chart based on controls."""
    if df.empty or not controls.get('chart_type'):
        return
    
    # Apply filters
    if controls.get('filters'):
        df = DataProcessor.filter_data(df, controls['filters'])
        if df.empty:
            st.warning("No data remaining after applying filters.")
            return
    
    # Limit data points for performance
    if len(df) > CONFIG['max_data_points']:
        st.warning(f"Dataset has {len(df):,} rows. Sampling {CONFIG['max_data_points']:,} rows for visualization.")
        df = df.sample(n=CONFIG['max_data_points'], random_state=42)
    
    chart_type = controls['chart_type']
    chart_generator = ChartGenerator()
    
    try:
        if chart_type == "Scatter Plot":
            fig = chart_generator.create_scatter_plot(
                df,
                x=controls['x_column'],
                y=controls['y_column'],
                color=controls.get('color_column'),
                size=controls.get('size_column')
            )
        
        elif chart_type == "Bar Chart":
            # Aggregate data for bar chart
            if df[controls['x_column']].dtype == 'object':
                agg_df = df.groupby(controls['x_column'])[controls['y_column']].mean().reset_index()
            else:
                agg_df = df
            
            fig = chart_generator.create_bar_chart(
                agg_df,
                x=controls['x_column'],
                y=controls['y_column'],
                color=controls.get('color_column')
            )
        
        elif chart_type == "Line Chart":
            fig = chart_generator.create_line_chart(
                df,
                x=controls['x_column'],
                y=controls['y_column'],
                color=controls.get('color_column')
            )
        
        elif chart_type == "Histogram":
            fig = chart_generator.create_histogram(
                df,
                column=controls['hist_column'],
                bins=controls.get('bins', 30)
            )
        
        elif chart_type == "Correlation Heatmap":
            fig = chart_generator.create_correlation_heatmap(df)
        
        elif chart_type == "Pie Chart":
            fig = chart_generator.create_pie_chart(
                df,
                column=controls['pie_column']
            )
        
        else:
            st.error(f"Unsupported chart type: {chart_type}")
            return
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Chart statistics
        with st.expander("📊 Chart Statistics"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Data Points", f"{len(df):,}")
            with col2:
                if 'filters' in controls and controls['filters']:
                    st.metric("Filters Applied", len(controls['filters']))
    
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        st.info("Please check your column selections and data types.")


def main() -> None:
    """Main application function."""
    # Header
    st.title("📊 Interactive Data Dashboard")
    st.markdown(
        "Upload your CSV data and create interactive visualizations with ease. "
        "Built with Streamlit, Pandas, and Plotly."
    )
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help=f"Maximum file size: {CONFIG['max_upload_size']} MB"
    )
    
    if uploaded_file is not None:
        # Load and process data
        with st.spinner("Loading data..."):
            df = DataProcessor.load_csv_data(uploaded_file)
        
        if not df.empty:
            # Clean data
            df = DataProcessor.clean_data(df)
            
            # Render sidebar controls
            controls = render_sidebar(df)
            
            # Main content area
            tab1, tab2 = st.tabs(["📈 Visualization", "📋 Data Overview"])
            
            with tab1:
                st.subheader("📈 Interactive Visualization")
                render_chart(df, controls)
            
            with tab2:
                render_data_overview(df)
        
        else:
            st.error("Failed to load the CSV file. Please check the file format.")
    
    else:
        # Welcome message and instructions
        st.info("👆 Please upload a CSV file to get started.")
        
        # Example usage
        with st.expander("📚 How to Use", expanded=True):
            st.markdown("""
            ### Getting Started
            
            1. **Upload Data**: Click the file uploader above and select a CSV file
            2. **Explore Data**: View your data overview in the "Data Overview" tab
            3. **Create Charts**: Use the sidebar controls to configure visualizations
            4. **Filter Data**: Apply filters to focus on specific data subsets
            5. **Interact**: Hover, zoom, and pan on charts for detailed exploration
            
            ### Supported Chart Types
            
            - **Scatter Plot**: Explore relationships between two numeric variables
            - **Bar Chart**: Compare values across categories
            - **Line Chart**: Show trends over time or ordered data
            - **Histogram**: Visualize data distribution
            - **Correlation Heatmap**: Analyze correlations between numeric variables
            - **Pie Chart**: Show proportions of categorical data
            
            ### Tips for Best Results
            
            - Ensure your CSV has column headers
            - Use numeric data for quantitative analysis
            - Keep file sizes under {max_size} MB for optimal performance
            - Clean data beforehand for better visualizations
            """.format(max_size=CONFIG['max_upload_size']))
        
        # Sample data section
        with st.expander("🎯 Try with Sample Data"):
            st.markdown("""
            Don't have data ready? Try these sample datasets:
            
            - [Iris Dataset](https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv)
            - [Tips Dataset](https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv)
            - [Car Crashes Dataset](https://raw.githubusercontent.com/mwaskom/seaborn-data/master/car_crashes.csv)
            
            Right-click any link and "Save as" to download, then upload here.
            """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>\n"
        "Built with ❤️ using Streamlit, Pandas, and Plotly | "
        "<a href='https://github.com/your-org/interactive-data-dashboard' target='_blank'>View Source</a>\n"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()