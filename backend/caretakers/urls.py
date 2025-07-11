# caretakers/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.CaretakerRegistrationView.as_view(), name='caretaker-register'),
    path('login/', views.CaretakerLoginView.as_view(), name='caretaker-login'),
    
    # Profile
    path('profile/', views.CaretakerProfileView.as_view(), name='caretaker-profile'),
    
    # Dashboard
    path('dashboard/', views.CaretakerDashboardView.as_view(), name='caretaker-dashboard'),
    
    # Patient Assignments
    path('assignments/', views.CaretakerPatientAssignmentView.as_view(), name='caretaker-assignments'),
    path('assignments/<int:pk>/', views.CaretakerPatientAssignmentDetailView.as_view(), name='caretaker-assignment-detail'),
    
    # Schedule
    path('schedule/', views.CaretakerScheduleView.as_view(), name='caretaker-schedule'),
    path('schedule/<int:pk>/', views.CaretakerScheduleDetailView.as_view(), name='caretaker-schedule-detail'),
    
    # Tasks
    path('tasks/', views.CaretakerTaskView.as_view(), name='caretaker-tasks'),
    path('tasks/<int:pk>/', views.CaretakerTaskDetailView.as_view(), name='caretaker-task-detail'),
    path('tasks/<int:pk>/update/', views.CaretakerTaskUpdateView.as_view(), name='caretaker-task-update'),
    
    # Additional endpoints
    path('patients/', views.caretaker_patients, name='caretaker-patients'),
    path('task-statistics/', views.caretaker_task_statistics, name='caretaker-task-statistics'),
] 