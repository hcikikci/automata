"""
Web route decorators and utilities.
Provides common decorators for route functions with error handling and service validation.
"""

import functools
import logging
from typing import Dict, Any, Callable, Optional
from ..interfaces import IService
from .responses import ResponseHandler
from ..constants import ErrorCodes, ServiceConstants

logger = logging.getLogger(__name__)


class RouteDecorators:
    """Collection of route decorators for common web functionality."""
    
    @staticmethod
    def require_service_initialization(func: Callable) -> Callable:
        """
        Decorator to automatically handle service initialization checks.
        
        Args:
            func: The route function to decorate
            
        Returns:
            Decorated function with automatic initialization check
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            service = RouteDecorators._get_service_from_module(func)
            
            if not service:
                return ResponseHandler.service_not_found("Unknown")
            
            if not service.is_initialized:
                return ResponseHandler.service_not_initialized(service.feature_name)
            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"Error in {func.__name__}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return ResponseHandler.unexpected_error(error_msg)
        
        return wrapper
    
    @staticmethod
    def handle_exceptions(func: Callable) -> Callable:
        """
        Decorator to handle exceptions in route functions.
        
        Args:
            func: The route function to decorate
            
        Returns:
            Decorated function with exception handling
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"Unexpected error in {func.__name__}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return ResponseHandler.unexpected_error(error_msg)
        
        return wrapper
    
    @staticmethod
    def log_route_call(func: Callable) -> Callable:
        """
        Decorator to log route function calls.
        
        Args:
            func: The route function to decorate
            
        Returns:
            Decorated function with logging
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Route {func.__name__} called with args: {args}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"Route {func.__name__} completed")
            return result
        
        return wrapper
    
    @staticmethod
    def _get_service_from_module(func: Callable) -> Optional[IService]:
        """Get the service instance from the function's module."""
        frame = func.__globals__
        
        # Find the service variable using the service variable pattern
        for var_name, var_value in frame.items():
            if (var_name.startswith('_') and 
                var_name.endswith('_service') and 
                var_value is not None and
                isinstance(var_value, IService)):
                return var_value
        
        return None


# Convenience function shortcuts
def require_initialization(func: Callable) -> Callable:
    """Shortcut for service initialization requirement decorator."""
    return RouteDecorators.require_service_initialization(func)


def handle_exceptions(func: Callable) -> Callable:
    """Shortcut for exception handling decorator."""
    return RouteDecorators.handle_exceptions(func)


def log_route_call(func: Callable) -> Callable:
    """Shortcut for route logging decorator."""
    return RouteDecorators.log_route_call(func) 