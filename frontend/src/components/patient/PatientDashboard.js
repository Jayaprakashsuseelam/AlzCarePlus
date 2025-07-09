import React, { useState } from 'react';
import './PatientDashboard.css';

const PatientDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');

  // Mock data - in a real app, this would come from API
  const patientData = {
    name: 'John Doe',
    age: 65,
    lastVisit: '2024-01-15',
    nextAppointment: '2024-02-20',
    medications: ['Donepezil', 'Memantine', 'Vitamin D'],
    recentTests: [
      { name: 'Cognitive Assessment', date: '2024-01-15', result: 'Mild Cognitive Impairment' },
      { name: 'Blood Test', date: '2024-01-10', result: 'Normal' }
    ]
  };

  const renderOverview = () => (
    <div className="dashboard-section">
      <div className="welcome-card">
        <h2>Welcome back, {patientData.name}!</h2>
        <p>Here's your health overview for today</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <h3>Next Appointment</h3>
            <p>{patientData.nextAppointment}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💊</div>
          <div className="stat-content">
            <h3>Active Medications</h3>
            <p>{patientData.medications.length} medications</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>Last Assessment</h3>
            <p>{patientData.lastVisit}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <h3>Health Score</h3>
            <p>85/100</p>
          </div>
        </div>
      </div>

      <div className="quick-actions">
        <h3>Quick Actions</h3>
        <div className="action-buttons">
          <button className="action-btn primary">Schedule Appointment</button>
          <button className="action-btn secondary">View Test Results</button>
          <button className="action-btn secondary">Update Symptoms</button>
          <button className="action-btn secondary">Contact Care Team</button>
        </div>
      </div>
    </div>
  );

  const renderMedications = () => (
    <div className="dashboard-section">
      <h2>Current Medications</h2>
      <div className="medications-list">
        {patientData.medications.map((med, index) => (
          <div key={index} className="medication-card">
            <div className="medication-info">
              <h3>{med}</h3>
              <p>Prescribed for Alzheimer's management</p>
            </div>
            <div className="medication-status">
              <span className="status active">Active</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderAppointments = () => (
    <div className="dashboard-section">
      <h2>Upcoming Appointments</h2>
      <div className="appointment-card">
        <div className="appointment-date">
          <div className="date-circle">
            <span className="day">20</span>
            <span className="month">FEB</span>
          </div>
        </div>
        <div className="appointment-details">
          <h3>Dr. Sarah Johnson - Neurology</h3>
          <p>Follow-up consultation</p>
          <p className="appointment-time">10:00 AM - 11:00 AM</p>
        </div>
        <div className="appointment-actions">
          <button className="btn-secondary">Reschedule</button>
          <button className="btn-primary">Join Meeting</button>
        </div>
      </div>
    </div>
  );

  const renderTestResults = () => (
    <div className="dashboard-section">
      <h2>Recent Test Results</h2>
      <div className="test-results">
        {patientData.recentTests.map((test, index) => (
          <div key={index} className="test-card">
            <div className="test-header">
              <h3>{test.name}</h3>
              <span className="test-date">{test.date}</span>
            </div>
            <div className="test-result">
              <p><strong>Result:</strong> {test.result}</p>
            </div>
            <button className="btn-secondary">View Details</button>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="patient-dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Patient Dashboard</h1>
          <div className="user-info">
            <span>Welcome, {patientData.name}</span>
            <button className="logout-btn">Logout</button>
          </div>
        </div>
      </header>

      <nav className="dashboard-nav">
        <button 
          className={`nav-tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`nav-tab ${activeTab === 'medications' ? 'active' : ''}`}
          onClick={() => setActiveTab('medications')}
        >
          Medications
        </button>
        <button 
          className={`nav-tab ${activeTab === 'appointments' ? 'active' : ''}`}
          onClick={() => setActiveTab('appointments')}
        >
          Appointments
        </button>
        <button 
          className={`nav-tab ${activeTab === 'test-results' ? 'active' : ''}`}
          onClick={() => setActiveTab('test-results')}
        >
          Test Results
        </button>
      </nav>

      <main className="dashboard-content">
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'medications' && renderMedications()}
        {activeTab === 'appointments' && renderAppointments()}
        {activeTab === 'test-results' && renderTestResults()}
      </main>
    </div>
  );
};

export default PatientDashboard; 