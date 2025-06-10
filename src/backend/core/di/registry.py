"""
Service registry and feature management.
Handles service registration, discovery, and feature lifecycle management.
"""

import importlib
import inspect
import re
import logging
from typing import Dict, Type, Optional, List, Tuple, Any
from datetime import datetime
from abc import ABC, abstractmethod

from ..interfaces import IService
from ..services.base import BaseService
from .container import get_container
from .singleton_factory import get_singleton_registry, create_singleton_factory
from .service_detector import IServiceDetector, ServiceDetectorFactory
from .interface_manager import IInterfaceManager, InterfaceManagerFactory
from ..constants import ServiceConstants, ContainerConstants, LoggingConstants

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """Registry for managing application services."""
    
    def __init__(self):
        """Initialize the service registry."""
        self._services: Dict[str, IService] = {}
        self._container = get_container()
    
    def register_service(self, service_name: str, service_instance: IService) -> bool:
        """
        Register a service instance.
        
        Args:
            service_name: Name of the service
            service_instance: Service instance to register
            
        Returns:
            True if registration successful
        """
        try:
            self._services[service_name] = service_instance
            self._container.register_instance(type(service_instance), service_instance)
            return True
        except Exception as e:
            logger.error(f"Failed to register service {service_name}: {e}")
            return False
    
    def get_service(self, service_name: str) -> Optional[IService]:
        """
        Get a service by name.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Service instance or None if not found
        """
        return self._services.get(service_name)
    
    def get_all_services(self) -> Dict[str, IService]:
        """Get all registered services."""
        return self._services.copy()
    
    def service_exists(self, service_name: str) -> bool:
        """Check if a service is registered."""
        return service_name in self._services
    
    def clear(self) -> None:
        """Clear all registered services."""
        self._services.clear()


class ServiceDiscovery:
    """
    Simplified service discovery using separated concerns.
    Coordinates service detection, registration, and routing setup.
    """
    
    def __init__(self, registry: ServiceRegistry, 
                 service_detector: IServiceDetector = None,
                 interface_manager: IInterfaceManager = None):
        """
        Initialize service discovery with configurable components.
        
        Args:
            registry: Service registry instance
            service_detector: Service detection strategy
            interface_manager: Interface registration manager
        """
        self._registry = registry
        self._service_detector = service_detector or ServiceDetectorFactory.create_default()
        self._interface_manager = interface_manager or InterfaceManagerFactory.create_default(
            self._registry._container
        )
        self._route_manager = RouteManager()
    
    def discover_and_register_services(self, module_path: str) -> bool:
        """
        Discover and register services in a module.
        
        Args:
            module_path: Python module path
            
        Returns:
            True if all services discovered and registered successfully
        """
        try:
            service_module = self._load_service_module(module_path)
            if service_module is None:
                return True  # Not having a service module is acceptable
            
            service_classes = self._service_detector.get_service_classes(service_module)
            
            for service_class in service_classes:
                if not self._register_service_class(service_class, module_path):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error discovering services in {module_path}: {e}")
            return False
    
    def _load_service_module(self, module_path: str):
        """Load service module, handling import errors gracefully."""
        try:
            return importlib.import_module(f"{module_path}.{ServiceConstants.SERVICE_MODULE_NAME}")
        except ImportError as e:
            logger.warning(f"Service module not found for {module_path}: {e}")
            return None
    
    def _register_service_class(self, service_class: Type[BaseService], 
                               module_path: str) -> bool:
        """Register a service class instance with all required registrations."""
        try:
            # Create and initialize service instance
            service_instance = service_class()
            
            if not service_instance.initialize():
                logger.error(f"Failed to initialize {service_class.__name__}")
                return False
            
            # Get service name from class metadata
            service_name = getattr(service_class, ServiceConstants.SERVICE_NAME_ATTRIBUTE)
            
            # Register service with registry
            if not self._registry.register_service(service_name, service_instance):
                return False
            
            # Register interfaces with DI container
            self._interface_manager.register_service_interfaces(service_class, service_instance)
            
            # Setup routes if module exists
            self._route_manager.setup_routes(module_path, service_name, service_instance)
            
            return True
            
        except Exception as e:
            logger.error(f"Error registering service {service_class.__name__}: {e}")
            return False


