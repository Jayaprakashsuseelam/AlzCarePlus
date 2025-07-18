// clinicApi.js - API service for clinic management

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ClinicApiService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/clinics`;
  }

  // Get auth token from localStorage
  getAuthToken() {
    return localStorage.getItem('clinicToken');
  }

  // Set auth headers
  getHeaders() {
    const token = this.getAuthToken();
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  // Handle API responses
  async handleResponse(response) {
    if (response.ok) {
      return await response.json();
    } else {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
  }

  // Authentication
  async login(credentials) {
    const response = await fetch(`${this.baseURL}/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    return this.handleResponse(response);
  }

  async register(clinicData) {
    const response = await fetch(`${this.baseURL}/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(clinicData),
    });
    return this.handleResponse(response);
  }

  async refreshToken(refreshToken) {
    const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });
    return this.handleResponse(response);
  }

  // Profile Management
  async getProfile() {
    const response = await fetch(`${this.baseURL}/profile/`, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async updateProfile(profileData) {
    const response = await fetch(`${this.baseURL}/profile/`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(profileData),
    });
    return this.handleResponse(response);
  }

  // Dashboard
  async getDashboard() {
    const response = await fetch(`${this.baseURL}/dashboard/`, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async getStatistics() {
    const response = await fetch(`${this.baseURL}/statistics/`, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  // Staff Management
  async getStaff(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${this.baseURL}/staff/?${queryString}` : `${this.baseURL}/staff/`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async getStaffMember(staffId) {
    const response = await fetch(`${this.baseURL}/staff/${staffId}/`, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async createStaff(staffData) {
    const response = await fetch(`${this.baseURL}/staff/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(staffData),
    });
    return this.handleResponse(response);
  }

  async updateStaff(staffId, staffData) {
    const response = await fetch(`${this.baseURL}/staff/${staffId}/`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(staffData),
    });
    return this.handleResponse(response);
  }

  async deleteStaff(staffId) {
    const response = await fetch(`${this.baseURL}/staff/${staffId}/`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  // Patient Management
  async getPatients(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${this.baseURL}/patients/?${queryString}` : `${this.baseURL}/patients/`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async getPatient(patientId) {
    const response = await fetch(`${this.baseURL}/patients/${patientId}/`, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async createPatient(patientData) {
    const response = await fetch(`${this.baseURL}/patients/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(patientData),
    });
    return this.handleResponse(response);
  }

  async updatePatient(patientId, patientData) {
    const response = await fetch(`${this.baseURL}/patients/${patientId}/`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(patientData),
    });
    return this.handleResponse(response);
  }

  async deletePatient(patientId) {
    const response = await fetch(`${this.baseURL}/patients/${patientId}/`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async searchPatients(searchTerm) {
    const response = await fetch(`${this.baseURL}/search-patients/?search=${encodeURIComponent(searchTerm)}`, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  // Appointment Management
  async getAppointments(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${this.baseURL}/appointments/?${queryString}` : `${this.baseURL}/appointments/`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async getAppointment(appointmentId) {
    const response = await fetch(`${this.baseURL}/appointments/${appointmentId}/`, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async createAppointment(appointmentData) {
    const response = await fetch(`${this.baseURL}/appointments/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(appointmentData),
    });
    return this.handleResponse(response);
  }

  async updateAppointment(appointmentId, appointmentData) {
    const response = await fetch(`${this.baseURL}/appointments/${appointmentId}/`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(appointmentData),
    });
    return this.handleResponse(response);
  }

  async deleteAppointment(appointmentId) {
    const response = await fetch(`${this.baseURL}/appointments/${appointmentId}/`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async checkInAppointment(appointmentId) {
    const response = await fetch(`${this.baseURL}/appointments/${appointmentId}/check-in/`, {
      method: 'POST',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async checkOutAppointment(appointmentId) {
    const response = await fetch(`${this.baseURL}/appointments/${appointmentId}/check-out/`, {
      method: 'POST',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  // Medical Records
  async getMedicalRecords(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${this.baseURL}/medical-records/?${queryString}` : `${this.baseURL}/medical-records/`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async getMedicalRecord(recordId) {
    const response = await fetch(`${this.baseURL}/medical-records/${recordId}/`, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async createMedicalRecord(recordData) {
    const response = await fetch(`${this.baseURL}/medical-records/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(recordData),
    });
    return this.handleResponse(response);
  }

  async updateMedicalRecord(recordId, recordData) {
    const response = await fetch(`${this.baseURL}/medical-records/${recordId}/`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(recordData),
    });
    return this.handleResponse(response);
  }

  async deleteMedicalRecord(recordId) {
    const response = await fetch(`${this.baseURL}/medical-records/${recordId}/`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  // Schedule Management
  async getSchedule(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${this.baseURL}/schedule/?${queryString}` : `${this.baseURL}/schedule/`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async getScheduleEntry(entryId) {
    const response = await fetch(`${this.baseURL}/schedule/${entryId}/`, {
      method: 'GET',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async createScheduleEntry(scheduleData) {
    const response = await fetch(`${this.baseURL}/schedule/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(scheduleData),
    });
    return this.handleResponse(response);
  }

  async updateScheduleEntry(entryId, scheduleData) {
    const response = await fetch(`${this.baseURL}/schedule/${entryId}/`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(scheduleData),
    });
    return this.handleResponse(response);
  }

  async deleteScheduleEntry(entryId) {
    const response = await fetch(`${this.baseURL}/schedule/${entryId}/`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  // Utility methods
  async uploadFile(file, type = 'document') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);

    const response = await fetch(`${this.baseURL}/upload/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.getAuthToken()}`,
      },
      body: formData,
    });
    return this.handleResponse(response);
  }

  // Logout
  logout() {
    localStorage.removeItem('clinicToken');
    localStorage.removeItem('clinicRefreshToken');
    localStorage.removeItem('clinicData');
  }

  // Check if user is authenticated
  isAuthenticated() {
    return !!this.getAuthToken();
  }

  // Get clinic data from localStorage
  getClinicData() {
    const data = localStorage.getItem('clinicData');
    return data ? JSON.parse(data) : null;
  }
}

// Create and export a singleton instance
const clinicApi = new ClinicApiService();
export default clinicApi; 