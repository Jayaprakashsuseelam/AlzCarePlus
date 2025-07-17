import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <h1>Advanced Alzheimer's Care Management</h1>
            <p>
              AlzCarePlus provides comprehensive care management solutions for Alzheimer's patients, 
              connecting caregivers, healthcare professionals, and families in one integrated platform.
            </p>
            <div className="hero-buttons">
              <Link to="/patient/register" className="btn btn-primary">
                Get Started Today
              </Link>
              <Link to="/about" className="btn btn-secondary">
                Learn More
              </Link>
            </div>
          </div>
          <div className="hero-image">
            <div className="hero-visual">
              <div className="floating-card card-1">
                <i className="fas fa-user-md"></i>
                <span>Professional Care</span>
              </div>
              <div className="floating-card card-2">
                <i className="fas fa-heart"></i>
                <span>Family Support</span>
              </div>
              <div className="floating-card card-3">
                <i className="fas fa-chart-line"></i>
                <span>Progress Tracking</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <div className="section-header">
            <h2>Why Choose AlzCarePlus?</h2>
            <p>Comprehensive care management designed specifically for Alzheimer's patients and their families</p>
          </div>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-brain"></i>
              </div>
              <h3>Cognitive Health Monitoring</h3>
              <p>Advanced AI-powered cognitive assessment and monitoring tools to track patient progress and detect early warning signs.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-users"></i>
              </div>
              <h3>Multi-Stakeholder Collaboration</h3>
              <p>Connect doctors, nurses, caregivers, and family members in one secure platform for coordinated care.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-mobile-alt"></i>
              </div>
              <h3>Mobile Accessibility</h3>
              <p>Access patient information, update care plans, and communicate with the care team from anywhere, anytime.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-shield-alt"></i>
              </div>
              <h3>HIPAA Compliant</h3>
              <p>Enterprise-grade security and privacy protection ensuring all patient data remains confidential and secure.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-chart-bar"></i>
              </div>
              <h3>Analytics & Reporting</h3>
              <p>Comprehensive analytics and reporting tools to track patient progress and care quality metrics.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-clock"></i>
              </div>
              <h3>24/7 Support</h3>
              <p>Round-the-clock technical support and emergency assistance for caregivers and healthcare professionals.</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works-section">
        <div className="container">
          <div className="section-header">
            <h2>How AlzCarePlus Works</h2>
            <p>Simple steps to get started with comprehensive Alzheimer's care management</p>
          </div>
          
          <div className="steps-container">
            <div className="step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Register & Onboard</h3>
                <p>Create your account and complete the initial patient assessment to set up personalized care plans.</p>
              </div>
            </div>
            
            <div className="step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Connect Care Team</h3>
                <p>Invite doctors, nurses, caregivers, and family members to collaborate on patient care.</p>
              </div>
            </div>
            
            <div className="step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Monitor & Manage</h3>
                <p>Track patient progress, update care plans, and communicate with the entire care team.</p>
              </div>
            </div>
            
            <div className="step">
              <div className="step-number">4</div>
              <div className="step-content">
                <h3>Optimize Care</h3>
                <p>Use AI-powered insights and analytics to continuously improve care quality and patient outcomes.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="testimonials-section">
        <div className="container">
          <div className="section-header">
            <h2>What Our Users Say</h2>
            <p>Trusted by healthcare professionals and families nationwide</p>
          </div>
          
          <div className="testimonials-grid">
            <div className="testimonial-card">
              <div className="testimonial-content">
                <p>"AlzCarePlus has revolutionized how we manage Alzheimer's patients. The platform's intuitive interface and comprehensive features have improved our care coordination significantly."</p>
              </div>
              <div className="testimonial-author">
                <div className="author-info">
                  <h4>Dr. Sarah Johnson</h4>
                  <span>Neurologist, Memory Care Center</span>
                </div>
              </div>
            </div>
            
            <div className="testimonial-card">
              <div className="testimonial-content">
                <p>"As a family caregiver, AlzCarePlus has given me peace of mind. I can easily communicate with my mother's care team and track her progress in real-time."</p>
              </div>
              <div className="testimonial-author">
                <div className="author-info">
                  <h4>Michael Chen</h4>
                  <span>Family Caregiver</span>
                </div>
              </div>
            </div>
            
            <div className="testimonial-card">
              <div className="testimonial-content">
                <p>"The AI-powered cognitive assessment tools have helped us detect early warning signs and adjust treatment plans proactively. It's a game-changer for patient care."</p>
              </div>
              <div className="testimonial-author">
                <div className="author-info">
                  <h4>Nurse Emily Rodriguez</h4>
                  <span>Registered Nurse, Senior Care Facility</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Transform Alzheimer's Care?</h2>
            <p>Join thousands of healthcare professionals and families who trust AlzCarePlus for comprehensive care management.</p>
            <div className="cta-buttons">
              <Link to="/patient/register" className="btn btn-primary btn-large">
                Start Free Trial
              </Link>
              <Link to="/contact" className="btn btn-outline btn-large">
                Schedule Demo
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-number">10,000+</div>
              <div className="stat-label">Patients Served</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">500+</div>
              <div className="stat-label">Healthcare Partners</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">99.9%</div>
              <div className="stat-label">Uptime</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <div className="stat-label">Support Available</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home; 