"""
Core constants and configuration values.
Centralized constants to eliminate magic strings and improve maintainability.
"""

from enum import Enum, auto
from typing import Final


class ServiceConstants:
    """Constants related to service management."""
    
    # Service detection
    SERVICE_NAME_ATTRIBUTE: Final[str] = '_service_name'
    INTERFACES_ATTRIBUTE: Final[str] = '__interfaces__'
    
    # Interface naming conventions
    INTERFACE_PREFIX: Final[str] = 'I'
    SERVICE_SUFFIX: Final[str] = 'Service'
    
    # Service variable naming pattern
    SERVICE_VAR_PATTERN: Final[str] = '_{}_service'
    
    # Module names
    SERVICE_MODULE_NAME: Final[str] = 'service'
    ROUTES_MODULE_NAME: Final[str] = 'routes'


class ContainerConstants:
    """Constants for dependency injection container."""
    
    # Container registry names
    CONTAINER_REGISTRY_NAME: Final[str] = 'container'
    SERVICE_REGISTRY_NAME: Final[str] = 'service_registry'
    WEB_API_REGISTRY_NAME: Final[str] = 'web_api'


class RouteConstants:
    """Constants for routing and web layer."""
    
    # Route exposure attributes
    EEL_EXPOSURE_ATTRIBUTE: Final[str] = '_needs_eel_exposure'
    ORIGINAL_FUNC_ATTRIBUTE: Final[str] = '_original_func'
    
    # Interface module detection
    INTERFACES_MODULE_KEYWORD: Final[str] = 'interfaces'


class ResponseConstants:
    """Constants for API response structure."""
    
    # Response keys
    SUCCESS_KEY: Final[str] = 'success'
    DATA_KEY: Final[str] = 'data'
    ERROR_KEY: Final[str] = 'error'
    CODE_KEY: Final[str] = 'code'


class LoggingConstants:
    """Constants for logging messages."""
    
    # Application lifecycle
    INIT_START: Final[str] = "Application initialization started"
    INIT_SUCCESS: Final[str] = "Application initialized successfully"
    INIT_FAILED: Final[str] = "Application initialization failed: {}"
    APP_CLOSING: Final[str] = "Application is closing"
    
    # Service management
    SERVICE_INIT_SUCCESS: Final[str] = "Service '{}' initialized successfully"
    SERVICE_INIT_FAILED: Final[str] = "Service '{}' initialization failed: {}"
    
    # Feature management
    FEATURE_REGISTERING: Final[str] = "Registering feature: {}"
    FEATURE_SUCCESS: Final[str] = "Feature '{}' registered successfully"
    FEATURE_FAILED: Final[str] = "Feature '{}' registration failed"
    FEATURES_REGISTERED: Final[str] = "All features registered: {}"
    
    # Web layer
    EEL_CONFIGURED: Final[str] = "Eel framework configured successfully"
    STATUS_RETRIEVED: Final[str] = "Application status retrieved successfully"


class ErrorCodes(Enum):
    """Enumeration of application error codes."""
    
    # General errors
    UNEXPECTED_ERROR = auto()
    INVALID_INPUT = auto()
    
    # Service errors
    SERVICE_NOT_FOUND = auto()
    SERVICE_NOT_INITIALIZED = auto()
    SERVICE_INIT_FAILED = auto()
    
    # Controller errors
    CONTROLLER_NOT_INITIALIZED = auto()
    CONTROLLER_OPERATION_FAILED = auto()
    
    # Feature errors
    FEATURE_NOT_FOUND = auto()
    FEATURE_REGISTRATION_FAILED = auto()
    
    # DI Container errors
    DEPENDENCY_NOT_FOUND = auto()
    CIRCULAR_DEPENDENCY = auto()
    CONTAINER_ERROR = auto()


class ValidationConstants:
    """Constants for input validation."""
    
    # Error messages
    EMPTY_INPUT_ERROR: Final[str] = "Input cannot be empty"
    INVALID_TYPE_ERROR: Final[str] = "Invalid input type: expected {}"
    
    # Validation rules
    MIN_STRING_LENGTH: Final[int] = 1
    MAX_STRING_LENGTH: Final[int] = 1000


class ConfigurationConstants:
    """Constants for application configuration."""
    
    # Default values
    DEFAULT_HOST: Final[str] = 'localhost'
    DEFAULT_PORT: Final[int] = 8080
    DEFAULT_MODE: Final[str] = 'chrome'
    
    # File paths
    CONFIG_FILE_NAME: Final[str] = 'app_settings.json'
    LOG_FILE_NAME: Final[str] = 'application.log'