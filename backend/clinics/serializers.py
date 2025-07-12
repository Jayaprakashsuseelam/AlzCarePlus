# clinics/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    Clinic, ClinicProfile, ClinicStaff, ClinicPatient, 
    Appointment, MedicalRecord, ClinicSchedule
)
from patients.models import Patient
from caretakers.models import Caretaker

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = [
            'id', 'email', 'clinic_name', 'clinic_type', 'phone', 'fax', 'website',
            'address', 'city', 'state', 'zip_code', 'country', 'license_number',
            'tax_id', 'npi_number', 'operating_hours', 'is_active', 'is_verified',
            'verification_date', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'is_verified', 'verification_date']

class ClinicProfileSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)
    
    class Meta:
        model = ClinicProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ClinicRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Clinic
        fields = [
            'email', 'password', 'confirm_password', 'clinic_name', 'clinic_type',
            'phone', 'fax', 'website', 'address', 'city', 'state', 'zip_code',
            'country', 'license_number', 'tax_id', 'npi_number', 'operating_hours'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        clinic = Clinic.objects.create_user(**validated_data)
        return clinic

class ClinicLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            clinic = authenticate(email=email, password=password)
            if not clinic:
                raise serializers.ValidationError('Invalid credentials')
            if not clinic.is_active:
                raise serializers.ValidationError('Clinic account is disabled')
            attrs['clinic'] = clinic
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return attrs

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'age', 'gender', 'date_of_birth']

class ClinicStaffSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    clinic = ClinicSerializer(read_only=True)
    
    class Meta:
        model = ClinicStaff
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'email': obj.user.email
        }

class ClinicStaffCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ClinicStaff
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_user_id(self, value):
        from django.contrib.auth.models import User
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        return value
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        from django.contrib.auth.models import User
        user = User.objects.get(id=user_id)
        validated_data['user'] = user
        return super().create(validated_data)

class ClinicPatientSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    clinic = ClinicSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ClinicPatient
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'registration_date', 'patient_number']
    
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
        
        # Generate patient number
        import uuid
        validated_data['patient_number'] = f"P{str(uuid.uuid4())[:8].upper()}"
        
        return super().create(validated_data)

class AppointmentSerializer(serializers.ModelSerializer):
    patient = ClinicPatientSerializer(read_only=True)
    staff = ClinicStaffSerializer(read_only=True)
    clinic = ClinicSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    staff_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'appointment_number', 'end_time']
    
    def validate_patient_id(self, value):
        try:
            ClinicPatient.objects.get(id=value)
        except ClinicPatient.DoesNotExist:
            raise serializers.ValidationError("Clinic patient does not exist")
        return value
    
    def validate_staff_id(self, value):
        try:
            ClinicStaff.objects.get(id=value)
        except ClinicStaff.DoesNotExist:
            raise serializers.ValidationError("Clinic staff does not exist")
        return value
    
    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id')
        staff_id = validated_data.pop('staff_id')
        
        patient = ClinicPatient.objects.get(id=patient_id)
        staff = ClinicStaff.objects.get(id=staff_id)
        
        validated_data['patient'] = patient
        validated_data['staff'] = staff
        
        # Generate appointment number
        import uuid
        validated_data['appointment_number'] = f"APT{str(uuid.uuid4())[:8].upper()}"
        
        return super().create(validated_data)

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status', 'check_in_time', 'check_out_time', 'diagnosis', 'treatment_plan', 'notes']

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = ClinicPatientSerializer(read_only=True)
    staff = ClinicStaffSerializer(read_only=True)
    clinic = ClinicSerializer(read_only=True)
    appointment = AppointmentSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    staff_id = serializers.IntegerField(write_only=True)
    appointment_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_patient_id(self, value):
        try:
            ClinicPatient.objects.get(id=value)
        except ClinicPatient.DoesNotExist:
            raise serializers.ValidationError("Clinic patient does not exist")
        return value
    
    def validate_staff_id(self, value):
        try:
            ClinicStaff.objects.get(id=value)
        except ClinicStaff.DoesNotExist:
            raise serializers.ValidationError("Clinic staff does not exist")
        return value
    
    def validate_appointment_id(self, value):
        if value:
            try:
                Appointment.objects.get(id=value)
            except Appointment.DoesNotExist:
                raise serializers.ValidationError("Appointment does not exist")
        return value
    
    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id')
        staff_id = validated_data.pop('staff_id')
        appointment_id = validated_data.pop('appointment_id', None)
        
        patient = ClinicPatient.objects.get(id=patient_id)
        staff = ClinicStaff.objects.get(id=staff_id)
        
        validated_data['patient'] = patient
        validated_data['staff'] = staff
        
        if appointment_id:
            appointment = Appointment.objects.get(id=appointment_id)
            validated_data['appointment'] = appointment
        
        return super().create(validated_data)

class ClinicScheduleSerializer(serializers.ModelSerializer):
    staff = ClinicStaffSerializer(read_only=True)
    clinic = ClinicSerializer(read_only=True)
    staff_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ClinicSchedule
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_staff_id(self, value):
        try:
            ClinicStaff.objects.get(id=value)
        except ClinicStaff.DoesNotExist:
            raise serializers.ValidationError("Clinic staff does not exist")
        return value
    
    def validate(self, attrs):
        if attrs['start_time'] >= attrs['end_time']:
            raise serializers.ValidationError("End time must be after start time")
        return attrs
    
    def create(self, validated_data):
        staff_id = validated_data.pop('staff_id')
        staff = ClinicStaff.objects.get(id=staff_id)
        validated_data['staff'] = staff
        return super().create(validated_data)

class ClinicDashboardSerializer(serializers.Serializer):
    total_patients = serializers.IntegerField()
    total_staff = serializers.IntegerField()
    today_appointments = serializers.IntegerField()
    completed_appointments_today = serializers.IntegerField()
    pending_appointments = serializers.IntegerField()
    recent_appointments = AppointmentSerializer(many=True)
    recent_patients = ClinicPatientSerializer(many=True)
    today_schedule = ClinicScheduleSerializer(many=True)

class ClinicStatisticsSerializer(serializers.Serializer):
    appointments_by_status = serializers.DictField()
    appointments_by_type = serializers.DictField()
    patients_by_gender = serializers.DictField()
    patients_by_age_group = serializers.DictField()
    staff_by_department = serializers.DictField()
    monthly_appointments = serializers.ListField()

class AppointmentFilterSerializer(serializers.Serializer):
    date = serializers.DateField(required=False)
    status = serializers.CharField(required=False)
    appointment_type = serializers.CharField(required=False)
    staff_id = serializers.IntegerField(required=False)
    patient_id = serializers.IntegerField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

class MedicalRecordFilterSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField(required=False)
    record_type = serializers.CharField(required=False)
    staff_id = serializers.IntegerField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    access_level = serializers.CharField(required=False) 