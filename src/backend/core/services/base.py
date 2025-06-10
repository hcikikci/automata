"""
Base service abstractions and implementations.
Provides common functionality and interface for all feature services.
"""

import logging
from typing import Optional, Type, TypeVar
from ..interfaces import IService
from ..constants import ErrorCodes, LoggingConstants, ValidationConstants

T = TypeVar('T')


class BaseService(IService):
    """Base implementation for all feature services."""
    
    def __init__(self, feature_name: str = None):
        """
        Initialize the base service.
        
        Args:
            feature_name: Name of the feature this service belongs to, 
                         if None, derives from class name
        """
        self._feature_name = feature_name or self._derive_feature_name()
        self._logger = logging.getLogger(f"{__name__}.{self._feature_name}")
        self._is_initialized = False
    
    def _derive_feature_name(self) -> str:
        """Derive feature name from class name."""
        class_name = self.__class__.__name__
        # Remove 'Service' suffix if present and convert to lowercase
        if class_name.endswith('Service'):
            class_name = class_name[:-7]
        return class_name.lower()
    
    @property
    def feature_name(self) -> str:
        """Get the feature name."""
        return self._feature_name
    
    @property
    def is_initialized(self) -> bool:
        """Check if service is initialized."""
        return self._is_initialized
    
    @property
    def logger(self) -> logging.Logger:
        """Get the service logger."""
        return self._logger
    
    def initialize(self) -> bool:
        """
        Initialize the service.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            self._initialize_specific()
            self._is_initialized = True
            self._logger.info(LoggingConstants.SERVICE_INIT_SUCCESS.format(self._feature_name))
            return True
        except Exception as e:
            self._logger.error(LoggingConstants.SERVICE_INIT_FAILED.format(self._feature_name, e))
            return False
    
    def _initialize_specific(self) -> None:
        """Override this method for feature-specific initialization."""
        pass
    
    def validate_input(self, data: any, expected_type: Type[T], 
                      allow_empty: bool = False) -> Optional[str]:
        """
        Validate input data with type checking.
        
        Args:
            data: Data to validate
            expected_type: Expected type
            allow_empty: Whether to allow empty values
            
        Returns:
            Error message if validation fails, None if valid
        """
        if not allow_empty and not data:
            return ValidationConstants.EMPTY_INPUT_ERROR
        
        if data is not None and not isinstance(data, expected_type):
            return ValidationConstants.INVALID_TYPE_ERROR.format(expected_type.__name__)
        
        return None 