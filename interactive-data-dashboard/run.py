#!/usr/bin/env python3
"""Simple script to run the Interactive Data Dashboard.

This script provides a convenient way to start the Streamlit application
with proper configuration and error handling.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        "streamlit",
        "pandas",
        "plotly",
        "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    return True


def setup_environment():
    """Set up environment variables and paths."""
    # Add src directory to Python path
    src_path = Path(__file__).parent / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))
    
    # Load environment variables from .env file if it exists
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            print("✅ Loaded environment variables from .env")
        except ImportError:
            print("⚠️  python-dotenv not installed, skipping .env file")
    
    # Set default Streamlit configuration
    os.environ.setdefault("STREAMLIT_SERVER_PORT", "8501")
    os.environ.setdefault("STREAMLIT_SERVER_ADDRESS", "localhost")
    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")


def run_streamlit():
    """Run the Streamlit application."""
    app_file = Path(__file__).parent / "app.py"
    
    if not app_file.exists():
        print("❌ app.py not found in the current directory")
        return False
    
    print("🚀 Starting Interactive Data Dashboard...")
    print(f"📁 App file: {app_file}")
    
    try:
        # Run streamlit with the app file
        cmd = [sys.executable, "-m", "streamlit", "run", str(app_file)]
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Streamlit: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return True


def main():
    """Main function to run the dashboard."""
    print("📊 Interactive Data Dashboard")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Please run this script from the project root directory")
        print("   (where app.py is located)")
        sys.exit(1)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All dependencies found")
    
    # Setup environment
    print("⚙️  Setting up environment...")
    setup_environment()
    
    # Run the application
    success = run_streamlit()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()