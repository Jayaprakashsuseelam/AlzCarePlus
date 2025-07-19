import React, { useState, useEffect } from 'react';
import { 
  FaUser, FaCalendarAlt, FaPills, FaFileMedical, 
  FaHeartbeat, FaTarget, FaChartLine, FaBell, 
  FaClock, FaCheckCircle, FaExclamationTriangle,
  FaThermometerHalf, FaWeight, FaStethoscope
} from 'react-icons/fa';
import './PatientDashboard.css';

const PatientDashboard = () => {
  const [dashboardData, setDashboardData] = useState({
    patient: {},
    statistics: {},
    recent_appointments: [],
    upcoming_appointments: [],
    recent_medical_records: [],
    active_medications: [],
    active_care_plans: [],
    recent_vital_signs: [],
    health_goals: []
  });
  const [loading, setLoading] = useState(true);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    fetchDashboardData();
    fetchNotifications();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Simulated API call - replace with actual API endpoint
      const mockData = {
        patient: {
          id: 1,
          first_name: 'John',
          last_name: 'Smith',
          email: 'john.smith@email.com',
          age: 68,
          gender: 'male'
        },
        statistics: {
          total_appointments: 15,
          upcoming_appointments: 2,
          completed_appointments: 13,
          total_medications: 4,
          active_medications: 3,
          total_medical_records: 25,
          recent_medical_records: 3,
          care_plans_count: 2,
          active_care_plans: 1,
          health_goals_count: 5,
          completed_goals: 2
        },
        recent_appointments: [
          {
            id: 1,
            appointment_type: 'Follow-up',
            scheduled_date: '2024-01-15',
            scheduled_time: '10:00',
            doctor_name: 'Dr. Sarah Johnson',
            specialty: 'Neurology',
            status: 'completed'
          },
          {
            id: 2,
            appointment_type: 'Cognitive Assessment',
            scheduled_date: '2024-01-10',
            scheduled_time: '14:30',
            doctor_name: 'Dr. Michael Chen',
            specialty: 'Psychology',
            status: 'completed'
          }
        ],
        upcoming_appointments: [
          {
            id: 3,
            appointment_type: 'Consultation',
            scheduled_date: '2024-02-20',
            scheduled_time: '09:00',
            doctor_name: 'Dr. Sarah Johnson',
            specialty: 'Neurology',
            status: 'confirmed'
          },
          {
            id: 4,
            appointment_type: 'Routine Checkup',
            scheduled_date: '2024-02-25',
            scheduled_time: '11:00',
            doctor_name: 'Dr. Emily Wilson',
            specialty: 'Primary Care',
            status: 'scheduled'
          }
        ],
        recent_medical_records: [
          {
            id: 1,
            record_type: 'Cognitive Assessment',
            title: 'MMSE Assessment',
            date_recorded: '2024-01-10',
            recorded_by: 'Dr. Michael Chen',
            mmse_score: 24
          },
          {
            id: 2,
            record_type: 'Vital Signs',
            title: 'Blood Pressure Check',
            date_recorded: '2024-01-08',
            recorded_by: 'Nurse Sarah',
            blood_pressure: '140/85'
          }
        ],
        active_medications: [
          {
            id: 1,
            name: 'Donepezil',
            dosage: '10mg',
            frequency: 'Once daily',
            status: 'active',
            prescription_date: '2024-01-01'
          },
          {
            id: 2,
            name: 'Memantine',
            dosage: '20mg',
            frequency: 'Twice daily',
            status: 'active',
            prescription_date: '2024-01-01'
          },
          {
            id: 3,
            name: 'Vitamin D',
            dosage: '1000 IU',
            frequency: 'Once daily',
            status: 'active',
            prescription_date: '2023-12-15'
          }
        ],
        active_care_plans: [
          {
            id: 1,
            title: 'Alzheimer\'s Management Plan',
            description: 'Comprehensive care plan for managing Alzheimer\'s symptoms',
            status: 'active',
            created_date: '2024-01-01',
            next_review_date: '2024-02-01'
          }
        ],
        recent_vital_signs: [
          {
            id: 1,
            blood_pressure_systolic: 140,
            blood_pressure_diastolic: 85,
            heart_rate: 72,
            temperature: 98.6,
            weight: 75.5,
            recorded_date: '2024-01-15'
          },
          {
            id: 2,
            blood_pressure_systolic: 135,
            blood_pressure_diastolic: 82,
            heart_rate: 68,
            temperature: 98.4,
            weight: 75.2,
            recorded_date: '2024-01-08'
          }
        ],
        health_goals: [
          {
            id: 1,
            title: 'Improve Memory',
            category: 'Cognitive Health',
            status: 'in_progress',
            progress_percentage: 60,
            target_date: '2024-03-01'
          },
          {
            id: 2,
            title: 'Maintain Blood Pressure',
            category: 'Physical Health',
            status: 'in_progress',
            progress_percentage: 80,
            target_date: '2024-02-15'
          },
          {
            id: 3,
            title: 'Exercise 3x per week',
            category: 'Lifestyle',
            status: 'completed',
            progress_percentage: 100,
            target_date: '2024-01-31'
          }
        ]
      };
      
      setDashboardData(mockData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  const fetchNotifications = async () => {
    // Simulated notifications
    const mockNotifications = [
      {
        id: 1,
        type: 'appointment',
        message: 'Appointment reminder: Dr. Johnson tomorrow at 9:00 AM',
        time: '2 hours ago',
        priority: 'high'
      },
      {
        id: 2,
        type: 'medication',
        message: 'Medication refill due for Donepezil',
        time: '1 day ago',
        priority: 'medium'
      },
      {
        id: 3,
        type: 'goal',
        message: 'Congratulations! You completed your exercise goal',
        time: '2 days ago',
        priority: 'low'
      }
    ];
    setNotifications(mockNotifications);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return '#28a745';
      case 'confirmed': return '#17a2b8';
      case 'scheduled': return '#ffc107';
      case 'cancelled': return '#dc3545';
      case 'in_progress': return '#007bff';
      default: return '#6c757d';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed': return 'Completed';
      case 'confirmed': return 'Confirmed';
      case 'scheduled': return 'Scheduled';
      case 'cancelled': return 'Cancelled';
      case 'in_progress': return 'In Progress';
      default: return status;
    }
  };

  const getGoalStatusColor = (status) => {
    switch (status) {
      case 'completed': return '#28a745';
      case 'in_progress': return '#007bff';
      case 'not_started': return '#6c757d';
      default: return '#6c757d';
    }
  };

  if (loading) {
    return (
      <div className="patient-dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading your health dashboard...</p>
      </div>
    );
  }

  return (
    <div className="patient-dashboard">
      <div className="dashboard-header">
        <div className="welcome-section">
          <h1>Welcome back, {dashboardData.patient.first_name}!</h1>
          <p>Here's your health overview for today</p>
        </div>
        <div className="dashboard-actions">
          <button className="btn btn-primary">
            <FaCalendarAlt /> Schedule Appointment
          </button>
          <button className="btn btn-secondary">
            <FaFileMedical /> View Records
          </button>
        </div>
      </div>

      {/* Health Overview Cards */}
      <div className="health-overview">
        <div className="overview-card primary">
          <div className="card-icon">
            <FaHeartbeat />
          </div>
          <div className="card-content">
            <h3>Health Status</h3>
            <p className="status-text">Good</p>
            <span className="last-updated">Updated today</span>
          </div>
        </div>

        <div className="overview-card">
          <div className="card-icon">
            <FaPills />
          </div>
          <div className="card-content">
            <h3>Active Medications</h3>
            <p className="number">{dashboardData.statistics.active_medications}</p>
            <span className="subtitle">Current prescriptions</span>
          </div>
        </div>

        <div className="overview-card">
          <div className="card-icon">
            <FaCalendarAlt />
          </div>
          <div className="card-content">
            <h3>Upcoming Appointments</h3>
            <p className="number">{dashboardData.statistics.upcoming_appointments}</p>
            <span className="subtitle">Next: {dashboardData.upcoming_appointments[0]?.scheduled_date}</span>
          </div>
        </div>

        <div className="overview-card">
          <div className="card-icon">
            <FaTarget />
          </div>
          <div className="card-content">
            <h3>Health Goals</h3>
            <p className="number">{dashboardData.statistics.completed_goals}/{dashboardData.statistics.health_goals_count}</p>
            <span className="subtitle">Completed</span>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-main">
          {/* Recent Vital Signs */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Recent Vital Signs</h2>
              <a href="/patient/vital-signs" className="view-all">View All</a>
            </div>
            <div className="vital-signs-grid">
              {dashboardData.recent_vital_signs.slice(0, 1).map(vital => (
                <div key={vital.id} className="vital-signs-card">
                  <div className="vital-sign">
                    <FaThermometerHalf className="vital-icon" />
                    <div className="vital-info">
                      <span className="vital-label">Blood Pressure</span>
                      <span className="vital-value">{vital.blood_pressure_systolic}/{vital.blood_pressure_diastolic} mmHg</span>
                    </div>
                  </div>
                  <div className="vital-sign">
                    <FaHeartbeat className="vital-icon" />
                    <div className="vital-info">
                      <span className="vital-label">Heart Rate</span>
                      <span className="vital-value">{vital.heart_rate} bpm</span>
                    </div>
                  </div>
                  <div className="vital-sign">
                    <FaWeight className="vital-icon" />
                    <div className="vital-info">
                      <span className="vital-label">Weight</span>
                      <span className="vital-value">{vital.weight} kg</span>
                    </div>
                  </div>
                  <div className="vital-sign">
                    <FaThermometerHalf className="vital-icon" />
                    <div className="vital-info">
                      <span className="vital-label">Temperature</span>
                      <span className="vital-value">{vital.temperature}°F</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Upcoming Appointments */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Upcoming Appointments</h2>
              <a href="/patient/appointments" className="view-all">View All</a>
            </div>
            <div className="appointments-list">
              {dashboardData.upcoming_appointments.map(appointment => (
                <div key={appointment.id} className="appointment-item">
                  <div className="appointment-info">
                    <h4>{appointment.appointment_type}</h4>
                    <p>{appointment.doctor_name} - {appointment.specialty}</p>
                    <span className="appointment-time">
                      <FaClock /> {new Date(appointment.scheduled_date).toLocaleDateString()} at {appointment.scheduled_time}
                    </span>
                  </div>
                  <div className="appointment-status">
                    <span 
                      className="status-badge"
                      style={{ backgroundColor: getStatusColor(appointment.status) }}
                    >
                      {getStatusText(appointment.status)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Active Medications */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Active Medications</h2>
              <a href="/patient/medications" className="view-all">View All</a>
            </div>
            <div className="medications-list">
              {dashboardData.active_medications.map(medication => (
                <div key={medication.id} className="medication-item">
                  <div className="medication-info">
                    <h4>{medication.name}</h4>
                    <p>{medication.dosage} - {medication.frequency}</p>
                    <span className="medication-date">
                      Prescribed: {new Date(medication.prescription_date).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="medication-status">
                    <span className="status-badge active">Active</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="dashboard-sidebar">
          {/* Notifications */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Notifications</h2>
              <FaBell className="notification-icon" />
            </div>
            <div className="notifications-list">
              {notifications.map(notification => (
                <div key={notification.id} className={`notification-item ${notification.priority}`}>
                  <div className="notification-content">
                    <p>{notification.message}</p>
                    <span className="notification-time">{notification.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Health Goals */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Health Goals</h2>
              <a href="/patient/goals" className="view-all">View All</a>
            </div>
            <div className="goals-list">
              {dashboardData.health_goals.map(goal => (
                <div key={goal.id} className="goal-item">
                  <div className="goal-info">
                    <h4>{goal.title}</h4>
                    <p>{goal.category}</p>
                    <div className="goal-progress">
                      <div className="progress-bar">
                        <div 
                          className="progress-fill"
                          style={{ 
                            width: `${goal.progress_percentage}%`,
                            backgroundColor: getGoalStatusColor(goal.status)
                          }}
                        ></div>
                      </div>
                      <span className="progress-text">{goal.progress_percentage}%</span>
                    </div>
                  </div>
                  <div className="goal-status">
                    <span 
                      className="status-badge"
                      style={{ backgroundColor: getGoalStatusColor(goal.status) }}
                    >
                      {goal.status.replace('_', ' ')}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Quick Actions</h2>
            </div>
            <div className="quick-actions">
              <button className="quick-action-btn">
                <FaCalendarAlt />
                <span>Schedule Appointment</span>
              </button>
              <button className="quick-action-btn">
                <FaFileMedical />
                <span>View Medical Records</span>
              </button>
              <button className="quick-action-btn">
                <FaPills />
                <span>Medication Reminder</span>
              </button>
              <button className="quick-action-btn">
                <FaTarget />
                <span>Update Goals</span>
              </button>
            </div>
          </div>

          {/* Recent Medical Records */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Recent Medical Records</h2>
              <a href="/patient/medical-records" className="view-all">View All</a>
            </div>
            <div className="records-list">
              {dashboardData.recent_medical_records.map(record => (
                <div key={record.id} className="record-item">
                  <div className="record-info">
                    <h4>{record.title}</h4>
                    <p>{record.record_type}</p>
                    <span className="record-date">
                      {new Date(record.date_recorded).toLocaleDateString()} by {record.recorded_by}
                    </span>
                    {record.mmse_score && (
                      <span className="record-score">MMSE Score: {record.mmse_score}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientDashboard; 