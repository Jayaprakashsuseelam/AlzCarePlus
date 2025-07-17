import React, { useState } from 'react';
import './Contact.css';

const Contact = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    organization: '',
    subject: '',
    message: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      setSubmitStatus('success');
      setFormData({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        organization: '',
        subject: '',
        message: ''
      });
    } catch (error) {
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  const contactMethods = [
    {
      icon: 'fas fa-phone',
      title: 'Phone Support',
      details: [
        'General Inquiries: +1 (555) 123-4567',
        'Technical Support: +1 (555) 123-4568',
        'Emergency: +1 (555) 123-4569'
      ],
      description: 'Available Monday-Friday, 8AM-6PM EST'
    },
    {
      icon: 'fas fa-envelope',
      title: 'Email Support',
      details: [
        'General: info@alzcareplus.com',
        'Support: support@alzcareplus.com',
        'Sales: sales@alzcareplus.com'
      ],
      description: 'We respond within 24 hours'
    },
    {
      icon: 'fas fa-comments',
      title: 'Live Chat',
      details: [
        'Available on our website',
        'Mobile app support',
        'Real-time assistance'
      ],
      description: 'Available 24/7 for urgent matters'
    }
  ];

  const officeLocations = [
    {
      city: 'San Francisco, CA',
      address: '123 Innovation Drive, Suite 100',
      zip: '94105',
      phone: '+1 (555) 123-4567',
      hours: 'Mon-Fri: 9AM-6PM PST'
    },
    {
      city: 'New York, NY',
      address: '456 Healthcare Avenue, Floor 15',
      zip: '10001',
      phone: '+1 (555) 123-4568',
      hours: 'Mon-Fri: 9AM-6PM EST'
    },
    {
      city: 'Austin, TX',
      address: '789 Tech Boulevard, Building A',
      zip: '73301',
      phone: '+1 (555) 123-4569',
      hours: 'Mon-Fri: 9AM-6PM CST'
    }
  ];

  const faqItems = [
    {
      question: 'How do I get started with AlzCarePlus?',
      answer: 'Getting started is easy! Simply register for an account, complete your profile, and our team will guide you through the onboarding process.'
    },
    {
      question: 'Is AlzCarePlus HIPAA compliant?',
      answer: 'Yes, AlzCarePlus is fully HIPAA compliant. We maintain the highest standards of data security and privacy protection.'
    },
    {
      question: 'What types of healthcare organizations can use AlzCarePlus?',
      answer: 'AlzCarePlus is designed for hospitals, clinics, nursing homes, home care agencies, and individual healthcare providers.'
    },
    {
      question: 'Do you offer training and support?',
      answer: 'Yes, we provide comprehensive training, documentation, and 24/7 support to ensure successful implementation and usage.'
    }
  ];

  return (
    <div className="contact">
      {/* Hero Section */}
      <section className="contact-hero">
        <div className="container">
          <div className="hero-content">
            <h1>Contact Us</h1>
            <p>
              We're here to help! Get in touch with our team for support, 
              questions, or to learn more about how AlzCarePlus can help you.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Methods */}
      <section className="contact-methods">
        <div className="container">
          <div className="section-header">
            <h2>Get in Touch</h2>
            <p>Choose the best way to reach our team</p>
          </div>
          
          <div className="methods-grid">
            {contactMethods.map((method, index) => (
              <div key={index} className="method-card">
                <div className="method-icon">
                  <i className={method.icon}></i>
                </div>
                <h3>{method.title}</h3>
                <div className="method-details">
                  {method.details.map((detail, detailIndex) => (
                    <p key={detailIndex}>{detail}</p>
                  ))}
                </div>
                <p className="method-description">{method.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Form & Office Locations */}
      <section className="contact-main">
        <div className="container">
          <div className="contact-content">
            {/* Contact Form */}
            <div className="contact-form-section">
              <h2>Send us a Message</h2>
              <p>Fill out the form below and we'll get back to you as soon as possible.</p>
              
              <form className="contact-form" onSubmit={handleSubmit}>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="firstName">First Name *</label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="lastName">Last Name *</label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="email">Email Address *</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="phone">Phone Number</label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                    />
                  </div>
                </div>
                
                <div className="form-group">
                  <label htmlFor="organization">Organization</label>
                  <input
                    type="text"
                    id="organization"
                    name="organization"
                    value={formData.organization}
                    onChange={handleInputChange}
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="subject">Subject *</label>
                  <select
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="">Select a subject</option>
                    <option value="general">General Inquiry</option>
                    <option value="support">Technical Support</option>
                    <option value="sales">Sales Inquiry</option>
                    <option value="partnership">Partnership</option>
                    <option value="feedback">Feedback</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label htmlFor="message">Message *</label>
                  <textarea
                    id="message"
                    name="message"
                    rows="6"
                    value={formData.message}
                    onChange={handleInputChange}
                    required
                    placeholder="Please describe your inquiry or question..."
                  ></textarea>
                </div>
                
                <div className="form-actions">
                  <button
                    type="submit"
                    className="btn btn-primary btn-large"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? 'Sending...' : 'Send Message'}
                  </button>
                </div>
                
                {submitStatus === 'success' && (
                  <div className="alert alert-success">
                    Thank you! Your message has been sent successfully. We'll get back to you soon.
                  </div>
                )}
                
                {submitStatus === 'error' && (
                  <div className="alert alert-error">
                    Sorry, there was an error sending your message. Please try again.
                  </div>
                )}
              </form>
            </div>

            {/* Office Locations */}
            <div className="office-locations">
              <h2>Our Offices</h2>
              <p>Visit us at one of our locations</p>
              
              <div className="locations-list">
                {officeLocations.map((location, index) => (
                  <div key={index} className="location-card">
                    <div className="location-header">
                      <h3>{location.city}</h3>
                      <i className="fas fa-map-marker-alt"></i>
                    </div>
                    <div className="location-details">
                      <p>{location.address}</p>
                      <p>{location.zip}</p>
                      <p><strong>Phone:</strong> {location.phone}</p>
                      <p><strong>Hours:</strong> {location.hours}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="faq-section">
        <div className="container">
          <div className="section-header">
            <h2>Frequently Asked Questions</h2>
            <p>Find answers to common questions about AlzCarePlus</p>
          </div>
          
          <div className="faq-grid">
            {faqItems.map((item, index) => (
              <div key={index} className="faq-item">
                <h3>{item.question}</h3>
                <p>{item.answer}</p>
              </div>
            ))}
          </div>
          
          <div className="faq-cta">
            <p>Can't find what you're looking for?</p>
            <a href="#contact-form" className="btn btn-outline">
              Contact Support
            </a>
          </div>
        </div>
      </section>

      {/* Map Section */}
      <section className="map-section">
        <div className="container">
          <div className="map-content">
            <h2>Find Us</h2>
            <p>Our headquarters and regional offices</p>
            <div className="map-placeholder">
              <i className="fas fa-map"></i>
              <p>Interactive map coming soon</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Contact; 