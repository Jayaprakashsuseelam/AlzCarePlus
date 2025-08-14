# Device Configuration Module

A comprehensive Django module for managing device configurations, parameters, and synchronization in the AlzCarePlus system.

## Overview

The Device Configuration module provides a robust framework for:
- Managing different types of devices and their configurations
- Defining configurable parameters with validation rules
- Tracking configuration changes and synchronization history
- Bulk operations and template management
- Export/import functionality in multiple formats
- Comprehensive audit trail and logging

## Features

### Core Functionality
- **Device Type Management**: Define and categorize different types of devices
- **Parameter Definition**: Create configurable parameters with constraints and validation
- **Configuration Storage**: Store device-specific configuration data in JSON format
- **Version Control**: Track configuration versions and changes
- **User Assignment**: Associate configurations with specific users or caretakers

### Advanced Features
- **Bulk Operations**: Update multiple device configurations simultaneously
- **Template System**: Create and apply configuration templates
- **Export/Import**: Support for JSON, CSV, and XML formats
- **Synchronization**: Track device sync status and history
- **Audit Trail**: Complete history of all configuration changes
- **Validation**: Parameter-level validation with custom rules

### Security & Performance
- **Authentication**: REST API with JWT authentication
- **Permission Control**: Role-based access control
- **Rate Limiting**: Configurable API rate limiting
- **Caching**: Query and result caching for performance
- **Logging**: Comprehensive logging and monitoring

## Models

### DeviceType
Represents different categories of devices (sensors, monitors, controllers, etc.)

```python
class DeviceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
```

### DeviceParameter
Defines configurable parameters for device types with validation rules

```python
class DeviceParameter(models.Model):
    device_type = models.ForeignKey(DeviceType)
    name = models.CharField(max_length=100)
    parameter_type = models.CharField(choices=PARAMETER_TYPE_CHOICES)
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    is_required = models.BooleanField(default=False)
```

### DeviceConfiguration
Stores device-specific configuration data and metadata

```python
class DeviceConfiguration(models.Model):
    device_type = models.ForeignKey(DeviceType)
    device_id = models.CharField(max_length=100, unique=True)
    config_data = models.JSONField(default=dict)
    status = models.CharField(choices=CONFIG_STATUS_CHOICES)
    version = models.CharField(max_length=20, default='1.0.0')
```

### DeviceConfigurationHistory
Tracks all changes to device configurations

```python
class DeviceConfigurationHistory(models.Model):
    device_config = models.ForeignKey(DeviceConfiguration)
    action = models.CharField(choices=HISTORY_ACTION_TYPES)
    old_values = models.JSONField(default=dict)
    new_values = models.JSONField(default=dict)
    changed_by = models.ForeignKey(User)
```

### DeviceSyncLog
Records device synchronization activities and results

```python
class DeviceSyncLog(models.Model):
    device_config = models.ForeignKey(DeviceConfiguration)
    sync_status = models.CharField(choices=SYNC_STATUS_CHOICES)
    sync_started = models.DateTimeField(auto_now_add=True)
    duration_ms = models.PositiveIntegerField(null=True)
    error_message = models.TextField(blank=True)
```

## API Endpoints

### Device Types
- `GET /api/device-types/` - List all device types
- `POST /api/device-types/` - Create new device type
- `GET /api/device-types/{id}/` - Get device type details
- `PUT /api/device-types/{id}/` - Update device type
- `DELETE /api/device-types/{id}/` - Delete device type
- `GET /api/device-types/{id}/configurations/` - Get configurations for device type
- `GET /api/device-types/{id}/parameters/` - Get parameters for device type

### Device Parameters
- `GET /api/parameters/` - List all parameters
- `POST /api/parameters/` - Create new parameter
- `GET /api/parameters/{id}/` - Get parameter details
- `PUT /api/parameters/{id}/` - Update parameter
- `DELETE /api/parameters/{id}/` - Delete parameter

### Device Configurations
- `GET /api/configurations/` - List all configurations
- `POST /api/configurations/` - Create new configuration
- `GET /api/configurations/{id}/` - Get configuration details
- `PUT /api/configurations/{id}/` - Update configuration
- `DELETE /api/configurations/{id}/` - Delete configuration
- `POST /api/configurations/{id}/sync/` - Sync configuration with device
- `POST /api/configurations/bulk_update/` - Bulk update configurations
- `POST /api/configurations/export/` - Export configurations

### History & Logs
- `GET /api/history/` - List configuration history
- `GET /api/sync-logs/` - List sync logs

## Usage Examples

### Creating a Device Type
```python
from device_config.models import DeviceType

# Create a new device type
device_type = DeviceType.objects.create(
    name='Temperature Sensor',
    manufacturer='SensorCorp',
    model_number='TS-100',
    description='Wireless temperature sensor for monitoring'
)
```

