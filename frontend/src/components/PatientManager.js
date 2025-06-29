// src/components/PatientManager.js

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './PatientManager.css';

const PatientManager = () => {
  const [patients, setPatients] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    medical_history: ''
  });

  const navigate = useNavigate();

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/patients/');
      setPatients(response.data);
    } catch (error) {
      console.error('Error fetching patients:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/patients/', formData);
      fetchPatients(); // Refresh list
      setFormData({ name: '', age: '', medical_history: '' });
    } catch (error) {
      console.error('Error adding patient:', error);
    }
  };

  const handleLogout = () => {
    // TODO: Add logout logic here (clear tokens, etc.)
    navigate('/login');
  };

  return (
    <div className="patient-manager">
      <header className="dashboard-header">
        <h1>AlzCarePlus Patient Manager</h1>
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </header>

      <div className="dashboard-content">
        <div className="add-patient-section">
          <h2>Add New Patient</h2>
          <form onSubmit={handleSubmit} className="patient-form">
            <div className="form-group">
              <input 
                type="text" 
                name="name" 
                placeholder="Patient Name" 
                value={formData.name} 
                onChange={handleChange} 
                required 
              />
            </div>
            <div className="form-group">
              <input 
                type="number" 
                name="age" 
                placeholder="Age" 
                value={formData.age} 
                onChange={handleChange} 
                required 
              />
            </div>
            <div className="form-group">
              <textarea 
                name="medical_history" 
                placeholder="Medical History" 
                value={formData.medical_history} 
                onChange={handleChange} 
                required 
              />
            </div>
            <button type="submit" className="add-button">Add Patient</button>
          </form>
        </div>

        <div className="patients-list-section">
          <h2>Patient List</h2>
          <div className="patients-grid">
            {patients.map((patient) => (
              <div key={patient.id} className="patient-card">
                <h3>{patient.name}</h3>
                <p><strong>Age:</strong> {patient.age}</p>
                <p><strong>Medical History:</strong></p>
                <p className="medical-history">{patient.medical_history}</p>
              </div>
            ))}
          </div>
          {patients.length === 0 && (
            <p className="no-patients">No patients found. Add your first patient above.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default PatientManager;
