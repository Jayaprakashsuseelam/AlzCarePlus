# patients/urls.py

from django.urls import path
from .views import PatientViewSet

urlpatterns = [
    path('', PatientViewSet.as_view({'get': 'list', 'post': 'create'}), name='patient-list'),
    path('<int:pk>/', PatientViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='patient-detail'),
]
