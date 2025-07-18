import React, { useState, useEffect } from 'react';
import { FaUsers, FaCalendarAlt, FaStethoscope, FaChartLine, FaBell, FaClock, FaUserMd, FaHospital } from 'react-icons/fa';
import './ClinicDashboard.css';

const ClinicDashboard = () => {
  const [dashboardData, setDashboardData] = useState({
    totalPatients: 0,
    totalStaff: 0,
    todayAppointments: 0,
    completedAppointmentsToday: 0,
    pendingAppointments: 0,
    recentAppointments: [],
    recentPatients: [],
    todaySchedule: []
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
        totalPatients: 1247,
        totalStaff: 45,
        todayAppointments: 23,
        completedAppointmentsToday: 18,
        pendingAppointments: 156,
        recentAppointments: [
          {
            id: 1,
            patientName: 'John Smith',
            appointmentType: 'Consultation',
            scheduledTime: '09:00 AM',
            status: 'completed'
          },
          {
            id: 2,
            patientName: 'Mary Johnson',
            appointmentType: 'Follow-up',
            scheduledTime: '10:30 AM',
            status: 'in_progress'
          },
          {
            id: 3,
            patientName: 'Robert Wilson',
            appointmentType: 'Routine Checkup',
            scheduledTime: '02:00 PM',
            status: 'scheduled'
          }
        ],
        recentPatients: [
          {
            id: 1,
            name: 'Sarah Davis',
            registrationDate: '2024-01-15',
            patientNumber: 'P001234'
          },
          {
            id: 2,
            name: 'Michael Brown',
            registrationDate: '2024-01-14',
            patientNumber: 'P001233'
          }
        ],
        todaySchedule: [
          {
            id: 1,
            staffName: 'Dr. Emily Chen',
            department: 'Neurology',
            startTime: '08:00 AM',
            endTime: '05:00 PM',
            scheduleType: 'regular'
          },
          {
            id: 2,
            staffName: 'Dr. James Wilson',
            department: 'Cardiology',
            startTime: '09:00 AM',
            endTime: '06:00 PM',
            scheduleType: 'regular'
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
        message: 'New appointment request from Patient #P001235',
        time: '5 minutes ago',
        priority: 'high'
      },
      {
        id: 2,
        type: 'staff',
        message: 'Dr. Sarah Johnson is running 15 minutes late',
        time: '10 minutes ago',
        priority: 'medium'
      },
      {
        id: 3,
        type: 'system',
        message: 'System maintenance scheduled for tonight at 2 AM',
        time: '1 hour ago',
        priority: 'low'
      }
    ];
    setNotifications(mockNotifications);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return '#28a745';
      case 'in_progress': return '#ffc107';
      case 'scheduled': return '#17a2b8';
      case 'cancelled': return '#dc3545';
      default: return '#6c757d';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed': return 'Completed';
      case 'in_progress': return 'In Progress';
      case 'scheduled': return 'Scheduled';
      case 'cancelled': return 'Cancelled';
      default: return status;
    }
  };

  if (loading) {
    return (
      <div className="clinic-dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="clinic-dashboard">
      <div className="dashboard-header">
        <h1>Clinic Dashboard</h1>
        <div className="dashboard-actions">
          <button className="btn btn-primary">
            <FaCalendarAlt /> New Appointment
          </button>
          <button className="btn btn-secondary">
            <FaUsers /> Add Patient
          </button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon patients">
            <FaUsers />
          </div>
          <div className="stat-content">
            <h3>{dashboardData.totalPatients.toLocaleString()}</h3>
            <p>Total Patients</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon staff">
            <FaUserMd />
          </div>
          <div className="stat-content">
            <h3>{dashboardData.totalStaff}</h3>
            <p>Staff Members</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon appointments">
            <FaCalendarAlt />
          </div>
          <div className="stat-content">
            <h3>{dashboardData.todayAppointments}</h3>
            <p>Today's Appointments</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon completed">
            <FaStethoscope />
          </div>
          <div className="stat-content">
            <h3>{dashboardData.completedAppointmentsToday}</h3>
            <p>Completed Today</p>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-main">
          {/* Recent Appointments */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Recent Appointments</h2>
              <a href="/clinic/appointments" className="view-all">View All</a>
            </div>
            <div className="appointments-list">
              {dashboardData.recentAppointments.map(appointment => (
                <div key={appointment.id} className="appointment-item">
                  <div className="appointment-info">
                    <h4>{appointment.patientName}</h4>
                    <p>{appointment.appointmentType}</p>
                    <span className="appointment-time">
                      <FaClock /> {appointment.scheduledTime}
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

          {/* Today's Schedule */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Today's Schedule</h2>
              <a href="/clinic/schedule" className="view-all">View All</a>
            </div>
            <div className="schedule-list">
              {dashboardData.todaySchedule.map(schedule => (
                <div key={schedule.id} className="schedule-item">
                  <div className="schedule-info">
                    <h4>{schedule.staffName}</h4>
                    <p>{schedule.department}</p>
                    <span className="schedule-time">
                      {schedule.startTime} - {schedule.endTime}
                    </span>
                  </div>
                  <div className="schedule-type">
                    <span className="type-badge">{schedule.scheduleType}</span>
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
                <FaUsers />
                <span>Register Patient</span>
              </button>
              <button className="quick-action-btn">
                <FaUserMd />
                <span>Add Staff</span>
              </button>
              <button className="quick-action-btn">
                <FaHospital />
                <span>View Reports</span>
              </button>
            </div>
          </div>

          {/* Recent Patients */}
          <div className="dashboard-section">
            <div className="section-header">
              <h2>Recent Patients</h2>
              <a href="/clinic/patients" className="view-all">View All</a>
            </div>
            <div className="patients-list">
              {dashboardData.recentPatients.map(patient => (
                <div key={patient.id} className="patient-item">
                  <div className="patient-info">
                    <h4>{patient.name}</h4>
                    <p>ID: {patient.patientNumber}</p>
                    <span className="registration-date">
                      Registered: {new Date(patient.registrationDate).toLocaleDateString()}
                    </span>
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

export default ClinicDashboard; 