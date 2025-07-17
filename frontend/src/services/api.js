// API service for handling backend communication

const API_BASE_URL = 'http://localhost:8000/api';

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

// Helper function to get auth headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('authToken');
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
};

// Authentication API calls
export const authAPI = {
  // Patient Registration
  register: async (patientData) => {
    const response = await fetch(`${API_BASE_URL}/patients/auth/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(patientData),
    });
    return handleResponse(response);
  },

  // Patient Login
  login: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/patients/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    return handleResponse(response);
  },

  // Patient Logout
  logout: async () => {
    const response = await fetch(`${API_BASE_URL}/patients/auth/logout/`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Password Reset Request
  resetPassword: async (email) => {
    const response = await fetch(`${API_BASE_URL}/patients/auth/reset-password/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    });
    return handleResponse(response);
  },

  // Caretaker Registration
  caretakerRegister: async (caretakerData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(caretakerData),
    });
    return handleResponse(response);
  },

  // Caretaker Login
  caretakerLogin: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    return handleResponse(response);
  },
};

// Patient Profile API calls
export const patientAPI = {
  // Get patient profile
  getProfile: async () => {
    const response = await fetch(`${API_BASE_URL}/patients/profile/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Update patient profile
  updateProfile: async (profileData) => {
    const response = await fetch(`${API_BASE_URL}/patients/profile/update/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(profileData),
    });
    return handleResponse(response);
  },

  // Get patient dashboard data
  getDashboard: async () => {
    const response = await fetch(`${API_BASE_URL}/patients/dashboard/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },
};

// Caretaker API calls
export const caretakerAPI = {
  // Get caretaker profile
  getProfile: async () => {
    const response = await fetch(`${API_BASE_URL}/caretakers/profile/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Update caretaker profile
  updateProfile: async (profileData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/profile/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(profileData),
    });
    return handleResponse(response);
  },

  // Get caretaker dashboard data
  getDashboard: async () => {
    const response = await fetch(`${API_BASE_URL}/caretakers/dashboard/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Get assigned patients
  getPatients: async () => {
    const response = await fetch(`${API_BASE_URL}/caretakers/patients/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Get tasks
  getTasks: async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/caretakers/tasks/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Create task
  createTask: async (taskData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/tasks/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(taskData),
    });
    return handleResponse(response);
  },

  // Update task
  updateTask: async (taskId, taskData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/tasks/${taskId}/update/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(taskData),
    });
    return handleResponse(response);
  },

  // Get schedule
  getSchedule: async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/caretakers/schedule/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Create schedule entry
  createSchedule: async (scheduleData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/schedule/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(scheduleData),
    });
    return handleResponse(response);
  },

  // Get task statistics
  getTaskStatistics: async () => {
    const response = await fetch(`${API_BASE_URL}/caretakers/task-statistics/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Caretaker Management (Admin/Management endpoints)
  getAllCaretakers: async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/caretakers/management/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  getCaretakerById: async (caretakerId) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  createCaretaker: async (caretakerData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(caretakerData),
    });
    return handleResponse(response);
  },

  updateCaretaker: async (caretakerId, caretakerData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(caretakerData),
    });
    return handleResponse(response);
  },

  deleteCaretaker: async (caretakerId) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Caretaker Profile Management
  getCaretakerProfile: async (caretakerId) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/profile/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  updateCaretakerProfile: async (caretakerId, profileData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/profile/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(profileData),
    });
    return handleResponse(response);
  },

  // Caretaker Assignments
  getCaretakerAssignments: async (caretakerId, filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/assignments/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  createCaretakerAssignment: async (caretakerId, assignmentData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/assignments/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(assignmentData),
    });
    return handleResponse(response);
  },

  updateCaretakerAssignment: async (caretakerId, assignmentId, assignmentData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/assignments/${assignmentId}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(assignmentData),
    });
    return handleResponse(response);
  },

  deleteCaretakerAssignment: async (caretakerId, assignmentId) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/assignments/${assignmentId}/`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Caretaker Tasks (Management)
  getCaretakerTasks: async (caretakerId, filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/tasks/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  createCaretakerTask: async (caretakerId, taskData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/tasks/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(taskData),
    });
    return handleResponse(response);
  },

  updateCaretakerTask: async (caretakerId, taskId, taskData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/tasks/${taskId}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(taskData),
    });
    return handleResponse(response);
  },

  deleteCaretakerTask: async (caretakerId, taskId) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/tasks/${taskId}/`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Caretaker Schedule (Management)
  getCaretakerSchedule: async (caretakerId, filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/schedule/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  createCaretakerSchedule: async (caretakerId, scheduleData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/schedule/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(scheduleData),
    });
    return handleResponse(response);
  },

  updateCaretakerSchedule: async (caretakerId, scheduleId, scheduleData) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/schedule/${scheduleId}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(scheduleData),
    });
    return handleResponse(response);
  },

  deleteCaretakerSchedule: async (caretakerId, scheduleId) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/schedule/${scheduleId}/`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Caretaker Statistics
  getCaretakerStatistics: async (caretakerId) => {
    const response = await fetch(`${API_BASE_URL}/caretakers/management/${caretakerId}/statistics/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },
};

// Clinic API calls
export const clinicAPI = {
  // Authentication
  register: async (clinicData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(clinicData),
    });
    return handleResponse(response);
  },

  login: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/clinics/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    return handleResponse(response);
  },

  // Profile
  getProfile: async () => {
    const response = await fetch(`${API_BASE_URL}/clinics/profile/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  updateProfile: async (profileData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/profile/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(profileData),
    });
    return handleResponse(response);
  },

  // Dashboard
  getDashboard: async () => {
    const response = await fetch(`${API_BASE_URL}/clinics/dashboard/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Staff Management
  getStaff: async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/clinics/staff/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  createStaff: async (staffData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/staff/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(staffData),
    });
    return handleResponse(response);
  },

  updateStaff: async (staffId, staffData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/staff/${staffId}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(staffData),
    });
    return handleResponse(response);
  },

  deleteStaff: async (staffId) => {
    const response = await fetch(`${API_BASE_URL}/clinics/staff/${staffId}/`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Patient Management
  getPatients: async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/clinics/patients/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  createPatient: async (patientData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/patients/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(patientData),
    });
    return handleResponse(response);
  },

  updatePatient: async (patientId, patientData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/patients/${patientId}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(patientData),
    });
    return handleResponse(response);
  },

  deletePatient: async (patientId) => {
    const response = await fetch(`${API_BASE_URL}/clinics/patients/${patientId}/`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  searchPatients: async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/clinics/search-patients/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Appointment Management
  getAppointments: async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/clinics/appointments/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  createAppointment: async (appointmentData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/appointments/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(appointmentData),
    });
    return handleResponse(response);
  },

  updateAppointment: async (appointmentId, appointmentData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/appointments/${appointmentId}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(appointmentData),
    });
    return handleResponse(response);
  },

  deleteAppointment: async (appointmentId) => {
    const response = await fetch(`${API_BASE_URL}/clinics/appointments/${appointmentId}/`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  checkInAppointment: async (appointmentId) => {
    const response = await fetch(`${API_BASE_URL}/clinics/appointments/${appointmentId}/check-in/`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  checkOutAppointment: async (appointmentId) => {
    const response = await fetch(`${API_BASE_URL}/clinics/appointments/${appointmentId}/check-out/`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Medical Records
  getMedicalRecords: async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/clinics/medical-records/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  createMedicalRecord: async (recordData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/medical-records/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(recordData),
    });
    return handleResponse(response);
  },

  updateMedicalRecord: async (recordId, recordData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/medical-records/${recordId}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(recordData),
    });
    return handleResponse(response);
  },

  deleteMedicalRecord: async (recordId) => {
    const response = await fetch(`${API_BASE_URL}/clinics/medical-records/${recordId}/`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Schedule Management
  getSchedules: async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/clinics/schedule/?${params}`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  createSchedule: async (scheduleData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/schedule/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(scheduleData),
    });
    return handleResponse(response);
  },

  updateSchedule: async (scheduleId, scheduleData) => {
    const response = await fetch(`${API_BASE_URL}/clinics/schedule/${scheduleId}/`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(scheduleData),
    });
    return handleResponse(response);
  },

  deleteSchedule: async (scheduleId) => {
    const response = await fetch(`${API_BASE_URL}/clinics/schedule/${scheduleId}/`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  // Statistics
  getStatistics: async () => {
    const response = await fetch(`${API_BASE_URL}/clinics/statistics/`, {
      method: 'GET',
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },
};

// Utility functions
export const authUtils = {
  // Store authentication token
  setToken: (token) => {
    localStorage.setItem('authToken', token);
  },

  // Get authentication token
  getToken: () => {
    return localStorage.getItem('authToken');
  },

  // Remove authentication token
  removeToken: () => {
    localStorage.removeItem('authToken');
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('authToken');
  },

  // Clear all auth data
  clearAuth: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
  },
};

// Error handling
export const handleAPIError = (error) => {
  console.error('API Error:', error);
  
  if (error.message.includes('401')) {
    authUtils.clearAuth();
    window.location.href = '/patient/login';
    return 'Session expired. Please login again.';
  }
  
  return error.message || 'An unexpected error occurred.';
}; 