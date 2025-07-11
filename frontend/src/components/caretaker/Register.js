import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI, authUtils, handleAPIError } from '../../services/api';
import './CaretakerAuth.css';

const CaretakerRegister = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    // Personal Information
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
    phone: '',
    date_of_birth: '',
    gender: '',
    
    // Professional Information
    professional_title: '',
    license_number: '',
    years_of_experience: '',
    specialization: '',
    employment_status: 'full-time',
    hire_date: '',
    
    // Terms
    agreeToTerms: false
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState('');

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

  const validateForm = () => {
    const newErrors = {};
    
    // Personal Information Validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }
    
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    if (!formData.first_name) {
      newErrors.first_name = 'First name is required';
    }
    
    if (!formData.last_name) {
      newErrors.last_name = 'Last name is required';
    }
    
    if (!formData.phone) {
      newErrors.phone = 'Phone number is required';
    }
    
    if (!formData.date_of_birth) {
      newErrors.date_of_birth = 'Date of birth is required';
    }
    
    if (!formData.gender) {
      newErrors.gender = 'Gender is required';
    }
    
    // Professional Information Validation
    if (!formData.professional_title) {
      newErrors.professional_title = 'Professional title is required';
    }
    
    if (!formData.license_number) {
      newErrors.license_number = 'License number is required';
    }
    
    if (!formData.years_of_experience) {
      newErrors.years_of_experience = 'Years of experience is required';
    } else if (isNaN(formData.years_of_experience) || parseInt(formData.years_of_experience) < 0) {
      newErrors.years_of_experience = 'Please enter a valid number';
    }
    
    if (!formData.specialization) {
      newErrors.specialization = 'Specialization is required';
    }
    
    if (!formData.hire_date) {
      newErrors.hire_date = 'Hire date is required';
    }
    
    // Terms Validation
    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms and conditions';
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
      const response = await authAPI.caretakerRegister({
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

      // Store the token
      authUtils.setToken(response.tokens.access);
      
      // Store user data
      localStorage.setItem('caretakerData', JSON.stringify(response.caretaker));

      // Redirect to dashboard
      navigate('/caretaker/dashboard');
      
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setApiError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Join AlzCarePlus</h1>
          <p>Create your professional caretaker account</p>
        </div>

        {apiError && (
          <div className="error-alert">
            {apiError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          {/* Personal Information */}
          <div className="professional-info">
            <h3>Personal Information</h3>
            <div className="professional-fields">
              <div className="form-group">
                <label htmlFor="first_name">First Name</label>
                <input
                  type="text"
                  id="first_name"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  className={errors.first_name ? 'error' : ''}
                  placeholder="Enter your first name"
                  disabled={isLoading}
                />
                {errors.first_name && <span className="error-message">{errors.first_name}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="last_name">Last Name</label>
                <input
                  type="text"
                  id="last_name"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  className={errors.last_name ? 'error' : ''}
                  placeholder="Enter your last name"
                  disabled={isLoading}
                />
                {errors.last_name && <span className="error-message">{errors.last_name}</span>}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={errors.email ? 'error' : ''}
                placeholder="Enter your email"
                disabled={isLoading}
              />
              {errors.email && <span className="error-message">{errors.email}</span>}
            </div>

            <div className="professional-fields">
              <div className="form-group">
                <label htmlFor="phone">Phone Number</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  className={errors.phone ? 'error' : ''}
                  placeholder="Enter your phone number"
                  disabled={isLoading}
                />
                {errors.phone && <span className="error-message">{errors.phone}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="date_of_birth">Date of Birth</label>
                <input
                  type="date"
                  id="date_of_birth"
                  name="date_of_birth"
                  value={formData.date_of_birth}
                  onChange={handleChange}
                  className={errors.date_of_birth ? 'error' : ''}
                  disabled={isLoading}
                />
                {errors.date_of_birth && <span className="error-message">{errors.date_of_birth}</span>}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="gender">Gender</label>
              <select
                id="gender"
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                className={errors.gender ? 'error' : ''}
                disabled={isLoading}
              >
                <option value="">Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
                <option value="prefer-not-to-say">Prefer not to say</option>
              </select>
              {errors.gender && <span className="error-message">{errors.gender}</span>}
            </div>
          </div>

          {/* Professional Information */}
          <div className="professional-info">
            <h3>Professional Information</h3>
            <div className="form-group">
              <label htmlFor="professional_title">Professional Title</label>
              <input
                type="text"
                id="professional_title"
                name="professional_title"
                value={formData.professional_title}
                onChange={handleChange}
                className={errors.professional_title ? 'error' : ''}
                placeholder="e.g., Registered Nurse, Certified Nursing Assistant"
                disabled={isLoading}
              />
              {errors.professional_title && <span className="error-message">{errors.professional_title}</span>}
            </div>

            <div className="professional-fields">
              <div className="form-group">
                <label htmlFor="license_number">License Number</label>
                <input
                  type="text"
                  id="license_number"
                  name="license_number"
                  value={formData.license_number}
                  onChange={handleChange}
                  className={errors.license_number ? 'error' : ''}
                  placeholder="Enter your license number"
                  disabled={isLoading}
                />
                {errors.license_number && <span className="error-message">{errors.license_number}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="years_of_experience">Years of Experience</label>
                <input
                  type="number"
                  id="years_of_experience"
                  name="years_of_experience"
                  value={formData.years_of_experience}
                  onChange={handleChange}
                  className={errors.years_of_experience ? 'error' : ''}
                  placeholder="0"
                  min="0"
                  disabled={isLoading}
                />
                {errors.years_of_experience && <span className="error-message">{errors.years_of_experience}</span>}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="specialization">Specialization</label>
              <input
                type="text"
                id="specialization"
                name="specialization"
                value={formData.specialization}
                onChange={handleChange}
                className={errors.specialization ? 'error' : ''}
                placeholder="e.g., Geriatric Care, Alzheimer's Care, Palliative Care"
                disabled={isLoading}
              />
              {errors.specialization && <span className="error-message">{errors.specialization}</span>}
            </div>

            <div className="professional-fields">
              <div className="form-group">
                <label htmlFor="employment_status">Employment Status</label>
                <select
                  id="employment_status"
                  name="employment_status"
                  value={formData.employment_status}
                  onChange={handleChange}
                  disabled={isLoading}
                >
                  <option value="full-time">Full Time</option>
                  <option value="part-time">Part Time</option>
                  <option value="contract">Contract</option>
                  <option value="volunteer">Volunteer</option>
                  <option value="private">Private Practice</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="hire_date">Hire Date</label>
                <input
                  type="date"
                  id="hire_date"
                  name="hire_date"
                  value={formData.hire_date}
                  onChange={handleChange}
                  className={errors.hire_date ? 'error' : ''}
                  disabled={isLoading}
                />
                {errors.hire_date && <span className="error-message">{errors.hire_date}</span>}
              </div>
            </div>
          </div>

          {/* Password */}
          <div className="professional-info">
            <h3>Account Security</h3>
            <div className="form-group">
              <label htmlFor="password">Password</label>
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
              {errors.password && <span className="error-message">{errors.password}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
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
              {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
            </div>
          </div>

          {/* Terms */}
          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="agreeToTerms"
                checked={formData.agreeToTerms}
                onChange={handleChange}
                disabled={isLoading}
              />
              <span className="checkmark"></span>
              I agree to the{' '}
              <a href="/terms" target="_blank" rel="noopener noreferrer" className="auth-link">
                Terms and Conditions
              </a>{' '}
              and{' '}
              <a href="/privacy" target="_blank" rel="noopener noreferrer" className="auth-link">
                Privacy Policy
              </a>
            </label>
            {errors.agreeToTerms && <span className="error-message">{errors.agreeToTerms}</span>}
          </div>

          <button 
            type="submit" 
            className={`auth-button ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Already have an account?{' '}
            <a href="/caretaker/login" className="auth-link">
              Sign in here
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default CaretakerRegister; 