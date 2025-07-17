import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { caretakerAPI, authUtils, handleAPIError } from '../../services/api';
import './CaretakerManagement.css';

const CaretakerManagement = () => {
  const navigate = useNavigate();
  const [caretakers, setCaretakers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingCaretaker, setEditingCaretaker] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const token = authUtils.getToken();
    if (!token) {
      navigate('/caretaker/login');
      return;
    }

    fetchCaretakers();
  }, [navigate, currentPage, filterStatus]);

  const fetchCaretakers = async () => {
    try {
      setIsLoading(true);
      const filters = {
        page: currentPage,
        search: searchTerm,
        status: filterStatus !== 'all' ? filterStatus : ''
      };
      
      const response = await caretakerAPI.getAllCaretakers(filters);
      setCaretakers(response.results || response);
      setTotalPages(response.total_pages || 1);
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

  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    fetchCaretakers();
  };

  const handleAddCaretaker = async (caretakerData) => {
    try {
      await caretakerAPI.createCaretaker(caretakerData);
      setShowAddForm(false);
      fetchCaretakers();
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setError(errorMessage);
    }
  };

  const handleUpdateCaretaker = async (caretakerId, caretakerData) => {
    try {
      await caretakerAPI.updateCaretaker(caretakerId, caretakerData);
      setEditingCaretaker(null);
      fetchCaretakers();
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setError(errorMessage);
    }
  };

  const handleDeleteCaretaker = async (caretakerId) => {
    if (window.confirm('Are you sure you want to delete this caretaker? This action cannot be undone.')) {
      try {
        await caretakerAPI.deleteCaretaker(caretakerId);
        fetchCaretakers();
      } catch (error) {
        const errorMessage = handleAPIError(error);
        setError(errorMessage);
      }
    }
  };

  const handleStatusChange = async (caretakerId, newStatus) => {
    try {
      await caretakerAPI.updateCaretaker(caretakerId, { is_active: newStatus });
      fetchCaretakers();
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setError(errorMessage);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
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

  if (isLoading && caretakers.length === 0) {
    return (
      <div className="caretaker-management">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading caretakers...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="caretaker-management">
      <div className="caretaker-management-header">
        <div className="header-content">
          <h1>Caretaker Management</h1>
          <p>Manage and oversee all caretaker accounts and assignments</p>
        </div>
        <button 
          className="add-caretaker-btn"
          onClick={() => setShowAddForm(true)}
        >
          <i className="fas fa-plus"></i>
          Add Caretaker
        </button>
      </div>

      {error && (
        <div className="error-message">
          <i className="fas fa-exclamation-triangle"></i>
          {error}
        </div>
      )}

      {/* Search and Filter Section */}
      <div className="search-filter-section">
        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-group">
            <i className="fas fa-search"></i>
            <input
              type="text"
              placeholder="Search caretakers by name, email, or license number..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <button type="submit" className="search-btn">
              Search
            </button>
          </div>
        </form>

        <div className="filter-controls">
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="status-filter"
          >
            <option value="all">All Status</option>
            <option value="true">Active</option>
            <option value="false">Inactive</option>
          </select>
        </div>
      </div>

      {/* Caretakers Table */}
      <div className="caretakers-table-container">
        <table className="caretakers-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Professional Title</th>
              <th>License Number</th>
              <th>Employment Status</th>
              <th>Status</th>
              <th>Date Joined</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {caretakers.map((caretaker) => (
              <tr key={caretaker.id}>
                <td>
                  <div className="caretaker-name">
                    <div className="avatar">
                      {caretaker.profile_picture ? (
                        <img src={caretaker.profile_picture} alt={caretaker.full_name} />
                      ) : (
                        <div className="avatar-placeholder">
                          {caretaker.first_name?.[0]}{caretaker.last_name?.[0]}
                        </div>
                      )}
                    </div>
                    <div className="name-info">
                      <span className="full-name">{caretaker.full_name}</span>
                      <span className="phone">{caretaker.phone || 'No phone'}</span>
                    </div>
                  </div>
                </td>
                <td>{caretaker.email}</td>
                <td>{caretaker.professional_title || 'N/A'}</td>
                <td>{caretaker.license_number || 'N/A'}</td>
                <td>{getEmploymentStatusBadge(caretaker.employment_status)}</td>
                <td>{getStatusBadge(caretaker.is_active)}</td>
                <td>{formatDate(caretaker.date_joined)}</td>
                <td>
                  <div className="action-buttons">
                    <button
                      className="action-btn view-btn"
                      onClick={() => navigate(`/caretaker/management/${caretaker.id}`)}
                      title="View Details"
                    >
                      <i className="fas fa-eye"></i>
                    </button>
                    <button
                      className="action-btn edit-btn"
                      onClick={() => setEditingCaretaker(caretaker)}
                      title="Edit Caretaker"
                    >
                      <i className="fas fa-edit"></i>
                    </button>
                    <button
                      className="action-btn toggle-btn"
                      onClick={() => handleStatusChange(caretaker.id, !caretaker.is_active)}
                      title={caretaker.is_active ? 'Deactivate' : 'Activate'}
                    >
                      <i className={`fas fa-${caretaker.is_active ? 'pause' : 'play'}`}></i>
                    </button>
                    <button
                      className="action-btn delete-btn"
                      onClick={() => handleDeleteCaretaker(caretaker.id)}
                      title="Delete Caretaker"
                    >
                      <i className="fas fa-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {caretakers.length === 0 && !isLoading && (
          <div className="no-caretakers">
            <i className="fas fa-users"></i>
            <h3>No Caretakers Found</h3>
            <p>No caretakers match your current search criteria.</p>
            <button 
              className="add-first-caretaker-btn"
              onClick={() => setShowAddForm(true)}
            >
              Add Your First Caretaker
            </button>
          </div>
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="pagination">
          <button
            className="pagination-btn"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(currentPage - 1)}
          >
            <i className="fas fa-chevron-left"></i>
            Previous
          </button>
          
          <div className="page-numbers">
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
              <button
                key={page}
                className={`page-btn ${currentPage === page ? 'active' : ''}`}
                onClick={() => setCurrentPage(page)}
              >
                {page}
              </button>
            ))}
          </div>
          
          <button
            className="pagination-btn"
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage(currentPage + 1)}
          >
            Next
            <i className="fas fa-chevron-right"></i>
          </button>
        </div>
      )}

      {/* Add Caretaker Modal */}
      {showAddForm && (
        <AddCaretakerForm
          onClose={() => setShowAddForm(false)}
          onSubmit={handleAddCaretaker}
        />
      )}

      {/* Edit Caretaker Modal */}
      {editingCaretaker && (
        <EditCaretakerForm
          caretaker={editingCaretaker}
          onClose={() => setEditingCaretaker(null)}
          onSubmit={handleUpdateCaretaker}
        />
      )}
    </div>
  );
};

