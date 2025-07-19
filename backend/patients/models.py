# patients/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
import uuid
from datetime import date

class Patient(AbstractUser):
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
    
    # Medical Information
    age = models.IntegerField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Account Information
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    # Verification
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs):
        # Hash password if it's not already hashed
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        
        # Calculate age if date of birth is provided
        if self.date_of_birth and not self.age:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class PatientProfile(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='patient_profiles/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, default='United States')
    
    # Health Information
    blood_type = models.CharField(
        max_length=5,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-')
        ],
        blank=True, null=True
    )
    allergies = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    
    # Care Information
    primary_care_physician = models.CharField(max_length=100, blank=True, null=True)
    specialist = models.CharField(max_length=100, blank=True, null=True)
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    insurance_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Additional Health Information
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in cm
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in kg
    bmi = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    
    # Lifestyle Information
    smoking_status = models.CharField(
        max_length=20,
        choices=[
            ('never', 'Never Smoked'),
            ('former', 'Former Smoker'),
            ('current', 'Current Smoker'),
            ('unknown', 'Unknown')
        ],
        default='unknown'
    )
    alcohol_consumption = models.CharField(
        max_length=20,
        choices=[
            ('none', 'None'),
            ('occasional', 'Occasional'),
            ('moderate', 'Moderate'),
            ('heavy', 'Heavy'),
            ('unknown', 'Unknown')
        ],
        default='unknown'
    )
    exercise_frequency = models.CharField(
        max_length=20,
        choices=[
            ('never', 'Never'),
            ('rarely', 'Rarely'),
            ('sometimes', 'Sometimes'),
            ('regularly', 'Regularly'),
            ('daily', 'Daily')
        ],
        default='never'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.patient.full_name}"

    def calculate_bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100  # Convert cm to meters
            self.bmi = self.weight / (height_m ** 2)
            return self.bmi
        return None

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    
    # Record Information
    record_type = models.CharField(
        max_length=50,
        choices=[
            ('vital_signs', 'Vital Signs'),
            ('lab_result', 'Laboratory Result'),
            ('imaging', 'Imaging Result'),
            ('medication', 'Medication Record'),
            ('procedure', 'Procedure Record'),
            ('progress_note', 'Progress Note'),
            ('discharge_summary', 'Discharge Summary'),
            ('allergy_record', 'Allergy Record'),
            ('immunization', 'Immunization Record'),
            ('cognitive_assessment', 'Cognitive Assessment'),
            ('other', 'Other')
        ]
    )
    
    # Record Details
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_recorded = models.DateField()
    recorded_by = models.CharField(max_length=100, blank=True, null=True)
    
    # Medical Details
    findings = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    
    # Vital Signs (if applicable)
    blood_pressure = models.CharField(max_length=20, blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    oxygen_saturation = models.IntegerField(blank=True, null=True)
    
    # Cognitive Assessment (if applicable)
    mmse_score = models.IntegerField(blank=True, null=True)  # Mini-Mental State Examination
    clock_drawing_score = models.IntegerField(blank=True, null=True)
    memory_score = models.IntegerField(blank=True, null=True)
    
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
        ordering = ['-date_recorded', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.patient.full_name} ({self.date_recorded})"

class Medication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medications')
    
    # Medication Information
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True, null=True)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    route = models.CharField(
        max_length=20,
        choices=[
            ('oral', 'Oral'),
            ('injection', 'Injection'),
            ('topical', 'Topical'),
            ('inhalation', 'Inhalation'),
            ('other', 'Other')
        ],
        default='oral'
    )
    
    # Prescription Details
    prescribed_by = models.CharField(max_length=100, blank=True, null=True)
    prescription_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('discontinued', 'Discontinued'),
            ('completed', 'Completed'),
            ('on_hold', 'On Hold')
        ],
        default='active'
    )
    
    # Instructions
    instructions = models.TextField(blank=True, null=True)
    side_effects = models.TextField(blank=True, null=True)
    contraindications = models.TextField(blank=True, null=True)
    
    # Refill Information
    refills_remaining = models.IntegerField(default=0)
    pharmacy = models.CharField(max_length=200, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-prescription_date']

    def __str__(self):
        return f"{self.name} - {self.patient.full_name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    
    # Appointment Details
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
            ('cognitive_assessment', 'Cognitive Assessment'),
            ('other', 'Other')
        ]
    )
    
    # Schedule
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    duration = models.IntegerField(default=30)  # minutes
    end_time = models.TimeField(blank=True, null=True)
    
    # Healthcare Provider
    doctor_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, blank=True, null=True)
    clinic_name = models.CharField(max_length=200, blank=True, null=True)
    
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
        return f"{self.appointment_type} - {self.patient.full_name} ({self.scheduled_date})"

    def save(self, *args, **kwargs):
        # Calculate end time if not provided
        if not self.end_time and self.scheduled_time:
            from datetime import timedelta
            start_time = self.scheduled_time
            end_time = (date.today() + timedelta(minutes=self.duration)).time()
            self.end_time = end_time
        super().save(*args, **kwargs)

class CarePlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='care_plans')
    
    # Plan Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.CharField(max_length=100)
    created_date = models.DateField(auto_now_add=True)
    
    # Plan Details
    diagnosis = models.TextField()
    goals = models.JSONField(default=list)  # List of care goals
    interventions = models.JSONField(default=list)  # List of interventions
    expected_outcomes = models.JSONField(default=list)  # List of expected outcomes
    
    # Timeline
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('discontinued', 'Discontinued'),
            ('on_hold', 'On Hold')
        ],
        default='active'
    )
    
    # Review Information
    review_frequency = models.CharField(
        max_length=20,
        choices=[
            ('weekly', 'Weekly'),
            ('biweekly', 'Bi-weekly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('as_needed', 'As Needed')
        ],
        default='monthly'
    )
    last_review_date = models.DateField(blank=True, null=True)
    next_review_date = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.title} - {self.patient.full_name}"

class HealthGoal(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_goals')
    care_plan = models.ForeignKey(CarePlan, on_delete=models.CASCADE, related_name='health_goals', blank=True, null=True)
    
    # Goal Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('physical', 'Physical Health'),
            ('mental', 'Mental Health'),
            ('cognitive', 'Cognitive Health'),
            ('social', 'Social Health'),
            ('lifestyle', 'Lifestyle'),
            ('medication', 'Medication Management'),
            ('other', 'Other')
        ]
    )
    
    # Goal Details
    target_value = models.CharField(max_length=100, blank=True, null=True)
    current_value = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    
    # Timeline
    start_date = models.DateField()
    target_date = models.DateField()
    completed_date = models.DateField(blank=True, null=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('not_started', 'Not Started'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='not_started'
    )
    
    # Progress Tracking
    progress_percentage = models.IntegerField(default=0)
    milestones = models.JSONField(default=list)  # List of milestones
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.patient.full_name}"

class VitalSigns(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    
    # Vital Signs
    blood_pressure_systolic = models.IntegerField(blank=True, null=True)
    blood_pressure_diastolic = models.IntegerField(blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    oxygen_saturation = models.IntegerField(blank=True, null=True)
    respiratory_rate = models.IntegerField(blank=True, null=True)
    
    # Additional Measurements
    bmi = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    blood_glucose = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Recording Information
    recorded_date = models.DateField()
    recorded_time = models.TimeField()
    recorded_by = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-recorded_date', '-recorded_time']

    def __str__(self):
        return f"Vital Signs - {self.patient.full_name} ({self.recorded_date})"

    def save(self, *args, **kwargs):
        # Calculate BMI if height and weight are provided
        if self.height and self.weight:
            height_m = self.height / 100  # Convert cm to meters
            self.bmi = self.weight / (height_m ** 2)
        super().save(*args, **kwargs)
