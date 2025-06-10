#!/usr/bin/env python3
"""
Simple run script for Automata application.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Change to src directory
os.chdir(src_path)

# Import and run the main application
from main import main

if __name__ == "__main__":
    main() 