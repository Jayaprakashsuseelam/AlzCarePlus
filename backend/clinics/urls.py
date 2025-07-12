# clinics/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.ClinicRegistrationView.as_view(), name='clinic-register'),
    path('login/', views.ClinicLoginView.as_view(), name='clinic-login'),
    
    # Profile
    path('profile/', views.ClinicProfileView.as_view(), name='clinic-profile'),
    
    # Dashboard
    path('dashboard/', views.ClinicDashboardView.as_view(), name='clinic-dashboard'),
    
    # Staff Management
    path('staff/', views.ClinicStaffView.as_view(), name='clinic-staff'),
    path('staff/<int:pk>/', views.ClinicStaffDetailView.as_view(), name='clinic-staff-detail'),
    
    # Patient Management
    path('patients/', views.ClinicPatientView.as_view(), name='clinic-patients'),
    path('patients/<int:pk>/', views.ClinicPatientDetailView.as_view(), name='clinic-patient-detail'),
    path('search-patients/', views.search_patients, name='search-patients'),
    
    # Appointment Management
    path('appointments/', views.AppointmentView.as_view(), name='clinic-appointments'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='clinic-appointment-detail'),
    path('appointments/<int:pk>/update/', views.AppointmentUpdateView.as_view(), name='clinic-appointment-update'),
    path('appointments/<int:appointment_id>/check-in/', views.check_in_appointment, name='check-in-appointment'),
    path('appointments/<int:appointment_id>/check-out/', views.check_out_appointment, name='check-out-appointment'),
    
    # Medical Records
    path('medical-records/', views.MedicalRecordView.as_view(), name='clinic-medical-records'),
    path('medical-records/<int:pk>/', views.MedicalRecordDetailView.as_view(), name='clinic-medical-record-detail'),
    
    # Schedule Management
    path('schedule/', views.ClinicScheduleView.as_view(), name='clinic-schedule'),
    path('schedule/<int:pk>/', views.ClinicScheduleDetailView.as_view(), name='clinic-schedule-detail'),
    
    # Statistics
    path('statistics/', views.clinic_statistics, name='clinic-statistics'),
] 