class RouteManager:
    """Manages route setup and registration for services."""
    
    def setup_routes(self, module_path: str, service_name: str, 
                    service_instance: IService) -> None:
        """Setup routes for a service if routes module exists."""
        try:
            routes_module = self._load_routes_module(module_path)
            if routes_module is None:
                return
            
            # Register service instance with routes module
            self._register_service_with_routes(routes_module, service_name, service_instance)
            
            # Instantiate route classes
            self._instantiate_route_classes(routes_module)
            
        except Exception as e:
            logger.warning(f"Error setting up routes for {module_path}: {e}")
    
    def _load_routes_module(self, module_path: str):
        """Load routes module, handling import errors gracefully."""
        try:
            return importlib.import_module(f"{module_path}.{ServiceConstants.ROUTES_MODULE_NAME}")
        except ImportError:
            return None  # Routes module might not exist
    
    def _register_service_with_routes(self, routes_module, service_name: str, 
                                    service_instance: IService) -> None:
        """Register service instance variable with routes module."""
        service_var_name = ServiceConstants.SERVICE_VAR_PATTERN.format(service_name)
        setattr(routes_module, service_var_name, service_instance)
    
    def _instantiate_route_classes(self, routes_module) -> None:
        """Find and instantiate route classes to register their exposed methods with Eel."""
        try:
            # Import BaseRoutes for type checking
            from ..web.routes import BaseRoutes
            
            for name, obj in inspect.getmembers(routes_module, inspect.isclass):
                if self._is_route_class(obj, routes_module):
                    # Instantiate the route class - this will trigger @expose_route decorators
                    route_instance = obj()
                    logger.info(f"Instantiated route class: {name}")
                    
        except Exception as e:
            logger.warning(f"Error instantiating route classes: {e}")
    
    def _is_route_class(self, obj: Type, routes_module) -> bool:
        """Check if a class is a route class."""
        try:
            from ..web.routes import BaseRoutes
            return (hasattr(obj, '__module__') and 
                    obj.__module__ == routes_module.__name__ and
                    issubclass(obj, BaseRoutes) and
                    obj is not BaseRoutes)
        except ImportError:
            return False


class IFeatureManager(ABC):
    """Interface for feature management."""
    
    @abstractmethod
    def register_features(self, feature_modules: List[Tuple[str, str]]) -> bool:
        """Register application features."""
        pass
    
    @abstractmethod
    def get_features_status(self) -> Dict[str, Any]:
        """Get status of all registered features."""
        pass


class FeatureManager(IFeatureManager):
    """Manages application features registration and status."""
    
    def __init__(self):
        """Initialize the feature manager."""
        self._features: Dict[str, Dict[str, Any]] = {}
        self._service_registry = get_service_registry()
    
    def register_features(self, feature_modules: List[Tuple[str, str]]) -> bool:
        """
        Register application features.
        
        Args:
            feature_modules: List of (feature_name, module_path) tuples
            
        Returns:
            True if all features registered successfully
        """
        try:
            for feature_name, module_path in feature_modules:
                logger.info(LoggingConstants.FEATURE_REGISTERING.format(feature_name))
                
                if auto_discover_services(module_path):
                    self._features[feature_name] = {
                        'module_path': module_path,
                        'status': 'active',
                        'registered_at': datetime.now().isoformat()
                    }
                    logger.info(LoggingConstants.FEATURE_SUCCESS.format(feature_name))
                else:
                    logger.error(LoggingConstants.FEATURE_FAILED.format(feature_name))
                    return False
            
            logger.info(LoggingConstants.FEATURES_REGISTERED.format(list(self._features.keys())))
            return True
            
        except Exception as e:
            logger.error(f"Error during feature registration: {e}")
            return False
    
    def get_features_status(self) -> Dict[str, Any]:
        """Get status of all registered features."""
        return {
            'total_features': len(self._features),
            'features': self._features.copy(),
            'services': list(self._service_registry.get_all_services().keys())
        }


def Service(name: Optional[str] = None):
    """
    Decorator for marking service classes for automatic registration.
    
    Usage:
        @Service("data")
        class DataService(BaseService):
            pass
    
    Args:
        name: Optional service name, defaults to class name in snake_case
        
    Returns:
        Decorated service class with registration metadata
    """
    def decorator(service_class: Type[BaseService]) -> Type[BaseService]:
        service_name = name or _camel_to_snake(service_class.__name__)
        setattr(service_class, ServiceConstants.SERVICE_NAME_ATTRIBUTE, service_name)
        return service_class
    
    return decorator


def _camel_to_snake(camel_str: str) -> str:
    """Convert CamelCase to snake_case."""
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', camel_str).lower()


# Initialize singleton factory for service registry
_registry_factory = create_singleton_factory(lambda: ServiceRegistry())
get_singleton_registry().register_factory(ContainerConstants.SERVICE_REGISTRY_NAME, _registry_factory)


def get_service_registry() -> ServiceRegistry:
    """Get the global service registry instance."""
    return get_singleton_registry().get_instance(ContainerConstants.SERVICE_REGISTRY_NAME)


def auto_discover_services(module_path: str) -> bool:
    """
    Automatically discover and initialize services in a module.
    
    Args:
        module_path: Python module path
        
    Returns:
        True if all services initialized successfully
    """
    registry = get_service_registry()
    discovery = ServiceDiscovery(registry)
    return discovery.discover_and_register_services(module_path) 