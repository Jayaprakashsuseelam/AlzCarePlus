"""
Device Configuration Module Configuration

This module contains configuration settings, constants, and utility functions
for the device configuration system.
"""

import os
from typing import Dict, List, Any, Optional
from django.conf import settings

# Device Configuration Settings
DEVICE_CONFIG_SETTINGS = {
    # Default configuration values
    'DEFAULT_VERSION': '1.0.0',
    'DEFAULT_STATUS': 'active',
    'MAX_DEVICE_ID_LENGTH': 100,
    'MAX_SERIAL_NUMBER_LENGTH': 100,
    'MAX_VERSION_LENGTH': 20,
    
    # Parameter validation settings
    'MAX_PARAMETER_NAME_LENGTH': 100,
    'MAX_DISPLAY_NAME_LENGTH': 200,
    'MAX_PARAMETER_DESCRIPTION_LENGTH': 1000,
    'MAX_HELP_TEXT_LENGTH': 500,
    
    # Configuration data limits
    'MAX_CONFIG_DATA_SIZE': 1024 * 1024,  # 1MB
    'MAX_CONFIG_KEYS': 1000,
    'MAX_CONFIG_VALUE_LENGTH': 10000,
    
    # Sync settings
    'DEFAULT_SYNC_TIMEOUT': 30,  # seconds
    'MAX_SYNC_RETRIES': 3,
    'SYNC_BATCH_SIZE': 100,
    
    # History and logging
    'MAX_HISTORY_ENTRIES': 1000,
    'MAX_SYNC_LOG_ENTRIES': 500,
    'HISTORY_RETENTION_DAYS': 365,
    
    # Export settings
    'MAX_EXPORT_RECORDS': 10000,
    'SUPPORTED_EXPORT_FORMATS': ['json', 'csv', 'xml'],
    
    # Security settings
    'ALLOWED_IP_RANGES': [],
    'REQUIRE_IP_LOGGING': True,
    'ENABLE_AUDIT_TRAIL': True,
}

# Device Type Categories
DEVICE_CATEGORIES = {
    'SENSOR': 'sensor',
    'MONITOR': 'monitor',
    'CONTROLLER': 'controller',
    'GATEWAY': 'gateway',
    'ACTUATOR': 'actuator',
    'DISPLAY': 'display',
    'INPUT_DEVICE': 'input_device',
    'OUTPUT_DEVICE': 'output_device',
    'COMMUNICATION': 'communication',
    'STORAGE': 'storage',
}

# Parameter Type Definitions
PARAMETER_TYPES = {
    'STRING': 'string',
    'INTEGER': 'integer',
    'FLOAT': 'float',
    'BOOLEAN': 'boolean',
    'JSON': 'json',
    'ENUM': 'enum',
    'DATE': 'date',
    'TIME': 'time',
    'DATETIME': 'datetime',
    'FILE': 'file',
    'URL': 'url',
    'EMAIL': 'email',
    'PHONE': 'phone',
    'IP_ADDRESS': 'ip_address',
    'MAC_ADDRESS': 'mac_address',
    'HEX': 'hex',
    'BASE64': 'base64',
}

# Configuration Status Options
CONFIG_STATUS_OPTIONS = {
    'ACTIVE': 'active',
    'INACTIVE': 'inactive',
    'TESTING': 'testing',
    'MAINTENANCE': 'maintenance',
    'DEPRECATED': 'deprecated',
    'ARCHIVED': 'archived',
}

# Sync Status Options
SYNC_STATUS_OPTIONS = {
    'SUCCESS': 'success',
    'FAILED': 'failed',
    'PARTIAL': 'partial',
    'TIMEOUT': 'timeout',
    'IN_PROGRESS': 'in_progress',
    'CANCELLED': 'cancelled',
}

