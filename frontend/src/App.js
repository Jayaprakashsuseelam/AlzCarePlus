/**
=========================================================
* Material Dashboard 2 React - v2.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2023 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';

// Import patient components
import PatientLogin from './components/patient/Login';
import PatientRegister from './components/patient/Register';
import ResetPassword from './components/patient/ResetPassword';
import PatientDashboard from './components/patient/PatientDashboard';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/patient/login" element={<PatientLogin />} />
          <Route path="/patient/register" element={<PatientRegister />} />
          <Route path="/patient/reset-password" element={<ResetPassword />} />
          <Route path="/patient/dashboard" element={<PatientDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

// Landing page component
function LandingPage() {
  return (
    <div className="landing-container">
      <h1 className="landing-title">AlzCarePlus</h1>
      <p className="landing-description">
        AlzCarePlus is an innovative platform designed to support patients, caregivers, and healthcare professionals in the management and care of Alzheimer's disease. Our mission is to provide accessible tools, resources, and insights to improve quality of life and care outcomes.
      </p>
      
      <div className="landing-actions">
        <h3>Patient Portal</h3>
        <div className="action-links">
          <Link to="/patient/login" className="landing-btn primary">Patient Login</Link>
          <Link to="/patient/register" className="landing-btn secondary">Patient Registration</Link>
          <Link to="/patient/dashboard" className="landing-btn secondary">View Dashboard</Link>
        </div>
      </div>
    </div>
  );
}

export default App;
