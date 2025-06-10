"""
Core application framework.
Provides the fundamental building blocks for the application architecture.
"""

# Application layer
from .app.application import Application, ApplicationFactory

# Dependency injection
from .di.container import Container, IContainer, get_container, reset_container
from .di.registry import (
    ServiceRegistry, ServiceDiscovery, FeatureManager, IFeatureManager,
    Service, get_service_registry, auto_discover_services
)
from .di.singleton_factory import (
    ISingletonFactory, SingletonFactory, SingletonRegistry,
    get_singleton_registry, create_singleton_factory
)
from .di.service_detector import (
    IServiceDetector, BaseServiceDetector, ServiceDetectorFactory
)
from .di.interface_manager import (
    IInterfaceManager, InterfaceRegistrationManager, InterfaceManagerFactory
)

# Interfaces
from .interfaces import IService

# Services
from .services.base import BaseService

# Web layer
from .web import get_web_api, reset_web_api
from .web.responses import ResponseHandler
from .web.decorators import (
    RouteDecorators, require_initialization, handle_exceptions, log_route_call
)

# Framework integration
from .framework.eel_setup import EelConfigurator, IEelConfigurator

# Constants
from .constants import (
    ServiceConstants, ContainerConstants, RouteConstants, ResponseConstants,
    LoggingConstants, ErrorCodes, ValidationConstants, ConfigurationConstants,
)

__all__ = [
    # Application
    'Application',
    'ApplicationFactory',
    
    # Dependency Injection
    'Container',
    'IContainer',
    'get_container',
    'reset_container',
    'ServiceRegistry',
    'ServiceDiscovery',
    'FeatureManager',
    'IFeatureManager',
    'Service',
    'get_service_registry',
    'auto_discover_services',
    
    # Singleton Management
    'ISingletonFactory',
    'SingletonFactory', 
    'SingletonRegistry',
    'get_singleton_registry',
    'create_singleton_factory',
    
    # Service Detection
    'IServiceDetector',
    'BaseServiceDetector',
    'ServiceDetectorFactory',
    
    # Interface Management
    'IInterfaceManager',
    'InterfaceRegistrationManager',
    'InterfaceManagerFactory',
    
    # Interfaces
    'IService',
    
    # Services
    'BaseService',
    
    # Web Layer
    'get_web_api',
    'reset_web_api',
    'ResponseHandler',
    'RouteDecorators',
    'require_initialization',
    'handle_exceptions',
    'log_route_call',
    
    # Framework
    'EelConfigurator',
    'IEelConfigurator',
    
    # Constants
    'ServiceConstants',
    'ContainerConstants', 
    'RouteConstants',
    'ResponseConstants',
    'LoggingConstants',
    'ErrorCodes',
    'ValidationConstants',
    'ConfigurationConstants',
] 