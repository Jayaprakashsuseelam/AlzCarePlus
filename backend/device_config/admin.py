from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    DeviceType, 
    DeviceConfiguration, 
    DeviceParameter, 
    DeviceConfigurationHistory, 
    DeviceSyncLog
)


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    """Admin interface for DeviceType model"""
    list_display = ['name', 'manufacturer', 'model_number', 'is_active', 'configurations_count', 'parameters_count', 'created_at']
    list_filter = ['is_active', 'manufacturer', 'created_at']
    search_fields = ['name', 'description', 'manufacturer', 'model_number']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'manufacturer', 'model_number')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def configurations_count(self, obj):
        """Display count of configurations for this device type"""
        count = obj.configurations.count()
        if count > 0:
            url = reverse('admin:device_config_deviceconfiguration_changelist') + f'?device_type__id__exact={obj.id}'
            return format_html('<a href="{}">{}</a>', url, count)
        return count
    configurations_count.short_description = 'Configurations'
    
    def parameters_count(self, obj):
        """Display count of parameters for this device type"""
        count = obj.parameters.count()
        if count > 0:
            url = reverse('admin:device_config_deviceparameter_changelist') + f'?device_type__id__exact={obj.id}'
            return format_html('<a href="{}">{}</a>', url, count)
        return count
    parameters_count.short_description = 'Parameters'


@admin.register(DeviceParameter)
class DeviceParameterAdmin(admin.ModelAdmin):
    """Admin interface for DeviceParameter model"""
    list_display = ['name', 'device_type', 'parameter_type', 'is_required', 'is_readonly', 'order', 'created_at']
    list_filter = ['parameter_type', 'is_required', 'is_readonly', 'device_type', 'created_at']
    search_fields = ['name', 'display_name', 'description', 'device_type__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['device_type__name', 'order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('device_type', 'name', 'display_name', 'parameter_type', 'description', 'help_text')
        }),
        ('Constraints', {
            'fields': ('default_value', 'min_value', 'max_value', 'allowed_values')
        }),
        ('Behavior', {
            'fields': ('is_required', 'is_readonly', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """Customize form based on parameter type"""
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.parameter_type == 'enum':
            form.base_fields['allowed_values'].help_text = 'Enter values as a JSON array, e.g., ["value1", "value2"]'
        return form


@admin.register(DeviceConfiguration)
class DeviceConfigurationAdmin(admin.ModelAdmin):
    """Admin interface for DeviceConfiguration model"""
    list_display = ['name', 'device_id', 'device_type', 'status', 'is_enabled', 'version', 'assigned_to', 'last_sync', 'created_at']
    list_filter = ['status', 'is_enabled', 'device_type', 'created_at', 'last_sync']
    search_fields = ['name', 'device_id', 'serial_number', 'description', 'device_type__name']
    readonly_fields = ['created_at', 'updated_at', 'last_sync']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'device_type', 'device_id', 'serial_number')
        }),
        ('Configuration Data', {
            'fields': ('config_data', 'version'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'is_enabled')
        }),
        ('User Associations', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_sync'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with related fields"""
        return super().get_queryset(request).select_related('device_type', 'created_by', 'assigned_to')
    
    def save_model(self, request, obj, form, change):
        """Set created_by user when creating new configuration"""
        if not change:  # New object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(DeviceConfigurationHistory)
class DeviceConfigurationHistoryAdmin(admin.ModelAdmin):
    """Admin interface for DeviceConfigurationHistory model"""
    list_display = ['device_config', 'action', 'changed_by', 'timestamp', 'ip_address']
    list_filter = ['action', 'timestamp', 'changed_by']
    search_fields = ['device_config__name', 'device_config__device_id', 'notes', 'changed_by__username']
    readonly_fields = ['timestamp', 'device_config', 'action', 'old_values', 'new_values', 'changed_fields', 'changed_by', 'ip_address']
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Change Information', {
            'fields': ('device_config', 'action', 'timestamp', 'changed_by', 'ip_address')
        }),
        ('Change Details', {
            'fields': ('old_values', 'new_values', 'changed_fields', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """History entries are created automatically, not manually"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """History entries should not be modified"""
        return False


@admin.register(DeviceSyncLog)
class DeviceSyncLogAdmin(admin.ModelAdmin):
    """Admin interface for DeviceSyncLog model"""
    list_display = ['device_config', 'sync_status', 'sync_started', 'duration_ms', 'device_ip', 'device_version']
    list_filter = ['sync_status', 'sync_started', 'device_ip']
    search_fields = ['device_config__name', 'device_config__device_id', 'error_message', 'device_ip']
    readonly_fields = ['sync_started', 'device_config', 'sync_status', 'data_sent', 'data_received', 'error_message', 'device_ip', 'device_version']
    ordering = ['-sync_started']
    
    fieldsets = (
        ('Sync Information', {
            'fields': ('device_config', 'sync_status', 'sync_started', 'sync_completed', 'duration_ms')
        }),
        ('Device Information', {
            'fields': ('device_ip', 'device_version')
        }),
        ('Sync Data', {
            'fields': ('data_sent', 'data_received', 'error_message'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Sync logs are created automatically, not manually"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Sync logs should not be modified"""
        return False
    
    def duration_display(self, obj):
        """Display duration in a readable format"""
        if obj.duration_ms:
            if obj.duration_ms < 1000:
                return f"{obj.duration_ms}ms"
            else:
                return f"{obj.duration_ms/1000:.2f}s"
        return "-"
    duration_display.short_description = 'Duration'


# Customize admin site
admin.site.site_header = "AlzCarePlus Device Configuration Admin"
admin.site.site_title = "Device Configuration Admin"
admin.site.index_title = "Device Configuration Management"
