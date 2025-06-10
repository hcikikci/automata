"""
Interface registration and management utilities.
Handles automatic interface detection and registration with DI container.
"""

import logging
from typing import Type, List
from abc import ABC, abstractmethod

from ..services.base import BaseService
from ..interfaces import IService
from .container import IContainer

logger = logging.getLogger(__name__)


class IInterfaceManager(ABC):
    """Interface for interface registration management."""
    
    @abstractmethod
    def register_service_interfaces(self, service_class: Type[BaseService], 
                                  service_instance: BaseService) -> bool:
        """Register all interfaces implemented by a service."""
        pass


class InterfaceDetectionStrategy(ABC):
    """Strategy for detecting interfaces implemented by a service."""
    
    @abstractmethod
    def get_interfaces(self, service_class: Type[BaseService]) -> List[Type]:
        """Get all interfaces implemented by a service class."""
        pass


class AbstractMethodInterfaceStrategy(InterfaceDetectionStrategy):
    """
    Detects interfaces based on abstract methods.
    Finds classes with abstract methods in the inheritance chain.
    """
    
    def get_interfaces(self, service_class: Type[BaseService]) -> List[Type]:
        """Get interfaces based on abstract method presence."""
        interfaces = []
        
        # Check direct base classes
        for base_class in service_class.__bases__:
            if self._is_interface(base_class):
                interfaces.append(base_class)
        
        # Check full inheritance chain (MRO - Method Resolution Order)
        for interface in service_class.__mro__:
            if self._is_interface_in_mro(interface):
                interfaces.append(interface)
        
        return interfaces
    
    def _is_interface(self, class_type: Type) -> bool:
        """Check if a class is an interface based on abstract methods."""
        return (hasattr(class_type, '__abstractmethods__') and 
                class_type.__abstractmethods__ and 
                class_type is not BaseService)
    
    def _is_interface_in_mro(self, class_type: Type) -> bool:
        """Check if a class in MRO is an interface."""
        return (hasattr(class_type, '__abstractmethods__') and 
                class_type.__abstractmethods__ and 
                class_type is not BaseService and
                self._follows_interface_naming_convention(class_type))
    
    def _follows_interface_naming_convention(self, class_type: Type) -> bool:
        """Check if class follows interface naming convention."""
        # Convention: interfaces start with 'I' and end with 'Service' or just 'I'
        name = class_type.__name__
        return (name.startswith('I') and 
                (name.endswith('Service') or len(name) > 1))


class AnnotationInterfaceStrategy(InterfaceDetectionStrategy):
    """
    Detects interfaces based on annotations or metadata.
    More explicit approach for interface detection.
    """
    
    def __init__(self, interface_marker: str = '__interfaces__'):
        """
        Initialize annotation-based strategy.
        
        Args:
            interface_marker: Attribute name that lists interfaces
        """
        self._interface_marker = interface_marker
    
    def get_interfaces(self, service_class: Type[BaseService]) -> List[Type]:
        """Get interfaces based on explicit annotation."""
        if hasattr(service_class, self._interface_marker):
            return getattr(service_class, self._interface_marker)
        return []


class InterfaceRegistrationManager(IInterfaceManager):
    """
    Manages interface registration with dependency injection container.
    Uses configurable strategies for interface detection.
    """
    
    def __init__(self, container: IContainer, 
                 detection_strategy: InterfaceDetectionStrategy = None):
        """
        Initialize interface registration manager.
        
        Args:
            container: DI container for registration
            detection_strategy: Strategy for detecting interfaces
        """
        self._container = container
        self._detection_strategy = detection_strategy or AbstractMethodInterfaceStrategy()
    
    def register_service_interfaces(self, service_class: Type[BaseService], 
                                  service_instance: BaseService) -> bool:
        """
        Register all interfaces implemented by a service.
        
        Args:
            service_class: Service class type
            service_instance: Service instance to register
            
        Returns:
            True if all interfaces registered successfully
        """
        try:
            interfaces = self._detection_strategy.get_interfaces(service_class)
            
            success_count = 0
            for interface in interfaces:
                if self._register_single_interface(interface, service_instance):
                    success_count += 1
            
            if interfaces:
                logger.info(f"Registered {success_count}/{len(interfaces)} interfaces for {service_class.__name__}")
            
            return success_count == len(interfaces) if interfaces else True
            
        except Exception as e:
            logger.error(f"Failed to register interfaces for {service_class.__name__}: {e}")
            return False
    
    def _register_single_interface(self, interface: Type, 
                                 service_instance: BaseService) -> bool:
        """
        Register a single interface with the container.
        
        Args:
            interface: Interface type to register
            service_instance: Service instance
            
        Returns:
            True if registration successful
        """
        try:
            self._container.register_instance(interface, service_instance)
            logger.debug(f"Registered interface {interface.__name__} for {service_instance.__class__.__name__}")
            return True
        except Exception as e:
            logger.warning(f"Could not register interface {interface.__name__}: {e}")
            return False


class InterfaceManagerFactory:
    """Factory for creating interface manager instances."""
    
    @staticmethod
    def create_default(container: IContainer) -> IInterfaceManager:
        """Create default interface manager."""
        return InterfaceRegistrationManager(container)
    
    @staticmethod
    def create_with_strategy(container: IContainer, 
                           strategy: InterfaceDetectionStrategy) -> IInterfaceManager:
        """Create interface manager with custom strategy."""
        return InterfaceRegistrationManager(container, strategy)
    
    @staticmethod
    def create_annotation_based(container: IContainer, 
                              marker: str = '__interfaces__') -> IInterfaceManager:
        """Create annotation-based interface manager."""
        strategy = AnnotationInterfaceStrategy(marker)
        return InterfaceRegistrationManager(container, strategy) 