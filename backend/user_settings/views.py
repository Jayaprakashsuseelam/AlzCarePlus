from django.shortcuts import render
from rest_framework import generics, permissions
from .models import UserSettings
from .serializers import UserSettingsSerializer

# Create your views here.

class UserSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, created = UserSettings.objects.get_or_create(user=self.request.user)
        return obj
