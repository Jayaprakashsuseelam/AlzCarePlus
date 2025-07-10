import React, { useState } from 'react';
import { authAPI, handleAPIError } from '../../services/api';
import './PatientAuth.css';

const ResetPassword = () => {
  const [formData, setFormData] = useState({
    email: ''
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
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
      await authAPI.resetPassword(formData.email);
      setIsSubmitted(true);
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setApiError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  if (isSubmitted) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-header">
            <h1>Check Your Email</h1>
            <p>We've sent a password reset link to your email address</p>
          </div>
          
          <div className="success-message">
            <div className="success-icon">✓</div>
            <p>
              If an account with the email <strong>{formData.email}</strong> exists, 
              you will receive a password reset link shortly.
            </p>
            <p className="email-note">
              Please check your spam folder if you don't see the email in your inbox.
            </p>
          </div>

          <div className="auth-footer">
            <p>
              Didn't receive the email?{' '}
              <button 
                onClick={() => setIsSubmitted(false)}
                className="auth-link-button"
              >
                Try again
              </button>
            </p>
            <p>
              <a href="/patient/login" className="auth-link">
                Back to Sign In
              </a>
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Reset Password</h1>
          <p>Enter your email address to receive a password reset link</p>
        </div>

        {apiError && (
          <div className="error-alert">
            {apiError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'error' : ''}
              placeholder="Enter your email address"
              disabled={isLoading}
            />
            {errors.email && <span className="error-message">{errors.email}</span>}
          </div>

          <button 
            type="submit" 
            className={`auth-button ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? 'Sending...' : 'Send Reset Link'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Remember your password?{' '}
            <a href="/patient/login" className="auth-link">
              Sign in here
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword; 