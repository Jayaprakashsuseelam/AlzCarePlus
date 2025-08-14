from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import json

User = get_user_model()


class DeviceType(models.Model):
    """Model for different types of devices that can be configured"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Device Type'
        verbose_name_plural = 'Device Types'

    def __str__(self):
        return f"{self.manufacturer} {self.name} - {self.model_number}"


class DeviceConfiguration(models.Model):
    """Model for storing device-specific configuration data"""
    CONFIG_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('testing', 'Testing'),
        ('maintenance', 'Maintenance'),
    ]

    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name='configurations')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Device identification
    device_id = models.CharField(max_length=100, unique=True)
    serial_number = models.CharField(max_length=100, blank=True)
    
    # Configuration data stored as JSON
    config_data = models.JSONField(default=dict)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=CONFIG_STATUS_CHOICES, default='active')
    is_enabled = models.BooleanField(default=True)
    
    # User associations
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_device_configs')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_device_configs')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    
    # Version control
    version = models.CharField(max_length=20, default='1.0.0')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Device Configuration'
        verbose_name_plural = 'Device Configurations'
        unique_together = ['device_id', 'version']

    def __str__(self):
        return f"{self.name} ({self.device_id}) - v{self.version}"

    def get_config_value(self, key, default=None):
        """Get a specific configuration value by key"""
        return self.config_data.get(key, default)

    def set_config_value(self, key, value):
        """Set a specific configuration value"""
        self.config_data[key] = value
        self.save()


class DeviceParameter(models.Model):
    """Model for defining configurable parameters for device types"""
    PARAMETER_TYPE_CHOICES = [
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
        ('enum', 'Enumeration'),
    ]

    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name='parameters')
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=200)
    parameter_type = models.CharField(max_length=20, choices=PARAMETER_TYPE_CHOICES)
    
    # Parameter constraints
    default_value = models.TextField(blank=True)
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    allowed_values = models.JSONField(default=list, blank=True)  # For enum types
    
    # Validation and UI
    is_required = models.BooleanField(default=False)
    is_readonly = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    help_text = models.TextField(blank=True)
    
    # Ordering
    order = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Device Parameter'
        verbose_name_plural = 'Device Parameters'
        unique_together = ['device_type', 'name']

    def __str__(self):
        return f"{self.device_type.name} - {self.display_name}"

    def validate_value(self, value):
        """Validate a parameter value based on type and constraints"""
        if self.parameter_type == 'integer':
            try:
                int_val = int(value)
                if self.min_value is not None and int_val < self.min_value:
                    return False, f"Value must be at least {self.min_value}"
                if self.max_value is not None and int_val > self.max_value:
                    return False, f"Value must be at most {self.max_value}"
                return True, None
            except (ValueError, TypeError):
                return False, "Value must be an integer"
        
        elif self.parameter_type == 'float':
            try:
                float_val = float(value)
                if self.min_value is not None and float_val < self.min_value:
                    return False, f"Value must be at least {self.min_value}"
                if self.max_value is not None and float_val > self.max_value:
                    return False, f"Value must be at most {self.max_value}"
                return True, None
            except (ValueError, TypeError):
                return False, "Value must be a number"
        
        elif self.parameter_type == 'boolean':
            if value not in [True, False, 'true', 'false', '1', '0']:
                return False, "Value must be a boolean"
            return True, None
        
        elif self.parameter_type == 'enum':
            if value not in self.allowed_values:
                return False, f"Value must be one of: {', '.join(map(str, self.allowed_values))}"
            return True, None
        
        return True, None


class DeviceConfigurationHistory(models.Model):
    """Model for tracking changes to device configurations"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('activated', 'Activated'),
        ('deactivated', 'Deactivated'),
        ('synced', 'Synced'),
    ]

    device_config = models.ForeignKey(DeviceConfiguration, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    
    # Change details
    old_values = models.JSONField(default=dict, blank=True)
    new_values = models.JSONField(default=dict, blank=True)
    changed_fields = models.JSONField(default=list, blank=True)
    
    # User who made the change
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Device Configuration History'
        verbose_name_plural = 'Device Configuration History'

    def __str__(self):
        return f"{self.device_config.name} - {self.action} at {self.timestamp}"


class DeviceSyncLog(models.Model):
    """Model for logging device synchronization activities"""
    SYNC_STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('partial', 'Partial Success'),
        ('timeout', 'Timeout'),
    ]

    device_config = models.ForeignKey(DeviceConfiguration, on_delete=models.CASCADE, related_name='sync_logs')
    sync_status = models.CharField(max_length=20, choices=SYNC_STATUS_CHOICES)
    
    # Sync details
    sync_started = models.DateTimeField(auto_now_add=True)
    sync_completed = models.DateTimeField(null=True, blank=True)
    duration_ms = models.PositiveIntegerField(null=True, blank=True)
    
    # Results
    data_sent = models.JSONField(default=dict, blank=True)
    data_received = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    
    # Device info
    device_ip = models.GenericIPAddressField(null=True, blank=True)
    device_version = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-sync_started']
        verbose_name = 'Device Sync Log'
        verbose_name_plural = 'Device Sync Logs'

    def __str__(self):
        return f"{self.device_config.name} - {self.sync_status} at {self.sync_started}"
