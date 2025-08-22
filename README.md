# AlzCarePlus - Patient Management System

A comprehensive healthcare management system designed for Alzheimer's care, featuring patient registration, login, and dashboard functionality.

## Features - Updated

### Patient Management
- **Patient Registration**: Complete registration form with validation
- **Patient Login**: Secure authentication with JWT tokens
- **Patient Dashboard**: Comprehensive health overview with statistics
- **Profile Management**: Update personal and medical information
- **Medical Records**: View and manage medical history
- **Appointments**: Schedule and track appointments
- **Medications**: Manage prescriptions and medication schedules
- **Care Plans**: Track treatment plans and progress
- **Health Goals**: Set and monitor health objectives
- **Vital Signs**: Record and track health metrics

### Clinic Management
- **Clinic Registration**: Multi-step clinic registration process
- **Clinic Login**: Secure clinic authentication
- **Clinic Dashboard**: Professional clinic management interface
- **Staff Management**: Manage clinic staff and roles
- **Patient Management**: View and manage patient records

## Technology Stack

### Backend
- **Django 5.1.1**: Web framework
- **Django REST Framework**: API development
- **Django REST Framework Simple JWT**: JWT authentication
- **Django CORS Headers**: Cross-origin resource sharing
- **SQLite/PostgreSQL**: Database (SQLite for development, PostgreSQL for production)

### Frontend
- **React**: User interface library
- **React Router**: Client-side routing
- **React Icons**: Icon library
- **CSS3**: Styling and responsive design

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup database**:
   ```bash
   python setup_db.py
   ```
   This will:
   - Run database migrations
   - Create a superuser account
   - Create a test patient account (test@patient.com / testpass123)

5. **Run development server**:
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Patient Authentication
- `POST /api/auth/register/` - Patient registration
- `POST /api/auth/login/` - Patient login
- `POST /api/auth/logout/` - Patient logout
- `POST /api/auth/reset-password/` - Password reset request

### Patient Profile
- `GET /api/profile/` - Get patient profile
- `PUT /api/profile/update/` - Update patient profile
- `GET /api/profile/details/` - Get detailed profile information

### Patient Dashboard
- `GET /api/dashboard/` - Get dashboard data and statistics

### Medical Records
- `GET /api/medical-records/` - List medical records
- `POST /api/medical-records/` - Create medical record
- `GET /api/medical-records/{id}/` - Get specific medical record
- `PUT /api/medical-records/{id}/` - Update medical record
- `DELETE /api/medical-records/{id}/` - Delete medical record

### Medications
- `GET /api/medications/` - List medications
- `POST /api/medications/` - Add medication
- `GET /api/medications/{id}/` - Get specific medication
- `PUT /api/medications/{id}/` - Update medication
- `DELETE /api/medications/{id}/` - Delete medication

### Appointments
- `GET /api/appointments/` - List appointments
- `POST /api/appointments/` - Schedule appointment
- `GET /api/appointments/{id}/` - Get specific appointment
- `PUT /api/appointments/{id}/` - Update appointment
- `DELETE /api/appointments/{id}/` - Cancel appointment

### Care Plans
- `GET /api/care-plans/` - List care plans
- `POST /api/care-plans/` - Create care plan
- `GET /api/care-plans/{id}/` - Get specific care plan
- `PUT /api/care-plans/{id}/` - Update care plan
- `DELETE /api/care-plans/{id}/` - Delete care plan

### Health Goals
- `GET /api/health-goals/` - List health goals
- `POST /api/health-goals/` - Create health goal
- `GET /api/health-goals/{id}/` - Get specific health goal
- `PUT /api/health-goals/{id}/` - Update health goal
- `DELETE /api/health-goals/{id}/` - Delete health goal

### Vital Signs
- `GET /api/vital-signs/` - List vital signs
- `POST /api/vital-signs/` - Record vital signs
- `GET /api/vital-signs/{id}/` - Get specific vital signs
- `PUT /api/vital-signs/{id}/` - Update vital signs
- `DELETE /api/vital-signs/{id}/` - Delete vital signs

## Usage Guide

### Patient Registration

