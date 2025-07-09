#!/usr/bin/env python3
"""Entry point for the Interactive Data Dashboard application.

This script serves as the main entry point for launching the Streamlit application.
It can be run directly or used with streamlit run command.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main application
if __name__ == "__main__":
    import streamlit as st
    from interactive_data_dashboard.main import main
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="Interactive Data Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Run the main application
    main()