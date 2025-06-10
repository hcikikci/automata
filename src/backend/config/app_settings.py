"""
Application settings module.
Provides configuration management with environment variable support.
"""

import os
from dataclasses import dataclass
from typing import Tuple, Optional
from pathlib import Path


@dataclass(frozen=True)
class WindowSettings:
    """Window-specific configuration settings."""
    size: Tuple[int, int] = (1200, 800)
    position: Tuple[int, int] = (100, 100)


@dataclass(frozen=True)
class ServerSettings:
    """Server-specific configuration settings."""
    host: str = 'localhost'
    port: int = 8000
    mode: str = 'chrome-app'


@dataclass(frozen=True)
class AppMetadata:
    """Application metadata and information."""
    name: str = "Automata"
    version: str = "1.0.0"
    description: str = "A modern Python Eel application"


class AppSettings:
    """Main application settings manager."""
    
    def __init__(self):
        """Initialize settings with environment support."""
        self._debug = self._get_bool_env('DEBUG', True)
        self._disable_cache = self._get_bool_env('DISABLE_CACHE', True)
        
        self.window = WindowSettings()
        self.server = ServerSettings(
            host=os.getenv('HOST', 'localhost'),
            port=int(os.getenv('PORT', '8000')),
            mode=os.getenv('MODE', 'chrome-app')
        )
        self.app = AppMetadata()
    
    @property
    def debug(self) -> bool:
        """Get debug mode status."""
        return self._debug
    
    @property
    def disable_cache(self) -> bool:
        """Get cache disable status."""
        return self._disable_cache
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self._debug
    
    @property
    def frontend_path(self) -> Path:
        """Get the frontend directory path."""
        current_file = Path(__file__)
        backend_dir = current_file.parent.parent
        return backend_dir.parent / 'frontend'
    
    @staticmethod
    def _get_bool_env(key: str, default: bool) -> bool:
        """Get boolean value from environment variable."""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on') 