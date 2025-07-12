# clinics/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from patients.models import Patient
from caretakers.models import Caretaker
import uuid
from datetime import datetime

class Clinic(AbstractUser):
    # Override username to use email
    username = None
    email = models.EmailField(unique=True)
    
    # Clinic Information
    clinic_name = models.CharField(max_length=200)
    clinic_type = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General Practice'),
            ('specialist', 'Specialist Clinic'),
            ('geriatric', 'Geriatric Care'),
            ('neurology', 'Neurology'),
            ('cardiology', 'Cardiology'),
            ('oncology', 'Oncology'),
            ('rehabilitation', 'Rehabilitation'),
            ('mental_health', 'Mental Health'),
            ('dental', 'Dental'),
            ('other', 'Other')
        ],
        default='general'
    )
    
    # Contact Information
    phone = models.CharField(max_length=20)
    fax = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Address Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='United States')
    
    # Business Information
    license_number = models.CharField(max_length=50, unique=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    npi_number = models.CharField(max_length=20, blank=True, null=True)  # National Provider Identifier
    
    # Operating Hours
    operating_hours = models.JSONField(default=dict)
    
    # Clinic Status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(blank=True, null=True)
    
    # Account Information
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['clinic_name', 'license_number']

    def __str__(self):
        return f"{self.clinic_name} ({self.email})"

    def save(self, *args, **kwargs):
        # Hash password if it's not already hashed
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class ClinicProfile(models.Model):
    clinic = models.OneToOneField(Clinic, on_delete=models.CASCADE, related_name='profile')
    logo = models.ImageField(upload_to='clinic_logos/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='clinic_banners/', blank=True, null=True)
    
    # Detailed Information
    description = models.TextField(blank=True, null=True)
    specialties = models.TextField(blank=True, null=True)
    services_offered = models.JSONField(default=list)
    insurance_accepted = models.JSONField(default=list)
    
    # Facility Information
    facility_type = models.CharField(
        max_length=50,
        choices=[
            ('outpatient', 'Outpatient Clinic'),
            ('inpatient', 'Inpatient Facility'),
            ('ambulatory', 'Ambulatory Care'),
            ('urgent_care', 'Urgent Care'),
            ('specialty_center', 'Specialty Center'),
            ('rehabilitation_center', 'Rehabilitation Center'),
            ('diagnostic_center', 'Diagnostic Center')
        ],
        default='outpatient'
    )
    
    # Capacity and Resources
    total_beds = models.IntegerField(default=0)
    total_rooms = models.IntegerField(default=0)
    parking_spaces = models.IntegerField(default=0)
    wheelchair_accessible = models.BooleanField(default=True)
    
    # Accreditation
    accreditations = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    
    # Emergency Information
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)
    after_hours_contact = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.clinic.clinic_name}"

class ClinicStaff(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='staff')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='clinic_employments')
    
    # Staff Information
    staff_type = models.CharField(
        max_length=50,
        choices=[
            ('doctor', 'Doctor'),
            ('nurse', 'Nurse'),
            ('receptionist', 'Receptionist'),
            ('administrator', 'Administrator'),
            ('technician', 'Technician'),
            ('therapist', 'Therapist'),
            ('pharmacist', 'Pharmacist'),
            ('other', 'Other')
        ]
    )
    
    # Employment Details
    employee_id = models.CharField(max_length=50, unique=True)
    hire_date = models.DateField()
    termination_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Professional Information
    license_number = models.CharField(max_length=50, blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    # Schedule
    work_schedule = models.JSONField(default=dict)
    
    # Permissions
    can_view_patients = models.BooleanField(default=False)
    can_edit_patients = models.BooleanField(default=False)
    can_view_records = models.BooleanField(default=False)
    can_edit_records = models.BooleanField(default=False)
    can_manage_appointments = models.BooleanField(default=False)
    can_manage_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['clinic', 'user', 'is_active']
        ordering = ['-hire_date']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.clinic.clinic_name} ({self.staff_type})"

