# AlzCare+
AlzCare+ - Comprehensive care, enhanced by AI &amp; ML. It is a AI-Based Lightweight platform (Web & Mobile App systems) to Monitor, Assist, and Alert Alzheimer's Patients and Caretakers.

## Scope of the project
Enable continuous, passive monitoring of patient activities (e.g., walking, sleeping, sitting, and falls) using mobile device sensors and optional wearable integrations to enhance safety and care personalization for Alzheimer's patients.

## 🧠 1. Patient Monitoring Features
 - Real-Time Location Tracking (GPS): Continuously monitor patient movement and alert if they wander beyond safe zones.
 - Geo-Fencing Alerts: Notify caretakers if the patient leaves a predefined safe area.
 - Activity Recognition (AI/ML): Detect walking, sleeping, sitting, or potential falls using device sensors.
 - Fall Detection: Immediate alert on sudden drops or inactivity suggestive of a fall.
 - Vitals Integration (Optional via wearables): Monitor heart rate, oxygen level, etc., if synced with smart bands.

## 🧩 2. Cognitive Assistance Features
 - Daily Routine Reminders: Medications, meals, hygiene, and appointments.
 - Voice Assistance (Conversational AI): Simple voice-based interaction to answer questions and guide actions.
 - Face Recognition for Familiar People: Helps identify family, friends, and caregivers.
 - Memory Diary (Photo + Voice Notes): Helps patients store and recall events via multimedia.
 - Calendar and Events Visualizer: Color-coded reminders for upcoming events.

## 🆘 3. Emergency & Alert Features
 - Emergency SOS Button: Direct call/message to caretaker with live location.
 - Auto Alerts to Multiple Caregivers: Notify all concerned via SMS, app, or email.
 - Unusual Behavior Detection (AI-powered): Alert when sudden disorientation, agitation, or nighttime wandering is detected.

## 🔒 4. Caregiver Dashboard Features
 - Multi-Patient Monitoring: For professional caregivers monitoring multiple patients.
 - Real-Time Notifications and Logs: Timeline of alerts, reminders sent, vitals, and behavior patterns.
 - Shared Access: Family and healthcare professionals can view/edit routines and notes.
 - AI-Generated Health Reports: Weekly summaries of behavior trends and alerts.

## 🌐 5. Connectivity & Integration
 - Wearable Integration: Connect with smartwatches, fitness bands, or fall sensors.
 - Voice Assistant Integration (Alexa/Google Assistant): For ambient reminders at home.
 - Cloud Sync + Offline Mode: Store essential data locally and sync to cloud when connected.

## 🧩 6. User Experience & Accessibility
 - Lightweight & Offline-Compatible App: Minimal resource usage; usable in low-connectivity zones.
 - Large Fonts & High Contrast UI: Tailored for elderly users with vision challenges.
 - Multilingual & Voice Input Support: Local language support with simple voice commands.
 - Mood Tracking (Optional): Patients can log how they feel; AI can detect mood shifts from voice tone or patterns.

   
## Dataset (Sample)
 - https://archive.ics.uci.edu/dataset/231/pamap2+physical+activity+monitoring
 - https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones

## Project structure (Growing)
alzcareplus/
├── backend/
│   ├── backend/             # Django project settings
│   ├── users/               # App for user authentication and management
│   ├── patients/            # App for patient-related models and views
│   ├── caregivers/          # App for caregiver-related models and views
│   ├── monitoring/          # App for real-time monitoring features
│   ├── reminders/           # App for scheduling and reminders
│   ├── ml_models/           # App for ML model integration
│   ├── requirements.txt     # Python dependencies
│   └── manage.py
├── ml/
├── frontend/
│   └── ...                  # React or Next.js frontend code
├── Deployment/
├── docker-compose.yml       # Optional
└── README.md

## Backend API Endpoints

### User Authentication & Management
- `POST   /api/users/auth/register/`         - Register a new user
- `POST   /api/users/auth/login/`            - User login
- `POST   /api/users/auth/logout/`           - User logout
- `GET    /api/users/profile/`               - Get current user profile
- `PUT    /api/users/profile/`               - Update current user profile
- `POST   /api/users/profile/change-password/` - Change password
- `POST   /api/users/auth/password-reset/`   - Request password reset
- `POST   /api/users/auth/password-reset/confirm/` - Confirm password reset
- `GET    /api/users/me/`                    - Get current user info
- `GET    /api/users/users/`                 - List all users (admin)
- `GET    /api/users/users/<id>/`            - Retrieve user by ID (admin)
- `PUT    /api/users/users/<id>/`            - Update user by ID (admin)
- `DELETE /api/users/users/<id>/`            - Deactivate user (admin)
- `POST   /api/users/users/<user_id>/verify/`- Verify user account (admin)
- `GET    /api/users/users/stats/`           - User statistics (admin)

### Patient Management
- `GET    /api/patients/`                    - List all patients
- `POST   /api/patients/`                    - Create a new patient
- `GET    /api/patients/<id>/`               - Retrieve patient by ID
- `PUT    /api/patients/<id>/`               - Update patient by ID
- `DELETE /api/patients/<id>/`               - Delete patient by ID

> More endpoints will be added as the project grows (caregivers, monitoring, reminders, etc.)

## Suggested technology stack
 - Backend:
    - Framework: Django
    - API: Django REST Framework
    - Database: PostgreSQL
    - Authentication: Token-based (e.g., JWT)
    - Machine Learning Integration: Python scripts or services integrated via Django views or Celery tasks

 - Frontend:
    - Framework: React or Next.js
    - Communication: Consume RESTful APIs provided by the Django backend

 - Deployment:
    - Containerization: Docker
    - Web Server: Gunicorn
    - Reverse Proxy: Nginx
    - Hosting: Cloud services like AWS, Heroku, or DigitalOcean

- Machine Learning
    - Algorithm :
    - 
