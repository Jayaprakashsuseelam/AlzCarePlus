from django.conf import settings
from django.db import models

# Create your models here.

class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    notification_preferences = models.JSONField(default=dict, blank=True)
    privacy_settings = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.username}"
