"""
Web API layer for application endpoints.
Handles HTTP/Eel layer interactions and delegates to application services.
"""

import eel
import logging
from typing import Dict, Any, TYPE_CHECKING

from .responses import ResponseHandler
from ..constants import LoggingConstants, ErrorCodes, ContainerConstants
from ..di.singleton_factory import get_singleton_registry, create_singleton_factory

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from ..app.application import Application

logger = logging.getLogger(__name__)


class WebAPI:
    """Web API layer for exposing application functionality via Eel."""
    
    def __init__(self, application: 'Application' = None):
        """
        Initialize the web API layer.
        
        Args:
            application: Application instance
        """
        self._application = application or self._create_application()
    
    def _create_application(self) -> 'Application':
        """Create an application instance using lazy import to avoid circular dependencies."""
        from ..app.application import ApplicationFactory
        return ApplicationFactory.create()
    
    def get_application_status(self) -> Dict[str, Any]:
        """Get comprehensive application and features status."""
        try:
            if not self._application.is_initialized:
                return ResponseHandler.error(
                    "Application not initialized",
                    ErrorCodes.CONTROLLER_NOT_INITIALIZED
                )
            
            status = self._application.get_status()
            logger.info(LoggingConstants.STATUS_RETRIEVED)
            return ResponseHandler.success(status)
            
        except Exception as e:
            error_msg = f"Error getting application status: {str(e)}"
            logger.error(error_msg)
            return ResponseHandler.unexpected_error(error_msg)


# Initialize singleton factory for web API
_web_api_factory = create_singleton_factory(lambda: WebAPI())
get_singleton_registry().register_factory(ContainerConstants.WEB_API_REGISTRY_NAME, _web_api_factory)


def get_web_api() -> WebAPI:
    """Get the global web API instance."""
    return get_singleton_registry().get_instance(ContainerConstants.WEB_API_REGISTRY_NAME)


# Eel exposed endpoints
@eel.expose
def get_features_status() -> Dict[str, Any]:
    """Get status of all registered features and application state."""
    return get_web_api().get_application_status()


def reset_web_api() -> None:
    """Reset the global web API instance (mainly for testing)."""
    get_singleton_registry().reset_instance(ContainerConstants.WEB_API_REGISTRY_NAME) 