1. Navigate to `http://localhost:3000/patient/register`
2. Fill out the registration form with:
   - First Name
   - Last Name
   - Email Address
   - Phone Number
   - Date of Birth
   - Gender
   - Password (minimum 8 characters)
   - Confirm Password
3. Agree to Terms and Conditions
4. Click "Create Account"

### Patient Login

1. Navigate to `http://localhost:3000/patient/login`
2. Enter your email and password
3. Optionally check "Remember me"
4. Click "Sign In"

### Patient Dashboard

After successful login, you'll be redirected to the patient dashboard which includes:

- **Health Overview**: Key health statistics
- **Recent Appointments**: Latest appointment history
- **Upcoming Appointments**: Scheduled future appointments
- **Active Medications**: Current prescriptions
- **Recent Medical Records**: Latest medical documentation
- **Active Care Plans**: Current treatment plans
- **Health Goals**: Progress on health objectives
- **Recent Vital Signs**: Latest health metrics
- **Notifications**: Important alerts and reminders

## Testing

### Test Accounts

The setup script creates the following test accounts:

**Test Patient**:
- Email: `test@patient.com`
- Password: `testpass123`

**Superuser**:
- Created during setup process
- Can access Django admin at `http://localhost:8000/admin/`

### API Testing

You can test the API endpoints using tools like:
- **Postman**: For API testing
- **curl**: Command-line API testing
- **Django REST Framework browsable API**: Available at `http://localhost:8000/api/`

Example API test with curl:

```bash
# Patient Registration
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "1234567890",
    "date_of_birth": "1980-01-01",
    "gender": "male",
    "password": "testpass123",
    "confirm_password": "testpass123"
  }'

# Patient Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "testpass123"
  }'
```

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Validation**: Strong password requirements
- **CORS Protection**: Cross-origin request security
- **Input Validation**: Comprehensive form validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Protection**: Built-in Django security features

## Development

### Project Structure

```
AlzCarePlus/
├── backend/
│   ├── backend/          # Django project settings
│   ├── patients/         # Patient management app
│   ├── clinics/          # Clinic management app
│   ├── users/            # User management app
│   ├── manage.py         # Django management script
│   └── setup_db.py       # Database setup script
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── styles/       # CSS styles
│   └── public/           # Static files
└── README.md
```

### Adding New Features

1. **Backend**: Add models, serializers, views, and URLs in the appropriate Django app
2. **Frontend**: Create React components and add routes in App.js
3. **API Integration**: Update API services to communicate with new endpoints
4. **Testing**: Test both backend and frontend functionality

## Deployment

### Production Setup

1. **Database**: Switch to PostgreSQL in settings.py
2. **Environment Variables**: Use python-decouple for sensitive settings
3. **Static Files**: Configure static file serving
4. **Security**: Enable HTTPS and security headers
5. **Monitoring**: Set up logging and monitoring

### Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team or create an issue in the repository.


## Reference Products:
Device / Platform Type Key Features Global / Affordable?
ADMarker Research prototype Multi-modal, federated AI, high accuracy Scalable, privacy-preserving
SafeWander Wearable sensor Bed exit alerts Affordable concept, replicable globally
Wander Alert, Vitality Monitor, Lively Mobile Plus, Memo Box Wearables / Smart Reminders Geo-fencing, vitals tracking, communication, memory aids Variable affordability & worldwide use
QuikTok & MedaCareLLM AI LLM companions Phone conversation, AI smart glasses support Designed for accessibility and broad reach
MICA (ValueCare) Conversational AI wristwear Voice prompts, real-time logging, cloud dashboard UK-based, scalable globally
Empatica Devices Health-monitoring wearables Vitals, seizure detection, remote monitoring Clinical-grade, more costly
Hexoskin Smart clothing Continuous biometric tracking Research-focused, scalable
Sleeptracker-AI Contactless monitoring Sleep data via sensors, cloud API High compliance, unobtrusive
Dementia Locate Tracker Commercial GPS wearable Wandering alerts, location tracking Affordable, available
Alzheimer Calendar Clock Assistive device Displays date/time clearly Very affordable, low-tech

## Reference Studies:
- https://arxiv.org/abs/2310.15301



## Core System Components
Button Sensor (Wearable Sensor)
Gateway (Signal Relay Unit)
Mobile App (iOS & Android)
