"""
Application constants module.
Centralized constants for error codes, messages, and application-wide values.
"""

from enum import Enum


class ErrorCodes(Enum):
    """Standard error codes for the application."""
    SERVICE_NOT_INITIALIZED = "SERVICE_NOT_INITIALIZED"
    SERVICE_NOT_FOUND = "SERVICE_NOT_FOUND"
    CONTROLLER_NOT_INITIALIZED = "CONTROLLER_NOT_INITIALIZED"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"
    INVALID_INPUT = "INVALID_INPUT"
    FEATURE_REGISTRATION_FAILED = "FEATURE_REGISTRATION_FAILED"


class LogMessages:
    """Standard log messages for the application."""
    
    # Initialization messages
    INIT_START = "🚀 Initializing Automata with feature-driven architecture..."
    INIT_SUCCESS = "✅ Application controller initialized successfully"
    INIT_FAILED = "❌ Failed to initialize app controller: {}"
    
    # Feature registration messages
    FEATURE_REGISTERING = "📋 Registering {} feature..."
    FEATURE_SUCCESS = "✅ {} feature registered successfully"
    FEATURE_FAILED = "❌ Failed to register {} feature"
    FEATURES_REGISTERED = "📦 Registered features: {}"
    
    # Service messages
    SERVICE_INIT_SUCCESS = "✅ {} service initialized"
    SERVICE_INIT_FAILED = "❌ Failed to initialize {} service: {}"
    
    # System messages
    APP_CLOSING = "👋 Application closing gracefully"
    CLEANUP_FEATURE = "🧹 Cleaning up {} feature..."
    EEL_CONFIGURED = "🔧 Eel configured with professional settings"
    STATUS_RETRIEVED = "📊 Features status retrieved successfully"


class Constants:
    """Application-wide constants."""
    
    # Feature modules configuration
    FEATURE_MODULES = [
        ('health', 'backend.features.health')
    ]
    
    # Service naming patterns
    SERVICE_VAR_PATTERN = "_{}_service"
    
    # Response structure keys
    RESPONSE_DATA = "data"
    RESPONSE_ERROR = "error"
    RESPONSE_SUCCESS = "success"
    RESPONSE_CODE = "code" 