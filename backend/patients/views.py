# patients/views.py

from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    total_patients = Patient.objects.count()
    recent_patients = Patient.objects.order_by('-created_at')[:5]
    recent_patients_data = PatientSerializer(recent_patients, many=True).data
    return Response({
        'total_patients': total_patients,
        'recent_patients': recent_patients_data,
    })
