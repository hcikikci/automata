"""
Core interfaces for the application.
Contains abstract interfaces to avoid circular dependencies.
"""

from abc import ABC, abstractmethod


class IService(ABC):
    """Interface for all application services."""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the service."""
        pass
    
    @property
    @abstractmethod
    def is_initialized(self) -> bool:
        """Check if service is initialized."""
        pass
    
    @property
    @abstractmethod
    def feature_name(self) -> str:
        """Get the feature name."""
        pass 