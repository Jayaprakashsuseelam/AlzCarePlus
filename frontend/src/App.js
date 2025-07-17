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
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import navigation and layout components
import Navigation from './components/Navigation';
import Footer from './components/Footer';

// Import main pages
import Home from './pages/Home';
import About from './pages/About';
import Contact from './pages/Contact';

// Import patient components
import PatientLogin from './components/patient/Login';
import PatientRegister from './components/patient/Register';
import ResetPassword from './components/patient/ResetPassword';
import PatientDashboard from './components/patient/PatientDashboard';

// Import caretaker components
import CaretakerLogin from './components/caretaker/Login';
import CaretakerRegister from './components/caretaker/Register';
import CaretakerDashboard from './components/caretaker/CaretakerDashboard';
import CaretakerManagement from './pages/caretaker/CaretakerManagement';
import CaretakerDetails from './pages/caretaker/CaretakerDetails';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <main className="main-content">
          <Routes>
            {/* Main Website Pages */}
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            
            {/* Patient Routes */}
            <Route path="/patient/login" element={<PatientLogin />} />
            <Route path="/patient/register" element={<PatientRegister />} />
            <Route path="/patient/reset-password" element={<ResetPassword />} />
            <Route path="/patient/dashboard" element={<PatientDashboard />} />
            
            {/* Caretaker Routes */}
            <Route path="/caretaker/login" element={<CaretakerLogin />} />
            <Route path="/caretaker/register" element={<CaretakerRegister />} />
            <Route path="/caretaker/dashboard" element={<CaretakerDashboard />} />
            <Route path="/caretaker/management" element={<CaretakerManagement />} />
            <Route path="/caretaker/details/:id" element={<CaretakerDetails />} />
            
            {/* Additional Routes - Placeholder pages */}
            <Route path="/services" element={<ServicesPage />} />
            <Route path="/services/patient-care" element={<ServicesPage />} />
            <Route path="/services/caregiver-support" element={<ServicesPage />} />
            <Route path="/services/healthcare-integration" element={<ServicesPage />} />
            <Route path="/services/analytics" element={<ServicesPage />} />
            <Route path="/patients" element={<PatientsPage />} />
            <Route path="/patient/care-plans" element={<PatientsPage />} />
            <Route path="/caregivers" element={<CaretakersPage />} />
            <Route path="/clinics" element={<ClinicsPage />} />
            <Route path="/clinic/register" element={<ClinicsPage />} />
            <Route path="/clinic/login" element={<ClinicsPage />} />
            <Route path="/clinic/dashboard" element={<ClinicsPage />} />
            <Route path="/clinic/staff" element={<ClinicsPage />} />
            <Route path="/resources" element={<ResourcesPage />} />
            <Route path="/blog" element={<BlogPage />} />
            <Route path="/research" element={<ResourcesPage />} />
            <Route path="/support" element={<ResourcesPage />} />
            <Route path="/training" element={<ResourcesPage />} />
            <Route path="/features" element={<FeaturesPage />} />
            <Route path="/pricing" element={<PricingPage />} />
            <Route path="/security" element={<SecurityPage />} />
            <Route path="/api" element={<ApiPage />} />
            <Route path="/integrations" element={<IntegrationsPage />} />
            <Route path="/hospitals" element={<HospitalsPage />} />
            <Route path="/enterprise" element={<EnterprisePage />} />
            <Route path="/docs" element={<DocsPage />} />
            <Route path="/careers" element={<CareersPage />} />
            <Route path="/press" element={<PressPage />} />
            <Route path="/partners" element={<PartnersPage />} />
            <Route path="/privacy" element={<PrivacyPage />} />
            <Route path="/terms" element={<TermsPage />} />
            <Route path="/cookies" element={<CookiesPage />} />
            <Route path="/accessibility" element={<AccessibilityPage />} />
            
            {/* 404 Page */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

// Placeholder page components
function ServicesPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Services</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function PatientsPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>For Patients</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function CaretakersPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>For Caregivers</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function ClinicsPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>For Clinics</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function ResourcesPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Resources</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function BlogPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Blog</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function FeaturesPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Features</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function PricingPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Pricing</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function SecurityPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Security</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function ApiPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>API</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function IntegrationsPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Integrations</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function HospitalsPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>For Hospitals</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function EnterprisePage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Enterprise</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function DocsPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Documentation</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function CareersPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Careers</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function PressPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Press</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function PartnersPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Partners</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function PrivacyPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Privacy Policy</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function TermsPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Terms of Service</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function CookiesPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Cookie Policy</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function AccessibilityPage() {
  return (
    <div className="placeholder-page">
      <div className="container">
        <h1>Accessibility</h1>
        <p>This page is under development. Please check back soon!</p>
      </div>
    </div>
  );
}

function NotFoundPage() {
  return (
    <div className="not-found-page">
      <div className="container">
        <h1>404 - Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/" className="btn btn-primary">Go Home</a>
      </div>
    </div>
  );
}

export default App;
