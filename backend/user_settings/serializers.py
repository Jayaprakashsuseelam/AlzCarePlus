from rest_framework import serializers
from .models import UserSettings

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ['notification_preferences', 'privacy_settings', 'updated_at'] 