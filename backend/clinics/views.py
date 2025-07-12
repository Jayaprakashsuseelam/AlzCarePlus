# clinics/views.py

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404
from collections import defaultdict

from .models import (
    Clinic, ClinicProfile, ClinicStaff, ClinicPatient, 
    Appointment, MedicalRecord, ClinicSchedule
)
from .serializers import (
    ClinicSerializer, ClinicProfileSerializer, ClinicRegistrationSerializer,
    ClinicLoginSerializer, ClinicStaffSerializer, ClinicStaffCreateSerializer,
    ClinicPatientSerializer, AppointmentSerializer, AppointmentUpdateSerializer,
    MedicalRecordSerializer, ClinicScheduleSerializer, ClinicDashboardSerializer,
    ClinicStatisticsSerializer, AppointmentFilterSerializer, MedicalRecordFilterSerializer
)
from patients.models import Patient

class IsClinic(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'clinic') or isinstance(request.user, Clinic)

class ClinicRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ClinicRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            clinic = serializer.save()
            
            # Create profile
            ClinicProfile.objects.create(clinic=clinic)
            
            # Generate tokens
            refresh = RefreshToken.for_user(clinic)
            
            return Response({
                'message': 'Clinic registered successfully',
                'clinic': ClinicSerializer(clinic).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClinicLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ClinicLoginSerializer(data=request.data)
        if serializer.is_valid():
            clinic = serializer.validated_data['clinic']
            
            # Generate tokens
            refresh = RefreshToken.for_user(clinic)
            
            # Update last login
            clinic.last_login = timezone.now()
            clinic.save()
            
            return Response({
                'message': 'Login successful',
                'clinic': ClinicSerializer(clinic).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClinicProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get(self, request):
        try:
            profile = request.user.profile
            serializer = ClinicProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClinicProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        try:
            profile = request.user.profile
            serializer = ClinicProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ClinicProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

class ClinicDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get(self, request):
        clinic = request.user
        today = date.today()
        
        # Get basic statistics
        total_patients = ClinicPatient.objects.filter(clinic=clinic, is_active=True).count()
        total_staff = ClinicStaff.objects.filter(clinic=clinic, is_active=True).count()
        
        # Appointment statistics
        today_appointments = Appointment.objects.filter(
            clinic=clinic,
            scheduled_date=today
        ).count()
        
        completed_appointments_today = Appointment.objects.filter(
            clinic=clinic,
            scheduled_date=today,
            status='completed'
        ).count()
        
        pending_appointments = Appointment.objects.filter(
            clinic=clinic,
            status__in=['scheduled', 'confirmed']
        ).count()
        
        # Recent data
        recent_appointments = Appointment.objects.filter(
            clinic=clinic
        ).order_by('-scheduled_date', '-scheduled_time')[:5]
        
        recent_patients = ClinicPatient.objects.filter(
            clinic=clinic,
            is_active=True
        ).order_by('-registration_date')[:5]
        
        today_schedule = ClinicSchedule.objects.filter(
            clinic=clinic,
            date=today
        ).order_by('start_time')
        
        dashboard_data = {
            'total_patients': total_patients,
            'total_staff': total_staff,
            'today_appointments': today_appointments,
            'completed_appointments_today': completed_appointments_today,
            'pending_appointments': pending_appointments,
            'recent_appointments': AppointmentSerializer(recent_appointments, many=True).data,
            'recent_patients': ClinicPatientSerializer(recent_patients, many=True).data,
            'today_schedule': ClinicScheduleSerializer(today_schedule, many=True).data,
        }
        
        serializer = ClinicDashboardSerializer(data=dashboard_data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClinicStaffView(generics.ListCreateAPIView):
    serializer_class = ClinicStaffSerializer
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get_queryset(self):
        return ClinicStaff.objects.filter(clinic=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(clinic=self.request.user)

class ClinicStaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClinicStaffSerializer
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get_queryset(self):
        return ClinicStaff.objects.filter(clinic=self.request.user)

class ClinicPatientView(generics.ListCreateAPIView):
    serializer_class = ClinicPatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get_queryset(self):
        queryset = ClinicPatient.objects.filter(clinic=self.request.user, is_active=True)
        
        # Filter by search term
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search) |
                Q(patient_number__icontains=search)
            )
        
        return queryset.order_by('-registration_date')
    
    def perform_create(self, serializer):
        serializer.save(clinic=self.request.user)

class ClinicPatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClinicPatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get_queryset(self):
        return ClinicPatient.objects.filter(clinic=self.request.user)

class AppointmentView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get_queryset(self):
        queryset = Appointment.objects.filter(clinic=self.request.user)
        
        # Apply filters
        filters = AppointmentFilterSerializer(data=self.request.query_params)
        if filters.is_valid():
            data = filters.validated_data
            
            if data.get('date'):
                queryset = queryset.filter(scheduled_date=data['date'])
            
            if data.get('status'):
                queryset = queryset.filter(status=data['status'])
            
            if data.get('appointment_type'):
                queryset = queryset.filter(appointment_type=data['appointment_type'])
            
            if data.get('staff_id'):
                queryset = queryset.filter(staff_id=data['staff_id'])
            
            if data.get('patient_id'):
                queryset = queryset.filter(patient_id=data['patient_id'])
            
            if data.get('start_date'):
                queryset = queryset.filter(scheduled_date__gte=data['start_date'])
            
            if data.get('end_date'):
                queryset = queryset.filter(scheduled_date__lte=data['end_date'])
        
        return queryset.order_by('-scheduled_date', '-scheduled_time')
    
    def perform_create(self, serializer):
        serializer.save(clinic=self.request.user)

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get_queryset(self):
        return Appointment.objects.filter(clinic=self.request.user)

class AppointmentUpdateView(generics.UpdateAPIView):
    serializer_class = AppointmentUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get_queryset(self):
        return Appointment.objects.filter(clinic=self.request.user)

class MedicalRecordView(generics.ListCreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get_queryset(self):
        queryset = MedicalRecord.objects.filter(clinic=self.request.user)
        
        # Apply filters
        filters = MedicalRecordFilterSerializer(data=self.request.query_params)
        if filters.is_valid():
            data = filters.validated_data
            
            if data.get('patient_id'):
                queryset = queryset.filter(patient_id=data['patient_id'])
            
            if data.get('record_type'):
                queryset = queryset.filter(record_type=data['record_type'])
            
            if data.get('staff_id'):
                queryset = queryset.filter(staff_id=data['staff_id'])
            
            if data.get('start_date'):
                queryset = queryset.filter(created_at__date__gte=data['start_date'])
            
            if data.get('end_date'):
                queryset = queryset.filter(created_at__date__lte=data['end_date'])
            
            if data.get('access_level'):
                queryset = queryset.filter(access_level=data['access_level'])
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(clinic=self.request.user)

class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get_queryset(self):
        return MedicalRecord.objects.filter(clinic=self.request.user)

class ClinicScheduleView(generics.ListCreateAPIView):
    serializer_class = ClinicScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get_queryset(self):
        queryset = ClinicSchedule.objects.filter(clinic=self.request.user)
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        staff_id = self.request.query_params.get('staff_id')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if staff_id:
            queryset = queryset.filter(staff_id=staff_id)
        
        return queryset.order_by('date', 'start_time')
    
    def perform_create(self, serializer):
        serializer.save(clinic=self.request.user)

class ClinicScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClinicScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsClinic]
    
    def get_queryset(self):
        return ClinicSchedule.objects.filter(clinic=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsClinic])
def clinic_statistics(request):
    """Get comprehensive clinic statistics"""
    clinic = request.user
    today = date.today()
    
    # Appointments by status
    appointments_by_status = Appointment.objects.filter(clinic=clinic).values('status').annotate(
        count=Count('id')
    )
    status_data = {item['status']: item['count'] for item in appointments_by_status}
    
    # Appointments by type
    appointments_by_type = Appointment.objects.filter(clinic=clinic).values('appointment_type').annotate(
        count=Count('id')
    )
    type_data = {item['appointment_type']: item['count'] for item in appointments_by_type}
    
    # Patients by gender
    patients_by_gender = ClinicPatient.objects.filter(clinic=clinic, is_active=True).values(
        'patient__gender'
    ).annotate(count=Count('id'))
    gender_data = {item['patient__gender']: item['count'] for item in patients_by_gender}
    
    # Staff by department
    staff_by_department = ClinicStaff.objects.filter(clinic=clinic, is_active=True).values(
        'department'
    ).annotate(count=Count('id'))
    department_data = {item['department']: item['count'] for item in staff_by_department}
    
    # Monthly appointments (last 6 months)
    monthly_data = []
    for i in range(6):
        month_date = today - timedelta(days=30*i)
        month_start = month_date.replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        count = Appointment.objects.filter(
            clinic=clinic,
            scheduled_date__range=[month_start, month_end]
        ).count()
        
        monthly_data.append({
            'month': month_start.strftime('%Y-%m'),
            'count': count
        })
    
    # Patients by age group
    patients = ClinicPatient.objects.filter(clinic=clinic, is_active=True).select_related('patient')
    age_groups = defaultdict(int)
    
    for clinic_patient in patients:
        if clinic_patient.patient.age:
            if clinic_patient.patient.age < 18:
                age_groups['0-17'] += 1
            elif clinic_patient.patient.age < 30:
                age_groups['18-29'] += 1
            elif clinic_patient.patient.age < 50:
                age_groups['30-49'] += 1
            elif clinic_patient.patient.age < 70:
                age_groups['50-69'] += 1
            else:
                age_groups['70+'] += 1
    
    return Response({
        'appointments_by_status': status_data,
        'appointments_by_type': type_data,
        'patients_by_gender': gender_data,
        'patients_by_age_group': dict(age_groups),
        'staff_by_department': department_data,
        'monthly_appointments': monthly_data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsClinic])
def search_patients(request):
    """Search for patients to add to clinic"""
    search = request.query_params.get('search', '')
    if not search:
        return Response({'error': 'Search term is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search in patients not already in this clinic
    clinic_patient_ids = ClinicPatient.objects.filter(
        clinic=request.user, 
        is_active=True
    ).values_list('patient_id', flat=True)
    
    patients = Patient.objects.filter(
        Q(first_name__icontains=search) |
        Q(last_name__icontains=search) |
        Q(email__icontains=search)
    ).exclude(id__in=clinic_patient_ids)[:10]
    
    from .serializers import PatientSerializer
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsClinic])
def check_in_appointment(request, appointment_id):
    """Check in a patient for appointment"""
    try:
        appointment = Appointment.objects.get(
            id=appointment_id, 
            clinic=request.user
        )
        appointment.check_in_time = timezone.now()
        appointment.status = 'in_progress'
        appointment.save()
        
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsClinic])
def check_out_appointment(request, appointment_id):
    """Check out a patient from appointment"""
    try:
        appointment = Appointment.objects.get(
            id=appointment_id, 
            clinic=request.user
        )
        appointment.check_out_time = timezone.now()
        appointment.status = 'completed'
        appointment.save()
        
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND) 