# Action Types for History Tracking
HISTORY_ACTION_TYPES = {
    'CREATED': 'created',
    'UPDATED': 'updated',
    'DELETED': 'deleted',
    'ACTIVATED': 'activated',
    'DEACTIVATED': 'deactivated',
    'SYNCED': 'synced',
    'EXPORTED': 'exported',
    'IMPORTED': 'imported',
    'VALIDATED': 'validated',
    'APPROVED': 'approved',
    'REJECTED': 'rejected',
}

# Validation Rules
VALIDATION_RULES = {
    'DEVICE_ID_PATTERN': r'^[a-zA-Z0-9_-]+$',
    'VERSION_PATTERN': r'^\d+\.\d+\.\d+$',
    'SERIAL_NUMBER_PATTERN': r'^[a-zA-Z0-9_-]+$',
    'IP_ADDRESS_PATTERN': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
    'MAC_ADDRESS_PATTERN': r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
    'EMAIL_PATTERN': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'URL_PATTERN': r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$',
}

# Error Messages
ERROR_MESSAGES = {
    'DEVICE_ID_EXISTS': 'Device ID already exists',
    'DEVICE_ID_INVALID': 'Device ID contains invalid characters',
    'VERSION_INVALID': 'Version format is invalid. Use format: X.Y.Z',
    'SERIAL_NUMBER_INVALID': 'Serial number contains invalid characters',
    'CONFIG_DATA_INVALID': 'Configuration data is invalid',
    'PARAMETER_REQUIRED': 'Required parameter is missing',
    'PARAMETER_VALUE_INVALID': 'Parameter value is invalid',
    'PARAMETER_CONSTRAINT_VIOLATION': 'Parameter value violates constraints',
    'DEVICE_TYPE_NOT_FOUND': 'Device type not found',
    'CONFIGURATION_NOT_FOUND': 'Device configuration not found',
    'SYNC_FAILED': 'Device synchronization failed',
    'EXPORT_FAILED': 'Configuration export failed',
    'IMPORT_FAILED': 'Configuration import failed',
    'VALIDATION_FAILED': 'Configuration validation failed',
    'PERMISSION_DENIED': 'Permission denied for this operation',
    'RATE_LIMIT_EXCEEDED': 'Rate limit exceeded',
    'TIMEOUT': 'Operation timed out',
    'NETWORK_ERROR': 'Network error occurred',
    'DEVICE_OFFLINE': 'Device is offline',
    'UNSUPPORTED_FORMAT': 'Unsupported format',
}

# Success Messages
SUCCESS_MESSAGES = {
    'DEVICE_CREATED': 'Device configuration created successfully',
    'DEVICE_UPDATED': 'Device configuration updated successfully',
    'DEVICE_DELETED': 'Device configuration deleted successfully',
    'DEVICE_SYNCED': 'Device configuration synchronized successfully',
    'DEVICE_EXPORTED': 'Device configuration exported successfully',
    'DEVICE_IMPORTED': 'Device configuration imported successfully',
    'DEVICE_VALIDATED': 'Device configuration validated successfully',
    'BULK_UPDATE_COMPLETED': 'Bulk update completed successfully',
    'TEMPLATE_CREATED': 'Configuration template created successfully',
    'TEMPLATE_APPLIED': 'Configuration template applied successfully',
}

# API Response Codes
API_RESPONSE_CODES = {
    'SUCCESS': 200,
    'CREATED': 201,
    'NO_CONTENT': 204,
    'BAD_REQUEST': 400,
    'UNAUTHORIZED': 401,
    'FORBIDDEN': 403,
    'NOT_FOUND': 404,
    'METHOD_NOT_ALLOWED': 405,
    'CONFLICT': 409,
    'UNPROCESSABLE_ENTITY': 422,
    'TOO_MANY_REQUESTS': 429,
    'INTERNAL_SERVER_ERROR': 500,
    'SERVICE_UNAVAILABLE': 503,
}

