from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'device-types', views.DeviceTypeViewSet, basename='device-type')
router.register(r'parameters', views.DeviceParameterViewSet, basename='device-parameter')
router.register(r'configurations', views.DeviceConfigurationViewSet, basename='device-configuration')
router.register(r'history', views.DeviceConfigurationHistoryViewSet, basename='device-configuration-history')
router.register(r'sync-logs', views.DeviceSyncLogViewSet, basename='device-sync-log')

app_name = 'device_config'

urlpatterns = [
    # Include router URLs
    path('api/', include(router.urls)),
    
    # Additional custom endpoints can be added here if needed
    path('api/health/', views.DeviceConfigurationViewSet.as_view({'get': 'list'}), name='health-check'),
]
