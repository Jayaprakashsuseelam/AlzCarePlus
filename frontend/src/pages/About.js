import React from 'react';
import { Link } from 'react-router-dom';
import './About.css';

const About = () => {
  const teamMembers = [
    {
      name: 'Dr. Sarah Johnson',
      role: 'CEO & Co-Founder',
      image: '/images/team/sarah.jpg',
      bio: 'Neurologist with 15+ years experience in Alzheimer\'s research and patient care.',
      linkedin: 'https://linkedin.com/in/sarah-johnson'
    },
    {
      name: 'Michael Chen',
      role: 'CTO & Co-Founder',
      image: '/images/team/michael.jpg',
      bio: 'Technology leader with expertise in healthcare AI and machine learning.',
      linkedin: 'https://linkedin.com/in/michael-chen'
    },
    {
      name: 'Dr. Emily Rodriguez',
      role: 'Chief Medical Officer',
      image: '/images/team/emily.jpg',
      bio: 'Board-certified geriatrician specializing in cognitive disorders.',
      linkedin: 'https://linkedin.com/in/emily-rodriguez'
    },
    {
      name: 'David Kim',
      role: 'Head of Product',
      image: '/images/team/david.jpg',
      bio: 'Product strategist focused on user-centered healthcare solutions.',
      linkedin: 'https://linkedin.com/in/david-kim'
    }
  ];

  const values = [
    {
      icon: 'fas fa-heart',
      title: 'Patient-Centered Care',
      description: 'Every decision we make is guided by what\'s best for patients and their families.'
    },
    {
      icon: 'fas fa-shield-alt',
      title: 'Privacy & Security',
      description: 'We maintain the highest standards of data protection and HIPAA compliance.'
    },
    {
      icon: 'fas fa-lightbulb',
      title: 'Innovation',
      description: 'We continuously innovate to improve care outcomes and user experience.'
    },
    {
      icon: 'fas fa-hands-helping',
      title: 'Collaboration',
      description: 'We believe in the power of collaboration between all care stakeholders.'
    }
  ];

  const milestones = [
    {
      year: '2020',
      title: 'Company Founded',
      description: 'AlzCarePlus was founded with a mission to revolutionize Alzheimer\'s care.'
    },
    {
      year: '2021',
      title: 'First Patient',
      description: 'Our platform helped its first patient and family manage their care journey.'
    },
    {
      year: '2022',
      title: 'AI Integration',
      description: 'Launched AI-powered cognitive assessment and monitoring tools.'
    },
    {
      year: '2023',
      title: '10,000+ Patients',
      description: 'Reached milestone of serving over 10,000 patients nationwide.'
    },
    {
      year: '2024',
      title: 'Enterprise Launch',
      description: 'Expanded to serve healthcare systems and large care organizations.'
    }
  ];

  return (
    <div className="about">
      {/* Hero Section */}
      <section className="about-hero">
        <div className="container">
          <div className="hero-content">
            <h1>About AlzCarePlus</h1>
            <p>
              We're on a mission to transform Alzheimer's care through technology, 
              compassion, and innovation. Our platform connects patients, caregivers, 
              and healthcare professionals in a seamless, secure ecosystem.
            </p>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="mission-section">
        <div className="container">
          <div className="mission-content">
            <div className="mission-text">
              <h2>Our Mission</h2>
              <p>
                To improve the quality of life for Alzheimer's patients and their families 
                by providing comprehensive, accessible, and personalized care management 
                solutions that empower better health outcomes.
              </p>
              <p>
                We believe that every person living with Alzheimer's deserves dignity, 
                respect, and the best possible care. Our technology bridges the gap 
                between patients, caregivers, and healthcare providers, creating a 
                coordinated care experience that adapts to individual needs.
              </p>
            </div>
            <div className="mission-stats">
              <div className="stat">
                <div className="stat-number">10,000+</div>
                <div className="stat-label">Patients Served</div>
              </div>
              <div className="stat">
                <div className="stat-number">500+</div>
                <div className="stat-label">Healthcare Partners</div>
              </div>
              <div className="stat">
                <div className="stat-number">99.9%</div>
                <div className="stat-label">Uptime</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="values-section">
        <div className="container">
          <div className="section-header">
            <h2>Our Values</h2>
            <p>The principles that guide everything we do</p>
          </div>
          
          <div className="values-grid">
            {values.map((value, index) => (
              <div key={index} className="value-card">
                <div className="value-icon">
                  <i className={value.icon}></i>
                </div>
                <h3>{value.title}</h3>
                <p>{value.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="team-section">
        <div className="container">
          <div className="section-header">
            <h2>Our Leadership Team</h2>
            <p>Meet the people behind AlzCarePlus</p>
          </div>
          
          <div className="team-grid">
            {teamMembers.map((member, index) => (
              <div key={index} className="team-card">
                <div className="team-photo">
                  <div className="photo-placeholder">
                    <i className="fas fa-user"></i>
                  </div>
                </div>
                <div className="team-info">
                  <h3>{member.name}</h3>
                  <p className="team-role">{member.role}</p>
                  <p className="team-bio">{member.bio}</p>
                  <a
                    href={member.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="team-linkedin"
                  >
                    <i className="fab fa-linkedin"></i>
                    Connect on LinkedIn
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Timeline Section */}
      <section className="timeline-section">
        <div className="container">
          <div className="section-header">
            <h2>Our Journey</h2>
            <p>Key milestones in our mission to transform Alzheimer's care</p>
          </div>
          
          <div className="timeline">
            {milestones.map((milestone, index) => (
              <div key={index} className={`timeline-item ${index % 2 === 0 ? 'left' : 'right'}`}>
                <div className="timeline-content">
                  <div className="timeline-year">{milestone.year}</div>
                  <h3>{milestone.title}</h3>
                  <p>{milestone.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="about-cta">
        <div className="container">
          <div className="cta-content">
            <h2>Join Us in Transforming Alzheimer's Care</h2>
            <p>
              Whether you're a patient, caregiver, or healthcare professional, 
              we invite you to be part of our mission to improve Alzheimer's care.
            </p>
            <div className="cta-buttons">
              <Link to="/patient/register" className="btn btn-primary btn-large">
                Get Started Today
              </Link>
              <Link to="/contact" className="btn btn-outline btn-large">
                Contact Us
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About; 