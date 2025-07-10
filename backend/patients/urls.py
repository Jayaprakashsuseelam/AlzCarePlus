# patients/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'patients', views.PatientViewSet)

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.patient_register, name='patient_register'),
    path('auth/login/', views.patient_login, name='patient_login'),
    path('auth/logout/', views.patient_logout, name='patient_logout'),
    path('auth/reset-password/', views.password_reset_request, name='password_reset_request'),
    
    # Patient profile endpoints
    path('profile/', views.patient_profile, name='patient_profile'),
    path('profile/update/', views.update_patient_profile, name='update_patient_profile'),
    
    # Dashboard endpoints
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('admin-dashboard/', views.dashboard_view, name='admin_dashboard'),
    
    # Include router URLs
    path('', include(router.urls)),
]
