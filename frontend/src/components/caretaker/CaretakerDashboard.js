import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { caretakerAPI, authUtils, handleAPIError } from '../../services/api';
import './CaretakerDashboard.css';

const CaretakerDashboard = () => {
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [caretakerData, setCaretakerData] = useState(null);

  useEffect(() => {
    const token = authUtils.getToken();
    if (!token) {
      navigate('/caretaker/login');
      return;
    }

    const storedData = localStorage.getItem('caretakerData');
    if (storedData) {
      setCaretakerData(JSON.parse(storedData));
    }

    fetchDashboardData();
  }, [navigate]);

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      const response = await caretakerAPI.getDashboard();
      setDashboardData(response);
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setError(errorMessage);
      if (errorMessage.includes('unauthorized') || errorMessage.includes('token')) {
        authUtils.removeToken();
        navigate('/caretaker/login');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    authUtils.removeToken();
    localStorage.removeItem('caretakerData');
    navigate('/caretaker/login');
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

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return 'urgent';
      case 'high': return 'high';
      case 'medium': return 'medium';
      case 'low': return 'low';
      default: return 'medium';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'pending';
      case 'in_progress': return 'in_progress';
      case 'completed': return 'completed';
      default: return 'pending';
    }
  };

  if (isLoading) {
    return (
      <div className="dashboard-container">
        <div className="dashboard-header">
          <div className="header-content">
            <div className="header-left">
              <h1>Loading...</h1>
            </div>
          </div>
        </div>
        <div className="dashboard-content">
          <div className="stats-grid">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="stat-card loading-skeleton" style={{ height: '120px' }}></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="dashboard-header">
          <div className="header-content">
            <div className="header-left">
              <h1>Error</h1>
              <p>{error}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Header */}
      <div className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <h1>Welcome back, {caretakerData?.first_name || 'Caretaker'}!</h1>
            <p>Here's your daily overview</p>
          </div>
          <div className="header-right">
            <div className="user-info">
              <div className="user-avatar">
                {caretakerData?.first_name?.charAt(0) || 'C'}
              </div>
              <span>{caretakerData?.first_name} {caretakerData?.last_name}</span>
            </div>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Dashboard Content */}
      <div className="dashboard-content">
        {/* Statistics Grid */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-header">
              <span className="stat-title">Total Patients</span>
              <div className="stat-icon patients">👥</div>
            </div>
            <div className="stat-value">{dashboardData?.total_patients || 0}</div>
            <div className="stat-description">Assigned patients</div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <span className="stat-title">Active Tasks</span>
              <div className="stat-icon tasks">📋</div>
            </div>
            <div className="stat-value">{dashboardData?.active_tasks || 0}</div>
            <div className="stat-description">Pending and in progress</div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <span className="stat-title">Completed Today</span>
              <div className="stat-icon completed">✅</div>
            </div>
            <div className="stat-value">{dashboardData?.completed_tasks_today || 0}</div>
            <div className="stat-description">Tasks completed today</div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <span className="stat-title">Appointments</span>
              <div className="stat-icon appointments">📅</div>
            </div>
            <div className="stat-value">{dashboardData?.upcoming_appointments || 0}</div>
            <div className="stat-description">Upcoming appointments</div>
          </div>
        </div>

        {/* Main Dashboard Grid */}
        <div className="dashboard-grid">
          {/* Main Content */}
          <div className="main-content">
            {/* Recent Tasks */}
            <div className="section-card">
              <div className="section-header">
                <h2 className="section-title">Recent Tasks</h2>
                <a href="/caretaker/tasks" className="section-action">View All</a>
              </div>
              
              {dashboardData?.recent_tasks?.length > 0 ? (
                <div className="task-list">
                  {dashboardData.recent_tasks.map((task) => (
                    <div key={task.id} className="task-item">
                      <div className={`task-priority ${getPriorityColor(task.priority)}`}></div>
                      <div className="task-content">
                        <div className="task-title">{task.title}</div>
                        <div className="task-details">
                          <div className="task-patient">
                            <span>👤</span>
                            {task.patient?.first_name} {task.patient?.last_name}
                          </div>
                          <div className="task-time">
                            <span>🕒</span>
                            {task.scheduled_date} {task.scheduled_time && formatTime(task.scheduled_time)}
                          </div>
                        </div>
                      </div>
                      <div className={`task-status ${getStatusColor(task.status)}`}>
                        {task.status.replace('_', ' ')}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  <div className="empty-state-icon">📋</div>
                  <div className="empty-state-title">No tasks yet</div>
                  <div className="empty-state-description">
                    You don't have any tasks assigned yet. Check back later for updates.
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="sidebar">
            {/* Assigned Patients */}
            <div className="section-card">
              <div className="section-header">
                <h2 className="section-title">My Patients</h2>
                <a href="/caretaker/patients" className="section-action">View All</a>
              </div>
              
              {dashboardData?.assigned_patients?.length > 0 ? (
                <div className="patient-list">
                  {dashboardData.assigned_patients.slice(0, 5).map((patient) => (
                    <div key={patient.id} className="patient-item">
                      <div className="patient-avatar">
                        {patient.first_name?.charAt(0) || 'P'}
                      </div>
                      <div className="patient-info">
                        <div className="patient-name">
                          {patient.first_name} {patient.last_name}
                        </div>
                        <div className="patient-details">
                          {patient.age} years • {patient.gender}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  <div className="empty-state-icon">👥</div>
                  <div className="empty-state-title">No patients assigned</div>
                  <div className="empty-state-description">
                    You haven't been assigned to any patients yet.
                  </div>
                </div>
              )}
            </div>

            {/* Today's Schedule */}
            <div className="section-card">
              <div className="section-header">
                <h2 className="section-title">Today's Schedule</h2>
                <a href="/caretaker/schedule" className="section-action">View All</a>
              </div>
              
              {dashboardData?.today_schedule?.length > 0 ? (
                <div className="schedule-list">
                  {dashboardData.today_schedule.map((schedule) => (
                    <div key={schedule.id} className="schedule-item">
                      <div className="schedule-time">
                        {formatTime(schedule.start_time)} - {formatTime(schedule.end_time)}
                      </div>
                      <div className="schedule-type">{schedule.schedule_type}</div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  <div className="empty-state-icon">📅</div>
                  <div className="empty-state-title">No schedule for today</div>
                  <div className="empty-state-description">
                    You don't have any scheduled shifts today.
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CaretakerDashboard; 