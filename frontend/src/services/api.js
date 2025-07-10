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
    ...(token && { 'Authorization': `Token ${token}` })
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