# Cache Keys
CACHE_KEYS = {
    'DEVICE_TYPE_LIST': 'device_config:device_types',
    'DEVICE_PARAMETERS': 'device_config:parameters:{device_type_id}',
    'DEVICE_CONFIG': 'device_config:config:{device_id}',
    'DEVICE_HISTORY': 'device_config:history:{device_id}',
    'SYNC_STATUS': 'device_config:sync:{device_id}',
    'VALIDATION_RULES': 'device_config:validation_rules',
}

# Cache Timeouts (in seconds)
CACHE_TIMEOUTS = {
    'DEVICE_TYPE_LIST': 3600,  # 1 hour
    'DEVICE_PARAMETERS': 1800,  # 30 minutes
    'DEVICE_CONFIG': 900,       # 15 minutes
    'DEVICE_HISTORY': 1800,     # 30 minutes
    'SYNC_STATUS': 300,         # 5 minutes
    'VALIDATION_RULES': 86400,  # 24 hours
}

# File Upload Settings
FILE_UPLOAD_SETTINGS = {
    'MAX_FILE_SIZE': 10 * 1024 * 1024,  # 10MB
    'ALLOWED_EXTENSIONS': ['.json', '.xml', '.csv', '.txt', '.yaml', '.yml'],
    'UPLOAD_DIR': 'device_configs/uploads/',
    'BACKUP_DIR': 'device_configs/backups/',
    'TEMP_DIR': 'device_configs/temp/',
}

# Notification Settings
NOTIFICATION_SETTINGS = {
    'ENABLE_EMAIL_NOTIFICATIONS': True,
    'ENABLE_SMS_NOTIFICATIONS': False,
    'ENABLE_PUSH_NOTIFICATIONS': True,
    'NOTIFICATION_TEMPLATES': {
        'DEVICE_CREATED': 'device_config/notifications/device_created.html',
        'DEVICE_UPDATED': 'device_config/notifications/device_updated.html',
        'DEVICE_SYNCED': 'device_config/notifications/device_synced.html',
        'SYNC_FAILED': 'device_config/notifications/sync_failed.html',
        'VALIDATION_FAILED': 'device_config/notifications/validation_failed.html',
    },
}

# Logging Configuration
LOGGING_CONFIG = {
    'LOGGER_NAME': 'device_config',
    'LOG_LEVEL': 'INFO',
    'LOG_FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'LOG_FILE': 'logs/device_config.log',
    'MAX_LOG_SIZE': 10 * 1024 * 1024,  # 10MB
    'BACKUP_COUNT': 5,
    'ENABLE_CONSOLE_LOGGING': True,
    'ENABLE_FILE_LOGGING': True,
}

# Performance Settings
PERFORMANCE_SETTINGS = {
    'ENABLE_DATABASE_OPTIMIZATION': True,
    'ENABLE_QUERY_CACHING': True,
    'ENABLE_RESULT_CACHING': True,
    'BATCH_SIZE': 100,
    'MAX_CONCURRENT_SYNCS': 10,
    'SYNC_TIMEOUT': 30,
    'QUERY_TIMEOUT': 10,
    'ENABLE_ASYNC_PROCESSING': True,
}

# Security Settings
SECURITY_SETTINGS = {
    'ENABLE_IP_WHITELISTING': False,
    'ENABLE_RATE_LIMITING': True,
    'ENABLE_CSRF_PROTECTION': True,
    'ENABLE_SQL_INJECTION_PROTECTION': True,
    'ENABLE_XSS_PROTECTION': True,
    'ENABLE_CONTENT_TYPE_VALIDATION': True,
    'MAX_LOGIN_ATTEMPTS': 5,
    'LOCKOUT_DURATION': 900,  # 15 minutes
    'SESSION_TIMEOUT': 3600,  # 1 hour
}