// Add Caretaker Form Component
const AddCaretakerForm = ({ onClose, onSubmit }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
    phone: '',
    date_of_birth: '',
    gender: '',
    professional_title: '',
    license_number: '',
    years_of_experience: '',
    specialization: '',
    employment_status: 'full-time',
    hire_date: ''
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.password) newErrors.password = 'Password is required';
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    if (!formData.first_name) newErrors.first_name = 'First name is required';
    if (!formData.last_name) newErrors.last_name = 'Last name is required';
    if (!formData.phone) newErrors.phone = 'Phone number is required';
    if (!formData.date_of_birth) newErrors.date_of_birth = 'Date of birth is required';
    if (!formData.gender) newErrors.gender = 'Gender is required';
    if (!formData.professional_title) newErrors.professional_title = 'Professional title is required';
    if (!formData.license_number) newErrors.license_number = 'License number is required';
    if (!formData.years_of_experience) newErrors.years_of_experience = 'Years of experience is required';
    if (!formData.specialization) newErrors.specialization = 'Specialization is required';
    if (!formData.hire_date) newErrors.hire_date = 'Hire date is required';

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsLoading(true);
    try {
      await onSubmit({
        email: formData.email,
        password: formData.password,
        confirm_password: formData.confirmPassword,
        first_name: formData.first_name,
        last_name: formData.last_name,
        phone: formData.phone,
        date_of_birth: formData.date_of_birth,
        gender: formData.gender,
        professional_title: formData.professional_title,
        license_number: formData.license_number,
        years_of_experience: parseInt(formData.years_of_experience),
        specialization: formData.specialization,
        employment_status: formData.employment_status,
        hire_date: formData.hire_date
      });
    } catch (error) {
      console.error('Error adding caretaker:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Add New Caretaker</h2>
          <button className="close-btn" onClick={onClose}>
            <i className="fas fa-times"></i>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="caretaker-form">
          <div className="form-sections">
            {/* Personal Information */}
            <div className="form-section">
              <h3>Personal Information</h3>
              <div className="form-row">
                <div className="form-group">
                  <label>First Name *</label>
                  <input
                    type="text"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    className={errors.first_name ? 'error' : ''}
                  />
                  {errors.first_name && <span className="error-text">{errors.first_name}</span>}
                </div>
                <div className="form-group">
                  <label>Last Name *</label>
                  <input
                    type="text"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    className={errors.last_name ? 'error' : ''}
                  />
                  {errors.last_name && <span className="error-text">{errors.last_name}</span>}
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Email *</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className={errors.email ? 'error' : ''}
                  />
                  {errors.email && <span className="error-text">{errors.email}</span>}
                </div>
                <div className="form-group">
                  <label>Phone *</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className={errors.phone ? 'error' : ''}
                  />
                  {errors.phone && <span className="error-text">{errors.phone}</span>}
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Date of Birth *</label>
                  <input
                    type="date"
                    name="date_of_birth"
                    value={formData.date_of_birth}
                    onChange={handleChange}
                    className={errors.date_of_birth ? 'error' : ''}
                  />
                  {errors.date_of_birth && <span className="error-text">{errors.date_of_birth}</span>}
                </div>
                <div className="form-group">
                  <label>Gender *</label>
                  <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleChange}
                    className={errors.gender ? 'error' : ''}
                  >
                    <option value="">Select Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                    <option value="prefer-not-to-say">Prefer not to say</option>
                  </select>
                  {errors.gender && <span className="error-text">{errors.gender}</span>}
                </div>
              </div>
            </div>

            {/* Professional Information */}
            <div className="form-section">
              <h3>Professional Information</h3>
              <div className="form-row">
                <div className="form-group">
                  <label>Professional Title *</label>
                  <input
                    type="text"
                    name="professional_title"
                    value={formData.professional_title}
                    onChange={handleChange}
                    className={errors.professional_title ? 'error' : ''}
                  />
                  {errors.professional_title && <span className="error-text">{errors.professional_title}</span>}
                </div>
                <div className="form-group">
                  <label>License Number *</label>
                  <input
                    type="text"
                    name="license_number"
                    value={formData.license_number}
                    onChange={handleChange}
                    className={errors.license_number ? 'error' : ''}
                  />
                  {errors.license_number && <span className="error-text">{errors.license_number}</span>}
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Years of Experience *</label>
                  <input
                    type="number"
                    name="years_of_experience"
                    value={formData.years_of_experience}
                    onChange={handleChange}
                    min="0"
                    className={errors.years_of_experience ? 'error' : ''}
                  />
                  {errors.years_of_experience && <span className="error-text">{errors.years_of_experience}</span>}
                </div>
                <div className="form-group">
                  <label>Employment Status *</label>
                  <select
                    name="employment_status"
                    value={formData.employment_status}
                    onChange={handleChange}
                  >
                    <option value="full-time">Full Time</option>
                    <option value="part-time">Part Time</option>
                    <option value="contract">Contract</option>
                    <option value="volunteer">Volunteer</option>
                    <option value="private">Private Practice</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Specialization *</label>
                <input
                  type="text"
                  name="specialization"
                  value={formData.specialization}
                  onChange={handleChange}
                  placeholder="e.g., Geriatric Care, Alzheimer's, Dementia"
                  className={errors.specialization ? 'error' : ''}
                />
                {errors.specialization && <span className="error-text">{errors.specialization}</span>}
              </div>

              <div className="form-group">
                <label>Hire Date *</label>
                <input
                  type="date"
                  name="hire_date"
                  value={formData.hire_date}
                  onChange={handleChange}
                  className={errors.hire_date ? 'error' : ''}
                />
                {errors.hire_date && <span className="error-text">{errors.hire_date}</span>}
              </div>
            </div>

            {/* Account Information */}
            <div className="form-section">
              <h3>Account Information</h3>
              <div className="form-row">
                <div className="form-group">
                  <label>Password *</label>
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    className={errors.password ? 'error' : ''}
                  />
                  {errors.password && <span className="error-text">{errors.password}</span>}
                </div>
                <div className="form-group">
                  <label>Confirm Password *</label>
                  <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    className={errors.confirmPassword ? 'error' : ''}
                  />
                  {errors.confirmPassword && <span className="error-text">{errors.confirmPassword}</span>}
                </div>
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button type="button" className="cancel-btn" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="submit-btn" disabled={isLoading}>
              {isLoading ? 'Adding...' : 'Add Caretaker'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Edit Caretaker Form Component
const EditCaretakerForm = ({ caretaker, onClose, onSubmit }) => {
  const [formData, setFormData] = useState({
    first_name: caretaker.first_name || '',
    last_name: caretaker.last_name || '',
    phone: caretaker.phone || '',
    date_of_birth: caretaker.date_of_birth || '',
    gender: caretaker.gender || '',
    professional_title: caretaker.professional_title || '',
    license_number: caretaker.license_number || '',
    years_of_experience: caretaker.years_of_experience || '',
    specialization: caretaker.specialization || '',
    employment_status: caretaker.employment_status || 'full-time',
    hire_date: caretaker.hire_date || '',
    is_active: caretaker.is_active
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.first_name) newErrors.first_name = 'First name is required';
    if (!formData.last_name) newErrors.last_name = 'Last name is required';
    if (!formData.phone) newErrors.phone = 'Phone number is required';
    if (!formData.date_of_birth) newErrors.date_of_birth = 'Date of birth is required';
    if (!formData.gender) newErrors.gender = 'Gender is required';
    if (!formData.professional_title) newErrors.professional_title = 'Professional title is required';
    if (!formData.license_number) newErrors.license_number = 'License number is required';
    if (!formData.years_of_experience) newErrors.years_of_experience = 'Years of experience is required';
    if (!formData.specialization) newErrors.specialization = 'Specialization is required';
    if (!formData.hire_date) newErrors.hire_date = 'Hire date is required';

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsLoading(true);
    try {
      await onSubmit(caretaker.id, {
        first_name: formData.first_name,
        last_name: formData.last_name,
        phone: formData.phone,
        date_of_birth: formData.date_of_birth,
        gender: formData.gender,
        professional_title: formData.professional_title,
        license_number: formData.license_number,
        years_of_experience: parseInt(formData.years_of_experience),
        specialization: formData.specialization,
        employment_status: formData.employment_status,
        hire_date: formData.hire_date,
        is_active: formData.is_active
      });
    } catch (error) {
      console.error('Error updating caretaker:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Edit Caretaker</h2>
          <button className="close-btn" onClick={onClose}>
            <i className="fas fa-times"></i>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="caretaker-form">
          <div className="form-sections">
            {/* Personal Information */}
            <div className="form-section">
              <h3>Personal Information</h3>
              <div className="form-row">
                <div className="form-group">
                  <label>First Name *</label>
                  <input
                    type="text"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    className={errors.first_name ? 'error' : ''}
                  />
                  {errors.first_name && <span className="error-text">{errors.first_name}</span>}
                </div>
                <div className="form-group">
                  <label>Last Name *</label>
                  <input
                    type="text"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    className={errors.last_name ? 'error' : ''}
                  />
                  {errors.last_name && <span className="error-text">{errors.last_name}</span>}
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Email</label>
                  <input
                    type="email"
                    value={caretaker.email}
                    disabled
                    className="disabled-input"
                  />
                  <small>Email cannot be changed</small>
                </div>
                <div className="form-group">
                  <label>Phone *</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className={errors.phone ? 'error' : ''}
                  />
                  {errors.phone && <span className="error-text">{errors.phone}</span>}
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Date of Birth *</label>
                  <input
                    type="date"
                    name="date_of_birth"
                    value={formData.date_of_birth}
                    onChange={handleChange}
                    className={errors.date_of_birth ? 'error' : ''}
                  />
                  {errors.date_of_birth && <span className="error-text">{errors.date_of_birth}</span>}
                </div>
                <div className="form-group">
                  <label>Gender *</label>
                  <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleChange}
                    className={errors.gender ? 'error' : ''}
                  >
                    <option value="">Select Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                    <option value="prefer-not-to-say">Prefer not to say</option>
                  </select>
                  {errors.gender && <span className="error-text">{errors.gender}</span>}
                </div>
              </div>
            </div>

            {/* Professional Information */}
            <div className="form-section">
              <h3>Professional Information</h3>
              <div className="form-row">
                <div className="form-group">
                  <label>Professional Title *</label>
                  <input
                    type="text"
                    name="professional_title"
                    value={formData.professional_title}
                    onChange={handleChange}
                    className={errors.professional_title ? 'error' : ''}
                  />
                  {errors.professional_title && <span className="error-text">{errors.professional_title}</span>}
                </div>
                <div className="form-group">
                  <label>License Number *</label>
                  <input
                    type="text"
                    name="license_number"
                    value={formData.license_number}
                    onChange={handleChange}
                    className={errors.license_number ? 'error' : ''}
                  />
                  {errors.license_number && <span className="error-text">{errors.license_number}</span>}
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Years of Experience *</label>
                  <input
                    type="number"
                    name="years_of_experience"
                    value={formData.years_of_experience}
                    onChange={handleChange}
                    min="0"
                    className={errors.years_of_experience ? 'error' : ''}
                  />
                  {errors.years_of_experience && <span className="error-text">{errors.years_of_experience}</span>}
                </div>
                <div className="form-group">
                  <label>Employment Status *</label>
                  <select
                    name="employment_status"
                    value={formData.employment_status}
                    onChange={handleChange}
                  >
                    <option value="full-time">Full Time</option>
                    <option value="part-time">Part Time</option>
                    <option value="contract">Contract</option>
                    <option value="volunteer">Volunteer</option>
                    <option value="private">Private Practice</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Specialization *</label>
                <input
                  type="text"
                  name="specialization"
                  value={formData.specialization}
                  onChange={handleChange}
                  placeholder="e.g., Geriatric Care, Alzheimer's, Dementia"
                  className={errors.specialization ? 'error' : ''}
                />
                {errors.specialization && <span className="error-text">{errors.specialization}</span>}
              </div>

              <div className="form-group">
                <label>Hire Date *</label>
                <input
                  type="date"
                  name="hire_date"
                  value={formData.hire_date}
                  onChange={handleChange}
                  className={errors.hire_date ? 'error' : ''}
                />
                {errors.hire_date && <span className="error-text">{errors.hire_date}</span>}
              </div>
            </div>

            {/* Account Status */}
            <div className="form-section">
              <h3>Account Status</h3>
              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="is_active"
                    checked={formData.is_active}
                    onChange={handleChange}
                  />
                  <span className="checkmark"></span>
                  Active Account
                </label>
                <small>Uncheck to deactivate this caretaker's account</small>
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button type="button" className="cancel-btn" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="submit-btn" disabled={isLoading}>
              {isLoading ? 'Updating...' : 'Update Caretaker'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CaretakerManagement; 