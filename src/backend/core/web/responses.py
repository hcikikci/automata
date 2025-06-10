"""
Response handling utilities.
Provides standardized response creation and error handling for web layer.
"""

from typing import Dict, Any, Optional
from ..constants import ErrorCodes, ResponseConstants


class ResponseHandler:
    """Centralized response handler for consistent API responses."""
    
    @staticmethod
    def success(data: Any = None) -> Dict[str, Any]:
        """
        Create a success response.
        
        Args:
            data: Response data
            
        Returns:
            Standardized success response
        """
        response = {ResponseConstants.SUCCESS_KEY: True}
        if data is not None:
            response[ResponseConstants.DATA_KEY] = data
        return response
    
    @staticmethod
    def error(message: str, error_code: ErrorCodes, data: Any = None) -> Dict[str, Any]:
        """
        Create an error response.
        
        Args:
            message: Error message
            error_code: Error code from ErrorCodes enum
            data: Optional additional data
            
        Returns:
            Standardized error response
        """
        response = {
            ResponseConstants.SUCCESS_KEY: False,
            ResponseConstants.ERROR_KEY: message,
            ResponseConstants.CODE_KEY: error_code.value
        }
        if data is not None:
            response[ResponseConstants.DATA_KEY] = data
        return response
    
    @staticmethod
    def service_not_initialized(service_name: str) -> Dict[str, Any]:
        """
        Create a service not initialized error response.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Service not initialized error response
        """
        return ResponseHandler.error(
            f"{service_name} service not initialized",
            ErrorCodes.SERVICE_NOT_INITIALIZED
        )
    
    @staticmethod
    def service_not_found(service_name: str) -> Dict[str, Any]:
        """
        Create a service not found error response.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Service not found error response
        """
        return ResponseHandler.error(
            f"{service_name} service not found",
            ErrorCodes.SERVICE_NOT_FOUND
        )
    
    @staticmethod
    def unexpected_error(message: str) -> Dict[str, Any]:
        """
        Create an unexpected error response.
        
        Args:
            message: Error message
            
        Returns:
            Unexpected error response
        """
        return ResponseHandler.error(
            message,
            ErrorCodes.UNEXPECTED_ERROR
        )
    
    @staticmethod
    def invalid_input(message: str) -> Dict[str, Any]:
        """
        Create an invalid input error response.
        
        Args:
            message: Error message
            
        Returns:
            Invalid input error response
        """
        return ResponseHandler.error(
            message,
            ErrorCodes.INVALID_INPUT
        ) 