# Environment-specific overrides
def get_setting(key: str, default: Any = None) -> Any:
    """
    Get a configuration setting with environment-specific overrides.
    
    Args:
        key: The configuration key to retrieve
        default: Default value if key is not found
        
    Returns:
        The configuration value
    """
    # Check for environment-specific override
    env_key = f'DEVICE_CONFIG_{key.upper()}'
    if env_key in os.environ:
        return os.environ[env_key]
    
    # Check in Django settings
    django_key = f'DEVICE_CONFIG_{key.upper()}'
    if hasattr(settings, django_key):
        return getattr(settings, django_key)
    
    # Return from local settings
    return DEVICE_CONFIG_SETTINGS.get(key, default)


def get_cache_timeout(key: str) -> int:
    """Get cache timeout for a specific key."""
    return CACHE_TIMEOUTS.get(key, 300)  # Default 5 minutes


def get_error_message(key: str) -> str:
    """Get error message for a specific key."""
    return ERROR_MESSAGES.get(key, 'An unknown error occurred')


def get_success_message(key: str) -> str:
    """Get success message for a specific key."""
    return SUCCESS_MESSAGES.get(key, 'Operation completed successfully')


def is_feature_enabled(feature: str) -> bool:
    """Check if a specific feature is enabled."""
    feature_settings = {
        'notifications': NOTIFICATION_SETTINGS.get('ENABLE_EMAIL_NOTIFICATIONS', False),
        'caching': PERFORMANCE_SETTINGS.get('ENABLE_QUERY_CACHING', False),
        'async_processing': PERFORMANCE_SETTINGS.get('ENABLE_ASYNC_PROCESSING', False),
        'security': SECURITY_SETTINGS.get('ENABLE_RATE_LIMITING', False),
        'logging': LOGGING_CONFIG.get('ENABLE_FILE_LOGGING', False),
    }
    return feature_settings.get(feature, False)


def get_supported_formats() -> List[str]:
    """Get list of supported export/import formats."""
    return DEVICE_CONFIG_SETTINGS.get('SUPPORTED_EXPORT_FORMATS', ['json'])


def get_max_file_size() -> int:
    """Get maximum allowed file size for uploads."""
    return FILE_UPLOAD_SETTINGS.get('MAX_FILE_SIZE', 10 * 1024 * 1024)


def get_allowed_extensions() -> List[str]:
    """Get list of allowed file extensions."""
    return FILE_UPLOAD_SETTINGS.get('ALLOWED_EXTENSIONS', ['.json'])


# Configuration validation
def validate_configuration() -> Dict[str, Any]:
    """
    Validate the current configuration and return any issues.
    
    Returns:
        Dictionary containing validation results and any issues found
    """
    issues = []
    warnings = []
    
    # Check required settings
    required_settings = ['DEFAULT_VERSION', 'DEFAULT_STATUS', 'MAX_DEVICE_ID_LENGTH']
    for setting in required_settings:
        if not get_setting(setting):
            issues.append(f"Required setting '{setting}' is not configured")
    
    # Check file paths
    upload_dir = FILE_UPLOAD_SETTINGS.get('UPLOAD_DIR')
    if upload_dir and not os.path.exists(upload_dir):
        warnings.append(f"Upload directory '{upload_dir}' does not exist")
    
    # Check cache configuration
    if PERFORMANCE_SETTINGS.get('ENABLE_QUERY_CACHING') and not hasattr(settings, 'CACHES'):
        warnings.append("Query caching enabled but no cache backend configured")
    
    # Check security settings
    if SECURITY_SETTINGS.get('ENABLE_IP_WHITELISTING') and not SECURITY_SETTINGS.get('ALLOWED_IP_RANGES'):
        warnings.append("IP whitelisting enabled but no allowed IP ranges configured")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings,
        'settings_count': len(DEVICE_CONFIG_SETTINGS),
        'features_enabled': sum(is_feature_enabled(f) for f in ['notifications', 'caching', 'async_processing', 'security', 'logging'])
    }
