# Health Feature

The Health feature provides comprehensive application monitoring and system status information. It's designed to help monitor the health and performance of the application in real-time.

## Features

### 🔍 Health Monitoring
- **Comprehensive health checks**: System information, memory usage, disk usage, CPU usage, and application uptime
- **Quick health status**: Lightweight endpoint for basic monitoring
- **System information**: Detailed platform and hardware information
- **Ping endpoint**: Simple connectivity check

### 📊 System Metrics
- **Memory Usage**: Total, available, used memory with percentage
- **Disk Usage**: Total, used, free disk space with percentage
- **CPU Usage**: Real-time CPU percentage and core information
- **Application Uptime**: Time since application started

### 🎯 Status Levels
- **Healthy**: All checks passing
- **Degraded**: Some checks failing but core functionality works
- **Unhealthy**: Multiple critical checks failing

## API Endpoints

All endpoints are exposed via Eel and can be called from the frontend.

### `get_health_status()`
Get comprehensive health status of the application.

**Returns:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00.000000",
    "checks": {
      "system_info": {
        "status": "pass",
        "data": {
          "platform": "Windows-10-10.0.26100-SP0",
          "system": "Windows",
          "processor": "Intel64 Family 6 Model 140 Stepping 1, GenuineIntel",
          "architecture": ["64bit", "WindowsPE"],
          "python_version": "3.11.0",
          "hostname": "MY-COMPUTER"
        }
      },
      "memory_usage": {
        "status": "pass",
        "data": {
          "total_gb": 16.0,
          "available_gb": 8.5,
          "used_gb": 7.5,
          "percentage": 46.9
        }
      },
      "disk_usage": {
        "status": "pass",
        "data": {
          "total_gb": 500.0,
          "used_gb": 250.0,
          "free_gb": 250.0,
          "percentage": 50.0
        }
      },
      "application_uptime": {
        "status": "pass",
        "data": {
          "uptime_seconds": 3600,
          "uptime_formatted": "1:00:00",
          "started_at": "2024-01-01T11:00:00.000000"
        }
      },
      "cpu_usage": {
        "status": "pass",
        "data": {
          "percentage": 15.2,
          "core_count": 8,
          "logical_core_count": 16
        }
      }
    },
    "summary": {
      "total_checks": 5,
      "passed": 5,
      "failed": 0
    }
  }
}
```

### `get_quick_health()`
Get a quick health status check for lightweight monitoring.

**Returns:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00.000000",
    "uptime_seconds": 3600,
    "memory_usage_percent": 46.9,
    "cpu_usage_percent": 15.2
  }
}
```

### `get_system_info()`
Get detailed system information.

**Returns:**
```json
{
  "success": true,
  "data": {
    "platform": "Windows-10-10.0.26100-SP0",
    "system": "Windows",
    "processor": "Intel64 Family 6 Model 140 Stepping 1, GenuineIntel",
    "architecture": ["64bit", "WindowsPE"],
    "python_version": "3.11.0",
    "hostname": "MY-COMPUTER"
  }
}
```

### `ping()`
Simple ping endpoint for basic connectivity check.

**Returns:**
```json
{
  "success": true,
  "data": {
    "message": "pong",
    "timestamp": "2024-01-01T12:00:00.000000",
    "service": "health"
  }
}
```

## Frontend Usage

You can call these endpoints from the frontend JavaScript:

```javascript
// Get comprehensive health status
const healthStatus = await eel.get_health_status()();
console.log('Health Status:', healthStatus);

// Quick health check
const quickHealth = await eel.get_quick_health()();
console.log('Quick Health:', quickHealth);

// Get system information
const systemInfo = await eel.get_system_info()();
console.log('System Info:', systemInfo);

// Simple ping
const ping = await eel.ping()();
console.log('Ping:', ping);
```

## Error Handling

All endpoints include proper error handling and will return standardized error responses:

```json
{
  "success": false,
  "error": "Error message description",
  "code": "ERROR_CODE"
}
```

## Architecture

The Health feature follows the core application architecture:

- **`HealthService`**: Main service class that inherits from `BaseService`
- **`@Service("health")`**: Decorator for automatic service registration
- **Routes**: Eel-exposed endpoints with decorators for error handling
- **Automatic Discovery**: The feature is automatically registered when the application starts

## Dependencies

- `psutil>=5.9.0`: For system and process utilities
- `platform`: For system information (built-in Python module)
- `datetime`: For timestamp and uptime calculations (built-in Python module) 