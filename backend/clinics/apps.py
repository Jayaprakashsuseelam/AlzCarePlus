# clinics/apps.py

from django.apps import AppConfig


class ClinicsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinics'
    verbose_name = 'Clinic Management' 