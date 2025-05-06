// src/components/PatientManager.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PatientManager = () => {
  const [patients, setPatients] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    medical_history: ''
  });

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

  return (
    <div>
      <h2>Patients</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
        <input type="number" name="age" placeholder="Age" value={formData.age} onChange={handleChange} required />
        <textarea name="medical_history" placeholder="Medical History" value={formData.medical_history} onChange={handleChange} required />
        <button type="submit">Add Patient</button>
      </form>

      <ul>
        {patients.map((patient) => (
          <li key={patient.id}>
            <strong>{patient.name}</strong> (Age: {patient.age})<br />
            {patient.medical_history}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PatientManager;
