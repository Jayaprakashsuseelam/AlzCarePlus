import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { clinicAPI, authUtils, handleAPIError } from '../../services/api';
import './ClinicAuth.css';

const ClinicRegister = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    // Basic Information
    email: '',
    password: '',
    confirmPassword: '',
    clinic_name: '',
    clinic_type: 'general',
    phone: '',
    fax: '',
    website: '',
    
    // Address Information
    address: '',
    city: '',
    state: '',
    zip_code: '',
    country: 'United States',
    
    // Business Information
    license_number: '',
    tax_id: '',
    npi_number: '',
    
    // Operating Hours
    operating_hours: {
      monday: { open: '09:00', close: '17:00', closed: false },
      tuesday: { open: '09:00', close: '17:00', closed: false },
      wednesday: { open: '09:00', close: '17:00', closed: false },
      thursday: { open: '09:00', close: '17:00', closed: false },
      friday: { open: '09:00', close: '17:00', closed: false },
      saturday: { open: '09:00', close: '13:00', closed: false },
      sunday: { open: '09:00', close: '13:00', closed: true }
    }
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  const clinicTypes = [
    { value: 'general', label: 'General Practice' },
    { value: 'specialist', label: 'Specialist Clinic' },
    { value: 'geriatric', label: 'Geriatric Care' },
    { value: 'neurology', label: 'Neurology' },
    { value: 'cardiology', label: 'Cardiology' },
    { value: 'oncology', label: 'Oncology' },
    { value: 'rehabilitation', label: 'Rehabilitation' },
    { value: 'mental_health', label: 'Mental Health' },
    { value: 'dental', label: 'Dental' },
    { value: 'other', label: 'Other' }
  ];

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
    if (apiError) {
      setApiError('');
    }
  };

  const handleOperatingHoursChange = (day, field, value) => {
    setFormData(prev => ({
      ...prev,
      operating_hours: {
        ...prev.operating_hours,
        [day]: {
          ...prev.operating_hours[day],
          [field]: value
        }
      }
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    
    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    
    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }
    
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    // Required fields
    if (!formData.clinic_name) {
      newErrors.clinic_name = 'Clinic name is required';
    }
    
    if (!formData.phone) {
      newErrors.phone = 'Phone number is required';
    }
    
    if (!formData.address) {
      newErrors.address = 'Address is required';
    }
    
    if (!formData.city) {
      newErrors.city = 'City is required';
    }
    
    if (!formData.state) {
      newErrors.state = 'State is required';
    }
    
    if (!formData.zip_code) {
      newErrors.zip_code = 'ZIP code is required';
    }
    
    if (!formData.license_number) {
      newErrors.license_number = 'License number is required';
    }
    
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
    setApiError('');

    try {
      const response = await clinicAPI.register(formData);

      // Store the token
      authUtils.setToken(response.tokens.access);
      
      // Store clinic data
      localStorage.setItem('clinicData', JSON.stringify(response.clinic));

      // Redirect to dashboard
      navigate('/clinic/dashboard');
      
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setApiError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="clinic-auth-container">
      <div className="clinic-auth-card">
        <div className="clinic-auth-header">
          <h1>Register Clinic</h1>
          <p>Join AlzCarePlus and manage your clinic operations</p>
        </div>

        {apiError && (
          <div className="clinic-error-alert">
            {apiError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="clinic-auth-form">
          {/* Basic Information */}
          <div className="clinic-form-section">
            <h3>Basic Information</h3>
            
            <div className="clinic-form-group">
              <label htmlFor="clinic_name">Clinic Name *</label>
              <input
                type="text"
                id="clinic_name"
                name="clinic_name"
                value={formData.clinic_name}
                onChange={handleChange}
                className={errors.clinic_name ? 'error' : ''}
                placeholder="Enter clinic name"
                disabled={isLoading}
              />
              {errors.clinic_name && <span className="clinic-error-message">{errors.clinic_name}</span>}
            </div>

            <div className="clinic-form-row">
              <div className="clinic-form-group">
                <label htmlFor="clinic_type">Clinic Type</label>
                <select
                  id="clinic_type"
                  name="clinic_type"
                  value={formData.clinic_type}
                  onChange={handleChange}
                  disabled={isLoading}
                >
                  {clinicTypes.map(type => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="clinic-form-group">
                <label htmlFor="phone">Phone Number *</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  className={errors.phone ? 'error' : ''}
                  placeholder="(555) 123-4567"
                  disabled={isLoading}
                />
                {errors.phone && <span className="clinic-error-message">{errors.phone}</span>}
              </div>
            </div>

            <div className="clinic-form-row">
              <div className="clinic-form-group">
                <label htmlFor="email">Email Address *</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className={errors.email ? 'error' : ''}
                  placeholder="clinic@example.com"
                  disabled={isLoading}
                />
                {errors.email && <span className="clinic-error-message">{errors.email}</span>}
              </div>

              <div className="clinic-form-group">
                <label htmlFor="fax">Fax Number</label>
                <input
                  type="tel"
                  id="fax"
                  name="fax"
                  value={formData.fax}
                  onChange={handleChange}
                  placeholder="(555) 123-4568"
                  disabled={isLoading}
                />
              </div>
            </div>

            <div className="clinic-form-group">
              <label htmlFor="website">Website</label>
              <input
                type="url"
                id="website"
                name="website"
                value={formData.website}
                onChange={handleChange}
                placeholder="https://www.clinic.com"
                disabled={isLoading}
              />
            </div>
          </div>

          {/* Address Information */}
          <div className="clinic-form-section">
            <h3>Address Information</h3>
            
            <div className="clinic-form-group">
              <label htmlFor="address">Street Address *</label>
              <input
                type="text"
                id="address"
                name="address"
                value={formData.address}
                onChange={handleChange}
                className={errors.address ? 'error' : ''}
                placeholder="123 Medical Center Dr"
                disabled={isLoading}
              />
              {errors.address && <span className="clinic-error-message">{errors.address}</span>}
            </div>

            <div className="clinic-form-row">
              <div className="clinic-form-group">
                <label htmlFor="city">City *</label>
                <input
                  type="text"
                  id="city"
                  name="city"
                  value={formData.city}
                  onChange={handleChange}
                  className={errors.city ? 'error' : ''}
                  placeholder="City"
                  disabled={isLoading}
                />
                {errors.city && <span className="clinic-error-message">{errors.city}</span>}
              </div>

              <div className="clinic-form-group">
                <label htmlFor="state">State *</label>
                <input
                  type="text"
                  id="state"
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  className={errors.state ? 'error' : ''}
                  placeholder="State"
                  disabled={isLoading}
                />
                {errors.state && <span className="clinic-error-message">{errors.state}</span>}
              </div>
            </div>

            <div className="clinic-form-row">
              <div className="clinic-form-group">
                <label htmlFor="zip_code">ZIP Code *</label>
                <input
                  type="text"
                  id="zip_code"
                  name="zip_code"
                  value={formData.zip_code}
                  onChange={handleChange}
                  className={errors.zip_code ? 'error' : ''}
                  placeholder="12345"
                  disabled={isLoading}
                />
                {errors.zip_code && <span className="clinic-error-message">{errors.zip_code}</span>}
              </div>

              <div className="clinic-form-group">
                <label htmlFor="country">Country</label>
                <input
                  type="text"
                  id="country"
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                  disabled={isLoading}
                />
              </div>
            </div>
          </div>

          {/* Business Information */}
          <div className="clinic-form-section">
            <h3>Business Information</h3>
            
            <div className="clinic-license-info">
              <h4>License Information</h4>
              <p>Please provide your clinic's official license number. This information is required for verification and compliance purposes.</p>
            </div>

            <div className="clinic-form-row">
              <div className="clinic-form-group">
                <label htmlFor="license_number">License Number *</label>
                <input
                  type="text"
                  id="license_number"
                  name="license_number"
                  value={formData.license_number}
                  onChange={handleChange}
                  className={errors.license_number ? 'error' : ''}
                  placeholder="CL123456"
                  disabled={isLoading}
                />
                {errors.license_number && <span className="clinic-error-message">{errors.license_number}</span>}
              </div>

              <div className="clinic-form-group">
                <label htmlFor="tax_id">Tax ID</label>
                <input
                  type="text"
                  id="tax_id"
                  name="tax_id"
                  value={formData.tax_id}
                  onChange={handleChange}
                  placeholder="12-3456789"
                  disabled={isLoading}
                />
              </div>
            </div>

            <div className="clinic-form-group">
              <label htmlFor="npi_number">NPI Number</label>
              <input
                type="text"
                id="npi_number"
                name="npi_number"
                value={formData.npi_number}
                onChange={handleChange}
                placeholder="1234567890"
                disabled={isLoading}
              />
            </div>
          </div>

          {/* Account Security */}
          <div className="clinic-form-section">
            <h3>Account Security</h3>
            
            <div className="clinic-form-row">
              <div className="clinic-form-group">
                <label htmlFor="password">Password *</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className={errors.password ? 'error' : ''}
                  placeholder="Create a strong password"
                  disabled={isLoading}
                />
                {errors.password && <span className="clinic-error-message">{errors.password}</span>}
              </div>

              <div className="clinic-form-group">
                <label htmlFor="confirmPassword">Confirm Password *</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className={errors.confirmPassword ? 'error' : ''}
                  placeholder="Confirm your password"
                  disabled={isLoading}
                />
                {errors.confirmPassword && <span className="clinic-error-message">{errors.confirmPassword}</span>}
              </div>
            </div>
          </div>

          <button 
            type="submit" 
            className={`clinic-auth-button ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? 'Creating Account...' : 'Register Clinic'}
          </button>
        </form>

        <div className="clinic-auth-footer">
          <p>
            Already have a clinic account?{' '}
            <a href="/clinic/login" className="clinic-auth-link">
              Sign in here
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default ClinicRegister; 