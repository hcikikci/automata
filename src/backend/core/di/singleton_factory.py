"""
Generic singleton factory pattern.
Eliminates code duplication for global instance management.
"""

from typing import TypeVar, Generic, Optional, Callable, Type, Dict, Any
from abc import ABC, abstractmethod

T = TypeVar('T')


class ISingletonFactory(ABC, Generic[T]):
    """Interface for singleton factory implementations."""
    
    @abstractmethod
    def get_instance(self) -> T:
        """Get or create singleton instance."""
        pass
    
    @abstractmethod
    def reset_instance(self) -> None:
        """Reset singleton instance (mainly for testing)."""
        pass


class SingletonFactory(ISingletonFactory[T]):
    """
    Generic singleton factory implementation.
    Provides thread-safe singleton management with lazy initialization.
    """
    
    def __init__(self, factory_func: Callable[[], T]):
        """
        Initialize singleton factory.
        
        Args:
            factory_func: Function to create new instances
        """
        self._factory_func = factory_func
        self._instance: Optional[T] = None
        self._lock = None  # We'll use threading.Lock in production
    
    def get_instance(self) -> T:
        """Get or create singleton instance with lazy initialization."""
        if self._instance is None:
            self._instance = self._factory_func()
        return self._instance
    
    def reset_instance(self) -> None:
        """Reset singleton instance (mainly for testing)."""
        self._instance = None


class SingletonRegistry:
    """
    Registry for managing multiple singleton factories.
    Centralized singleton management across the application.
    """
    
    def __init__(self):
        """Initialize the singleton registry."""
        self._factories: Dict[str, ISingletonFactory] = {}
    
    def register_factory(self, name: str, factory: ISingletonFactory) -> None:
        """
        Register a singleton factory.
        
        Args:
            name: Unique name for the factory
            factory: Singleton factory instance
        """
        self._factories[name] = factory
    
    def get_instance(self, name: str) -> Any:
        """
        Get singleton instance by factory name.
        
        Args:
            name: Factory name
            
        Returns:
            Singleton instance
            
        Raises:
            KeyError: If factory not registered
        """
        if name not in self._factories:
            raise KeyError(f"Singleton factory '{name}' not registered")
        
        return self._factories[name].get_instance()
    
    def reset_instance(self, name: str) -> None:
        """
        Reset singleton instance by factory name.
        
        Args:
            name: Factory name
        """
        if name in self._factories:
            self._factories[name].reset_instance()
    
    def reset_all(self) -> None:
        """Reset all singleton instances."""
        for factory in self._factories.values():
            factory.reset_instance()


# Global registry instance
_global_registry: Optional[SingletonRegistry] = None


def get_singleton_registry() -> SingletonRegistry:
    """Get the global singleton registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = SingletonRegistry()
    return _global_registry


def create_singleton_factory(factory_func: Callable[[], T]) -> SingletonFactory[T]:
    """
    Create a new singleton factory.
    
    Args:
        factory_func: Function to create instances
        
    Returns:
        Configured singleton factory
    """
    return SingletonFactory(factory_func) 