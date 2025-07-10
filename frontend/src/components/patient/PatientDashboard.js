import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { patientAPI, authAPI, authUtils, handleAPIError } from '../../services/api';
import './PatientDashboard.css';

const PatientDashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [dashboardData, setDashboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      const data = await patientAPI.getDashboard();
      setDashboardData(data);
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      authUtils.clearAuth();
      navigate('/patient/login');
    } catch (error) {
      console.error('Logout error:', error);
      // Even if logout fails, clear local data and redirect
      authUtils.clearAuth();
      navigate('/patient/login');
    }
  };

  if (isLoading) {
    return (
      <div className="dashboard-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="error-message">
          <h2>Error Loading Dashboard</h2>
          <p>{error}</p>
          <button onClick={loadDashboardData} className="retry-button">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="dashboard-container">
        <div className="error-message">
          <h2>No Data Available</h2>
          <p>Unable to load dashboard data.</p>
        </div>
      </div>
    );
  }

  const { patient, stats, recent_activity, medications, upcoming_appointments } = dashboardData;

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="welcome-section">
            <h1>Welcome back, {patient.first_name}!</h1>
            <p>Here's your health overview for today</p>
          </div>
          <div className="header-actions">
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <h3>{stats.total_appointments}</h3>
            <p>Total Appointments</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⏰</div>
          <div className="stat-content">
            <h3>{stats.upcoming_appointments}</h3>
            <p>Upcoming Appointments</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>{stats.completed_tests}</h3>
            <p>Completed Tests</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">💊</div>
          <div className="stat-content">
            <h3>{stats.active_medications}</h3>
            <p>Active Medications</p>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="dashboard-tabs">
        <button
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab-button ${activeTab === 'medications' ? 'active' : ''}`}
          onClick={() => setActiveTab('medications')}
        >
          Medications
        </button>
        <button
          className={`tab-button ${activeTab === 'appointments' ? 'active' : ''}`}
          onClick={() => setActiveTab('appointments')}
        >
          Appointments
        </button>
        <button
          className={`tab-button ${activeTab === 'test-results' ? 'active' : ''}`}
          onClick={() => setActiveTab('test-results')}
        >
          Test Results
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="content-grid">
              <div className="content-card">
                <h3>Recent Activity</h3>
                <div className="activity-list">
                  {recent_activity.map((activity, index) => (
                    <div key={index} className="activity-item">
                      <div className="activity-icon">
                        {activity.type === 'appointment' && '📅'}
                        {activity.type === 'test_result' && '📊'}
                        {activity.type === 'medication' && '💊'}
                      </div>
                      <div className="activity-content">
                        <h4>{activity.title}</h4>
                        <p>{activity.date} {activity.time && `• ${activity.time}`}</p>
                        {activity.result && <p className="result">{activity.result}</p>}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="content-card">
                <h3>Quick Actions</h3>
                <div className="quick-actions">
                  <button className="action-button">
                    📅 Schedule Appointment
                  </button>
                  <button className="action-button">
                    💊 Request Refill
                  </button>
                  <button className="action-button">
                    📞 Contact Doctor
                  </button>
                  <button className="action-button">
                    📋 Update Profile
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'medications' && (
          <div className="medications-tab">
            <div className="content-card">
              <h3>Current Medications</h3>
              <div className="medications-list">
                {medications.map((medication, index) => (
                  <div key={index} className="medication-item">
                    <div className="medication-info">
                      <h4>{medication.name}</h4>
                      <p className="dosage">{medication.dosage}</p>
                      <p className="frequency">{medication.frequency}</p>
                    </div>
                    <div className="medication-status">
                      <span className={`status-badge ${medication.status}`}>
                        {medication.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'appointments' && (
          <div className="appointments-tab">
            <div className="content-card">
              <h3>Upcoming Appointments</h3>
              <div className="appointments-list">
                {upcoming_appointments.map((appointment, index) => (
                  <div key={index} className="appointment-item">
                    <div className="appointment-info">
                      <h4>{appointment.doctor}</h4>
                      <p className="specialty">{appointment.specialty}</p>
                      <p className="date-time">
                        {appointment.date} • {appointment.time}
                      </p>
                      <p className="type">{appointment.type}</p>
                    </div>
                    <div className="appointment-actions">
                      <button className="action-button small">Reschedule</button>
                      <button className="action-button small secondary">Cancel</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'test-results' && (
          <div className="test-results-tab">
            <div className="content-card">
              <h3>Recent Test Results</h3>
              <div className="test-results-list">
                <div className="test-result-item">
                  <div className="test-info">
                    <h4>Cognitive Assessment</h4>
                    <p className="date">January 15, 2024</p>
                    <p className="result">Mild Cognitive Impairment</p>
                  </div>
                  <div className="test-actions">
                    <button className="action-button small">View Details</button>
                    <button className="action-button small secondary">Download</button>
                  </div>
                </div>
                <div className="test-result-item">
                  <div className="test-info">
                    <h4>Blood Work</h4>
                    <p className="date">January 10, 2024</p>
                    <p className="result">Normal Range</p>
                  </div>
                  <div className="test-actions">
                    <button className="action-button small">View Details</button>
                    <button className="action-button small secondary">Download</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PatientDashboard; 