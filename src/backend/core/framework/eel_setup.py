"""
Eel framework configuration and setup.
Handles Eel initialization, configuration, and application server setup.
"""

import eel
import logging
from abc import ABC, abstractmethod

from ...config.app_settings import AppSettings
from ..constants import LoggingConstants

logger = logging.getLogger(__name__)


class IEelConfigurator(ABC):
    """Interface for Eel framework configuration."""
    
    @abstractmethod
    def configure_eel(self, settings: AppSettings) -> None:
        """Configure Eel with application settings."""
        pass


class EelConfigurator(IEelConfigurator):
    """Handles Eel framework configuration and setup."""
    
    def configure_eel(self, settings: AppSettings) -> None:
        """
        Configure Eel framework with application settings.
        
        Args:
            settings: Application settings instance containing server configuration
        """
        eel._start_args = {
            'mode': settings.server.mode,
            'host': settings.server.host,
            'port': settings.server.port,
            'close_callback': self._on_app_close
        }
        
        logger.info(LoggingConstants.EEL_CONFIGURED)
    
    def _on_app_close(self, page, sockets):
        """Handle application close event."""
        logger.info(LoggingConstants.APP_CLOSING) 