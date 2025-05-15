// Created by Sanna Ascard Soederstroem 2025.04.08

import React, { useState } from 'react';
import axios from 'axios';
import './SignupForm.css';

function TherapistSignup() {
  const [formData, setFormData] = useState({
    name: '',
    username: '',
    pronouns: '',
    experience_years: '',
    languages: '',
    focus_areas: '',
    password: '',
    proof_of_education: null,
  });

  const [availability, setAvailability] = useState({
    monday: { start_time: '', end_time: '' },
    tuesday: { start_time: '', end_time: '' },
    wednesday: { start_time: '', end_time: '' },
    thursday: { start_time: '', end_time: '' },
    friday: { start_time: '', end_time: '' },
    saturday: { start_time: '', end_time: '' },
    sunday: { start_time: '', end_time: '' },
  });

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === 'proof_of_education') {
      setFormData({ ...formData, [name]: files[0] });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleAvailabilityChange = (day, field, value) => {
    setAvailability((prev) => ({
      ...prev,
      [day]: { ...prev[day], [field]: value },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();

    for (let key in formData) {
      data.append(key, formData[key]);
    }

    for (let day in availability) {
      data.append(`availability[${day}][start_time]`, availability[day].start_time);
      data.append(`availability[${day}][end_time]`, availability[day].end_time);
    }

    try {
      const res = await axios.post('http://127.0.0.1:5000/therapist/register_therapist', data);
      alert(res.data.message);
    } catch (err) {
      alert(err.response?.data?.message || 'Signup failed.');
    }
  };

  return (
    <div className="signup-wrapper">
      <form className="signup-form" onSubmit={handleSubmit}>
        <h2>Therapist Signup</h2>
        <input type="text" name="name" placeholder="Name" onChange={handleChange} required />
        <input type="text" name="username" placeholder="Username" onChange={handleChange} required />
        <input type="text" name="pronouns" placeholder="Pronouns" onChange={handleChange} />
        <input type="number" name="experience_years" placeholder="Years of Experience" onChange={handleChange} />
        <input type="text" name="languages" placeholder="Languages (comma-separated)" onChange={handleChange} />
        <input type="text" name="focus_areas" placeholder="Focus Areas (comma-separated)" onChange={handleChange} />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
        <input type="file" name="proof_of_education" accept=".pdf" onChange={handleChange} required />

        <h4>Availability</h4>
        {Object.keys(availability).map((day) => (
          <div key={day}>
            <label>{day.charAt(0).toUpperCase() + day.slice(1)}:</label>
            <input
              type="time"
              onChange={(e) => handleAvailabilityChange(day, 'start_time', e.target.value)}
            />
            <input
              type="time"
              onChange={(e) => handleAvailabilityChange(day, 'end_time', e.target.value)}
            />
          </div>
        ))}

        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default TherapistSignup;
