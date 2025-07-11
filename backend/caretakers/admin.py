# caretakers/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Caretaker, CaretakerProfile, CaretakerPatientAssignment, CaretakerSchedule, CaretakerTask

@admin.register(Caretaker)
class CaretakerAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'professional_title', 'employment_status', 'is_active', 'date_joined']
    list_filter = ['employment_status', 'is_active', 'email_verified', 'background_check_verified', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'professional_title']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'phone', 'date_of_birth', 'gender')}),
        ('Professional Information', {'fields': ('professional_title', 'license_number', 'years_of_experience', 'specialization')}),
        ('Employment', {'fields': ('employment_status', 'hire_date', 'is_active')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Verification', {'fields': ('email_verified', 'background_check_verified', 'background_check_date')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

@admin.register(CaretakerProfile)
class CaretakerProfileAdmin(admin.ModelAdmin):
    list_display = ['caretaker', 'city', 'state', 'country', 'created_at']
    list_filter = ['country', 'state', 'created_at']
    search_fields = ['caretaker__email', 'caretaker__first_name', 'caretaker__last_name', 'city']
    ordering = ['-created_at']

@admin.register(CaretakerPatientAssignment)
class CaretakerPatientAssignmentAdmin(admin.ModelAdmin):
    list_display = ['caretaker', 'patient', 'assignment_type', 'assignment_date', 'is_active']
    list_filter = ['assignment_type', 'is_active', 'assignment_date']
    search_fields = ['caretaker__email', 'patient__email', 'caretaker__first_name', 'patient__first_name']
    ordering = ['-assignment_date']
    date_hierarchy = 'assignment_date'

@admin.register(CaretakerSchedule)
class CaretakerScheduleAdmin(admin.ModelAdmin):
    list_display = ['caretaker', 'date', 'start_time', 'end_time', 'schedule_type', 'is_available']
    list_filter = ['schedule_type', 'is_available', 'date']
    search_fields = ['caretaker__email', 'caretaker__first_name', 'caretaker__last_name']
    ordering = ['-date', 'start_time']
    date_hierarchy = 'date'

@admin.register(CaretakerTask)
class CaretakerTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'caretaker', 'patient', 'task_type', 'priority', 'status', 'scheduled_date']
    list_filter = ['task_type', 'priority', 'status', 'scheduled_date']
    search_fields = ['title', 'caretaker__email', 'patient__email', 'description']
    ordering = ['-scheduled_date', '-scheduled_time']
    date_hierarchy = 'scheduled_date'
    
    fieldsets = (
        ('Basic Information', {'fields': ('title', 'description', 'caretaker', 'patient')}),
        ('Task Details', {'fields': ('task_type', 'priority', 'status')}),
        ('Schedule', {'fields': ('scheduled_date', 'scheduled_time', 'completed_date')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at'] 