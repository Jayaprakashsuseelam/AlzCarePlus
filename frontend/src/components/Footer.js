import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const footerSections = [
    {
      title: 'Product',
      links: [
        { name: 'Features', path: '/features' },
        { name: 'Pricing', path: '/pricing' },
        { name: 'Security', path: '/security' },
        { name: 'API', path: '/api' },
        { name: 'Integrations', path: '/integrations' }
      ]
    },
    {
      title: 'Solutions',
      links: [
        { name: 'For Patients', path: '/patients' },
        { name: 'For Caregivers', path: '/caregivers' },
        { name: 'For Clinics', path: '/clinics' },
        { name: 'For Hospitals', path: '/hospitals' },
        { name: 'Enterprise', path: '/enterprise' }
      ]
    },
    {
      title: 'Resources',
      links: [
        { name: 'Blog', path: '/blog' },
        { name: 'Documentation', path: '/docs' },
        { name: 'Support Center', path: '/support' },
        { name: 'Training', path: '/training' },
        { name: 'Research', path: '/research' }
      ]
    },
    {
      title: 'Company',
      links: [
        { name: 'About Us', path: '/about' },
        { name: 'Careers', path: '/careers' },
        { name: 'Press', path: '/press' },
        { name: 'Partners', path: '/partners' },
        { name: 'Contact', path: '/contact' }
      ]
    }
  ];

  const socialLinks = [
    { name: 'Facebook', icon: 'fab fa-facebook', url: 'https://facebook.com' },
    { name: 'Twitter', icon: 'fab fa-twitter', url: 'https://twitter.com' },
    { name: 'LinkedIn', icon: 'fab fa-linkedin', url: 'https://linkedin.com' },
    { name: 'YouTube', icon: 'fab fa-youtube', url: 'https://youtube.com' },
    { name: 'Instagram', icon: 'fab fa-instagram', url: 'https://instagram.com' }
  ];

  return (
    <footer className="footer">
      <div className="footer-container">
        {/* Main Footer Content */}
        <div className="footer-main">
          {/* Company Info */}
          <div className="footer-section company-info">
            <div className="footer-logo">
              <div className="logo-icon">
                <i className="fas fa-brain"></i>
              </div>
              <span className="logo-text">AlzCarePlus</span>
            </div>
            <p className="company-description">
              Advanced Alzheimer's care management platform connecting patients, 
              caregivers, and healthcare professionals for better outcomes.
            </p>
            <div className="social-links">
              {socialLinks.map((social, index) => (
                <a
                  key={index}
                  href={social.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="social-link"
                  aria-label={social.name}
                >
                  <i className={social.icon}></i>
                </a>
              ))}
            </div>
          </div>

          {/* Footer Links */}
          {footerSections.map((section, index) => (
            <div key={index} className="footer-section">
              <h3 className="footer-title">{section.title}</h3>
              <ul className="footer-links">
                {section.links.map((link, linkIndex) => (
                  <li key={linkIndex}>
                    <Link to={link.path} className="footer-link">
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Newsletter Signup */}
        <div className="footer-newsletter">
          <div className="newsletter-content">
            <h3>Stay Updated</h3>
            <p>Get the latest news and updates about Alzheimer's care and our platform.</p>
            <form className="newsletter-form">
              <div className="form-group">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="newsletter-input"
                  required
                />
                <button type="submit" className="newsletter-btn">
                  Subscribe
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="footer-bottom">
          <div className="footer-bottom-content">
            <div className="footer-legal">
              <p>&copy; {currentYear} AlzCarePlus. All rights reserved.</p>
              <div className="legal-links">
                <Link to="/privacy" className="legal-link">Privacy Policy</Link>
                <Link to="/terms" className="legal-link">Terms of Service</Link>
                <Link to="/cookies" className="legal-link">Cookie Policy</Link>
                <Link to="/accessibility" className="legal-link">Accessibility</Link>
              </div>
            </div>
            <div className="footer-certifications">
              <div className="certification">
                <i className="fas fa-shield-alt"></i>
                <span>HIPAA Compliant</span>
              </div>
              <div className="certification">
                <i className="fas fa-lock"></i>
                <span>256-bit SSL</span>
              </div>
              <div className="certification">
                <i className="fas fa-certificate"></i>
                <span>ISO 27001</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 