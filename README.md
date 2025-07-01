# AlzCare+
AlzCare+ - Comprehensive care, enhanced by AI &amp; ML. It is a AI-Based Lightweight platform (Web & Mobile App systems) to Monitor, Assist, and Alert Alzheimer's Patients and Caretakers.

## 🚀 Recent Updates (Latest)

### ✅ Implemented Features
- **JWT Authentication System**: Secure token-based authentication with refresh tokens
- **User Registration & Login**: Complete authentication flow with validation
- **Patient Management**: CRUD operations for patient data
- **Modern React Frontend**: Flat design UI with login/register forms
- **API Documentation**: Comprehensive REST API endpoints
- **Database Migrations**: PostgreSQL-ready with SQLite for development

### 🔧 Technical Stack
- **Backend**: Django 5.2 + Django REST Framework + JWT Authentication
- **Frontend**: React 19 + React Router + Modern CSS
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: JWT (JSON Web Tokens) with refresh mechanism

---

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

## 📊 Dataset (Sample)
 - https://archive.ics.uci.edu/dataset/231/pamap2+physical+activity+monitoring
 - https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones

## 🏗️ Project Structure
```
alzcareplus/
├── backend/
│   ├── backend/             # Django project settings
│   │   ├── settings.py      # JWT, CORS, Database config
│   │   ├── urls.py          # Main URL routing
│   │   └── ...
│   ├── users/               # User authentication & management
│   │   ├── models.py        # Custom User, UserProfile models
│   │   ├── serializers.py   # JWT auth serializers
│   │   ├── views.py         # Registration, login, profile views
│   │   ├── urls.py          # Auth endpoints
│   │   └── migrations/      # Database migrations
│   ├── patients/            # Patient management
│   │   ├── models.py        # Patient model
│   │   ├── views.py         # Patient CRUD views
│   │   ├── urls.py          # Patient endpoints
│   │   └── migrations/      # Database migrations
│   ├── requirements.txt     # Python dependencies
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js     # Login form component
│   │   │   ├── Register.js  # Registration form component
│   │   │   ├── PatientManager.js # Patient dashboard
│   │   │   ├── Auth.css     # Authentication styles
│   │   │   └── PatientManager.css # Dashboard styles
│   │   ├── App.js           # Main app with routing
│   │   └── ...
│   ├── package.json         # React dependencies
│   └── ...
├── ml/                      # Machine learning models
├── dataset/                 # Training datasets
└── README.md
```

## 🔌 API Endpoints

### Authentication & User Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/users/register/` | Register new user | No |
| `POST` | `/api/users/login/` | User login (JWT) | No |
| `POST` | `/api/users/logout/` | User logout | Yes |
| `POST` | `/api/users/token/refresh/` | Refresh JWT token | No |
| `GET` | `/api/users/profile/` | Get user profile | Yes |
| `PUT` | `/api/users/profile/` | Update user profile | Yes |
| `GET` | `/api/users/me/` | Get current user details | Yes |
| `GET` | `/api/users/info/` | Get user info | Yes |
| `POST` | `/api/users/change-password/` | Change password | Yes |
| `POST` | `/api/users/reset-password/` | Request password reset | No |
| `POST` | `/api/users/reset-password/confirm/` | Confirm password reset | No |

### Patient Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/patients/` | List all patients | Yes |
| `POST` | `/api/patients/` | Create new patient | Yes |
| `GET` | `/api/patients/<id>/` | Get patient details | Yes |
| `PUT` | `/api/patients/<id>/` | Update patient | Yes |
| `DELETE` | `/api/patients/<id>/` | Delete patient | Yes |

### Admin Endpoints (Optional)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/users/list/` | List all users | Yes |
| `GET` | `/api/users/stats/` | User statistics | Yes |
| `POST` | `/api/users/verify/<id>/` | Verify user account | Yes |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, SQLite for development)

### Backend Setup
```bash
# Clone the repository
git clone <repository-url>
cd AlzCarePlus

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Database Configuration

#### SQLite (Development - Default)
The project is configured to use SQLite by default for development.

#### PostgreSQL (Production)
1. Install PostgreSQL and create a database
2. Update `backend/backend/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'alzcareplus_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🔐 Authentication Flow

### Registration
1. Send POST request to `/api/users/register/` with:
   ```json
   {
     "username": "user123",
     "email": "user@example.com",
     "password": "securepassword",
     "password_confirm": "securepassword",
     "first_name": "John",
     "last_name": "Doe",
     "role": "caregiver"
   }
   ```

2. Receive JWT tokens:
   ```json
   {
     "message": "User registered successfully",
     "user": { ... },
     "tokens": {
       "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
       "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
     }
   }
   ```

### Login
1. Send POST request to `/api/users/login/` with:
   ```json
   {
     "username": "user123",
     "password": "securepassword"
   }
   ```

2. Receive JWT tokens (same format as registration)

### Using JWT Tokens
Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## 🎨 Frontend Features

### Authentication Pages
- **Login Page**: Modern flat design with email/password fields
- **Register Page**: Comprehensive registration form with validation
- **Responsive Design**: Works on desktop and mobile devices

### Patient Dashboard
- **Patient List**: View all patients in a grid layout
- **Add Patient**: Form to create new patient records
- **Patient Cards**: Display patient information in organized cards

### Styling
- **Flat Design**: Clean, modern interface without gradients or shadows
- **Blue Theme**: Consistent color scheme throughout the application
- **Responsive**: Mobile-friendly design with proper breakpoints

## 🔧 Development

### Adding New Features
1. Create models in appropriate Django apps
2. Generate and run migrations
3. Create serializers for API responses
4. Implement views with proper permissions
5. Add URL patterns
6. Update frontend components as needed

### Code Style
- Follow Django and React best practices
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Include proper error handling

## 📝 TODO

### Backend
- [ ] Implement email verification
- [ ] Add file upload for patient documents
- [ ] Create caregiver-patient relationships
- [ ] Add activity monitoring endpoints
- [ ] Implement real-time notifications

### Frontend
- [ ] Add patient detail pages
- [ ] Implement real-time updates
- [ ] Add data visualization charts
- [ ] Create mobile-responsive dashboard
- [ ] Add offline functionality

### ML Integration
- [ ] Activity recognition models
- [ ] Fall detection algorithms
- [ ] Behavior pattern analysis
- [ ] Predictive health insights

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support
For support and questions, please open an issue in the GitHub repository.
