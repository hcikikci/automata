"""
Application orchestration and lifecycle management.
Main entry point for application coordination and initialization.
"""

import logging
from typing import Dict, Any, Optional

from ..di.registry import IFeatureManager, FeatureManager
from ..framework.eel_setup import IEelConfigurator, EelConfigurator
from ..constants import LoggingConstants
from ...config.app_settings import AppSettings

logger = logging.getLogger(__name__)


class Application:
    """
    Main application orchestrator.
    Handles application lifecycle, initialization, and coordination of components.
    """
    
    def __init__(self, 
                 feature_manager: IFeatureManager, 
                 eel_configurator: IEelConfigurator,
                 settings: AppSettings):
        """
        Initialize the application with required dependencies.
        
        Args:
            feature_manager: Feature management instance (required)
            eel_configurator: Eel framework configurator (required)
            settings: Application settings (required)
            
        Raises:
            ValueError: If any required dependency is None
        """
        self._feature_manager = feature_manager
        self._eel_configurator = eel_configurator
        self._settings = settings
        self._is_initialized = False
    
    @property
    def is_initialized(self) -> bool:
        """Check if application is initialized."""
        return self._is_initialized
    
    def start(self, feature_modules: list = None) -> bool:
        """
        Start the application with full initialization sequence.
        
        Args:
            feature_modules: List of feature modules to register
        
        Returns:
            True if startup successful, False otherwise
        """
        try:
            logger.info(LoggingConstants.INIT_START)
            
            # Register all features if provided
            if feature_modules and not self._feature_manager.register_features(feature_modules):
                raise Exception("Failed to register features")
            
            # Configure Eel framework
            self._eel_configurator.configure_eel(self._settings)
            
            self._is_initialized = True
            logger.info(LoggingConstants.INIT_SUCCESS)
            return True
            
        except Exception as e:
            logger.error(LoggingConstants.INIT_FAILED.format(e))
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive application status."""
        status = self._feature_manager.get_features_status()
        status['application'] = {
            'initialized': self._is_initialized,
            'settings_loaded': self._settings is not None
        }
        return status


class ApplicationFactory:
    """Factory for creating Application instances with proper dependency injection."""
    
    @staticmethod
    def create(settings: AppSettings = None) -> Application:
        """
        Create a standard Application instance with default dependencies.
        
        Args:
            settings: Application settings, creates default if None
            
        Returns:
            Configured Application instance
        """
        # Create default dependencies
        app_settings = settings or AppSettings()
        feature_manager = FeatureManager()
        eel_configurator = EelConfigurator()
        
        return Application(feature_manager, eel_configurator, app_settings)
    
    @staticmethod
    def create_with_dependencies(
        feature_manager: IFeatureManager,
        eel_configurator: IEelConfigurator,
        settings: AppSettings
    ) -> Application:
        """
        Create Application with specific dependencies.
        
        Args:
            feature_manager: Feature management instance
            eel_configurator: Eel configurator instance  
            settings: Application settings
            
        Returns:
            Application instance with injected dependencies
        """
        return Application(feature_manager, eel_configurator, settings)
    
    @staticmethod
    def create_for_testing(
        feature_manager: IFeatureManager = None,
        eel_configurator: IEelConfigurator = None,
        settings: AppSettings = None
    ) -> Application:
        """
        Create Application instance for testing with mock dependencies.
        
        Args:
            feature_manager: Mock feature manager, creates default if None
            eel_configurator: Mock eel configurator, creates default if None
            settings: Mock settings, creates default if None
            
        Returns:
            Application instance suitable for testing
        """
        # Create test dependencies with defaults
        test_feature_manager = feature_manager or FeatureManager()
        test_eel_configurator = eel_configurator or EelConfigurator()
        test_settings = settings or AppSettings()
        
        return Application(test_feature_manager, test_eel_configurator, test_settings) 