### Defining Parameters
```python
from device_config.models import DeviceParameter

# Create parameters for the device type
DeviceParameter.objects.create(
    device_type=device_type,
    name='sampling_interval',
    display_name='Sampling Interval',
    parameter_type='integer',
    min_value=1,
    max_value=3600,
    default_value='60',
    is_required=True,
    description='Interval between temperature readings in seconds'
)

DeviceParameter.objects.create(
    device_type=device_type,
    name='temperature_unit',
    display_name='Temperature Unit',
    parameter_type='enum',
    allowed_values=['celsius', 'fahrenheit', 'kelvin'],
    default_value='celsius',
    is_required=True
)
```

### Creating Device Configuration
```python
from device_config.models import DeviceConfiguration

# Create device configuration
config = DeviceConfiguration.objects.create(
    device_type=device_type,
    name='Living Room Sensor',
    device_id='temp_sensor_001',
    serial_number='TS100-2024-001',
    config_data={
        'sampling_interval': 120,
        'temperature_unit': 'celsius',
        'alert_threshold': 30.0
    },
    status='active',
    assigned_to=user
)
```

### Bulk Operations
```python
# Bulk update multiple devices
from device_config.views import DeviceConfigurationViewSet

data = {
    'device_ids': ['temp_sensor_001', 'temp_sensor_002'],
    'config_updates': {'sampling_interval': 180},
    'force_update': False
}

response = DeviceConfigurationViewSet.bulk_update(request, data)
```

### Export Configurations
```python
# Export configurations to CSV
data = {
    'device_ids': ['temp_sensor_001'],
    'include_history': True,
    'include_sync_logs': False,
    'format': 'csv'
}

response = DeviceConfigurationViewSet.export(request, data)
```

## Configuration

The module includes a comprehensive configuration system in `config.py`:

```python
from device_config.config import (
    DEVICE_CONFIG_SETTINGS,
    get_setting,
    validate_configuration
)

# Get configuration values
max_file_size = get_setting('MAX_FILE_SIZE')
default_version = get_setting('DEFAULT_VERSION')

# Validate configuration
validation_result = validate_configuration()
if not validation_result['valid']:
    print(f"Configuration issues: {validation_result['issues']}")
```

### Environment Variables
You can override configuration using environment variables:

```bash
export DEVICE_CONFIG_MAX_FILE_SIZE=20971520  # 20MB
export DEVICE_CONFIG_ENABLE_EMAIL_NOTIFICATIONS=false
export DEVICE_CONFIG_SYNC_TIMEOUT=60
```

## Admin Interface

The module provides a comprehensive Django admin interface:

- **Device Type Management**: Create, edit, and manage device types
- **Parameter Configuration**: Define parameters with validation rules
- **Configuration Management**: Manage device configurations and assignments
- **History Tracking**: View all configuration changes and sync logs
- **Bulk Operations**: Perform bulk updates through the admin interface

## Security Features

- **Authentication**: JWT-based authentication required for all operations
- **Permission Control**: Role-based access control for different operations
- **IP Logging**: Track IP addresses for audit purposes
- **Rate Limiting**: Prevent API abuse with configurable rate limits
- **Input Validation**: Comprehensive validation of all input data
- **SQL Injection Protection**: Parameterized queries and input sanitization

## Performance Optimization

- **Database Optimization**: Efficient queries with proper indexing
- **Query Caching**: Cache frequently accessed data
- **Result Caching**: Cache API responses for better performance
- **Batch Processing**: Support for bulk operations
- **Async Processing**: Background processing for long-running operations

## Monitoring & Logging

- **Comprehensive Logging**: Log all operations and errors
- **Audit Trail**: Complete history of all changes
- **Sync Monitoring**: Track device synchronization status
- **Performance Metrics**: Monitor API response times and throughput
- **Error Tracking**: Detailed error logging with stack traces

## Testing

The module includes comprehensive test coverage:

```bash
# Run tests for the device_config module
python manage.py test device_config

# Run specific test classes
python manage.py test device_config.tests.test_models
python manage.py test device_config.tests.test_views
python manage.py test device_config.tests.test_serializers
```

## Dependencies

- Django 5.1+
- Django REST Framework 3.14+
- Python 3.8+

## Installation

1. Add `device_config` to your `INSTALLED_APPS` in Django settings:

```python
INSTALLED_APPS = [
    # ... other apps
    'device_config',
]
```

2. Run migrations:

```bash
python manage.py makemigrations device_config
python manage.py migrate
```

3. Include URLs in your main URL configuration:

```python
from django.urls import path, include

urlpatterns = [
    # ... other URLs
    path('device-config/', include('device_config.urls')),
]
```

## Contributing

When contributing to this module:

1. Follow Django coding standards
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Ensure backward compatibility
5. Add proper error handling and validation

## License

This module is part of the AlzCarePlus system and follows the same licensing terms.

## Support

For support and questions:
- Check the Django documentation
- Review the module's test cases
- Check the admin interface for examples
- Review the configuration options in `config.py`
