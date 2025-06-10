"""
Health feature API routes.
Provides Eel-exposed endpoints for health monitoring and system status using class-based architecture with dependency injection.
"""

import eel
from datetime import datetime
from typing import Dict, Any

from ...core.web.routes import BaseRoutes, expose_route
from .service import IHealthService

class HealthRoutes(BaseRoutes):
    """
    Health monitoring routes with automatic dependency injection.
    Provides comprehensive health status endpoints for system monitoring.
    """
    
    # Type annotation for automatic injection via BaseRoutes
    health_service: IHealthService
    
    def __init__(self):
        """Initialize health routes with automatic dependency injection."""
        super().__init__()
    
    @expose_route
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get comprehensive health status of the application.
        
        Returns:
            Dictionary containing detailed health information including:
            - System information
            - Memory and disk usage
            - CPU usage
            - Application uptime
            - Overall health status
        """
        return self.health_service.get_health_status()
    
    @expose_route
    def get_quick_health(self) -> Dict[str, Any]:
        """
        Get a quick health status check for lightweight monitoring.
        
        Returns:
            Dictionary with basic health information:
            - Status (healthy/degraded/unhealthy)
            - Timestamp
            - Uptime
            - Basic resource usage
        """
        return self.health_service.get_quick_status()
    
    @expose_route
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get detailed system information.
        
        Returns:
            Dictionary containing system information:
            - Platform details
            - Hardware information
            - Python version
            - Hostname
        """
        return self.health_service.get_system_info()
    
    @expose_route
    def ping(self) -> Dict[str, Any]:
        """
        Simple ping endpoint for basic connectivity check.
        Does not require health service as it's a basic connectivity test.
        
        Returns:
            Simple response indicating the service is running
        """
        return {
            "success": True,
            "data": {
                "message": "pong",
                "timestamp": datetime.now().isoformat(),
                "service": "health"
            }
        } 