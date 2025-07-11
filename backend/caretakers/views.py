# caretakers/views.py

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404

from .models import (
    Caretaker, CaretakerProfile, CaretakerPatientAssignment, 
    CaretakerSchedule, CaretakerTask
)
from .serializers import (
    CaretakerSerializer, CaretakerProfileSerializer, CaretakerRegistrationSerializer,
    CaretakerLoginSerializer, CaretakerPatientAssignmentSerializer,
    CaretakerScheduleSerializer, CaretakerTaskSerializer, CaretakerDashboardSerializer,
    CaretakerTaskUpdateSerializer
)
from patients.models import Patient

class IsCaretaker(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'caretaker') or isinstance(request.user, Caretaker)

class CaretakerRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = CaretakerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            caretaker = serializer.save()
            
            # Create profile
            CaretakerProfile.objects.create(caretaker=caretaker)
            
            # Generate tokens
            refresh = RefreshToken.for_user(caretaker)
            
            return Response({
                'message': 'Caretaker registered successfully',
                'caretaker': CaretakerSerializer(caretaker).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CaretakerLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = CaretakerLoginSerializer(data=request.data)
        if serializer.is_valid():
            caretaker = serializer.validated_data['caretaker']
            
            # Generate tokens
            refresh = RefreshToken.for_user(caretaker)
            
            # Update last login
            caretaker.last_login = timezone.now()
            caretaker.save()
            
            return Response({
                'message': 'Login successful',
                'caretaker': CaretakerSerializer(caretaker).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CaretakerProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCaretaker]
    
    def get(self, request):
        try:
            profile = request.user.profile
            serializer = CaretakerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CaretakerProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        try:
            profile = request.user.profile
            serializer = CaretakerProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CaretakerProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

class CaretakerDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCaretaker]
    
    def get(self, request):
        caretaker = request.user
        today = date.today()
        
        # Get assigned patients
        assignments = CaretakerPatientAssignment.objects.filter(
            caretaker=caretaker, 
            is_active=True
        )
        assigned_patients = [assignment.patient for assignment in assignments]
        
        # Get task statistics
        active_tasks = CaretakerTask.objects.filter(
            caretaker=caretaker,
            status__in=['pending', 'in_progress']
        ).count()
        
        completed_tasks_today = CaretakerTask.objects.filter(
            caretaker=caretaker,
            status='completed',
            completed_date__date=today
        ).count()
        
        # Get recent tasks
        recent_tasks = CaretakerTask.objects.filter(
            caretaker=caretaker
        ).order_by('-created_at')[:5]
        
        # Get today's schedule
        today_schedule = CaretakerSchedule.objects.filter(
            caretaker=caretaker,
            date=today
        ).order_by('start_time')
        
        # Count upcoming appointments (tasks with appointment type)
        upcoming_appointments = CaretakerTask.objects.filter(
            caretaker=caretaker,
            task_type='appointment',
            scheduled_date__gte=today,
            status__in=['pending', 'in_progress']
        ).count()
        
        dashboard_data = {
            'total_patients': len(assigned_patients),
            'active_tasks': active_tasks,
            'completed_tasks_today': completed_tasks_today,
            'upcoming_appointments': upcoming_appointments,
            'recent_tasks': CaretakerTaskSerializer(recent_tasks, many=True).data,
            'assigned_patients': CaretakerSerializer(assigned_patients, many=True).data,
            'today_schedule': CaretakerScheduleSerializer(today_schedule, many=True).data,
        }
        
        serializer = CaretakerDashboardSerializer(data=dashboard_data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

class CaretakerPatientAssignmentView(generics.ListCreateAPIView):
    serializer_class = CaretakerPatientAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCaretaker]
    
    def get_queryset(self):
        return CaretakerPatientAssignment.objects.filter(caretaker=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(caretaker=self.request.user)

class CaretakerPatientAssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CaretakerPatientAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCaretaker]
    
    def get_queryset(self):
        return CaretakerPatientAssignment.objects.filter(caretaker=self.request.user)

class CaretakerScheduleView(generics.ListCreateAPIView):
    serializer_class = CaretakerScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsCaretaker]
    
    def get_queryset(self):
        queryset = CaretakerSchedule.objects.filter(caretaker=self.request.user)
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.order_by('date', 'start_time')
    
    def perform_create(self, serializer):
        serializer.save(caretaker=self.request.user)

class CaretakerScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CaretakerScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsCaretaker]
    
    def get_queryset(self):
        return CaretakerSchedule.objects.filter(caretaker=self.request.user)

class CaretakerTaskView(generics.ListCreateAPIView):
    serializer_class = CaretakerTaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsCaretaker]
    
    def get_queryset(self):
        queryset = CaretakerTask.objects.filter(caretaker=self.request.user)
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by patient if provided
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by date if provided
        date_filter = self.request.query_params.get('date')
        if date_filter:
            queryset = queryset.filter(scheduled_date=date_filter)
        
        return queryset.order_by('-scheduled_date', '-scheduled_time')
    
    def perform_create(self, serializer):
        serializer.save(caretaker=self.request.user)

class CaretakerTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CaretakerTaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsCaretaker]
    
    def get_queryset(self):
        return CaretakerTask.objects.filter(caretaker=self.request.user)

class CaretakerTaskUpdateView(generics.UpdateAPIView):
    serializer_class = CaretakerTaskUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsCaretaker]
    
    def get_queryset(self):
        return CaretakerTask.objects.filter(caretaker=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsCaretaker])
def caretaker_patients(request):
    """Get all patients assigned to the caretaker"""
    assignments = CaretakerPatientAssignment.objects.filter(
        caretaker=request.user,
        is_active=True
    )
    patients = [assignment.patient for assignment in assignments]
    serializer = CaretakerSerializer(patients, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsCaretaker])
def caretaker_task_statistics(request):
    """Get task statistics for the caretaker"""
    caretaker = request.user
    today = date.today()
    
    # Task counts by status
    task_stats = CaretakerTask.objects.filter(caretaker=caretaker).aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='pending')),
        in_progress=Count('id', filter=Q(status='in_progress')),
        completed=Count('id', filter=Q(status='completed')),
        cancelled=Count('id', filter=Q(status='cancelled'))
    )
    
    # Tasks completed today
    completed_today = CaretakerTask.objects.filter(
        caretaker=caretaker,
        status='completed',
        completed_date__date=today
    ).count()
    
    # Tasks due today
    due_today = CaretakerTask.objects.filter(
        caretaker=caretaker,
        scheduled_date=today,
        status__in=['pending', 'in_progress']
    ).count()
    
    return Response({
        'task_statistics': task_stats,
        'completed_today': completed_today,
        'due_today': due_today
    }, status=status.HTTP_200_OK) 