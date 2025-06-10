"""
Health service for application monitoring and status checks.
Provides comprehensive health information about the application state.
"""

import platform
import psutil
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Any, List

from ...core import BaseService, Service, ResponseHandler
from ...config.constants import ErrorCodes


class IHealthService(ABC):
    """Interface for health monitoring service."""
    
    @abstractmethod
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get comprehensive health status of the application.
        
        Returns:
            Dictionary containing detailed health information
        """
        pass
    
    @abstractmethod
    def get_quick_status(self) -> Dict[str, Any]:
        """
        Get a quick health status check for lightweight monitoring.
        
        Returns:
            Dictionary with basic health information
        """
        pass
    
    @abstractmethod
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get detailed system information.
        
        Returns:
            Dictionary containing system information
        """
        pass
    
    @abstractmethod
    def is_initialized(self) -> bool:
        """Check if the service is properly initialized."""
        pass


@Service("health")
class HealthService(BaseService, IHealthService):
    """Service for monitoring application health and system status."""
    
    def __init__(self):
        """Initialize the health service."""
        super().__init__("health")
        self._start_time = None
        self._health_checks = []
    
    def _initialize_specific(self) -> None:
        """Initialize health-specific functionality."""
        self._start_time = datetime.now()
        self._register_health_checks()
        self.logger.info("Health service initialized with monitoring capabilities")
    
    def _register_health_checks(self) -> None:
        """Register available health checks."""
        self._health_checks = [
            ("system_info", self._get_system_info),
            ("memory_usage", self._get_memory_usage),
            ("disk_usage", self._get_disk_usage),
            ("application_uptime", self._get_application_uptime),
            ("cpu_usage", self._get_cpu_usage)
        ]
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get comprehensive health status of the application.
        
        Returns:
            Dictionary containing detailed health information
        """
        try:
            health_data = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "checks": {},
                "summary": {
                    "total_checks": len(self._health_checks),
                    "passed": 0,
                    "failed": 0
                }
            }
            
            # Run all health checks
            for check_name, check_function in self._health_checks:
                try:
                    check_result = check_function()
                    health_data["checks"][check_name] = {
                        "status": "pass",
                        "data": check_result
                    }
                    health_data["summary"]["passed"] += 1
                except Exception as e:
                    health_data["checks"][check_name] = {
                        "status": "fail",
                        "error": str(e)
                    }
                    health_data["summary"]["failed"] += 1
                    self.logger.warning(f"Health check {check_name} failed: {e}")
            
            # Determine overall status
            if health_data["summary"]["failed"] > 0:
                health_data["status"] = "degraded" if health_data["summary"]["passed"] > 0 else "unhealthy"
            
            return ResponseHandler.success(health_data)
            
        except Exception as e:
            error_msg = f"Error getting health status: {str(e)}"
            self.logger.error(error_msg)
            return ResponseHandler.error(error_msg, ErrorCodes.UNEXPECTED_ERROR)
    
    def get_quick_status(self) -> Dict[str, Any]:
        """
        Get a quick health status check for lightweight monitoring.
        
        Returns:
            Dictionary with basic health information
        """
        try:
            quick_data = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": self._get_uptime_seconds(),
                "memory_usage_percent": psutil.virtual_memory().percent,
                "cpu_usage_percent": psutil.cpu_percent()
            }
            
            return ResponseHandler.success(quick_data)
            
        except Exception as e:
            error_msg = f"Error getting quick status: {str(e)}"
            self.logger.error(error_msg)
            return ResponseHandler.error(error_msg, ErrorCodes.UNEXPECTED_ERROR)
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get detailed system information.
        
        Returns:
            Dictionary containing system information
        """
        try:
            system_data = self._get_system_info()
            return ResponseHandler.success(system_data)
            
        except Exception as e:
            error_msg = f"Error getting system info: {str(e)}"
            self.logger.error(error_msg)
            return ResponseHandler.error(error_msg, ErrorCodes.UNEXPECTED_ERROR)
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get basic system information."""
        return {
            "platform": platform.platform(),
            "system": platform.system(),
            "processor": platform.processor(),
            "architecture": platform.architecture(),
            "python_version": platform.python_version(),
            "hostname": platform.node()
        }
    
    def _get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage information."""
        memory = psutil.virtual_memory()
        return {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "used_gb": round(memory.used / (1024**3), 2),
            "percentage": memory.percent
        }
    
    def _get_disk_usage(self) -> Dict[str, Any]:
        """Get disk usage information."""
        disk = psutil.disk_usage('/')
        return {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percentage": round((disk.used / disk.total) * 100, 2)
        }
    
    def _get_application_uptime(self) -> Dict[str, Any]:
        """Get application uptime information."""
        if not self._start_time:
            return {"uptime_seconds": 0, "uptime_formatted": "Unknown"}
        
        uptime_seconds = self._get_uptime_seconds()
        uptime_delta = timedelta(seconds=uptime_seconds)
        
        return {
            "uptime_seconds": uptime_seconds,
            "uptime_formatted": str(uptime_delta),
            "started_at": self._start_time.isoformat()
        }
    
    def _get_cpu_usage(self) -> Dict[str, Any]:
        """Get CPU usage information."""
        return {
            "percentage": psutil.cpu_percent(interval=1),
            "core_count": psutil.cpu_count(),
            "logical_core_count": psutil.cpu_count(logical=True)
        }
    
    def _get_uptime_seconds(self) -> int:
        """Get application uptime in seconds."""
        if not self._start_time:
            return 0
        return int((datetime.now() - self._start_time).total_seconds()) 