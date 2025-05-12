# backend/settings.py

INSTALLED_APPS = [
    ..
    'rest_framework',
    'patients',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'alzcareplus_be_db',
        'USER': 'postgres',
        'PASSWORD': '#postgres@usr5466',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
