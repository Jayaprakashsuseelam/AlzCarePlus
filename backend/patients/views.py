# patients/views.py

from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count, Avg
from datetime import date, timedelta
from .models import (
    Patient, PatientProfile, MedicalRecord, Medication, 
    Appointment, CarePlan, HealthGoal, VitalSigns
)
from .serializers import (
    PatientSerializer, PatientRegistrationSerializer, 
    PatientLoginSerializer, PatientDashboardSerializer,
    PasswordResetSerializer, PatientProfileSerializer,
    MedicalRecordSerializer, MedicationSerializer,
    AppointmentSerializer, CarePlanSerializer,
    HealthGoalSerializer, VitalSignsSerializer,
    PatientStatisticsSerializer, PatientDashboardDataSerializer,
    PatientSearchSerializer, MedicalRecordFilterSerializer,
    AppointmentFilterSerializer, PatientSummarySerializer,
    MedicalRecordSummarySerializer, AppointmentSummarySerializer,
    MedicationSummarySerializer, PatientExportSerializer
)

# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def patient_register(request):
    """Register a new patient"""
    serializer = PatientRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        patient = serializer.save()
        # Create profile for the new patient
        PatientProfile.objects.create(patient=patient)
        # Create token for the new patient
        token, created = Token.objects.get_or_create(user=patient)
        
        return Response({
            'message': 'Patient registered successfully',
            'patient': PatientSerializer(patient).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def patient_login(request):
    """Login a patient"""
    serializer = PatientLoginSerializer(data=request.data)
    if serializer.is_valid():
        patient = serializer.validated_data['patient']
        login(request, patient)
        
        # Update last login
        patient.last_login = timezone.now()
        patient.save()
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=patient)
        
        return Response({
            'message': 'Login successful',
            'patient': PatientSerializer(patient).data,
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def patient_logout(request):
    """Logout a patient"""
    try:
        # Delete the token
        request.user.auth_token.delete()
    except:
        pass
    
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """Request password reset"""
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        # In a real application, you would send an email here
        # For now, we'll just return a success message
        return Response({
            'message': f'Password reset link has been sent to {email}'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Profile Management Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_profile(request):
    """Get current patient's profile"""
    patient = request.user
    serializer = PatientSerializer(patient)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_patient_profile(request):
    """Update current patient's profile"""
    patient = request.user
    serializer = PatientSerializer(patient, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'patient': serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def patient_profile_details(request):
    """Get or update patient profile details"""
    patient = request.user
    profile, created = PatientProfile.objects.get_or_create(patient=patient)
    
    if request.method == 'GET':
        serializer = PatientProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = PatientProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile details updated successfully',
                'profile': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Dashboard Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_dashboard(request):
    """Get patient dashboard data"""
    patient = request.user
    today = date.today()
    
    # Get statistics
    total_appointments = Appointment.objects.filter(patient=patient).count()
    upcoming_appointments = Appointment.objects.filter(
        patient=patient, 
        scheduled_date__gte=today,
        status__in=['scheduled', 'confirmed']
    ).count()
    completed_appointments = Appointment.objects.filter(
        patient=patient, 
        status='completed'
    ).count()
    
    total_medications = Medication.objects.filter(patient=patient).count()
    active_medications = Medication.objects.filter(
        patient=patient, 
        status='active'
    ).count()
    
    total_medical_records = MedicalRecord.objects.filter(patient=patient).count()
    recent_medical_records = MedicalRecord.objects.filter(
        patient=patient,
        date_recorded__gte=today - timedelta(days=30)
    ).count()
    
    care_plans_count = CarePlan.objects.filter(patient=patient).count()
    active_care_plans = CarePlan.objects.filter(
        patient=patient, 
        status='active'
    ).count()
    
    health_goals_count = HealthGoal.objects.filter(patient=patient).count()
    completed_goals = HealthGoal.objects.filter(
        patient=patient, 
        status='completed'
    ).count()
    
    # Get recent data
    recent_appointments = Appointment.objects.filter(
        patient=patient
    ).order_by('-scheduled_date', '-scheduled_time')[:5]
    
    upcoming_appointments_list = Appointment.objects.filter(
        patient=patient,
        scheduled_date__gte=today,
        status__in=['scheduled', 'confirmed']
    ).order_by('scheduled_date', 'scheduled_time')[:5]
    
    recent_medical_records_list = MedicalRecord.objects.filter(
        patient=patient
    ).order_by('-date_recorded')[:5]
    
    active_medications_list = Medication.objects.filter(
        patient=patient,
        status='active'
    ).order_by('-prescription_date')[:5]
    
    active_care_plans_list = CarePlan.objects.filter(
        patient=patient,
        status='active'
    ).order_by('-created_date')[:3]
    
    recent_vital_signs = VitalSigns.objects.filter(
        patient=patient
    ).order_by('-recorded_date')[:5]
    
    health_goals = HealthGoal.objects.filter(
        patient=patient
    ).order_by('-created_at')[:5]
    
    dashboard_data = {
        'patient': PatientDashboardSerializer(patient).data,
        'statistics': {
            'total_appointments': total_appointments,
            'upcoming_appointments': upcoming_appointments,
            'completed_appointments': completed_appointments,
            'total_medications': total_medications,
            'active_medications': active_medications,
            'total_medical_records': total_medical_records,
            'recent_medical_records': recent_medical_records,
            'care_plans_count': care_plans_count,
            'active_care_plans': active_care_plans,
            'health_goals_count': health_goals_count,
            'completed_goals': completed_goals
        },
        'recent_appointments': AppointmentSummarySerializer(recent_appointments, many=True).data,
        'upcoming_appointments': AppointmentSummarySerializer(upcoming_appointments_list, many=True).data,
        'recent_medical_records': MedicalRecordSummarySerializer(recent_medical_records_list, many=True).data,
        'active_medications': MedicationSummarySerializer(active_medications_list, many=True).data,
        'active_care_plans': CarePlanSerializer(active_care_plans_list, many=True).data,
        'recent_vital_signs': VitalSignsSerializer(recent_vital_signs, many=True).data,
        'health_goals': HealthGoalSerializer(health_goals, many=True).data
    }
    
    serializer = PatientDashboardDataSerializer(data=dashboard_data)
    serializer.is_valid()
    return Response(serializer.data, status=status.HTTP_200_OK)

# Medical Records Views
class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MedicalRecord.objects.filter(patient=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def medical_records_filtered(request):
    """Get filtered medical records"""
    patient = request.user
    queryset = MedicalRecord.objects.filter(patient=patient)
    
    # Apply filters
    record_type = request.query_params.get('record_type')
    if record_type:
        queryset = queryset.filter(record_type=record_type)
    
    date_from = request.query_params.get('date_from')
    if date_from:
        queryset = queryset.filter(date_recorded__gte=date_from)
    
    date_to = request.query_params.get('date_to')
    if date_to:
        queryset = queryset.filter(date_recorded__lte=date_to)
    
    recorded_by = request.query_params.get('recorded_by')
    if recorded_by:
        queryset = queryset.filter(recorded_by__icontains=recorded_by)
    
    serializer = MedicalRecordSerializer(queryset.order_by('-date_recorded'), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Medication Views
class MedicationViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Medication.objects.filter(patient=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def medications_by_status(request):
    """Get medications filtered by status"""
    patient = request.user
    status_filter = request.query_params.get('status', 'active')
    
    medications = Medication.objects.filter(
        patient=patient,
        status=status_filter
    ).order_by('-prescription_date')
    
    serializer = MedicationSerializer(medications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Appointment Views
class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointments_filtered(request):
    """Get filtered appointments"""
    patient = request.user
    queryset = Appointment.objects.filter(patient=patient)
    
    # Apply filters
    appointment_type = request.query_params.get('appointment_type')
    if appointment_type:
        queryset = queryset.filter(appointment_type=appointment_type)
    
    status_filter = request.query_params.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    date_from = request.query_params.get('date_from')
    if date_from:
        queryset = queryset.filter(scheduled_date__gte=date_from)
    
    date_to = request.query_params.get('date_to')
    if date_to:
        queryset = queryset.filter(scheduled_date__lte=date_to)
    
    doctor_name = request.query_params.get('doctor_name')
    if doctor_name:
        queryset = queryset.filter(doctor_name__icontains=doctor_name)
    
    serializer = AppointmentSerializer(queryset.order_by('-scheduled_date'), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Care Plan Views
class CarePlanViewSet(viewsets.ModelViewSet):
    serializer_class = CarePlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CarePlan.objects.filter(patient=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

# Health Goal Views
class HealthGoalViewSet(viewsets.ModelViewSet):
    serializer_class = HealthGoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return HealthGoal.objects.filter(patient=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_goal_progress(request, goal_id):
    """Update health goal progress"""
    goal = get_object_or_404(HealthGoal, id=goal_id, patient=request.user)
    
    progress_percentage = request.data.get('progress_percentage')
    current_value = request.data.get('current_value')
    status = request.data.get('status')
    
    if progress_percentage is not None:
        goal.progress_percentage = progress_percentage
    
    if current_value is not None:
        goal.current_value = current_value
    
    if status is not None:
        goal.status = status
        if status == 'completed':
            goal.completed_date = date.today()
    
    goal.save()
    
    serializer = HealthGoalSerializer(goal)
    return Response({
        'message': 'Goal progress updated successfully',
        'goal': serializer.data
    }, status=status.HTTP_200_OK)

# Vital Signs Views
class VitalSignsViewSet(viewsets.ModelViewSet):
    serializer_class = VitalSignsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return VitalSigns.objects.filter(patient=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vital_signs_trends(request):
    """Get vital signs trends over time"""
    patient = request.user
    days = int(request.query_params.get('days', 30))
    
    start_date = date.today() - timedelta(days=days)
    vital_signs = VitalSigns.objects.filter(
        patient=patient,
        recorded_date__gte=start_date
    ).order_by('recorded_date')
    
    # Group by date and calculate averages
    trends = {}
    for vital in vital_signs:
        date_str = vital.recorded_date.strftime('%Y-%m-%d')
        if date_str not in trends:
            trends[date_str] = {
                'date': date_str,
                'blood_pressure_systolic': [],
                'blood_pressure_diastolic': [],
                'heart_rate': [],
                'temperature': [],
                'weight': [],
                'oxygen_saturation': [],
                'bmi': []
            }
        
        if vital.blood_pressure_systolic:
            trends[date_str]['blood_pressure_systolic'].append(vital.blood_pressure_systolic)
        if vital.blood_pressure_diastolic:
            trends[date_str]['blood_pressure_diastolic'].append(vital.blood_pressure_diastolic)
        if vital.heart_rate:
            trends[date_str]['heart_rate'].append(vital.heart_rate)
        if vital.temperature:
            trends[date_str]['temperature'].append(float(vital.temperature))
        if vital.weight:
            trends[date_str]['weight'].append(float(vital.weight))
        if vital.oxygen_saturation:
            trends[date_str]['oxygen_saturation'].append(vital.oxygen_saturation)
        if vital.bmi:
            trends[date_str]['bmi'].append(float(vital.bmi))
    
    # Calculate averages
    for date_str, data in trends.items():
        for key, values in data.items():
            if key != 'date' and values:
                trends[date_str][key] = sum(values) / len(values)
            elif key != 'date':
                trends[date_str][key] = None
    
    return Response(list(trends.values()), status=status.HTTP_200_OK)

# Search and Filter Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_patients(request):
    """Search patients (for admin/staff use)"""
    search = request.query_params.get('search', '')
    gender = request.query_params.get('gender')
    age_min = request.query_params.get('age_min')
    age_max = request.query_params.get('age_max')
    blood_type = request.query_params.get('blood_type')
    
    queryset = Patient.objects.all()
    
    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
    
    if gender:
        queryset = queryset.filter(gender=gender)
    
    if age_min:
        queryset = queryset.filter(age__gte=age_min)
    
    if age_max:
        queryset = queryset.filter(age__lte=age_max)
    
    if blood_type:
        queryset = queryset.filter(profile__blood_type=blood_type)
    
    serializer = PatientSummarySerializer(queryset[:50], many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Export and Report Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_patient_data(request):
    """Export patient data"""
    patient = request.user
    
    # Get all related data
    patient_data = PatientExportSerializer(patient).data
    medical_records = MedicalRecordSerializer(
        patient.medical_records.all(), many=True
    ).data
    medications = MedicationSerializer(
        patient.medications.all(), many=True
    ).data
    appointments = AppointmentSerializer(
        patient.appointments.all(), many=True
    ).data
    care_plans = CarePlanSerializer(
        patient.care_plans.all(), many=True
    ).data
    vital_signs = VitalSignsSerializer(
        patient.vital_signs.all(), many=True
    ).data
    
    export_data = {
        'patient': patient_data,
        'medical_records': medical_records,
        'medications': medications,
        'appointments': appointments,
        'care_plans': care_plans,
        'vital_signs': vital_signs,
        'export_date': timezone.now().isoformat()
    }
    
    return Response(export_data, status=status.HTTP_200_OK)

# Legacy Views (for backward compatibility)
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    """Legacy dashboard view for admin"""
    total_patients = Patient.objects.count()
    recent_patients = Patient.objects.order_by('-date_joined')[:5]
    recent_patients_data = PatientSerializer(recent_patients, many=True).data
    return Response({
        'total_patients': total_patients,
        'recent_patients': recent_patients_data,
    })
