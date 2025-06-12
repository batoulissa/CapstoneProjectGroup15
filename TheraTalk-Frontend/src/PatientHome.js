// PatientHome.js
// Created by Sanna Ascard Soederstroem 2025.04.08

import React from 'react';
import { useNavigate } from 'react-router-dom';
import './home.css'; 

function PatientHome() {
    const navigate = useNavigate();
    const username = sessionStorage.getItem('username');

    const handleLogout = async () => {
        const username = sessionStorage.getItem('username');
        const password = sessionStorage.getItem('password');
      
        if (!username || !password) {
          alert('Missing login info. Please log in again.');
          navigate('/'); // go back to home
          return;
        }
      
        try {
          const response = await fetch('http://127.0.0.1:5000/patient/logout_patient', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            credentials: 'include', // include session cookie
            body: JSON.stringify({ username, password })
          });
      
          const data = await response.json();
      
          if (response.ok) {
            alert(data.message);
            sessionStorage.clear(); // clear credentials
            navigate('/');
          } else {
            alert(data.message);
          }
        } catch (error) {
          console.error('Logout error:', error);
          alert('An error occurred during logout.');
        }
      };
          

    return (
        <div className="home-wrapper">
          
          <div className="home-form">
            <h1>Welcome to TheraTalk {username}!</h1>
            <div className="header">
            <div className="notifications">
              <button className="notification-icon">
                <span>0</span> {/* Number of notifications */}
              </button>
            </div>
          </div>

            <button className="home-button sage" onClick={() => navigate('/profile')}>My Account</button>
            <button className="home-button sage" onClick={() => navigate('/booking')}>Appointments with Therapist</button>
            <button className="home-button sage" onClick={() => navigate('/match-page')}>Find a Therapist</button>
            <button className="home-button sage" onClick={() => navigate('/moodtracker')}>Log Mood</button>
            <button className="home-button sage" onClick={() => navigate('/aichatbot')}>Talk to AI ChatBot</button>


            <button className="logout-button" onClick={handleLogout}>Logout</button>
          </div>

          <div className="tab-bar">
            <button onClick={() => navigate('/patient/home')} className="tab-button">🏠</button>
            <button onClick={() => navigate('/video-call')} className="tab-button">🎥</button>
            <button onClick={() => navigate('/chats')} className="tab-button">💬</button>
            <button onClick={() => navigate('/profile')} className="tab-button">👤</button>
          </div>

        </div>
      );
}

export default PatientHome;
