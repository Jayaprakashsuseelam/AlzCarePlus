import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { caretakerAPI, authUtils, handleAPIError } from '../../services/api';
import './CaretakerDetails.css';

const CaretakerDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [caretaker, setCaretaker] = useState(null);
  const [profile, setProfile] = useState(null);
  const [assignments, setAssignments] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [schedule, setSchedule] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const token = authUtils.getToken();
    if (!token) {
      navigate('/caretaker/login');
      return;
    }

    fetchCaretakerDetails();
  }, [id, navigate]);

  const fetchCaretakerDetails = async () => {
    try {
      setIsLoading(true);
      const [caretakerData, profileData, assignmentsData, tasksData, scheduleData] = await Promise.all([
        caretakerAPI.getCaretakerById(id),
        caretakerAPI.getCaretakerProfile(id),
        caretakerAPI.getCaretakerAssignments(id),
        caretakerAPI.getCaretakerTasks(id),
        caretakerAPI.getCaretakerSchedule(id)
      ]);

      setCaretaker(caretakerData);
      setProfile(profileData);
      setAssignments(assignmentsData);
      setTasks(tasksData);
      setSchedule(scheduleData);
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

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
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

  const getStatusBadge = (isActive) => {
    return (
      <span className={`status-badge ${isActive ? 'active' : 'inactive'}`}>
        {isActive ? 'Active' : 'Inactive'}
      </span>
    );
  };

  const getEmploymentStatusBadge = (status) => {
    const statusMap = {
      'full-time': { label: 'Full Time', class: 'full-time' },
      'part-time': { label: 'Part Time', class: 'part-time' },
      'contract': { label: 'Contract', class: 'contract' },
      'volunteer': { label: 'Volunteer', class: 'volunteer' },
      'private': { label: 'Private Practice', class: 'private' }
    };
    
    const statusInfo = statusMap[status] || { label: status, class: 'default' };
    
    return (
      <span className={`employment-badge ${statusInfo.class}`}>
        {statusInfo.label}
      </span>
    );
  };

  const getTaskStatusBadge = (status) => {
    const statusMap = {
      'pending': { label: 'Pending', class: 'pending' },
      'in_progress': { label: 'In Progress', class: 'in-progress' },
      'completed': { label: 'Completed', class: 'completed' },
      'cancelled': { label: 'Cancelled', class: 'cancelled' }
    };
    
    const statusInfo = statusMap[status] || { label: status, class: 'default' };
    
    return (
      <span className={`task-status-badge ${statusInfo.class}`}>
        {statusInfo.label}
      </span>
    );
  };

  const getTaskPriorityBadge = (priority) => {
    const priorityMap = {
      'low': { label: 'Low', class: 'low' },
      'medium': { label: 'Medium', class: 'medium' },
      'high': { label: 'High', class: 'high' },
      'urgent': { label: 'Urgent', class: 'urgent' }
    };
    
    const priorityInfo = priorityMap[priority] || { label: priority, class: 'default' };
    
    return (
      <span className={`priority-badge ${priorityInfo.class}`}>
        {priorityInfo.label}
      </span>
    );
  };

  if (isLoading) {
    return (
      <div className="caretaker-details">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading caretaker details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="caretaker-details">
        <div className="error-container">
          <i className="fas fa-exclamation-triangle"></i>
          <h3>Error Loading Caretaker</h3>
          <p>{error}</p>
          <button onClick={() => navigate('/caretaker/management')} className="back-btn">
            Back to Management
          </button>
        </div>
      </div>
    );
  }

  if (!caretaker) {
    return (
      <div className="caretaker-details">
        <div className="not-found">
          <i className="fas fa-user-slash"></i>
          <h3>Caretaker Not Found</h3>
          <p>The requested caretaker could not be found.</p>
          <button onClick={() => navigate('/caretaker/management')} className="back-btn">
            Back to Management
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="caretaker-details">
      {/* Header */}
      <div className="caretaker-header">
        <div className="header-content">
          <button onClick={() => navigate('/caretaker/management')} className="back-btn">
            <i className="fas fa-arrow-left"></i>
            Back to Management
          </button>
          <div className="caretaker-info">
            <div className="caretaker-avatar">
              {caretaker.profile_picture ? (
                <img src={caretaker.profile_picture} alt={caretaker.full_name} />
              ) : (
                <div className="avatar-placeholder">
                  {caretaker.first_name?.[0]}{caretaker.last_name?.[0]}
                </div>
              )}
            </div>
            <div className="caretaker-basic-info">
              <h1>{caretaker.full_name}</h1>
              <p className="professional-title">{caretaker.professional_title}</p>
              <div className="caretaker-badges">
                {getStatusBadge(caretaker.is_active)}
                {getEmploymentStatusBadge(caretaker.employment_status)}
              </div>
            </div>
          </div>
        </div>
        <div className="header-actions">
          <button 
            className="edit-btn"
            onClick={() => navigate(`/caretaker/management/edit/${id}`)}
          >
            <i className="fas fa-edit"></i>
            Edit Caretaker
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="tabs-navigation">
        <button 
          className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          <i className="fas fa-user"></i>
          Overview
        </button>
        <button 
          className={`tab-btn ${activeTab === 'assignments' ? 'active' : ''}`}
          onClick={() => setActiveTab('assignments')}
        >
          <i className="fas fa-users"></i>
          Patient Assignments ({assignments.length})
        </button>
        <button 
          className={`tab-btn ${activeTab === 'tasks' ? 'active' : ''}`}
          onClick={() => setActiveTab('tasks')}
        >
          <i className="fas fa-tasks"></i>
          Tasks ({tasks.length})
        </button>
        <button 
          className={`tab-btn ${activeTab === 'schedule' ? 'active' : ''}`}
          onClick={() => setActiveTab('schedule')}
        >
          <i className="fas fa-calendar"></i>
          Schedule
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="overview-grid">
              {/* Personal Information */}
              <div className="info-card">
                <h3>Personal Information</h3>
                <div className="info-list">
                  <div className="info-item">
                    <span className="label">Full Name:</span>
                    <span className="value">{caretaker.full_name}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Email:</span>
                    <span className="value">{caretaker.email}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Phone:</span>
                    <span className="value">{caretaker.phone || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Date of Birth:</span>
                    <span className="value">{formatDate(caretaker.date_of_birth)}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Gender:</span>
                    <span className="value">{caretaker.gender || 'N/A'}</span>
                  </div>
                </div>
              </div>

              {/* Professional Information */}
              <div className="info-card">
                <h3>Professional Information</h3>
                <div className="info-list">
                  <div className="info-item">
                    <span className="label">Professional Title:</span>
                    <span className="value">{caretaker.professional_title || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">License Number:</span>
                    <span className="value">{caretaker.license_number || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Years of Experience:</span>
                    <span className="value">{caretaker.years_of_experience || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Specialization:</span>
                    <span className="value">{caretaker.specialization || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Employment Status:</span>
                    <span className="value">{getEmploymentStatusBadge(caretaker.employment_status)}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Hire Date:</span>
                    <span className="value">{formatDate(caretaker.hire_date)}</span>
                  </div>
                </div>
              </div>

              {/* Account Information */}
              <div className="info-card">
                <h3>Account Information</h3>
                <div className="info-list">
                  <div className="info-item">
                    <span className="label">Account Status:</span>
                    <span className="value">{getStatusBadge(caretaker.is_active)}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Date Joined:</span>
                    <span className="value">{formatDate(caretaker.date_joined)}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Last Login:</span>
                    <span className="value">{formatDate(caretaker.last_login)}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Email Verified:</span>
                    <span className="value">
                      <i className={`fas fa-${caretaker.email_verified ? 'check' : 'times'}`}></i>
                      {caretaker.email_verified ? 'Yes' : 'No'}
                    </span>
                  </div>
                  <div className="info-item">
                    <span className="label">Background Check:</span>
                    <span className="value">
                      <i className={`fas fa-${caretaker.background_check_verified ? 'check' : 'times'}`}></i>
                      {caretaker.background_check_verified ? 'Verified' : 'Not Verified'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Profile Information */}
              {profile && (
                <div className="info-card">
                  <h3>Profile Information</h3>
                  <div className="info-list">
                    <div className="info-item">
                      <span className="label">Address:</span>
                      <span className="value">{profile.address || 'N/A'}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">City:</span>
                      <span className="value">{profile.city || 'N/A'}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">State:</span>
                      <span className="value">{profile.state || 'N/A'}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Languages:</span>
                      <span className="value">{profile.languages_spoken || 'N/A'}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Emergency Contact:</span>
                      <span className="value">
                        {profile.emergency_contact_name ? 
                          `${profile.emergency_contact_name} (${profile.emergency_contact_phone})` : 
                          'N/A'
                        }
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Bio Section */}
            {profile && profile.bio && (
              <div className="bio-section">
                <h3>Biography</h3>
                <p>{profile.bio}</p>
              </div>
            )}

            {/* Certifications & Education */}
            {(profile?.certifications || profile?.education) && (
              <div className="credentials-section">
                <div className="credentials-grid">
                  {profile.certifications && (
                    <div className="credential-card">
                      <h4>Certifications</h4>
                      <p>{profile.certifications}</p>
                    </div>
                  )}
                  {profile.education && (
                    <div className="credential-card">
                      <h4>Education</h4>
                      <p>{profile.education}</p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'assignments' && (
          <div className="assignments-tab">
            <div className="tab-header">
              <h3>Patient Assignments</h3>
              <button className="add-assignment-btn">
                <i className="fas fa-plus"></i>
                Add Assignment
              </button>
            </div>
            
            {assignments.length === 0 ? (
              <div className="empty-state">
                <i className="fas fa-users"></i>
                <h4>No Patient Assignments</h4>
                <p>This caretaker has not been assigned to any patients yet.</p>
              </div>
            ) : (
              <div className="assignments-grid">
                {assignments.map((assignment) => (
                  <div key={assignment.id} className="assignment-card">
                    <div className="assignment-header">
                      <div className="patient-info">
                        <h4>{assignment.patient.full_name}</h4>
                        <p>Patient ID: {assignment.patient.id}</p>
                      </div>
                      <span className={`assignment-type ${assignment.assignment_type}`}>
                        {assignment.assignment_type}
                      </span>
                    </div>
                    <div className="assignment-details">
                      <div className="detail-item">
                        <span className="label">Assignment Date:</span>
                        <span className="value">{formatDate(assignment.assignment_date)}</span>
                      </div>
                      {assignment.end_date && (
                        <div className="detail-item">
                          <span className="label">End Date:</span>
                          <span className="value">{formatDate(assignment.end_date)}</span>
                        </div>
                      )}
                      <div className="detail-item">
                        <span className="label">Status:</span>
                        <span className="value">
                          <span className={`status-badge ${assignment.is_active ? 'active' : 'inactive'}`}>
                            {assignment.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </span>
                      </div>
                    </div>
                    {assignment.notes && (
                      <div className="assignment-notes">
                        <strong>Notes:</strong>
                        <p>{assignment.notes}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'tasks' && (
          <div className="tasks-tab">
            <div className="tab-header">
              <h3>Tasks</h3>
              <div className="task-filters">
                <select className="status-filter">
                  <option value="">All Status</option>
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
            </div>
            
            {tasks.length === 0 ? (
              <div className="empty-state">
                <i className="fas fa-tasks"></i>
                <h4>No Tasks</h4>
                <p>This caretaker has no assigned tasks.</p>
              </div>
            ) : (
              <div className="tasks-list">
                {tasks.map((task) => (
                  <div key={task.id} className="task-card">
                    <div className="task-header">
                      <h4>{task.title}</h4>
                      <div className="task-badges">
                        {getTaskStatusBadge(task.status)}
                        {getTaskPriorityBadge(task.priority)}
                      </div>
                    </div>
                    <div className="task-details">
                      <p className="task-description">{task.description}</p>
                      <div className="task-meta">
                        <div className="meta-item">
                          <span className="label">Patient:</span>
                          <span className="value">{task.patient.full_name}</span>
                        </div>
                        <div className="meta-item">
                          <span className="label">Type:</span>
                          <span className="value">{task.task_type}</span>
                        </div>
                        <div className="meta-item">
                          <span className="label">Scheduled:</span>
                          <span className="value">
                            {formatDate(task.scheduled_date)} {task.scheduled_time && formatTime(task.scheduled_time)}
                          </span>
                        </div>
                        {task.completed_date && (
                          <div className="meta-item">
                            <span className="label">Completed:</span>
                            <span className="value">{formatDate(task.completed_date)}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'schedule' && (
          <div className="schedule-tab">
            <div className="tab-header">
              <h3>Schedule</h3>
              <button className="add-schedule-btn">
                <i className="fas fa-plus"></i>
                Add Schedule Entry
              </button>
            </div>
            
            {schedule.length === 0 ? (
              <div className="empty-state">
                <i className="fas fa-calendar"></i>
                <h4>No Schedule Entries</h4>
                <p>No schedule entries found for this caretaker.</p>
              </div>
            ) : (
              <div className="schedule-list">
                {schedule.map((entry) => (
                  <div key={entry.id} className="schedule-card">
                    <div className="schedule-header">
                      <div className="schedule-date">
                        <h4>{formatDate(entry.date)}</h4>
                        <p>{formatTime(entry.start_time)} - {formatTime(entry.end_time)}</p>
                      </div>
                      <div className="schedule-badges">
                        <span className={`schedule-type ${entry.schedule_type}`}>
                          {entry.schedule_type}
                        </span>
                        <span className={`availability-badge ${entry.is_available ? 'available' : 'unavailable'}`}>
                          {entry.is_available ? 'Available' : 'Unavailable'}
                        </span>
                      </div>
                    </div>
                    {entry.notes && (
                      <div className="schedule-notes">
                        <strong>Notes:</strong>
                        <p>{entry.notes}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default CaretakerDetails; 