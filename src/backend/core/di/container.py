"""
Dependency injection container.
Provides centralized dependency management and service resolution.
"""

from typing import Dict, TypeVar, Type, Optional, Callable, Any
from abc import ABC, abstractmethod

T = TypeVar('T')


class IContainer(ABC):
    """Interface for dependency injection container."""
    
    @abstractmethod
    def register(self, interface: Type[T], implementation: Type[T], 
                 singleton: bool = True) -> None:
        """Register a service implementation."""
        pass
    
    @abstractmethod
    def register_instance(self, interface: Type[T], instance: T) -> None:
        """Register a service instance."""
        pass
    
    @abstractmethod
    def resolve(self, interface: Type[T]) -> T:
        """Resolve a service instance."""
        pass
    
    @abstractmethod
    def is_registered(self, interface: Type[T]) -> bool:
        """Check if a service is registered."""
        pass


class Container(IContainer):
    """Simple dependency injection container implementation."""
    
    def __init__(self):
        """Initialize the container."""
        self._services: Dict[Type, Any] = {}
        self._singletons: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}
    
    def register(self, interface: Type[T], implementation: Type[T], 
                 singleton: bool = True) -> None:
        """
        Register a service implementation.
        
        Args:
            interface: The interface type
            implementation: The implementation type
            singleton: Whether to use singleton pattern
        """
        if singleton:
            self._services[interface] = implementation
        else:
            self._factories[interface] = implementation
    
    def register_instance(self, interface: Type[T], instance: T) -> None:
        """
        Register a service instance.
        
        Args:
            interface: The interface type
            instance: The service instance
        """
        self._singletons[interface] = instance
    
    def register_factory(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """
        Register a factory function for creating service instances.
        
        Args:
            interface: The interface type
            factory: Factory function
        """
        self._factories[interface] = factory
    
    def resolve(self, interface: Type[T]) -> T:
        """
        Resolve a service instance.
        
        Args:
            interface: The interface type to resolve
            
        Returns:
            The service instance
            
        Raises:
            ValueError: If service is not registered
        """
        # Check for existing singleton instance
        if interface in self._singletons:
            return self._singletons[interface]
        
        # Check for registered singleton service
        if interface in self._services:
            if interface not in self._singletons:
                self._singletons[interface] = self._services[interface]()
            return self._singletons[interface]
        
        # Check for factory
        if interface in self._factories:
            return self._factories[interface]()
        
        raise ValueError(f"Service {interface.__name__} is not registered")
    
    def is_registered(self, interface: Type[T]) -> bool:
        """
        Check if a service is registered.
        
        Args:
            interface: The interface type
            
        Returns:
            True if service is registered
        """
        return (interface in self._services or 
                interface in self._singletons or 
                interface in self._factories)
    
    def clear(self) -> None:
        """Clear all registered services."""
        self._services.clear()
        self._singletons.clear()
        self._factories.clear()


# Import singleton factory
from .singleton_factory import get_singleton_registry, create_singleton_factory

# Initialize singleton factory for container
_container_factory = create_singleton_factory(lambda: Container())
get_singleton_registry().register_factory('container', _container_factory)


def get_container() -> Container:
    """Get the global container instance."""
    return get_singleton_registry().get_instance('container')


def reset_container() -> None:
    """Reset the global container (mainly for testing)."""
    get_singleton_registry().reset_instance('container') 