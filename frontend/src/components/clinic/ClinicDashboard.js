import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { clinicAPI, authUtils } from '../../services/api';
import './ClinicDashboard.css';

const ClinicDashboard = () => {
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      const data = await clinicAPI.getDashboard();
      setDashboardData(data);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    authUtils.removeToken();
    localStorage.removeItem('clinicData');
    navigate('/clinic/login');
  };

  const formatTime = (timeString) => {
    if (!timeString) return '';
    const time = new Date(`2000-01-01T${timeString}`);
    return time.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  };

  const getStatusClass = (status) => {
    const statusMap = {
      'scheduled': 'scheduled',
      'confirmed': 'confirmed',
      'in_progress': 'in-progress',
      'completed': 'completed',
      'cancelled': 'cancelled',
      'no_show': 'cancelled',
      'rescheduled': 'scheduled'
    };
    return statusMap[status] || 'scheduled';
  };

  const getInitials = (firstName, lastName) => {
    const first = firstName ? firstName.charAt(0) : '';
    const last = lastName ? lastName.charAt(0) : '';
    return (first + last).toUpperCase();
  };

  if (isLoading) {
    return (
      <div className="clinic-dashboard">
        <div className="clinic-main-content">
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <div className="clinic-loading">Loading dashboard...</div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="clinic-dashboard">
        <div className="clinic-main-content">
          <div className="clinic-error-alert">
            {error}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="clinic-dashboard">
      {/* Header */}
      <div className="clinic-header">
        <div className="clinic-header-content">
          <div className="clinic-header-left">
            <h1>Clinic Dashboard</h1>
            <p>Welcome back! Here's what's happening today.</p>
          </div>
          <div className="clinic-header-right">
            <div className="clinic-user-info">
              <h3>Medical Center</h3>
              <p>Clinic Administrator</p>
            </div>
            <button className="clinic-logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="clinic-main-content">
        {/* Statistics Grid */}
        <div className="clinic-stats-grid">
          <div className="clinic-stat-card patients">
            <div className="clinic-stat-header">
              <span className="clinic-stat-title">Total Patients</span>
              <div className="clinic-stat-icon patients">👥</div>
            </div>
            <div className="clinic-stat-value">{dashboardData?.total_patients || 0}</div>
            <div className="clinic-stat-change">
              <span>↗</span>
              <span>+12% from last month</span>
            </div>
          </div>

          <div className="clinic-stat-card staff">
            <div className="clinic-stat-header">
              <span className="clinic-stat-title">Staff Members</span>
              <div className="clinic-stat-icon staff">👨‍⚕️</div>
            </div>
            <div className="clinic-stat-value">{dashboardData?.total_staff || 0}</div>
            <div className="clinic-stat-change">
              <span>↗</span>
              <span>+3 this month</span>
            </div>
          </div>

          <div className="clinic-stat-card appointments">
            <div className="clinic-stat-header">
              <span className="clinic-stat-title">Today's Appointments</span>
              <div className="clinic-stat-icon appointments">📅</div>
            </div>
            <div className="clinic-stat-value">{dashboardData?.today_appointments || 0}</div>
            <div className="clinic-stat-change">
              <span>↗</span>
              <span>+5 from yesterday</span>
            </div>
          </div>

          <div className="clinic-stat-card completed">
            <div className="clinic-stat-header">
              <span className="clinic-stat-title">Completed Today</span>
              <div className="clinic-stat-icon completed">✅</div>
            </div>
            <div className="clinic-stat-value">{dashboardData?.completed_appointments_today || 0}</div>
            <div className="clinic-stat-change">
              <span>↗</span>
              <span>85% completion rate</span>
            </div>
          </div>
        </div>

        {/* Dashboard Grid */}
        <div className="clinic-dashboard-grid">
          {/* Recent Appointments */}
          <div className="clinic-recent-appointments">
            <div className="clinic-section-header">
              <h2 className="clinic-section-title">Recent Appointments</h2>
              <a href="/clinic/appointments" className="clinic-view-all">View All</a>
            </div>
            
            {dashboardData?.recent_appointments?.length > 0 ? (
              dashboardData.recent_appointments.map((appointment) => (
                <div key={appointment.id} className="clinic-appointment-item">
                  <div className="clinic-appointment-info">
                    <h4>{appointment.patient?.patient?.first_name} {appointment.patient?.patient?.last_name}</h4>
                    <p>
                      {formatDate(appointment.scheduled_date)} at {formatTime(appointment.scheduled_time)} • 
                      {appointment.appointment_type.replace('_', ' ')} • 
                      Dr. {appointment.staff?.user?.first_name} {appointment.staff?.user?.last_name}
                    </p>
                  </div>
                  <span className={`clinic-appointment-status ${getStatusClass(appointment.status)}`}>
                    {appointment.status.replace('_', ' ')}
                  </span>
                </div>
              ))
            ) : (
              <div className="clinic-empty-state">
                <h3>No Recent Appointments</h3>
                <p>No appointments scheduled for today.</p>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="clinic-sidebar">
            {/* Today's Schedule */}
            <div className="clinic-today-schedule">
              <div className="clinic-section-header">
                <h2 className="clinic-section-title">Today's Schedule</h2>
              </div>
              
              {dashboardData?.today_schedule?.length > 0 ? (
                dashboardData.today_schedule.map((schedule) => (
                  <div key={schedule.id} className="clinic-schedule-item">
                    <div className="clinic-schedule-time">
                      {formatTime(schedule.start_time)} - {formatTime(schedule.end_time)}
                    </div>
                    <div className="clinic-schedule-info">
                      <h4>{schedule.staff?.user?.first_name} {schedule.staff?.user?.last_name}</h4>
                      <p>{schedule.department || 'General'} • {schedule.schedule_type.replace('_', ' ')}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="clinic-empty-state">
                  <h3>No Schedule</h3>
                  <p>No staff scheduled for today.</p>
                </div>
              )}
            </div>

            {/* Recent Patients */}
            <div className="clinic-recent-patients">
              <div className="clinic-section-header">
                <h2 className="clinic-section-title">Recent Patients</h2>
                <a href="/clinic/patients" className="clinic-view-all">View All</a>
              </div>
              
              {dashboardData?.recent_patients?.length > 0 ? (
                dashboardData.recent_patients.map((patient) => (
                  <div key={patient.id} className="clinic-patient-item">
                    <div className="clinic-patient-avatar">
                      {getInitials(patient.patient?.first_name, patient.patient?.last_name)}
                    </div>
                    <div className="clinic-patient-info">
                      <h4>{patient.patient?.first_name} {patient.patient?.last_name}</h4>
                      <p>Patient #{patient.patient_number} • {formatDate(patient.registration_date)}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="clinic-empty-state">
                  <h3>No Recent Patients</h3>
                  <p>No new patient registrations.</p>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="clinic-quick-actions">
              <div className="clinic-section-header">
                <h2 className="clinic-section-title">Quick Actions</h2>
              </div>
              
              <div className="clinic-action-buttons">
                <button 
                  className="clinic-action-btn"
                  onClick={() => navigate('/clinic/appointments/new')}
                >
                  <span className="clinic-action-icon">📅</span>
                  New Appointment
                </button>
                
                <button 
                  className="clinic-action-btn secondary"
                  onClick={() => navigate('/clinic/patients/new')}
                >
                  <span className="clinic-action-icon">👤</span>
                  Add Patient
                </button>
                
                <button 
                  className="clinic-action-btn tertiary"
                  onClick={() => navigate('/clinic/staff/new')}
                >
                  <span className="clinic-action-icon">👨‍⚕️</span>
                  Add Staff
                </button>
                
                <button 
                  className="clinic-action-btn quaternary"
                  onClick={() => navigate('/clinic/medical-records/new')}
                >
                  <span className="clinic-action-icon">📋</span>
                  New Record
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClinicDashboard; 