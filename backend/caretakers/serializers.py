# caretakers/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Caretaker, CaretakerProfile, CaretakerPatientAssignment, CaretakerSchedule, CaretakerTask
from patients.models import Patient

class CaretakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caretaker
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth', 
            'gender', 'professional_title', 'license_number', 'years_of_experience',
            'specialization', 'employment_status', 'hire_date', 'is_active',
            'date_joined', 'last_login', 'email_verified', 'background_check_verified',
            'background_check_date'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'email_verified', 
                           'background_check_verified', 'background_check_date']

class CaretakerProfileSerializer(serializers.ModelSerializer):
    caretaker = CaretakerSerializer(read_only=True)
    
    class Meta:
        model = CaretakerProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class CaretakerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Caretaker
        fields = [
            'email', 'password', 'confirm_password', 'first_name', 'last_name',
            'phone', 'date_of_birth', 'gender', 'professional_title',
            'license_number', 'years_of_experience', 'specialization',
            'employment_status', 'hire_date'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        caretaker = Caretaker.objects.create_user(**validated_data)
        return caretaker

class CaretakerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            caretaker = authenticate(email=email, password=password)
            if not caretaker:
                raise serializers.ValidationError('Invalid credentials')
            if not caretaker.is_active:
                raise serializers.ValidationError('Account is disabled')
            attrs['caretaker'] = caretaker
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return attrs

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'age', 'gender']

class CaretakerPatientAssignmentSerializer(serializers.ModelSerializer):
    caretaker = CaretakerSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CaretakerPatientAssignment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'assignment_date']
    
    def validate_patient_id(self, value):
        try:
            Patient.objects.get(id=value)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient does not exist")
        return value
    
    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id')
        patient = Patient.objects.get(id=patient_id)
        validated_data['patient'] = patient
        return super().create(validated_data)

class CaretakerScheduleSerializer(serializers.ModelSerializer):
    caretaker = CaretakerSerializer(read_only=True)
    
    class Meta:
        model = CaretakerSchedule
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, attrs):
        if attrs['start_time'] >= attrs['end_time']:
            raise serializers.ValidationError("End time must be after start time")
        return attrs

class CaretakerTaskSerializer(serializers.ModelSerializer):
    caretaker = CaretakerSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CaretakerTask
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_patient_id(self, value):
        try:
            Patient.objects.get(id=value)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient does not exist")
        return value
    
    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id')
        patient = Patient.objects.get(id=patient_id)
        validated_data['patient'] = patient
        return super().create(validated_data)

class CaretakerDashboardSerializer(serializers.Serializer):
    total_patients = serializers.IntegerField()
    active_tasks = serializers.IntegerField()
    completed_tasks_today = serializers.IntegerField()
    upcoming_appointments = serializers.IntegerField()
    recent_tasks = CaretakerTaskSerializer(many=True)
    assigned_patients = PatientSerializer(many=True)
    today_schedule = CaretakerScheduleSerializer(many=True)

class CaretakerTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaretakerTask
        fields = ['status', 'completed_date', 'notes']
    
    def update(self, instance, validated_data):
        if validated_data.get('status') == 'completed' and not instance.completed_date:
            from django.utils import timezone
            validated_data['completed_date'] = timezone.now()
        return super().update(instance, validated_data) 