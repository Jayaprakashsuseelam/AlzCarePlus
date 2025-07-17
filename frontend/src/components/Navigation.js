import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

const Navigation = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeSubmenu, setActiveSubmenu] = useState(null);
  const [isScrolled, setIsScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    setIsMenuOpen(false);
    setActiveSubmenu(null);
  }, [location]);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const toggleSubmenu = (menuName) => {
    setActiveSubmenu(activeSubmenu === menuName ? null : menuName);
  };

  const menuItems = [
    {
      name: 'Home',
      path: '/',
      hasSubmenu: false
    },
    {
      name: 'Services',
      path: '/services',
      hasSubmenu: true,
      submenu: [
        { name: 'Patient Care', path: '/services/patient-care' },
        { name: 'Caregiver Support', path: '/services/caregiver-support' },
        { name: 'Healthcare Integration', path: '/services/healthcare-integration' },
        { name: 'AI-Powered Analytics', path: '/services/analytics' }
      ]
    },
    {
      name: 'For Patients',
      path: '/patients',
      hasSubmenu: true,
      submenu: [
        { name: 'Register', path: '/patient/register' },
        { name: 'Login', path: '/patient/login' },
        { name: 'Dashboard', path: '/patient/dashboard' },
        { name: 'Care Plans', path: '/patient/care-plans' }
      ]
    },
    {
      name: 'For Caregivers',
      path: '/caregivers',
      hasSubmenu: true,
      submenu: [
        { name: 'Register', path: '/caretaker/register' },
        { name: 'Login', path: '/caretaker/login' },
        { name: 'Dashboard', path: '/caretaker/dashboard' },
        { name: 'Management', path: '/caretaker/management' }
      ]
    },
    {
      name: 'For Clinics',
      path: '/clinics',
      hasSubmenu: true,
      submenu: [
        { name: 'Register', path: '/clinic/register' },
        { name: 'Login', path: '/clinic/login' },
        { name: 'Dashboard', path: '/clinic/dashboard' },
        { name: 'Staff Management', path: '/clinic/staff' }
      ]
    },
    {
      name: 'Resources',
      path: '/resources',
      hasSubmenu: true,
      submenu: [
        { name: 'Blog', path: '/blog' },
        { name: 'Research', path: '/research' },
        { name: 'Support Center', path: '/support' },
        { name: 'Training Materials', path: '/training' }
      ]
    },
    {
      name: 'About',
      path: '/about',
      hasSubmenu: false
    },
    {
      name: 'Contact',
      path: '/contact',
      hasSubmenu: false
    }
  ];

  return (
    <nav className={`navigation ${isScrolled ? 'scrolled' : ''}`}>
      <div className="nav-container">
        {/* Logo */}
        <Link to="/" className="nav-logo">
          <div className="logo-icon">
            <i className="fas fa-brain"></i>
          </div>
          <span className="logo-text">AlzCarePlus</span>
        </Link>

        {/* Desktop Menu */}
        <div className={`nav-menu ${isMenuOpen ? 'active' : ''}`}>
          {menuItems.map((item, index) => (
            <div
              key={index}
              className={`nav-item ${item.hasSubmenu ? 'has-submenu' : ''}`}
              onMouseEnter={() => item.hasSubmenu && setActiveSubmenu(item.name)}
              onMouseLeave={() => item.hasSubmenu && setActiveSubmenu(null)}
            >
              {item.hasSubmenu ? (
                <>
                  <button
                    className="nav-link submenu-trigger"
                    onClick={() => toggleSubmenu(item.name)}
                  >
                    {item.name}
                    <i className="fas fa-chevron-down"></i>
                  </button>
                  <div className={`submenu ${activeSubmenu === item.name ? 'active' : ''}`}>
                    {item.submenu.map((subItem, subIndex) => (
                      <Link
                        key={subIndex}
                        to={subItem.path}
                        className="submenu-item"
                      >
                        {subItem.name}
                      </Link>
                    ))}
                  </div>
                </>
              ) : (
                <Link to={item.path} className="nav-link">
                  {item.name}
                </Link>
              )}
            </div>
          ))}
        </div>

        {/* CTA Buttons */}
        <div className="nav-actions">
          <Link to="/patient/login" className="btn btn-outline btn-small">
            Patient Login
          </Link>
          <Link to="/patient/register" className="btn btn-primary btn-small">
            Get Started
          </Link>
        </div>

        {/* Mobile Menu Toggle */}
        <button
          className={`mobile-menu-toggle ${isMenuOpen ? 'active' : ''}`}
          onClick={toggleMenu}
          aria-label="Toggle menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>

      {/* Mobile Menu */}
      <div className={`mobile-menu ${isMenuOpen ? 'active' : ''}`}>
        <div className="mobile-menu-content">
          {menuItems.map((item, index) => (
            <div key={index} className="mobile-nav-item">
              {item.hasSubmenu ? (
                <>
                  <button
                    className="mobile-nav-link submenu-trigger"
                    onClick={() => toggleSubmenu(item.name)}
                  >
                    {item.name}
                    <i className={`fas fa-chevron-${activeSubmenu === item.name ? 'up' : 'down'}`}></i>
                  </button>
                  <div className={`mobile-submenu ${activeSubmenu === item.name ? 'active' : ''}`}>
                    {item.submenu.map((subItem, subIndex) => (
                      <Link
                        key={subIndex}
                        to={subItem.path}
                        className="mobile-submenu-item"
                      >
                        {subItem.name}
                      </Link>
                    ))}
                  </div>
                </>
              ) : (
                <Link to={item.path} className="mobile-nav-link">
                  {item.name}
                </Link>
              )}
            </div>
          ))}
          
          <div className="mobile-actions">
            <Link to="/patient/login" className="btn btn-outline btn-full">
              Patient Login
            </Link>
            <Link to="/patient/register" className="btn btn-primary btn-full">
              Get Started
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation; 