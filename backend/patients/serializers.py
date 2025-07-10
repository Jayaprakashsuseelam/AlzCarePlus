# patients/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Patient, PatientProfile

class PatientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'date_of_birth', 'gender', 'password', 'confirm_password'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        patient = Patient.objects.create_user(**validated_data)
        # Create a profile for the patient
        PatientProfile.objects.create(patient=patient)
        return patient

class PatientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            patient = authenticate(email=email, password=password)
            if not patient:
                raise serializers.ValidationError('Invalid email or password')
            if not patient.is_active:
                raise serializers.ValidationError('Account is disabled')
            attrs['patient'] = patient
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return attrs

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    profile = PatientProfileSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'age', 'medical_history',
            'emergency_contact_name', 'emergency_contact_phone',
            'date_joined', 'last_login', 'email_verified', 'profile'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'email_verified']

class PatientDashboardSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'full_name', 'email', 'age', 'date_joined', 'last_login'
        ]

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not Patient.objects.filter(email=value).exists():
            raise serializers.ValidationError('No patient found with this email address')
        return value
