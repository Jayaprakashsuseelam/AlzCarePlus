# AlzCarePlus - Patient Authentication Setup Guide

This guide will help you set up the integrated patient registration and login system with PostgreSQL backend and React frontend.

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL database
- npm or yarn

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Database Configuration

The application is configured to use PostgreSQL. Make sure you have:
- PostgreSQL server running
- Database `alzcareplus_be_db` created
- User `postgres` with password `#postgres@usr5466`

If you need to change the database configuration, edit `backend/backend/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Run Migrations

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Dummy Data

```bash
python setup_db.py
```

This will create 5 dummy patients with the following test credentials:
- Email: `john.smith@email.com`
- Password: `testpass123`

### 5. Start the Backend Server

```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start the Frontend Development Server

```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication Endpoints

- `POST /api/patients/auth/register/` - Patient registration
- `POST /api/patients/auth/login/` - Patient login
- `POST /api/patients/auth/logout/` - Patient logout
- `POST /api/patients/auth/reset-password/` - Password reset request

### Patient Endpoints

- `GET /api/patients/profile/` - Get patient profile
- `PUT /api/patients/profile/update/` - Update patient profile
- `GET /api/patients/dashboard/` - Get dashboard data

## Features Implemented

### Backend Features

1. **Custom Patient Model**: Extended Django's AbstractUser for patient-specific fields
2. **Token Authentication**: Uses Django REST Framework's TokenAuthentication
3. **Patient Profile**: Separate model for detailed patient information
4. **API Serializers**: Comprehensive serializers for all patient operations
5. **Dummy Data**: Script to create test patients with realistic data

### Frontend Features

1. **Modern UI**: Clean, responsive design with gradient backgrounds
2. **Form Validation**: Client-side validation with error handling
3. **Loading States**: Visual feedback during API calls
4. **Error Handling**: Comprehensive error messages and recovery
5. **Authentication Flow**: Complete login/register/logout flow
6. **Dashboard**: Interactive dashboard with tabs and mock data
7. **Responsive Design**: Works on desktop and mobile devices

### Authentication Flow

1. **Registration**: Users can create accounts with email, password, and personal info
2. **Login**: Email/password authentication with token storage
3. **Dashboard**: Protected routes with authentication checks
4. **Logout**: Token cleanup and session termination
5. **Password Reset**: Email-based password reset (mock implementation)

## Testing the Application

1. **Registration**: Visit `http://localhost:3000/patient/register` to create a new account
2. **Login**: Use the test credentials or register a new account
3. **Dashboard**: After login, you'll be redirected to the dashboard
4. **Navigation**: Use the tabs to explore different sections

## File Structure

```
AlzCarePlus/
├── backend/
│   ├── patients/
│   │   ├── models.py          # Patient and PatientProfile models
│   │   ├── serializers.py     # API serializers
│   │   ├── views.py           # API views and endpoints
│   │   └── urls.py            # URL routing
│   ├── backend/
│   │   └── settings.py        # Django settings
│   └── setup_db.py            # Database setup script
├── frontend/
│   ├── src/
│   │   ├── components/patient/
│   │   │   ├── Login.js       # Login component
│   │   │   ├── Register.js    # Registration component
│   │   │   ├── ResetPassword.js # Password reset component
│   │   │   ├── PatientDashboard.js # Dashboard component
│   │   │   ├── PatientAuth.css # Authentication styles
│   │   │   └── PatientDashboard.css # Dashboard styles
│   │   ├── services/
│   │   │   └── api.js         # API service functions
│   │   └── App.js             # Main app with routing
│   └── package.json
└── SETUP.md                   # This file
```

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure PostgreSQL is running and credentials are correct
2. **CORS Errors**: Check that the backend CORS settings include your frontend URL
3. **Migration Errors**: Delete the database and recreate it if migration conflicts occur
4. **Port Conflicts**: Ensure ports 3000 (frontend) and 8000 (backend) are available

### Debug Mode

The application is configured for development with:
- Django DEBUG = True
- CORS allowed for localhost
- Detailed error messages

## Next Steps

1. **Email Integration**: Implement real email sending for password reset
2. **File Upload**: Add profile picture upload functionality
3. **Real Data**: Connect to actual medical data sources
4. **Security**: Add rate limiting and additional security measures
5. **Testing**: Add unit and integration tests

## Support

For issues or questions, check the error logs in both frontend and backend consoles. 