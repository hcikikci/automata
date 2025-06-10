# Core Framework Architecture

This directory contains the foundational components of the application, organized by clear separation of concerns.

## Directory Structure

```
core/
├── app/              # Application orchestration layer
│   └── application.py   # Main application lifecycle management
├── di/               # Dependency injection layer
│   ├── container.py     # DI container implementation
│   └── registry.py      # Service registry and feature management
├── services/         # Service abstractions
│   └── base.py          # Base service classes and interfaces
├── web/              # Web layer components
│   ├── api.py           # Web API endpoints
│   ├── decorators.py    # Route decorators and utilities
│   └── responses.py     # Standardized response handling
├── framework/        # Framework integration
│   └── eel_setup.py     # Eel framework configuration
└── __init__.py       # Public API exports
```

## Core Components

### Application Layer (`app/`)
- **`Application`**: Main application orchestrator that handles lifecycle and coordination
- **`ApplicationFactory`**: Factory for creating application instances with different configurations

### Dependency Injection (`di/`)
- **`Container`**: Simple DI container for managing dependencies
- **`ServiceRegistry`**: Service registration and discovery
- **`FeatureManager`**: Feature lifecycle management
- **`@Service`**: Decorator for marking service classes

### Services (`services/`)
- **`IService`**: Interface for all application services
- **`BaseService`**: Base implementation with common functionality

### Web Layer (`web/`)
- **`WebAPI`**: Web API layer for Eel endpoints
- **`ResponseHandler`**: Standardized response creation
- **`RouteDecorators`**: Common decorators for route functions

### Framework Integration (`framework/`)
- **`EelConfigurator`**: Eel framework setup and configuration

## Key Improvements

### ✅ Better Organization
- Clear separation of concerns
- Logical grouping by functionality
- Easier to navigate and understand

### ✅ Clearer Naming
- `Application` instead of `AppController`
- `WebAPI` instead of `api_endpoints`
- `ResponseHandler` instead of `response_handler`

### ✅ Consolidated Responsibilities
- Combined `app_controller` + `app_initializer` → `Application`
- Combined `service_registry` + `feature_manager` → `di/registry.py`
- Grouped web-related components together

### ✅ Improved Testability
- Factories for creating instances
- Clear interfaces and abstractions
- Better dependency injection

## Usage Examples

### Creating and Starting the Application
```python
from backend.core import ApplicationFactory

# Simple usage
app = ApplicationFactory.create()
if app.start():
    print("Application started successfully")

# With custom settings
from backend.config.app_settings import AppSettings
settings = AppSettings()
app = ApplicationFactory.create(settings)
```

### Creating a Service
```python
from backend.core import BaseService, Service

@Service("my_feature")
class MyFeatureService(BaseService):
    def __init__(self):
        super().__init__("my_feature")
    
    def _initialize_specific(self):
        # Custom initialization logic
        self.logger.info("My feature service initialized")
```

### Using Route Decorators
```python
from backend.core import require_initialization, handle_exceptions
import eel

@eel.expose
@require_initialization
@handle_exceptions
def my_api_endpoint():
    # Your endpoint logic here
    return {"success": True}
```

This new structure provides a solid foundation for scalable application development with clear responsibilities and improved maintainability. 