"""
Web layer components for the application.
Provides route handling, API management, and web-related functionality.
"""

from .routes import BaseRoutes, expose_route
from .responses import ResponseHandler
from .decorators import (
    RouteDecorators, require_initialization, handle_exceptions, log_route_call
)

# Lazy import for API to avoid circular dependencies
def get_web_api():
    """Get the web API instance with lazy import."""
    from .api import get_web_api as _get_web_api
    return _get_web_api()

def reset_web_api():
    """Reset web API with lazy import."""
    from .api import reset_web_api as _reset_web_api
    return _reset_web_api()

__all__ = [
    # Route handling
    'BaseRoutes',
    'expose_route',
    
    # API management (lazy imports)
    'get_web_api',
    'reset_web_api',
    
    # Response handling
    'ResponseHandler',
    
    # Decorators
    'RouteDecorators',
    'require_initialization',
    'handle_exceptions',
    'log_route_call',
] 