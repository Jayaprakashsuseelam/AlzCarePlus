# patients/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'patients', views.PatientViewSet)
router.register(r'medical-records', views.MedicalRecordViewSet, basename='medical-record')
router.register(r'medications', views.MedicationViewSet, basename='medication')
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')
router.register(r'care-plans', views.CarePlanViewSet, basename='care-plan')
router.register(r'health-goals', views.HealthGoalViewSet, basename='health-goal')
router.register(r'vital-signs', views.VitalSignsViewSet, basename='vital-sign')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.patient_register, name='patient_register'),
    path('auth/login/', views.patient_login, name='patient_login'),
    path('auth/logout/', views.patient_logout, name='patient_logout'),
    path('auth/reset-password/', views.password_reset_request, name='password_reset_request'),
    
    # Patient profile endpoints
    path('profile/', views.patient_profile, name='patient_profile'),
    path('profile/update/', views.update_patient_profile, name='update_patient_profile'),
    path('profile/details/', views.patient_profile_details, name='patient_profile_details'),
    
    # Dashboard endpoints
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('admin-dashboard/', views.dashboard_view, name='admin_dashboard'),
    
    # Medical Records endpoints
    path('medical-records/filtered/', views.medical_records_filtered, name='medical_records_filtered'),
    
    # Medication endpoints
    path('medications/by-status/', views.medications_by_status, name='medications_by_status'),
    
    # Appointment endpoints
    path('appointments/filtered/', views.appointments_filtered, name='appointments_filtered'),
    
    # Health Goals endpoints
    path('health-goals/<int:goal_id>/progress/', views.update_goal_progress, name='update_goal_progress'),
    
    # Vital Signs endpoints
    path('vital-signs/trends/', views.vital_signs_trends, name='vital_signs_trends'),
    
    # Search and Export endpoints
    path('search/', views.search_patients, name='search_patients'),
    path('export/', views.export_patient_data, name='export_patient_data'),
    
    # Include router URLs
    path('', include(router.urls)),
]
