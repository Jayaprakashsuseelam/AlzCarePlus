import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { caretakerAPI, authUtils, handleAPIError } from '../../services/api';
import '../caretaker/CaretakerDashboard.css';

const Tasks = () => {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    date: ''
  });

  useEffect(() => {
    const token = authUtils.getToken();
    if (!token) {
      navigate('/caretaker/login');
      return;
    }

    fetchTasks();
  }, [navigate, filters]);

  const fetchTasks = async () => {
    try {
      setIsLoading(true);
      const response = await caretakerAPI.getTasks(filters);
      setTasks(response.results || response);
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

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleStatusUpdate = async (taskId, newStatus) => {
    try {
      await caretakerAPI.updateTask(taskId, { status: newStatus });
      fetchTasks(); // Refresh the list
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setError(errorMessage);
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

  const getTaskTypeIcon = (taskType) => {
    switch (taskType) {
      case 'medication': return '💊';
      case 'hygiene': return '🧼';
      case 'feeding': return '🍽️';
      case 'exercise': return '🏃';
      case 'monitoring': return '📊';
      case 'appointment': return '📅';
      case 'emergency': return '🚨';
      default: return '📋';
    }
  };

  if (isLoading) {
    return (
      <div className="dashboard-container">
        <div className="dashboard-header">
          <div className="header-content">
            <div className="header-left">
              <h1>Tasks</h1>
            </div>
          </div>
        </div>
        <div className="dashboard-content">
          <div className="section-card">
            <div className="loading-skeleton" style={{ height: '400px' }}></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <h1>Tasks Management</h1>
            <p>Manage your assigned tasks and patient care activities</p>
          </div>
          <div className="header-right">
            <button 
              className="logout-btn" 
              onClick={() => navigate('/caretaker/dashboard')}
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        {/* Filters */}
        <div className="section-card">
          <div className="section-header">
            <h2 className="section-title">Filters</h2>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
            <div className="form-group">
              <label htmlFor="status">Status</label>
              <select
                id="status"
                name="status"
                value={filters.status}
                onChange={handleFilterChange}
              >
                <option value="">All Status</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="priority">Priority</label>
              <select
                id="priority"
                name="priority"
                value={filters.priority}
                onChange={handleFilterChange}
              >
                <option value="">All Priorities</option>
                <option value="urgent">Urgent</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="date">Date</label>
              <input
                type="date"
                id="date"
                name="date"
                value={filters.date}
                onChange={handleFilterChange}
              />
            </div>
          </div>
        </div>

        {/* Tasks List */}
        <div className="section-card">
          <div className="section-header">
            <h2 className="section-title">All Tasks ({tasks.length})</h2>
          </div>

          {error && (
            <div className="error-alert">
              {error}
            </div>
          )}

          {tasks.length > 0 ? (
            <div className="task-list">
              {tasks.map((task) => (
                <div key={task.id} className="task-item">
                  <div className={`task-priority ${getPriorityColor(task.priority)}`}></div>
                  
                  <div style={{ fontSize: '1.5rem', marginRight: '10px' }}>
                    {getTaskTypeIcon(task.task_type)}
                  </div>
                  
                  <div className="task-content">
                    <div className="task-title">{task.title}</div>
                    <div style={{ color: '#718096', fontSize: '0.9rem', marginBottom: '8px' }}>
                      {task.description}
                    </div>
                    <div className="task-details">
                      <div className="task-patient">
                        <span>👤</span>
                        {task.patient?.first_name} {task.patient?.last_name}
                      </div>
                      <div className="task-time">
                        <span>🕒</span>
                        {task.scheduled_date} {task.scheduled_time && formatTime(task.scheduled_time)}
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                        <span>📋</span>
                        {task.task_type}
                      </div>
                    </div>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', alignItems: 'flex-end' }}>
                    <div className={`task-status ${getStatusColor(task.status)}`}>
                      {task.status.replace('_', ' ')}
                    </div>
                    
                    {task.status !== 'completed' && task.status !== 'cancelled' && (
                      <select
                        value=""
                        onChange={(e) => handleStatusUpdate(task.id, e.target.value)}
                        style={{
                          padding: '4px 8px',
                          fontSize: '0.8rem',
                          border: '1px solid #e2e8f0',
                          borderRadius: '4px',
                          backgroundColor: 'white'
                        }}
                      >
                        <option value="">Update Status</option>
                        <option value="in_progress">Start</option>
                        <option value="completed">Complete</option>
                        <option value="cancelled">Cancel</option>
                      </select>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <div className="empty-state-icon">📋</div>
              <div className="empty-state-title">No tasks found</div>
              <div className="empty-state-description">
                {Object.values(filters).some(f => f) 
                  ? 'No tasks match your current filters. Try adjusting your search criteria.'
                  : 'You don\'t have any tasks assigned yet. Check back later for updates.'
                }
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Tasks; 