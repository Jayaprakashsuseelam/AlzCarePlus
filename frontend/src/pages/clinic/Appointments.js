import React, { useState, useEffect } from 'react';
import { clinicAPI, handleAPIError } from '../../services/api';
import './ClinicPages.css';

const Appointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    date: '',
    status: '',
    appointment_type: '',
    staff_id: '',
    patient_id: ''
  });

  useEffect(() => {
    fetchAppointments();
  }, [filters]);

  const fetchAppointments = async () => {
    try {
      setIsLoading(true);
      const data = await clinicAPI.getAppointments(filters);
      setAppointments(data);
    } catch (err) {
      setError('Failed to load appointments');
      console.error('Appointments error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCheckIn = async (appointmentId) => {
    try {
      await clinicAPI.checkInAppointment(appointmentId);
      fetchAppointments(); // Refresh the list
    } catch (err) {
      setError('Failed to check in appointment');
    }
  };

  const handleCheckOut = async (appointmentId) => {
    try {
      await clinicAPI.checkOutAppointment(appointmentId);
      fetchAppointments(); // Refresh the list
    } catch (err) {
      setError('Failed to check out appointment');
    }
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
      weekday: 'short',
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

  if (isLoading) {
    return (
      <div className="clinic-page">
        <div className="clinic-page-content">
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <div className="clinic-loading">Loading appointments...</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="clinic-page">
      <div className="clinic-page-header">
        <h1>Appointments Management</h1>
        <button className="clinic-primary-btn">New Appointment</button>
      </div>

      <div className="clinic-page-content">
        {error && (
          <div className="clinic-error-alert">
            {error}
          </div>
        )}

        {/* Filters */}
        <div className="clinic-filters">
          <div className="clinic-filter-row">
            <div className="clinic-filter-group">
              <label>Date</label>
              <input
                type="date"
                name="date"
                value={filters.date}
                onChange={handleFilterChange}
              />
            </div>
            
            <div className="clinic-filter-group">
              <label>Status</label>
              <select
                name="status"
                value={filters.status}
                onChange={handleFilterChange}
              >
                <option value="">All Status</option>
                <option value="scheduled">Scheduled</option>
                <option value="confirmed">Confirmed</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
                <option value="no_show">No Show</option>
                <option value="rescheduled">Rescheduled</option>
              </select>
            </div>
            
            <div className="clinic-filter-group">
              <label>Type</label>
              <select
                name="appointment_type"
                value={filters.appointment_type}
                onChange={handleFilterChange}
              >
                <option value="">All Types</option>
                <option value="consultation">Consultation</option>
                <option value="follow_up">Follow-up</option>
                <option value="emergency">Emergency</option>
                <option value="routine_checkup">Routine Checkup</option>
                <option value="procedure">Procedure</option>
                <option value="therapy">Therapy</option>
                <option value="diagnostic">Diagnostic Test</option>
                <option value="vaccination">Vaccination</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>
        </div>

        {/* Appointments List */}
        <div className="clinic-appointments-list">
          {appointments.length > 0 ? (
            appointments.map((appointment) => (
              <div key={appointment.id} className="clinic-appointment-card">
                <div className="clinic-appointment-header">
                  <div className="clinic-appointment-info">
                    <h3>{appointment.patient?.patient?.first_name} {appointment.patient?.patient?.last_name}</h3>
                    <p className="clinic-appointment-number">#{appointment.appointment_number}</p>
                  </div>
                  <span className={`clinic-appointment-status ${getStatusClass(appointment.status)}`}>
                    {appointment.status.replace('_', ' ')}
                  </span>
                </div>
                
                <div className="clinic-appointment-details">
                  <div className="clinic-appointment-detail">
                    <span className="clinic-detail-label">Date & Time:</span>
                    <span>{formatDate(appointment.scheduled_date)} at {formatTime(appointment.scheduled_time)}</span>
                  </div>
                  
                  <div className="clinic-appointment-detail">
                    <span className="clinic-detail-label">Type:</span>
                    <span>{appointment.appointment_type.replace('_', ' ')}</span>
                  </div>
                  
                  <div className="clinic-appointment-detail">
                    <span className="clinic-detail-label">Staff:</span>
                    <span>Dr. {appointment.staff?.user?.first_name} {appointment.staff?.user?.last_name}</span>
                  </div>
                  
                  {appointment.room_number && (
                    <div className="clinic-appointment-detail">
                      <span className="clinic-detail-label">Room:</span>
                      <span>{appointment.room_number}</span>
                    </div>
                  )}
                  
                  {appointment.reason && (
                    <div className="clinic-appointment-detail">
                      <span className="clinic-detail-label">Reason:</span>
                      <span>{appointment.reason}</span>
                    </div>
                  )}
                </div>
                
                <div className="clinic-appointment-actions">
                  {appointment.status === 'scheduled' && (
                    <button 
                      className="clinic-action-btn"
                      onClick={() => handleCheckIn(appointment.id)}
                    >
                      Check In
                    </button>
                  )}
                  
                  {appointment.status === 'in_progress' && (
                    <button 
                      className="clinic-action-btn"
                      onClick={() => handleCheckOut(appointment.id)}
                    >
                      Check Out
                    </button>
                  )}
                  
                  <button className="clinic-secondary-btn">
                    Edit
                  </button>
                  
                  <button className="clinic-danger-btn">
                    Cancel
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="clinic-empty-state">
              <h3>No Appointments Found</h3>
              <p>No appointments match your current filters.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Appointments; 