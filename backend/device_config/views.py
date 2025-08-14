from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
import csv
from io import StringIO

from .models import (
    DeviceType, 
    DeviceConfiguration, 
    DeviceParameter, 
    DeviceConfigurationHistory, 
    DeviceSyncLog
)
from .serializers import (
    DeviceTypeSerializer,
    DeviceConfigurationSerializer,
    DeviceConfigurationDetailSerializer,
    DeviceParameterSerializer,
    DeviceConfigurationHistorySerializer,
    DeviceSyncLogSerializer,
    DeviceConfigurationBulkUpdateSerializer,
    DeviceConfigurationTemplateSerializer,
    DeviceConfigurationExportSerializer
)


class DeviceTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing device types"""
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = DeviceType.objects.all()
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by manufacturer
        manufacturer = self.request.query_params.get('manufacturer', None)
        if manufacturer:
            queryset = queryset.filter(manufacturer__icontains=manufacturer)
        
        return queryset

    @action(detail=True, methods=['get'])
    def configurations(self, request, pk=None):
        """Get all configurations for a specific device type"""
        device_type = self.get_object()
        configurations = device_type.configurations.all()
        serializer = DeviceConfigurationSerializer(configurations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def parameters(self, request, pk=None):
        """Get all parameters for a specific device type"""
        device_type = self.get_object()
        parameters = device_type.parameters.all()
        serializer = DeviceParameterSerializer(parameters, many=True)
        return Response(serializer.data)


class DeviceParameterViewSet(viewsets.ModelViewSet):
    """ViewSet for managing device parameters"""
    queryset = DeviceParameter.objects.all()
    serializer_class = DeviceParameterSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = DeviceParameter.objects.all()
        
        # Filter by device type
        device_type_id = self.request.query_params.get('device_type', None)
        if device_type_id:
            queryset = queryset.filter(device_type_id=device_type_id)
        
        # Filter by parameter type
        parameter_type = self.request.query_params.get('type', None)
        if parameter_type:
            queryset = queryset.filter(parameter_type=parameter_type)
        
        return queryset


class DeviceConfigurationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing device configurations"""
    queryset = DeviceConfiguration.objects.all()
    serializer_class = DeviceConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve actions"""
        if self.action == 'retrieve':
            return DeviceConfigurationDetailSerializer
        return DeviceConfigurationSerializer
    
    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = DeviceConfiguration.objects.all()
        
        # Filter by device type
        device_type_id = self.request.query_params.get('device_type', None)
        if device_type_id:
            queryset = queryset.filter(device_type_id=device_type_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by enabled status
        is_enabled = self.request.query_params.get('is_enabled', None)
        if is_enabled is not None:
            queryset = queryset.filter(is_enabled=is_enabled.lower() == 'true')
        
        # Filter by assigned user
        assigned_to = self.request.query_params.get('assigned_to', None)
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        
        return queryset

    def perform_create(self, serializer):
        """Create device configuration with history tracking"""
        with transaction.atomic():
            device_config = serializer.save(created_by=self.request.user)
            
            # Create history entry
            DeviceConfigurationHistory.objects.create(
                device_config=device_config,
                action='created',
                new_values=serializer.data,
                changed_by=self.request.user,
                ip_address=self.get_client_ip()
            )

    def perform_update(self, serializer):
        """Update device configuration with history tracking"""
        with transaction.atomic():
            old_values = DeviceConfigurationSerializer(self.get_object()).data
            device_config = serializer.save()
            
            # Create history entry
            DeviceConfigurationHistory.objects.create(
                device_config=device_config,
                action='updated',
                old_values=old_values,
                new_values=serializer.data,
                changed_fields=list(set(old_values.keys()) - set(serializer.data.keys())),
                changed_by=self.request.user,
                ip_address=self.get_client_ip()
            )

    def perform_destroy(self, instance):
        """Delete device configuration with history tracking"""
        with transaction.atomic():
            old_values = DeviceConfigurationSerializer(instance).data
            
            # Create history entry before deletion
            DeviceConfigurationHistory.objects.create(
                device_config=instance,
                action='deleted',
                old_values=old_values,
                changed_by=self.request.user,
                ip_address=self.get_client_ip()
            )
            
            instance.delete()

    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        """Sync device configuration with the actual device"""
        device_config = self.get_object()
        
        try:
            # Simulate device sync (in real implementation, this would communicate with the device)
            sync_started = timezone.now()
            
            # Create sync log entry
            sync_log = DeviceSyncLog.objects.create(
                device_config=device_config,
                sync_status='success',
                sync_started=sync_started,
                sync_completed=timezone.now(),
                duration_ms=100,  # Simulated duration
                data_sent=device_config.config_data,
                data_received={'status': 'synced', 'timestamp': timezone.now().isoformat()},
                device_ip=request.META.get('REMOTE_ADDR'),
                device_version=device_config.version
            )
            
            # Update last sync timestamp
            device_config.last_sync = sync_started
            device_config.save()
            
            return Response({
                'status': 'success',
                'message': 'Device configuration synced successfully',
                'sync_log_id': sync_log.id
            })
            
        except Exception as e:
            # Create failed sync log entry
            DeviceSyncLog.objects.create(
                device_config=device_config,
                sync_status='failed',
                sync_started=timezone.now(),
                error_message=str(e),
                device_ip=request.META.get('REMOTE_ADDR')
            )
            
            return Response({
                'status': 'error',
                'message': f'Sync failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Bulk update multiple device configurations"""
        serializer = DeviceConfigurationBulkUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        device_ids = serializer.validated_data['device_ids']
        config_updates = serializer.validated_data['config_updates']
        force_update = serializer.validated_data['force_update']
        
        updated_count = 0
        errors = []
        
        with transaction.atomic():
            for device_id in device_ids:
                try:
                    device_config = DeviceConfiguration.objects.get(device_id=device_id)
                    
                    # Validate updates if not forcing
                    if not force_update:
                        # Here you would add validation logic
                        pass
                    
                    # Update configuration data
                    device_config.config_data.update(config_updates)
                    device_config.save()
                    
                    # Create history entry
                    DeviceConfigurationHistory.objects.create(
                        device_config=device_config,
                        action='updated',
                        new_values=DeviceConfigurationSerializer(device_config).data,
                        changed_fields=list(config_updates.keys()),
                        changed_by=request.user,
                        ip_address=self.get_client_ip()
                    )
                    
                    updated_count += 1
                    
                except DeviceConfiguration.DoesNotExist:
                    errors.append(f"Device {device_id} not found")
                except Exception as e:
                    errors.append(f"Error updating device {device_id}: {str(e)}")
        
        return Response({
            'updated_count': updated_count,
            'errors': errors,
            'message': f'Successfully updated {updated_count} devices'
        })

    @action(detail=False, methods=['post'])
    def export(self, request):
        """Export device configurations"""
        serializer = DeviceConfigurationExportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        device_ids = serializer.validated_data.get('device_ids')
        include_history = serializer.validated_data.get('include_history', False)
        include_sync_logs = serializer.validated_data.get('include_sync_logs', False)
        export_format = serializer.validated_data.get('format', 'json')
        
        # Get configurations to export
        if device_ids:
            configurations = DeviceConfiguration.objects.filter(device_id__in=device_ids)
        else:
            configurations = DeviceConfiguration.objects.all()
        
        if export_format == 'json':
            data = DeviceConfigurationSerializer(configurations, many=True).data
            
            if include_history:
                for config_data in data:
                    config_obj = configurations.get(id=config_data['id'])
                    config_data['history'] = DeviceConfigurationHistorySerializer(
                        config_obj.history.all(), many=True
                    ).data
            
            if include_sync_logs:
                for config_data in data:
                    config_obj = configurations.get(id=config_data['id'])
                    config_data['sync_logs'] = DeviceSyncLogSerializer(
                        config_obj.sync_logs.all(), many=True
                    ).data
            
            return Response(data)
        
        elif export_format == 'csv':
            # Generate CSV export
            output = StringIO()
            writer = csv.writer(output)
            
            # Write headers
            headers = ['Device ID', 'Name', 'Device Type', 'Status', 'Version', 'Created At']
            writer.writerow(headers)
            
            # Write data
            for config in configurations:
                writer.writerow([
                    config.device_id,
                    config.name,
                    config.device_type.name if config.device_type else '',
                    config.status,
                    config.version,
                    config.created_at.strftime('%Y-%m-%d %H:%M:%S')
                ])
            
            output.seek(0)
            response = Response(output.getvalue())
            response['Content-Type'] = 'text/csv'
            response['Content-Disposition'] = 'attachment; filename="device_configurations.csv"'
            return response
        
        else:
            return Response(
                {'error': 'Unsupported export format'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_client_ip(self):
        """Get client IP address from request"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class DeviceConfigurationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing device configuration history (read-only)"""
    queryset = DeviceConfigurationHistory.objects.all()
    serializer_class = DeviceConfigurationHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = DeviceConfigurationHistory.objects.all()
        
        # Filter by device configuration
        device_config_id = self.request.query_params.get('device_config', None)
        if device_config_id:
            queryset = queryset.filter(device_config_id=device_config_id)
        
        # Filter by action
        action_filter = self.request.query_params.get('action', None)
        if action_filter:
            queryset = queryset.filter(action=action_filter)
        
        # Filter by user who made the change
        changed_by = self.request.query_params.get('changed_by', None)
        if changed_by:
            queryset = queryset.filter(changed_by_id=changed_by)
        
        return queryset


class DeviceSyncLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing device sync logs (read-only)"""
    queryset = DeviceSyncLog.objects.all()
    serializer_class = DeviceSyncLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = DeviceSyncLog.objects.all()
        
        # Filter by device configuration
        device_config_id = self.request.query_params.get('device_config', None)
        if device_config_id:
            queryset = queryset.filter(device_config_id=device_config_id)
        
        # Filter by sync status
        sync_status = self.request.query_params.get('sync_status', None)
        if sync_status:
            queryset = queryset.filter(sync_status=sync_status)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            queryset = queryset.filter(sync_started__date__gte=start_date)
        
        end_date = self.request.query_params.get('end_date', None)
        if end_date:
            queryset = queryset.filter(sync_started__date__lte=end_date)
        
        return queryset
