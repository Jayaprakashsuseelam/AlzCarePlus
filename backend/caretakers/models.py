# caretakers/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from patients.models import Patient
import uuid

class Caretaker(AbstractUser):
    # Override username to use email
    username = None
    email = models.EmailField(unique=True)
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=20,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer-not-to-say', 'Prefer not to say')
        ],
        blank=True,
        null=True
    )
    
    # Professional Information
    professional_title = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    
    # Employment Information
    employment_status = models.CharField(
        max_length=20,
        choices=[
            ('full-time', 'Full Time'),
            ('part-time', 'Part Time'),
            ('contract', 'Contract'),
            ('volunteer', 'Volunteer'),
            ('private', 'Private Practice')
        ],
        default='full-time'
    )
    hire_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Account Information
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    # Verification
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    background_check_verified = models.BooleanField(default=False)
    background_check_date = models.DateField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs):
        # Hash password if it's not already hashed
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class CaretakerProfile(models.Model):
    caretaker = models.OneToOneField(Caretaker, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='caretaker_profiles/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, default='United States')
    
    # Professional Details
    bio = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    languages_spoken = models.CharField(max_length=200, blank=True, null=True)
    
    # Availability
    availability_schedule = models.JSONField(default=dict, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.caretaker.full_name}"

class CaretakerPatientAssignment(models.Model):
    caretaker = models.ForeignKey(Caretaker, on_delete=models.CASCADE, related_name='patient_assignments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='caretaker_assignments')
    assignment_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Assignment Details
    assignment_type = models.CharField(
        max_length=20,
        choices=[
            ('primary', 'Primary Caretaker'),
            ('secondary', 'Secondary Caretaker'),
            ('temporary', 'Temporary Caretaker'),
            ('specialist', 'Specialist Caretaker')
        ],
        default='primary'
    )
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['caretaker', 'patient', 'is_active']
        ordering = ['-assignment_date']

    def __str__(self):
        return f"{self.caretaker.full_name} - {self.patient.full_name} ({self.assignment_type})"

class CaretakerSchedule(models.Model):
    caretaker = models.ForeignKey(Caretaker, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    # Schedule Details
    schedule_type = models.CharField(
        max_length=20,
        choices=[
            ('regular', 'Regular Shift'),
            ('overtime', 'Overtime'),
            ('on-call', 'On Call'),
            ('emergency', 'Emergency'),
            ('vacation', 'Vacation'),
            ('sick', 'Sick Leave')
        ],
        default='regular'
    )
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['caretaker', 'date', 'start_time']
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.caretaker.full_name} - {self.date} ({self.start_time}-{self.end_time})"

class CaretakerTask(models.Model):
    caretaker = models.ForeignKey(Caretaker, on_delete=models.CASCADE, related_name='tasks')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='caretaker_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Task Details
    task_type = models.CharField(
        max_length=20,
        choices=[
            ('medication', 'Medication'),
            ('hygiene', 'Hygiene'),
            ('feeding', 'Feeding'),
            ('exercise', 'Exercise'),
            ('monitoring', 'Monitoring'),
            ('appointment', 'Appointment'),
            ('emergency', 'Emergency'),
            ('other', 'Other')
        ],
        default='other'
    )
    
    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent')
        ],
        default='medium'
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField(blank=True, null=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date', '-scheduled_time']

    def __str__(self):
        return f"{self.title} - {self.caretaker.full_name} for {self.patient.full_name}" 