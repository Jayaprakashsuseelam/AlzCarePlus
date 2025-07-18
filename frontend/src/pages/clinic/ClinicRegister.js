import React, { useState } from 'react';
import { FaHospital, FaEye, FaEyeSlash, FaSpinner, FaArrowLeft, FaArrowRight, FaCheck } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom';
import './ClinicRegister.css';

const ClinicRegister = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    // Step 1: Basic Information
    clinic_name: '',
    clinic_type: 'general',
    email: '',
    password: '',
    confirm_password: '',
    
    // Step 2: Contact Information
    phone: '',
    fax: '',
    website: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    country: 'United States',
    
    // Step 3: Business Information
    license_number: '',
    tax_id: '',
    npi_number: '',
    
    // Step 4: Operating Hours
    operating_hours: {
      monday: { open: '09:00', close: '17:00', closed: false },
      tuesday: { open: '09:00', close: '17:00', closed: false },
      wednesday: { open: '09:00', close: '17:00', closed: false },
      thursday: { open: '09:00', close: '17:00', closed: false },
      friday: { open: '09:00', close: '17:00', closed: false },
      saturday: { open: '09:00', close: '17:00', closed: false },
      sunday: { open: '09:00', close: '17:00', closed: true }
    }
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const steps = [
    { number: 1, title: 'Basic Information', description: 'Clinic details and account setup' },
    { number: 2, title: 'Contact Information', description: 'Address and contact details' },
    { number: 3, title: 'Business Information', description: 'Licenses and certifications' },
    { number: 4, title: 'Operating Hours', description: 'Schedule and availability' }
  ];

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

  const daysOfWeek = [
    { key: 'monday', label: 'Monday' },
    { key: 'tuesday', label: 'Tuesday' },
    { key: 'wednesday', label: 'Wednesday' },
    { key: 'thursday', label: 'Thursday' },
    { key: 'friday', label: 'Friday' },
    { key: 'saturday', label: 'Saturday' },
    { key: 'sunday', label: 'Sunday' }
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
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

  const validateStep = (step) => {
    const newErrors = {};

    switch (step) {
      case 1:
        if (!formData.clinic_name.trim()) {
          newErrors.clinic_name = 'Clinic name is required';
        }
        if (!formData.email) {
          newErrors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
          newErrors.email = 'Please enter a valid email address';
        }
        if (!formData.password) {
          newErrors.password = 'Password is required';
        } else if (formData.password.length < 8) {
          newErrors.password = 'Password must be at least 8 characters';
        }
        if (!formData.confirm_password) {
          newErrors.confirm_password = 'Please confirm your password';
        } else if (formData.password !== formData.confirm_password) {
          newErrors.confirm_password = 'Passwords do not match';
        }
        break;

      case 2:
        if (!formData.phone.trim()) {
          newErrors.phone = 'Phone number is required';
        }
        if (!formData.address.trim()) {
          newErrors.address = 'Address is required';
        }
        if (!formData.city.trim()) {
          newErrors.city = 'City is required';
        }
        if (!formData.state.trim()) {
          newErrors.state = 'State is required';
        }
        if (!formData.zip_code.trim()) {
          newErrors.zip_code = 'ZIP code is required';
        }
        break;

      case 3:
        if (!formData.license_number.trim()) {
          newErrors.license_number = 'License number is required';
        }
        break;

      case 4:
        // Validate that at least one day is open
        const hasOpenDay = Object.values(formData.operating_hours).some(day => !day.closed);
        if (!hasOpenDay) {
          newErrors.operating_hours = 'At least one day must be open';
        }
        break;

      default:
        break;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const nextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, steps.length));
    }
  };

  const prevStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateStep(currentStep)) {
      return;
    }

    setLoading(true);

    try {
      // Simulated API call - replace with actual API endpoint
      const response = await fetch('/api/clinics/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        
        // Store tokens and clinic data
        localStorage.setItem('clinicToken', data.tokens.access);
        localStorage.setItem('clinicRefreshToken', data.tokens.refresh);
        localStorage.setItem('clinicData', JSON.stringify(data.clinic));
        
        // Redirect to clinic dashboard
        navigate('/clinic/dashboard');
      } else {
        const errorData = await response.json();
        setErrors({
          general: errorData.message || 'Registration failed. Please try again.'
        });
      }
    } catch (error) {
      console.error('Registration error:', error);
      setErrors({
        general: 'Network error. Please try again.'
      });
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="step-content">
            <div className="form-group">
              <label htmlFor="clinic_name">Clinic Name *</label>
              <input
                type="text"
                id="clinic_name"
                name="clinic_name"
                value={formData.clinic_name}
                onChange={handleChange}
                className={errors.clinic_name ? 'error' : ''}
                placeholder="Enter your clinic name"
                disabled={loading}
              />
              {errors.clinic_name && <span className="error-text">{errors.clinic_name}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="clinic_type">Clinic Type</label>
              <select
                id="clinic_type"
                name="clinic_type"
                value={formData.clinic_type}
                onChange={handleChange}
                disabled={loading}
              >
                {clinicTypes.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="email">Email Address *</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={errors.email ? 'error' : ''}
                placeholder="Enter your clinic email"
                disabled={loading}
              />
              {errors.email && <span className="error-text">{errors.email}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="password">Password *</label>
              <div className="input-container">
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className={errors.password ? 'error' : ''}
                  placeholder="Create a strong password"
                  disabled={loading}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={loading}
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              {errors.password && <span className="error-text">{errors.password}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="confirm_password">Confirm Password *</label>
              <div className="input-container">
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  id="confirm_password"
                  name="confirm_password"
                  value={formData.confirm_password}
                  onChange={handleChange}
                  className={errors.confirm_password ? 'error' : ''}
                  placeholder="Confirm your password"
                  disabled={loading}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  disabled={loading}
                >
                  {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              {errors.confirm_password && <span className="error-text">{errors.confirm_password}</span>}
            </div>
          </div>
        );

      case 2:
        return (
          <div className="step-content">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="phone">Phone Number *</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  className={errors.phone ? 'error' : ''}
                  placeholder="Enter phone number"
                  disabled={loading}
                />
                {errors.phone && <span className="error-text">{errors.phone}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="fax">Fax Number</label>
                <input
                  type="tel"
                  id="fax"
                  name="fax"
                  value={formData.fax}
                  onChange={handleChange}
                  placeholder="Enter fax number"
                  disabled={loading}
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="website">Website</label>
              <input
                type="url"
                id="website"
                name="website"
                value={formData.website}
                onChange={handleChange}
                placeholder="Enter website URL"
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="address">Address *</label>
              <textarea
                id="address"
                name="address"
                value={formData.address}
                onChange={handleChange}
                className={errors.address ? 'error' : ''}
                placeholder="Enter full address"
                rows="3"
                disabled={loading}
              />
              {errors.address && <span className="error-text">{errors.address}</span>}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="city">City *</label>
                <input
                  type="text"
                  id="city"
                  name="city"
                  value={formData.city}
                  onChange={handleChange}
                  className={errors.city ? 'error' : ''}
                  placeholder="Enter city"
                  disabled={loading}
                />
                {errors.city && <span className="error-text">{errors.city}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="state">State *</label>
                <input
                  type="text"
                  id="state"
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  className={errors.state ? 'error' : ''}
                  placeholder="Enter state"
                  disabled={loading}
                />
                {errors.state && <span className="error-text">{errors.state}</span>}
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="zip_code">ZIP Code *</label>
                <input
                  type="text"
                  id="zip_code"
                  name="zip_code"
                  value={formData.zip_code}
                  onChange={handleChange}
                  className={errors.zip_code ? 'error' : ''}
                  placeholder="Enter ZIP code"
                  disabled={loading}
                />
                {errors.zip_code && <span className="error-text">{errors.zip_code}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="country">Country</label>
                <input
                  type="text"
                  id="country"
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                  placeholder="Enter country"
                  disabled={loading}
                />
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="step-content">
            <div className="form-group">
              <label htmlFor="license_number">License Number *</label>
              <input
                type="text"
                id="license_number"
                name="license_number"
                value={formData.license_number}
                onChange={handleChange}
                className={errors.license_number ? 'error' : ''}
                placeholder="Enter clinic license number"
                disabled={loading}
              />
              {errors.license_number && <span className="error-text">{errors.license_number}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="tax_id">Tax ID</label>
              <input
                type="text"
                id="tax_id"
                name="tax_id"
                value={formData.tax_id}
                onChange={handleChange}
                placeholder="Enter tax ID"
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="npi_number">NPI Number</label>
              <input
                type="text"
                id="npi_number"
                name="npi_number"
                value={formData.npi_number}
                onChange={handleChange}
                placeholder="Enter National Provider Identifier"
                disabled={loading}
              />
            </div>
          </div>
        );

      case 4:
        return (
          <div className="step-content">
            <div className="operating-hours">
              <h3>Operating Hours</h3>
              <p>Set your clinic's operating hours for each day of the week</p>
              
              {daysOfWeek.map(day => (
                <div key={day.key} className="day-schedule">
                  <div className="day-header">
                    <label className="day-label">
                      <input
                        type="checkbox"
                        checked={!formData.operating_hours[day.key].closed}
                        onChange={(e) => handleOperatingHoursChange(day.key, 'closed', !e.target.checked)}
                        disabled={loading}
                      />
                      <span>{day.label}</span>
                    </label>
                  </div>
                  
                  {!formData.operating_hours[day.key].closed && (
                    <div className="time-inputs">
                      <div className="time-input">
                        <label>Open</label>
                        <input
                          type="time"
                          value={formData.operating_hours[day.key].open}
                          onChange={(e) => handleOperatingHoursChange(day.key, 'open', e.target.value)}
                          disabled={loading}
                        />
                      </div>
                      <div className="time-input">
                        <label>Close</label>
                        <input
                          type="time"
                          value={formData.operating_hours[day.key].close}
                          onChange={(e) => handleOperatingHoursChange(day.key, 'close', e.target.value)}
                          disabled={loading}
                        />
                      </div>
                    </div>
                  )}
                </div>
              ))}
              
              {errors.operating_hours && (
                <span className="error-text">{errors.operating_hours}</span>
              )}
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="clinic-register-container">
      <div className="clinic-register-card">
        <div className="register-header">
          <div className="logo-container">
            <FaHospital className="logo-icon" />
            <h1>AlzCarePlus</h1>
          </div>
          <h2>Register Your Clinic</h2>
          <p>Join our network of healthcare providers</p>
        </div>

        {/* Progress Steps */}
        <div className="progress-steps">
          {steps.map((step, index) => (
            <div
              key={step.number}
              className={`step ${currentStep >= step.number ? 'active' : ''} ${currentStep > step.number ? 'completed' : ''}`}
            >
              <div className="step-number">
                {currentStep > step.number ? <FaCheck /> : step.number}
              </div>
              <div className="step-info">
                <h4>{step.title}</h4>
                <p>{step.description}</p>
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="register-form">
          {errors.general && (
            <div className="error-message general">
              {errors.general}
            </div>
          )}

          {renderStepContent()}

          <div className="form-actions">
            {currentStep > 1 && (
              <button
                type="button"
                className="btn btn-secondary"
                onClick={prevStep}
                disabled={loading}
              >
                <FaArrowLeft /> Previous
              </button>
            )}
            
            {currentStep < steps.length ? (
              <button
                type="button"
                className="btn btn-primary"
                onClick={nextStep}
                disabled={loading}
              >
                Next <FaArrowRight />
              </button>
            ) : (
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <FaSpinner className="spinner" />
                    Creating Account...
                  </>
                ) : (
                  <>
                    <FaCheck />
                    Create Account
                  </>
                )}
              </button>
            )}
          </div>
        </form>

        <div className="register-footer">
          <p>
            Already have a clinic account?{' '}
            <Link to="/clinic/login" className="login-link">
              Sign in here
            </Link>
          </p>
          <p>
            <Link to="/" className="back-home">
              ← Back to Home
            </Link>
          </p>
        </div>
      </div>

      <div className="register-background">
        <div className="background-pattern"></div>
        <div className="background-overlay"></div>
      </div>
    </div>
  );
};

export default ClinicRegister; 