# clinics/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Clinic, ClinicProfile, ClinicStaff, ClinicPatient, Appointment, MedicalRecord, ClinicSchedule

@admin.register(Clinic)
class ClinicAdmin(UserAdmin):
    list_display = ['clinic_name', 'email', 'clinic_type', 'city', 'state', 'is_active', 'is_verified', 'date_joined']
    list_filter = ['clinic_type', 'is_active', 'is_verified', 'date_joined', 'state', 'city']
    search_fields = ['clinic_name', 'email', 'license_number', 'address']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Clinic Information', {'fields': ('clinic_name', 'clinic_type', 'phone', 'fax', 'website')}),
        ('Address', {'fields': ('address', 'city', 'state', 'zip_code', 'country')}),
        ('Business Information', {'fields': ('license_number', 'tax_id', 'npi_number', 'operating_hours')}),
        ('Status', {'fields': ('is_active', 'is_verified', 'verification_date')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'clinic_name', 'license_number'),
        }),
    )

@admin.register(ClinicProfile)
class ClinicProfileAdmin(admin.ModelAdmin):
    list_display = ['clinic', 'facility_type', 'total_rooms', 'total_beds', 'created_at']
    list_filter = ['facility_type', 'wheelchair_accessible', 'created_at']
    search_fields = ['clinic__clinic_name', 'description', 'specialties']
    ordering = ['-created_at']

@admin.register(ClinicStaff)
class ClinicStaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'clinic', 'staff_type', 'department', 'employee_id', 'is_active', 'hire_date']
    list_filter = ['staff_type', 'department', 'is_active', 'hire_date', 'clinic']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'employee_id', 'clinic__clinic_name']
    ordering = ['-hire_date']
    date_hierarchy = 'hire_date'

@admin.register(ClinicPatient)
class ClinicPatientAdmin(admin.ModelAdmin):
    list_display = ['patient', 'clinic', 'patient_number', 'registration_date', 'is_active', 'insurance_provider']
    list_filter = ['is_active', 'registration_date', 'clinic', 'insurance_provider']
    search_fields = ['patient__first_name', 'patient__last_name', 'patient_number', 'clinic__clinic_name']
    ordering = ['-registration_date']
    date_hierarchy = 'registration_date'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['appointment_number', 'patient', 'staff', 'clinic', 'appointment_type', 'scheduled_date', 'scheduled_time', 'status']
    list_filter = ['appointment_type', 'status', 'scheduled_date', 'clinic', 'department']
    search_fields = ['appointment_number', 'patient__patient__first_name', 'patient__patient__last_name', 'staff__user__first_name']
    ordering = ['-scheduled_date', '-scheduled_time']
    date_hierarchy = 'scheduled_date'
    
    fieldsets = (
        ('Basic Information', {'fields': ('appointment_number', 'clinic', 'patient', 'staff')}),
        ('Appointment Details', {'fields': ('appointment_type', 'scheduled_date', 'scheduled_time', 'duration', 'end_time')}),
        ('Status & Location', {'fields': ('status', 'room_number', 'department')}),
        ('Medical Information', {'fields': ('reason', 'diagnosis', 'treatment_plan', 'notes')}),
        ('Timestamps', {'fields': ('check_in_time', 'check_out_time', 'created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at', 'appointment_number', 'end_time']

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['title', 'patient', 'clinic', 'record_type', 'staff', 'created_at', 'access_level']
    list_filter = ['record_type', 'access_level', 'is_private', 'created_at', 'clinic']
    search_fields = ['title', 'patient__patient__first_name', 'patient__patient__last_name', 'staff__user__first_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {'fields': ('clinic', 'patient', 'staff', 'appointment')}),
        ('Record Details', {'fields': ('record_type', 'title', 'description', 'findings', 'diagnosis', 'treatment')}),
        ('Vital Signs', {'fields': ('blood_pressure', 'heart_rate', 'temperature', 'weight', 'height', 'oxygen_saturation')}),
        ('Prescriptions & Attachments', {'fields': ('prescriptions', 'attachments')}),
        ('Privacy', {'fields': ('is_private', 'access_level')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ClinicSchedule)
class ClinicScheduleAdmin(admin.ModelAdmin):
    list_display = ['staff', 'clinic', 'date', 'start_time', 'end_time', 'schedule_type', 'is_available']
    list_filter = ['schedule_type', 'is_available', 'date', 'clinic', 'department']
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'clinic__clinic_name']
    ordering = ['-date', 'start_time']
    date_hierarchy = 'date' 