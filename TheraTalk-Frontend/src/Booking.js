// Created by Sanna Ascard Soederstroem 2025.06.02

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './SignupForm.css';

function BookingPage() {
  const [appointments, setAppointments] = useState([]);
  const [appointmentTime, setAppointmentTime] = useState('');
  const [selectedTherapist, setSelectedTherapist] = useState('');
  const [therapists, setTherapists] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const userType = sessionStorage.getItem('user_type'); // 'patient' or 'therapist'

  // 🧾 Fetch appointments
  useEffect(() => {
    fetch('http://127.0.0.1:5000/booking/bookings', {
      method: 'GET',
      credentials: 'include',
    })
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setAppointments(data);
        } else {
          setError(data.error || 'Failed to fetch bookings.');
        }
      })
      .catch(err => {
        console.error('Error fetching bookings:', err);
        setError('Could not load bookings.');
      });
  }, []);

  // 👩‍⚕️ Fetch all therapists
  useEffect(() => {
    fetch('http://127.0.0.1:5000/get_all_therapists', {
      method: 'GET',
      credentials: 'include',
    })
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setTherapists(data);
        } else {
          setError(data.error || 'Failed to fetch therapists.');
        }
      })
      .catch(err => {
        console.error('Error fetching therapists:', err);
        setError('Could not load therapist list.');
      });
  }, []);

  // 📅 Book appointment (patient only)
  const handleBook = () => {
    if (userType !== 'patient') {
      setError('Only patients can book appointments.');
      return;
    }
  
    if (!selectedTherapist || !appointmentTime) {
      setError('Please select a therapist and appointment time.');
      return;
    }
  
    // Convert "2025-06-02T14:30" to "2025-06-02 14:30"
    const formattedTime = appointmentTime.replace('T', ' ');
  
    fetch('http://127.0.0.1:5000/booking/book', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        therapist_id: selectedTherapist,
        appointment_time: formattedTime,
      }),
    })
      .then(res => res.json())
      .then(data => {
        if (data.message) {
          setSuccess(data.message);
          setError('');
          setAppointmentTime('');
          setSelectedTherapist('');
        } else {
          setError(data.error || 'Booking failed.');
        }
      })
      .catch(err => {
        console.error('Booking error:', err);
        setError('Could not book appointment.');
      });
  };
  

  return (
    <div className="chat-container" style={{ paddingTop: '60px' }}>

        <button 
        onClick={() => navigate(-1)} 
        style={{ 
          position: 'absolute', 
          top: '15px', 
          left: '15px', 
          backgroundColor: '#ccc', 
          border: 'none', 
          padding: '5px 5px', 
          borderRadius: '8px',
          cursor: 'pointer',
          fontWeight: 'bold'
        }}
      >
        ⬅ Back
      </button>

      <h2>TheraTalk Appointments</h2>
      {userType === 'patient' && (
        <div className="form-section">
          <h3>Book Appointment</h3>
          
          <select
            value={selectedTherapist}
            onChange={(e) => setSelectedTherapist(e.target.value)}
          >
            <option value="">Select a therapist</option>
            {therapists.map((therapist) => (
              <option key={therapist.therapist_id} value={therapist.therapist_id}>
                {therapist.name} ({therapist.username})
              </option>
            ))}
          </select>

          <input
            type="datetime-local"
            value={appointmentTime}
            onChange={(e) => setAppointmentTime(e.target.value)}
          />
          <button onClick={handleBook}>Book</button>
        </div>
      )}

      <div className="chat-box">
        <h3>Your Appointments</h3>
        {appointments.length > 0 ? (
          appointments.map((appt) => (
            <div key={appt.booking_id} className="message">
              <strong>{appt.appointment_time}</strong> - Status: {appt.booking_status}
              <br />
              Therapist ID: {appt.therapist_id} | Patient ID: {appt.patient_id}
            </div>
          ))
        ) : (
          <p>No appointments found.</p>
        )}
      </div>

      {error && <p className="error">{error}</p>}
      {success && <p className="success">{success}</p>}
    </div>
  );
}

export default BookingPage;
