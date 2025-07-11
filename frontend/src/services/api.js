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