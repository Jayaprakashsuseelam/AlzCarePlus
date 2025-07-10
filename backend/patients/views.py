# patients/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Patient, PatientProfile
from .serializers import (
    PatientSerializer, PatientRegistrationSerializer, 
    PatientLoginSerializer, PatientDashboardSerializer,
    PasswordResetSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def patient_register(request):
    """Register a new patient"""
    serializer = PatientRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        patient = serializer.save()
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_dashboard(request):
    """Get patient dashboard data"""
    patient = request.user
    
    # Mock dashboard data - in a real app, this would come from various models
    dashboard_data = {
        'patient': PatientDashboardSerializer(patient).data,
        'stats': {
            'total_appointments': 5,
            'upcoming_appointments': 2,
            'completed_tests': 8,
            'active_medications': 3
        },
        'recent_activity': [
            {
                'type': 'appointment',
                'title': 'Dr. Sarah Johnson - Neurology',
                'date': '2024-02-20',
                'time': '10:00 AM'
            },
            {
                'type': 'test_result',
                'title': 'Cognitive Assessment',
                'date': '2024-01-15',
                'result': 'Mild Cognitive Impairment'
            },
            {
                'type': 'medication',
                'title': 'Donepezil prescription renewed',
                'date': '2024-01-10'
            }
        ],
        'medications': [
            {
                'name': 'Donepezil',
                'dosage': '10mg',
                'frequency': 'Once daily',
                'status': 'active'
            },
            {
                'name': 'Memantine',
                'dosage': '20mg',
                'frequency': 'Twice daily',
                'status': 'active'
            },
            {
                'name': 'Vitamin D',
                'dosage': '1000 IU',
                'frequency': 'Once daily',
                'status': 'active'
            }
        ],
        'upcoming_appointments': [
            {
                'id': 1,
                'doctor': 'Dr. Sarah Johnson',
                'specialty': 'Neurology',
                'date': '2024-02-20',
                'time': '10:00 AM - 11:00 AM',
                'type': 'Follow-up consultation'
            }
        ]
    }
    
    return Response(dashboard_data, status=status.HTTP_200_OK)

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
