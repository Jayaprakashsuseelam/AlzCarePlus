from rest_framework import serializers
from .models import (
    DeviceType, 
    DeviceConfiguration, 
    DeviceParameter, 
    DeviceConfigurationHistory, 
    DeviceSyncLog
)


class DeviceTypeSerializer(serializers.ModelSerializer):
    """Serializer for DeviceType model"""
    configurations_count = serializers.SerializerMethodField()
    parameters_count = serializers.SerializerMethodField()

    class Meta:
        model = DeviceType
        fields = [
            'id', 'name', 'description', 'manufacturer', 'model_number',
            'is_active', 'created_at', 'updated_at', 'configurations_count', 'parameters_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_configurations_count(self, obj):
        return obj.configurations.count()

    def get_parameters_count(self, obj):
        return obj.parameters.count()


class DeviceParameterSerializer(serializers.ModelSerializer):
    """Serializer for DeviceParameter model"""
    device_type_name = serializers.CharField(source='device_type.name', read_only=True)

    class Meta:
        model = DeviceParameter
        fields = [
            'id', 'device_type', 'device_type_name', 'name', 'display_name',
            'parameter_type', 'default_value', 'min_value', 'max_value',
            'allowed_values', 'is_required', 'is_readonly', 'description',
            'help_text', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate parameter constraints"""
        if data.get('parameter_type') == 'enum' and not data.get('allowed_values'):
            raise serializers.ValidationError("Enum parameters must have allowed values")
        
        if data.get('min_value') is not None and data.get('max_value') is not None:
            if data['min_value'] >= data['max_value']:
                raise serializers.ValidationError("min_value must be less than max_value")
        
        return data


class DeviceConfigurationSerializer(serializers.ModelSerializer):
    """Serializer for DeviceConfiguration model"""
    device_type_name = serializers.CharField(source='device_type.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    
    # Nested serialization for related data
    device_type = DeviceTypeSerializer(read_only=True)
    
    class Meta:
        model = DeviceConfiguration
        fields = [
            'id', 'device_type', 'device_type_name', 'name', 'description',
            'device_id', 'serial_number', 'config_data', 'status', 'is_enabled',
            'created_by', 'created_by_username', 'assigned_to', 'assigned_to_username',
            'created_at', 'updated_at', 'last_sync', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_sync']

    def validate_device_id(self, value):
        """Ensure device_id is unique"""
        if DeviceConfiguration.objects.filter(device_id=value).exists():
            raise serializers.ValidationError("Device ID must be unique")
        return value

    def validate_config_data(self, value):
        """Validate configuration data structure"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Configuration data must be a dictionary")
        return value


class DeviceConfigurationDetailSerializer(DeviceConfigurationSerializer):
    """Detailed serializer for DeviceConfiguration with full parameter validation"""
    parameters = DeviceParameterSerializer(source='device_type.parameters', many=True, read_only=True)
    validation_errors = serializers.SerializerMethodField()

    class Meta(DeviceConfigurationSerializer.Meta):
        fields = DeviceConfigurationSerializer.Meta.fields + ['parameters', 'validation_errors']

    def get_validation_errors(self, obj):
        """Get validation errors for the current configuration"""
        errors = []
        if not obj.device_type:
            return errors
        
        for param in obj.device_type.parameters.all():
            if param.is_required and param.name not in obj.config_data:
                errors.append(f"Required parameter '{param.display_name}' is missing")
            elif param.name in obj.config_data:
                is_valid, error_msg = param.validate_value(obj.config_data[param.name])
                if not is_valid:
                    errors.append(f"Parameter '{param.display_name}': {error_msg}")
        
        return errors


class DeviceConfigurationHistorySerializer(serializers.ModelSerializer):
    """Serializer for DeviceConfigurationHistory model"""
    device_config_name = serializers.CharField(source='device_config.name', read_only=True)
    changed_by_username = serializers.CharField(source='changed_by.username', read_only=True)

    class Meta:
        model = DeviceConfigurationHistory
        fields = [
            'id', 'device_config', 'device_config_name', 'action', 'old_values',
            'new_values', 'changed_fields', 'changed_by', 'changed_by_username',
            'timestamp', 'notes', 'ip_address'
        ]
        read_only_fields = ['id', 'timestamp']


class DeviceSyncLogSerializer(serializers.ModelSerializer):
    """Serializer for DeviceSyncLog model"""
    device_config_name = serializers.CharField(source='device_config.name', read_only=True)

    class Meta:
        model = DeviceSyncLog
        fields = [
            'id', 'device_config', 'device_config_name', 'sync_status',
            'sync_started', 'sync_completed', 'duration_ms', 'data_sent',
            'data_received', 'error_message', 'device_ip', 'device_version'
        ]
        read_only_fields = ['id', 'sync_started']


class DeviceConfigurationBulkUpdateSerializer(serializers.Serializer):
    """Serializer for bulk updating device configurations"""
    device_ids = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of device IDs to update"
    )
    config_updates = serializers.DictField(
        help_text="Configuration updates to apply to all devices"
    )
    force_update = serializers.BooleanField(
        default=False,
        help_text="Force update even if validation fails"
    )

    def validate_device_ids(self, value):
        """Validate that all device IDs exist"""
        existing_ids = DeviceConfiguration.objects.filter(device_id__in=value).values_list('device_id', flat=True)
        missing_ids = set(value) - set(existing_ids)
        
        if missing_ids:
            raise serializers.ValidationError(f"Device IDs not found: {', '.join(missing_ids)}")
        
        return value


class DeviceConfigurationTemplateSerializer(serializers.Serializer):
    """Serializer for creating device configuration templates"""
    template_name = serializers.CharField(max_length=200)
    device_type_id = serializers.IntegerField()
    config_template = serializers.DictField()
    description = serializers.CharField(required=False, allow_blank=True)
    
    def validate_device_type_id(self, value):
        """Validate that device type exists"""
        try:
            DeviceType.objects.get(id=value)
        except DeviceType.DoesNotExist:
            raise serializers.ValidationError("Device type does not exist")
        return value


class DeviceConfigurationExportSerializer(serializers.Serializer):
    """Serializer for exporting device configurations"""
    device_ids = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Specific device IDs to export (if not provided, exports all)"
    )
    include_history = serializers.BooleanField(default=False)
    include_sync_logs = serializers.BooleanField(default=False)
    format = serializers.ChoiceField(
        choices=['json', 'csv', 'xml'],
        default='json'
    )
