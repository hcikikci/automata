#!/usr/bin/env python3
"""
Main entry point for the Eel application.
This module initializes and starts the application with proper configuration.
"""

import eel
import sys
import os
from pathlib import Path

# Add the src directory to Python path for imports
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from backend.config.app_settings import AppSettings
from backend.core import Application, ApplicationFactory

def initialize_app():
    """Initialize the Eel application with proper configuration."""
    try:
        # Initialize Eel with the frontend directory
        frontend_path = src_path / "frontend"
        eel.init(str(frontend_path))
        
        # Initialize application with feature-driven architecture
        application = ApplicationFactory.create()
        
        # Import and use default feature modules from constants
        from backend.config.constants import Constants
        
        if not application.start(Constants.FEATURE_MODULES):
            raise Exception("Failed to start application")
        
        print("✅ Application initialized successfully with feature-driven architecture")
        print("🏥 Health monitoring feature registered and active")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize application: {e}")
        return False

def main():
    """Main application entry point."""
    print("🚀 Starting Automata Application...")
    
    if not initialize_app():
        sys.exit(1)
    
    try:
        # Start the application
        settings = AppSettings()
        print(f"🌐 Starting server at http://{settings.server.host}:{settings.server.port}")
        eel.start(
            'pages/index.html',
            size=settings.window.size,
            position=settings.window.position,
            disable_cache=settings.disable_cache,
            mode=settings.server.mode,
            host=settings.server.host,
            port=settings.server.port,
            block=True
        )
        
    except (SystemExit, KeyboardInterrupt):
        print("\n👋 Application closed by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 