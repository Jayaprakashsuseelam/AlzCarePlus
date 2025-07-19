# patients/serializers.py

from rest_framework import serializers
from .models import (
    Patient, PatientProfile, MedicalRecord, Medication, 
    Appointment, CarePlan, HealthGoal, VitalSigns
)

class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'date_of_birth', 'age', 'gender', 'medical_history',
            'emergency_contact_name', 'emergency_contact_phone',
            'is_active', 'date_joined', 'last_login', 'email_verified'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'email_verified']

class PatientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'email', 'first_name', 'last_name', 'password', 'confirm_password',
            'phone', 'date_of_birth', 'gender', 'medical_history',
            'emergency_contact_name', 'emergency_contact_phone'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return Patient.objects.create_user(**validated_data)

class PatientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        from django.contrib.auth import authenticate
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('Account is disabled')
        attrs['patient'] = user
        return attrs

class PatientDashboardSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'date_of_birth', 'age', 'gender'
        ]

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not Patient.objects.filter(email=value).exists():
            raise serializers.ValidationError('No patient found with this email address')
        return value

class PatientProfileSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    
    class Meta:
        model = PatientProfile
        fields = [
            'id', 'patient', 'patient_name', 'profile_picture', 'address',
            'city', 'state', 'zip_code', 'country', 'blood_type', 'allergies',
            'current_medications', 'primary_care_physician', 'specialist',
            'insurance_provider', 'insurance_number', 'height', 'weight', 'bmi',
            'smoking_status', 'alcohol_consumption', 'exercise_frequency',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    record_type_display = serializers.CharField(source='get_record_type_display', read_only=True)
    access_level_display = serializers.CharField(source='get_access_level_display', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'patient_name', 'record_type', 'record_type_display',
            'title', 'description', 'date_recorded', 'recorded_by', 'findings',
            'diagnosis', 'treatment', 'recommendations', 'blood_pressure',
            'heart_rate', 'temperature', 'weight', 'height', 'oxygen_saturation',
            'mmse_score', 'clock_drawing_score', 'memory_score', 'attachments',
            'is_private', 'access_level', 'access_level_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class MedicationSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    route_display = serializers.CharField(source='get_route_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Medication
        fields = [
            'id', 'patient', 'patient_name', 'name', 'generic_name', 'dosage',
            'frequency', 'route', 'route_display', 'prescribed_by',
            'prescription_date', 'start_date', 'end_date', 'status', 'status_display',
            'instructions', 'side_effects', 'contraindications', 'refills_remaining',
            'pharmacy', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    appointment_type_display = serializers.CharField(source='get_appointment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'appointment_type', 'appointment_type_display',
            'scheduled_date', 'scheduled_time', 'duration', 'end_time', 'doctor_name',
            'specialty', 'clinic_name', 'status', 'status_display', 'room_number',
            'department', 'reason', 'notes', 'diagnosis', 'treatment_plan',
            'check_in_time', 'check_out_time', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'end_time', 'created_at', 'updated_at']

class CarePlanSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    review_frequency_display = serializers.CharField(source='get_review_frequency_display', read_only=True)
    
    class Meta:
        model = CarePlan
        fields = [
            'id', 'patient', 'patient_name', 'title', 'description', 'created_by',
            'created_date', 'diagnosis', 'goals', 'interventions', 'expected_outcomes',
            'start_date', 'end_date', 'status', 'status_display', 'review_frequency',
            'review_frequency_display', 'last_review_date', 'next_review_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_date', 'created_at', 'updated_at']

class HealthGoalSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = HealthGoal
        fields = [
            'id', 'patient', 'patient_name', 'care_plan', 'title', 'description',
            'category', 'category_display', 'target_value', 'current_value', 'unit',
            'start_date', 'target_date', 'completed_date', 'status', 'status_display',
            'progress_percentage', 'milestones', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class VitalSignsSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    
    class Meta:
        model = VitalSigns
        fields = [
            'id', 'patient', 'patient_name', 'blood_pressure_systolic',
            'blood_pressure_diastolic', 'heart_rate', 'temperature', 'weight',
            'height', 'oxygen_saturation', 'respiratory_rate', 'bmi',
            'blood_glucose', 'recorded_date', 'recorded_time', 'recorded_by',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'bmi', 'created_at', 'updated_at']

# Dashboard and Statistics Serializers
class PatientStatisticsSerializer(serializers.Serializer):
    total_appointments = serializers.IntegerField()
    upcoming_appointments = serializers.IntegerField()
    completed_appointments = serializers.IntegerField()
    total_medications = serializers.IntegerField()
    active_medications = serializers.IntegerField()
    total_medical_records = serializers.IntegerField()
    recent_medical_records = serializers.IntegerField()
    care_plans_count = serializers.IntegerField()
    active_care_plans = serializers.IntegerField()
    health_goals_count = serializers.IntegerField()
    completed_goals = serializers.IntegerField()

class PatientDashboardDataSerializer(serializers.Serializer):
    patient = PatientDashboardSerializer()
    statistics = PatientStatisticsSerializer()
    recent_appointments = AppointmentSerializer(many=True)
    upcoming_appointments = AppointmentSerializer(many=True)
    recent_medical_records = MedicalRecordSerializer(many=True)
    active_medications = MedicationSerializer(many=True)
    active_care_plans = CarePlanSerializer(many=True)
    recent_vital_signs = VitalSignsSerializer(many=True)
    health_goals = HealthGoalSerializer(many=True)

# Search and Filter Serializers
class PatientSearchSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    age_min = serializers.IntegerField(required=False)
    age_max = serializers.IntegerField(required=False)
    blood_type = serializers.CharField(required=False)
    has_medications = serializers.BooleanField(required=False)
    has_care_plans = serializers.BooleanField(required=False)

class MedicalRecordFilterSerializer(serializers.Serializer):
    record_type = serializers.CharField(required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    recorded_by = serializers.CharField(required=False)

class AppointmentFilterSerializer(serializers.Serializer):
    appointment_type = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    doctor_name = serializers.CharField(required=False)

# Summary and List Serializers
class PatientSummarySerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    profile = PatientProfileSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'date_of_birth', 'age', 'gender', 'profile'
        ]

class MedicalRecordSummarySerializer(serializers.ModelSerializer):
    record_type_display = serializers.CharField(source='get_record_type_display', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'record_type', 'record_type_display', 'title',
            'date_recorded', 'recorded_by', 'created_at'
        ]

class AppointmentSummarySerializer(serializers.ModelSerializer):
    appointment_type_display = serializers.CharField(source='get_appointment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'appointment_type', 'appointment_type_display',
            'scheduled_date', 'scheduled_time', 'doctor_name',
            'specialty', 'status', 'status_display'
        ]

class MedicationSummarySerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Medication
        fields = [
            'id', 'name', 'dosage', 'frequency', 'status',
            'status_display', 'prescription_date', 'end_date'
        ]

# Export and Report Serializers
class PatientExportSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    profile = PatientProfileSerializer(read_only=True)
    medical_records_count = serializers.SerializerMethodField()
    appointments_count = serializers.SerializerMethodField()
    medications_count = serializers.SerializerMethodField()
    care_plans_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'date_of_birth', 'age', 'gender', 'medical_history',
            'emergency_contact_name', 'emergency_contact_phone',
            'date_joined', 'profile', 'medical_records_count',
            'appointments_count', 'medications_count', 'care_plans_count'
        ]
    
    def get_medical_records_count(self, obj):
        return obj.medical_records.count()
    
    def get_appointments_count(self, obj):
        return obj.appointments.count()
    
    def get_medications_count(self, obj):
        return obj.medications.count()
    
    def get_care_plans_count(self, obj):
        return obj.care_plans.count()
