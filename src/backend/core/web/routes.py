"""
Base route classes for building API endpoints with dependency injection.
Provides common functionality and structure for feature-specific route implementations.
"""

import eel
import logging
from typing import Dict, Any, Optional, Type, TypeVar, get_type_hints
from functools import wraps

from ..di.container import get_container
from ..interfaces import IService
from ..constants import RouteConstants
from ..web.decorators import handle_exceptions, log_route_call

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=IService)


class BaseRoutes:
    """
    Base class for all route implementations.
    Provides dependency injection and common route functionality with automatic service injection.
    """
    
    def __init__(self):
        """Initialize the base routes with automatic dependency injection."""
        self._container = get_container()
        self._services: Dict[str, IService] = {}
        self._auto_inject_dependencies()
        self._expose_routes_to_eel()
    
    def _auto_inject_dependencies(self) -> None:
        """
        Automatically inject dependencies based on type annotations.
        FAIL FAST approach: If injection fails, application startup should fail.
        
        Scans class type annotations and automatically injects services
        that implement interfaces (detected by 'interfaces' in module name).
        """
        hints = get_type_hints(self.__class__)
        required_services = []
        
        for attr_name, attr_type in hints.items():
            # Skip built-in types and non-service attributes
            if not hasattr(attr_type, '__module__'):
                continue
                
            # Check if this is likely a service interface
            if (RouteConstants.INTERFACES_MODULE_KEYWORD in attr_type.__module__ or 
                attr_type.__name__.startswith('I') and attr_type.__name__.endswith('Service')):
                
                # Derive service name from attribute name or interface name
                service_name = self._derive_service_name(attr_name, attr_type)
                required_services.append((attr_name, attr_type, service_name))
                
                # Inject the service - FAIL FAST if not available
                service = self._inject_service(attr_type, service_name)
                if service is None:
                    raise ValueError(
                        f"Failed to inject required service '{service_name}' for {self.__class__.__name__}. "
                        f"Ensure the service is properly registered in the DI container."
                    )
                
                setattr(self, attr_name, service)
                logger.debug(f"Auto-injected {attr_name}: {attr_type.__name__}")
        
        if required_services:
            logger.info(f"Successfully injected {len(required_services)} services for {self.__class__.__name__}")
    
    def _derive_service_name(self, attr_name: str, attr_type: Type) -> str:
        """
        Derive service name from attribute name or type.
        
        Args:
            attr_name: The attribute name (e.g., 'health_service')
            attr_type: The service interface type (e.g., IHealthService)
            
        Returns:
            Derived service name for container lookup
        """
        # Try to derive from attribute name first
        service_name = attr_name.replace('_service', '').replace('service', '')
        
        # If that doesn't work, derive from interface name
        if not service_name or service_name == attr_name:
            interface_name = attr_type.__name__
            # Remove 'I' prefix and 'Service' suffix
            if interface_name.startswith('I'):
                interface_name = interface_name[1:]
            if interface_name.endswith('Service'):
                interface_name = interface_name[:-7]
            service_name = interface_name.lower()
        
        return service_name
    
    def _expose_routes_to_eel(self) -> None:
        """Expose methods marked with @expose_route to Eel."""
        import inspect
        
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            # Check if the method was decorated with @expose_route
            if hasattr(method, RouteConstants.EEL_EXPOSURE_ATTRIBUTE) and getattr(method, RouteConstants.EEL_EXPOSURE_ATTRIBUTE):
                # Get the original function name for Eel exposure
                func_name = getattr(method, '__name__', name)
                
                # Expose the bound method to Eel
                eel.expose(method)
                logger.debug(f"Exposed route method '{func_name}' from {self.__class__.__name__}")
    
    def _inject_service(self, service_type: Type[T], service_name: str) -> Optional[T]:
        """
        Inject a service dependency with FAIL FAST approach.
        
        Args:
            service_type: The service interface type
            service_name: Name of the service for caching
            
        Returns:
            Service instance or None if not available
        """
        if service_name not in self._services:
            try:
                service = self._container.resolve(service_type)
                
                # Verify service is properly initialized
                if not service.is_initialized:
                    raise ValueError(f"Service '{service_name}' is not properly initialized")
                
                self._services[service_name] = service
                logger.debug(f"Injected service: {service_name}")
            except Exception as e:
                logger.error(f"Service injection failed for '{service_name}': {e}")
                return None
                
        return self._services[service_name]


def expose_route(func):
    """
    Decorator to expose a method as an Eel route with common decorators.
    
    Args:
        func: The method to expose
        
    Returns:
        Decorated method with Eel exposure and common decorators
    """
    # Mark the function as needing Eel exposure
    setattr(func, RouteConstants.EEL_EXPOSURE_ATTRIBUTE, True)
    
    @handle_exceptions
    @log_route_call
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    setattr(wrapper, RouteConstants.EEL_EXPOSURE_ATTRIBUTE, True)
    setattr(wrapper, RouteConstants.ORIGINAL_FUNC_ATTRIBUTE, func)
    return wrapper 