class ClinicPatient(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='patients')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='clinics')
    
    # Registration Information
    registration_date = models.DateField(auto_now_add=True)
    patient_number = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    # Insurance Information
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    insurance_number = models.CharField(max_length=50, blank=True, null=True)
    insurance_group = models.CharField(max_length=50, blank=True, null=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)
    
    # Medical Information
    primary_care_physician = models.CharField(max_length=100, blank=True, null=True)
    referring_physician = models.CharField(max_length=100, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    
    # Notes
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['clinic', 'patient', 'is_active']
        ordering = ['-registration_date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.clinic.clinic_name}"

class Appointment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(ClinicPatient, on_delete=models.CASCADE, related_name='appointments')
    staff = models.ForeignKey(ClinicStaff, on_delete=models.CASCADE, related_name='appointments')
    
    # Appointment Details
    appointment_number = models.CharField(max_length=50, unique=True)
    appointment_type = models.CharField(
        max_length=50,
        choices=[
            ('consultation', 'Consultation'),
            ('follow_up', 'Follow-up'),
            ('emergency', 'Emergency'),
            ('routine_checkup', 'Routine Checkup'),
            ('procedure', 'Procedure'),
            ('therapy', 'Therapy'),
            ('diagnostic', 'Diagnostic Test'),
            ('vaccination', 'Vaccination'),
            ('other', 'Other')
        ]
    )
    
    # Schedule
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    duration = models.IntegerField(default=30)  # minutes
    end_time = models.TimeField(blank=True, null=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('confirmed', 'Confirmed'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show'),
            ('rescheduled', 'Rescheduled')
        ],
        default='scheduled'
    )
    
    # Location
    room_number = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    # Notes
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment_plan = models.TextField(blank=True, null=True)
    
    # Timestamps
    check_in_time = models.DateTimeField(blank=True, null=True)
    check_out_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date', '-scheduled_time']

    def __str__(self):
        return f"{self.appointment_number} - {self.patient.patient.full_name} ({self.scheduled_date})"

    def save(self, *args, **kwargs):
        if not self.end_time and self.scheduled_time and self.duration:
            from datetime import timedelta
            start_time = self.scheduled_time
            end_time = (datetime.combine(datetime.min, start_time) + timedelta(minutes=self.duration)).time()
            self.end_time = end_time
        super().save(*args, **kwargs)

class MedicalRecord(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='medical_records')
    patient = models.ForeignKey(ClinicPatient, on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='medical_records', blank=True, null=True)
    staff = models.ForeignKey(ClinicStaff, on_delete=models.CASCADE, related_name='medical_records')
    
    # Record Information
    record_type = models.CharField(
        max_length=50,
        choices=[
            ('vital_signs', 'Vital Signs'),
            ('physical_exam', 'Physical Examination'),
            ('lab_results', 'Laboratory Results'),
            ('imaging', 'Imaging Results'),
            ('medication', 'Medication Record'),
            ('procedure', 'Procedure Record'),
            ('progress_note', 'Progress Note'),
            ('discharge_summary', 'Discharge Summary'),
            ('allergy_record', 'Allergy Record'),
            ('immunization', 'Immunization Record'),
            ('other', 'Other')
        ]
    )
    
    # Record Details
    title = models.CharField(max_length=200)
    description = models.TextField()
    findings = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    prescriptions = models.JSONField(default=list)
    
    # Vital Signs
    blood_pressure = models.CharField(max_length=20, blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    oxygen_saturation = models.IntegerField(blank=True, null=True)
    
    # Attachments
    attachments = models.JSONField(default=list)  # File paths or URLs
    
    # Privacy
    is_private = models.BooleanField(default=False)
    access_level = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('staff', 'Staff Only'),
            ('doctor', 'Doctors Only'),
            ('private', 'Private')
        ],
        default='staff'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.patient.patient.full_name} ({self.created_at.date()})"

class ClinicSchedule(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='schedules')
    staff = models.ForeignKey(ClinicStaff, on_delete=models.CASCADE, related_name='clinic_schedules')
    
    # Schedule Information
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    # Schedule Type
    schedule_type = models.CharField(
        max_length=20,
        choices=[
            ('regular', 'Regular Hours'),
            ('overtime', 'Overtime'),
            ('on_call', 'On Call'),
            ('emergency', 'Emergency'),
            ('vacation', 'Vacation'),
            ('sick', 'Sick Leave'),
            ('holiday', 'Holiday'),
            ('training', 'Training'),
            ('meeting', 'Meeting')
        ],
        default='regular'
    )
    
    # Location
    department = models.CharField(max_length=100, blank=True, null=True)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Notes
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['clinic', 'staff', 'date', 'start_time']
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.staff.user.get_full_name()} - {self.date} ({self.start_time}-{self.end_time})" 