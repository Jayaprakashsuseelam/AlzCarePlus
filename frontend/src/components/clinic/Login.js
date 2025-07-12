import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { clinicAPI, authUtils, handleAPIError } from '../../services/api';
import './ClinicAuth.css';

const ClinicLogin = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false
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
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    if (!formData.password) {
      newErrors.password = 'Password is required';
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
      const response = await clinicAPI.login({
        email: formData.email,
        password: formData.password
      });

      // Store the token
      authUtils.setToken(response.tokens.access);
      
      // Store clinic data if remember me is checked
      if (formData.rememberMe) {
        localStorage.setItem('clinicData', JSON.stringify(response.clinic));
      }

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
          <h1>Clinic Login</h1>
          <p>Access your AlzCarePlus clinic management portal</p>
        </div>

        {apiError && (
          <div className="clinic-error-alert">
            {apiError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="clinic-auth-form">
          <div className="clinic-form-group">
            <label htmlFor="email">Clinic Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'error' : ''}
              placeholder="Enter your clinic email"
              disabled={isLoading}
            />
            {errors.email && <span className="clinic-error-message">{errors.email}</span>}
          </div>

          <div className="clinic-form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className={errors.password ? 'error' : ''}
              placeholder="Enter your password"
              disabled={isLoading}
            />
            {errors.password && <span className="clinic-error-message">{errors.password}</span>}
          </div>

          <div className="clinic-form-options">
            <label className="clinic-checkbox-label">
              <input
                type="checkbox"
                name="rememberMe"
                checked={formData.rememberMe}
                onChange={handleChange}
                disabled={isLoading}
              />
              Remember me
            </label>
            <a href="/clinic/reset-password" className="clinic-forgot-password">
              Forgot Password?
            </a>
          </div>

          <button 
            type="submit" 
            className={`clinic-auth-button ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? 'Signing In...' : 'Sign In to Clinic Portal'}
          </button>
        </form>

        <div className="clinic-auth-footer">
          <p>
            Don't have a clinic account?{' '}
            <a href="/clinic/register" className="clinic-auth-link">
              Register your clinic
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default ClinicLogin; 