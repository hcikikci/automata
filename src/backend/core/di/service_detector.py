"""
Service detection and validation utilities.
Handles service class discovery and validation logic.
"""

import inspect
import logging
from typing import Type, List, Any
from abc import ABC, abstractmethod

from ..services.base import BaseService

logger = logging.getLogger(__name__)


class IServiceDetector(ABC):
    """Interface for service detection strategies."""
    
    @abstractmethod
    def is_service_class(self, obj: Type) -> bool:
        """Check if a class is a service class."""
        pass
    
    @abstractmethod
    def get_service_classes(self, module: Any) -> List[Type[BaseService]]:
        """Get all service classes from a module."""
        pass


class BaseServiceDetector(IServiceDetector):
    """
    Default service detector implementation.
    Detects services based on BaseService inheritance and naming conventions.
    """
    
    def __init__(self):
        """Initialize the service detector."""
        self._service_criteria = [
            self._inherits_from_base_service,
            self._is_not_base_service_itself,
            self._has_service_name_attribute
        ]
    
    def is_service_class(self, obj: Type) -> bool:
        """
        Check if a class is a service class using configurable criteria.
        
        Args:
            obj: Class to check
            
        Returns:
            True if class meets all service criteria
        """
        if not inspect.isclass(obj):
            return False
        
        return all(criterion(obj) for criterion in self._service_criteria)
    
    def get_service_classes(self, module: Any) -> List[Type[BaseService]]:
        """
        Get all service classes from a module.
        
        Args:
            module: Python module to scan
            
        Returns:
            List of service classes found in the module
        """
        service_classes = []
        
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if self.is_service_class(obj):
                service_classes.append(obj)
                logger.debug(f"Detected service class: {name}")
        
        return service_classes
    
    def _inherits_from_base_service(self, obj: Type) -> bool:
        """Check if class inherits from BaseService."""
        return issubclass(obj, BaseService)
    
    def _is_not_base_service_itself(self, obj: Type) -> bool:
        """Check if class is not BaseService itself."""
        return obj is not BaseService
    
    def _has_service_name_attribute(self, obj: Type) -> bool:
        """Check if class has service name attribute."""
        return hasattr(obj, '_service_name')


class AnnotationBasedServiceDetector(IServiceDetector):
    """
    Service detector that uses annotations for detection.
    More flexible approach for future extensibility.
    """
    
    def __init__(self, service_annotation: str = '_service_name'):
        """
        Initialize annotation-based detector.
        
        Args:
            service_annotation: Attribute name that marks service classes
        """
        self._service_annotation = service_annotation
    
    def is_service_class(self, obj: Type) -> bool:
        """Check if class has service annotation."""
        return (inspect.isclass(obj) and 
                hasattr(obj, self._service_annotation) and
                issubclass(obj, BaseService) and
                obj is not BaseService)
    
    def get_service_classes(self, module: Any) -> List[Type[BaseService]]:
        """Get annotated service classes from module."""
        return [obj for name, obj in inspect.getmembers(module, inspect.isclass)
                if self.is_service_class(obj)]


class ServiceDetectorFactory:
    """Factory for creating service detector instances."""
    
    @staticmethod
    def create_default() -> IServiceDetector:
        """Create default service detector."""
        return BaseServiceDetector()
    
    @staticmethod
    def create_annotation_based(annotation: str = '_service_name') -> IServiceDetector:
        """Create annotation-based service detector."""
        return AnnotationBasedServiceDetector(annotation) 