import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Auth.css';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    keepSignedIn: false
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Add authentication logic here
    navigate('/dashboard');
  };

  return (
    <div className="auth-root">
      <div className="auth-left">
        <div className="company-name">COMPANY NAME</div>
        <div className="welcome-title">Nice to see you again</div>
        <div className="welcome-main">WELCOME BACK</div>
        <div className="welcome-desc">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nos
        </div>
      </div>
      <div className="auth-right">
        <div className="auth-card">
          <h2>Login Account</h2>
          <div className="auth-desc">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.
          </div>
          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="Email ID"
                autoComplete="username"
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                placeholder="Password"
                autoComplete="current-password"
              />
            </div>
            <div className="auth-options">
              <label>
                <input
                  type="checkbox"
                  name="keepSignedIn"
                  checked={formData.keepSignedIn}
                  onChange={handleChange}
                />
                Keep me signed in
              </label>
              <Link to="/register" className="auth-link">Already a member?</Link>
            </div>
            <button type="submit" className="auth-button">
              SUBSCRIBE
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login; 