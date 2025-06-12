// Created by Sanna Ascard Soederstroem 2025.04.08

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'
import './SignupForm.css';

function PatientSignup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    username: '',
    birthdate: '',
    pronouns: '',
    medical_history: '',
    therapy_need: '',
    languages: '',
    password: '',
    patient_id_card: null,
  });

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === 'patient_id_card') {
      setFormData({ ...formData, [name]: files[0] });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();
    for (let key in formData) {
      data.append(key, formData[key]);
    }

    try {
      const res = await axios.post('http://127.0.0.1:5000/patient/register_patient', data);
      navigate('/signup-result', { state: { success: true, message: res.data.message } });
    } catch (err) {
      navigate('/signup-result', {
        state: {
          success: false,
          message: err.response?.data?.message || 'Signup failed.',
        },
      });
    }
  };

  return (
    <div className="signup-wrapper">
      <form className="signup-form" onSubmit={handleSubmit}>
        <h2>Patient Signup</h2>
        <input type="text" name="name" placeholder="Name" onChange={handleChange} required />
        <input type="text" name="username" placeholder="Username" onChange={handleChange} required />
        <p>Birthday{''}</p>
        <input type="date" name="birthdate" onChange={handleChange} required />
        <input type="text" name="pronouns" placeholder="Pronouns" onChange={handleChange} />
        <input type="text" name="medical_history" placeholder="Medical History" onChange={handleChange} />
        <input type="text" name="therapy_need" placeholder="Therapy Need" onChange={handleChange} />
        <input type="text" name="languages" placeholder="Languages (comma-separated)" onChange={handleChange} />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
        <p>Please submit a form of identification (only PDF file is accepted){' '}</p>
        <input type="file" name="patient_id_card" accept=".pdf" onChange={handleChange} required />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default PatientSignup;
