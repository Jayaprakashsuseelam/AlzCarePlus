# AlzCarePlus Caretaker Management Features

## Overview

This document provides a comprehensive guide to the new caretaker management features added to the AlzCarePlus application. These features enable administrators and managers to efficiently manage caretaker accounts, view detailed information, and oversee caretaker operations.

## Table of Contents

1. [Features Overview](#features-overview)
2. [Frontend Components](#frontend-components)
3. [API Endpoints](#api-endpoints)
4. [Database Models](#database-models)
5. [Usage Instructions](#usage-instructions)
6. [Setup and Configuration](#setup-and-configuration)
7. [Security Considerations](#security-considerations)

## Features Overview

### Core Management Features

1. **Caretaker Management Dashboard**
   - View all caretakers in a comprehensive table
   - Search and filter caretakers by various criteria
   - Pagination for large datasets
   - Quick status updates and actions

2. **Add/Edit Caretaker Forms**
   - Comprehensive registration form for new caretakers
   - Professional information collection
   - Validation and error handling
   - Profile picture upload support

3. **Detailed Caretaker View**
   - Complete caretaker profile information
   - Patient assignments overview
   - Task management and tracking
   - Schedule management
   - Professional credentials and certifications

4. **Advanced Management Capabilities**
   - Bulk operations support
   - Status management (active/inactive)
   - Assignment management
   - Performance tracking

## Frontend Components

### 1. CaretakerManagement.js

**Location**: `frontend/src/pages/caretaker/CaretakerManagement.js`

**Purpose**: Main management interface for viewing and managing all caretakers.

**Key Features**:
- Responsive table with caretaker information
- Search and filter functionality
- Add/Edit/Delete operations
- Status management
- Pagination support

**Component Structure**:
```javascript
const CaretakerManagement = () => {
  // State management
  const [caretakers, setCaretakers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingCaretaker, setEditingCaretaker] = useState(null);
  
  // API calls
  const fetchCaretakers = async () => { /* ... */ };
  const handleAddCaretaker = async (caretakerData) => { /* ... */ };
  const handleUpdateCaretaker = async (caretakerId, caretakerData) => { /* ... */ };
  const handleDeleteCaretaker = async (caretakerId) => { /* ... */ };
  
  // Render methods
  return (
    <div className="caretaker-management">
      {/* Header, Search, Table, Modals */}
    </div>
  );
};
```

### 2. CaretakerDetails.js

**Location**: `frontend/src/pages/caretaker/CaretakerDetails.js`

**Purpose**: Detailed view of individual caretaker information with tabbed interface.

**Key Features**:
- Tabbed interface (Overview, Assignments, Tasks, Schedule)
- Comprehensive profile information
- Patient assignment management
- Task tracking and management
- Schedule overview

**Component Structure**:
```javascript
const CaretakerDetails = () => {
  const { id } = useParams();
  const [activeTab, setActiveTab] = useState('overview');
  const [caretaker, setCaretaker] = useState(null);
  const [profile, setProfile] = useState(null);
  const [assignments, setAssignments] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [schedule, setSchedule] = useState([]);
  
  // API calls for different data types
  const fetchCaretakerDetails = async () => { /* ... */ };
  
  return (
    <div className="caretaker-details">
      {/* Header, Tabs, Content */}
    </div>
  );
};
```

### 3. CSS Styling

**Files**:
- `frontend/src/pages/caretaker/CaretakerManagement.css`
- `frontend/src/pages/caretaker/CaretakerDetails.css`

**Design Features**:
- Modern, professional medical theme
- Responsive design for all screen sizes
- Consistent color scheme and typography
- Interactive hover effects and animations
- Accessibility considerations

## API Endpoints

### Caretaker Management Endpoints

#### 1. Get All Caretakers
```
GET /api/caretakers/management/
```
**Parameters**:
- `page`: Page number for pagination
- `search`: Search term for name, email, or license
- `status`: Filter by active status (true/false)
- `employment_status`: Filter by employment type

**Response**:
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/caretakers/management/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "caretaker@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "professional_title": "Registered Nurse",
      "license_number": "RN123456",
      "employment_status": "full-time",
      "is_active": true,
      "date_joined": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### 2. Get Caretaker by ID
```
GET /api/caretakers/management/{id}/
```

#### 3. Create Caretaker
```
POST /api/caretakers/management/
```
**Request Body**:
```json
{
  "email": "newcaretaker@example.com",
  "password": "securepassword123",
  "confirm_password": "securepassword123",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "+1234567890",
  "date_of_birth": "1985-05-15",
  "gender": "female",
  "professional_title": "Licensed Practical Nurse",
  "license_number": "LPN789012",
  "years_of_experience": 8,
  "specialization": "Geriatric Care",
  "employment_status": "full-time",
  "hire_date": "2024-01-20"
}
```

#### 4. Update Caretaker
```
PUT /api/caretakers/management/{id}/
```

#### 5. Delete Caretaker
```
DELETE /api/caretakers/management/{id}/
```

### Profile Management Endpoints

#### 1. Get Caretaker Profile
```
GET /api/caretakers/management/{id}/profile/
```

#### 2. Update Caretaker Profile
```
PUT /api/caretakers/management/{id}/profile/
```

### Assignment Management Endpoints

#### 1. Get Caretaker Assignments
```
GET /api/caretakers/management/{id}/assignments/
```

#### 2. Create Assignment
```
POST /api/caretakers/management/{id}/assignments/
```

#### 3. Update Assignment
```
PUT /api/caretakers/management/{id}/assignments/{assignment_id}/
```

#### 4. Delete Assignment
```
DELETE /api/caretakers/management/{id}/assignments/{assignment_id}/
```

### Task Management Endpoints

#### 1. Get Caretaker Tasks
```
GET /api/caretakers/management/{id}/tasks/
```

#### 2. Create Task
```
POST /api/caretakers/management/{id}/tasks/
```

#### 3. Update Task
```
PUT /api/caretakers/management/{id}/tasks/{task_id}/
```

#### 4. Delete Task
```
DELETE /api/caretakers/management/{id}/tasks/{task_id}/
```

### Schedule Management Endpoints

#### 1. Get Caretaker Schedule
```
GET /api/caretakers/management/{id}/schedule/
```

#### 2. Create Schedule Entry
```
POST /api/caretakers/management/{id}/schedule/
```

#### 3. Update Schedule Entry
```
PUT /api/caretakers/management/{id}/schedule/{schedule_id}/
```

#### 4. Delete Schedule Entry
```
DELETE /api/caretakers/management/{id}/schedule/{schedule_id}/
```

## Database Models

### Existing Models (Enhanced)

The caretaker management features utilize the existing models with additional functionality:

#### 1. Caretaker Model
```python
class Caretaker(AbstractUser):
    # Personal Information
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    
    # Professional Information
    professional_title = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES)
    hire_date = models.DateField(blank=True, null=True)
    
    # Account Status
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    background_check_verified = models.BooleanField(default=False)
```

#### 2. CaretakerProfile Model
```python
class CaretakerProfile(models.Model):
    caretaker = models.OneToOneField(Caretaker, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='caretaker_profiles/')
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    languages_spoken = models.CharField(max_length=200, blank=True, null=True)
    availability_schedule = models.JSONField(default=dict)
```

#### 3. CaretakerPatientAssignment Model
```python
class CaretakerPatientAssignment(models.Model):
    caretaker = models.ForeignKey(Caretaker, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assignment_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_CHOICES)
    notes = models.TextField(blank=True, null=True)
```

#### 4. CaretakerTask Model
```python
class CaretakerTask(models.Model):
    caretaker = models.ForeignKey(Caretaker, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    task_type = models.CharField(max_length=20, choices=TASK_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField(blank=True, null=True)
    completed_date = models.DateTimeField(blank=True, null=True)
```

#### 5. CaretakerSchedule Model
```python
class CaretakerSchedule(models.Model):
    caretaker = models.ForeignKey(Caretaker, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_CHOICES)
    notes = models.TextField(blank=True, null=True)
```

## Usage Instructions

### 1. Accessing Caretaker Management

1. Navigate to the caretaker management dashboard:
   ```
   /caretaker/management
   ```

2. Ensure you have appropriate permissions (admin or manager role)

### 2. Adding a New Caretaker

1. Click the "Add Caretaker" button in the management dashboard
2. Fill out the comprehensive registration form:
   - Personal Information (name, email, phone, etc.)
   - Professional Information (title, license, experience)
   - Account Information (password, confirm password)
3. Submit the form to create the caretaker account
4. The system will automatically create a profile for the new caretaker

### 3. Editing Caretaker Information

1. Click the "Edit" button (pencil icon) next to any caretaker in the table
2. Modify the desired fields in the edit form
3. Submit to update the caretaker information
4. Note: Email address cannot be changed for security reasons

### 4. Viewing Caretaker Details

1. Click the "View" button (eye icon) next to any caretaker
2. Navigate through the different tabs:
   - **Overview**: Personal and professional information
   - **Assignments**: Patient assignments and relationships
   - **Tasks**: Task history and current assignments
   - **Schedule**: Work schedule and availability

### 5. Managing Caretaker Status

1. Use the toggle button (play/pause icon) to activate/deactivate caretakers
2. Inactive caretakers cannot log in or access the system
3. Status changes are logged for audit purposes

### 6. Deleting Caretakers

1. Click the "Delete" button (trash icon) next to a caretaker
2. Confirm the deletion in the popup dialog
3. **Warning**: This action is irreversible and will remove all associated data

## Setup and Configuration

### 1. Backend Setup

Ensure the caretakers app is properly configured in your Django settings:

```python
# settings.py
INSTALLED_APPS = [
    # ... other apps
    'caretakers',
]

# URL Configuration
urlpatterns = [
    # ... other patterns
    path('api/caretakers/', include('caretakers.urls')),
]
```

### 2. Frontend Setup

1. Ensure the new components are properly imported in your routing configuration
2. Add the management routes to your React router:

```javascript
// App.js or router configuration
import CaretakerManagement from './pages/caretaker/CaretakerManagement';
import CaretakerDetails from './pages/caretaker/CaretakerDetails';

// Routes
<Route path="/caretaker/management" element={<CaretakerManagement />} />
<Route path="/caretaker/management/:id" element={<CaretakerDetails />} />
```

### 3. Permissions Configuration

Set up appropriate permissions for caretaker management:

```python
# permissions.py
class CanManageCaretakers(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.has_perm('caretakers.manage_caretakers')
```

### 4. Environment Variables

Ensure the following environment variables are configured:

```bash
# .env
MEDIA_URL=/media/
MEDIA_ROOT=media/
STATIC_URL=/static/
STATIC_ROOT=static/
```

## Security Considerations

### 1. Authentication and Authorization

- All management endpoints require authentication
- Implement role-based access control (RBAC)
- Regular session management and token validation

### 2. Data Protection

- Encrypt sensitive information (passwords, personal data)
- Implement proper data validation and sanitization
- Regular security audits and updates

### 3. Audit Logging

- Log all management operations
- Track user actions for compliance
- Maintain audit trails for sensitive operations

### 4. Input Validation

- Validate all form inputs on both frontend and backend
- Implement CSRF protection
- Use parameterized queries to prevent SQL injection

### 5. File Upload Security

- Validate file types and sizes for profile pictures
- Implement secure file storage
- Scan uploaded files for malware

## Troubleshooting

### Common Issues

1. **Permission Denied Errors**
   - Check user permissions and roles
   - Verify authentication token is valid
   - Ensure proper API endpoint access

2. **Form Validation Errors**
   - Check required field validation
   - Verify data format (dates, emails, etc.)
   - Review error messages for specific issues

3. **API Connection Issues**
   - Verify backend server is running
   - Check API endpoint URLs
   - Review network connectivity

4. **Image Upload Issues**
   - Check file size limits
   - Verify supported file formats
   - Ensure proper media directory permissions

### Support

For technical support or feature requests, please contact the development team or create an issue in the project repository.

## Future Enhancements

### Planned Features

1. **Bulk Operations**
   - Bulk import/export of caretaker data
   - Mass status updates
   - Batch assignment operations

2. **Advanced Analytics**
   - Performance metrics and reports
   - Workload analysis
   - Efficiency tracking

3. **Integration Features**
   - Calendar integration
   - Email notifications
   - Mobile app support

4. **Enhanced Security**
   - Two-factor authentication
   - Advanced audit logging
   - Compliance reporting

### API Versioning

The API endpoints are designed to support versioning for future updates:

```
/api/v1/caretakers/management/
/api/v2/caretakers/management/
```

This ensures backward compatibility while allowing for feature enhancements. 