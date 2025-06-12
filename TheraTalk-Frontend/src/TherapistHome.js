// TherapistHome.js
// Created by Sanna Ascard Soederstroem 2025.05.13

import React from 'react';
import { useNavigate } from 'react-router-dom';
import './home.css'; 

function TherapistHome() {
    const navigate = useNavigate();

    const handleLogout = async () => {
        const username = sessionStorage.getItem('username');
        const password = sessionStorage.getItem('password');
      
        if (!username || !password) {
          alert('Missing login info. Please log in again.');
          navigate('/'); // go back to home
          return;
        }
      
        try {
          const response = await fetch('http://127.0.0.1:5000/therapist/logout_therapist', {
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
            navigate('/therapist/home');
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
            <h1>Welcome to TheraTalk!</h1>
            <p>Choose an option below:</p>

            <button className="home-button sage" onClick={() => navigate('/')}>My Account</button>
            <button className="home-button sage" onClick={() => navigate('/')}>Appointments</button>

            <button className="logout-button" onClick={handleLogout}>Logout</button>
          </div>
          <div className="tab-bar">
            <button onClick={() => navigate('/home')} className="tab-button">🏠</button>
            <button onClick={() => navigate('/video-call')} className="tab-button">🎥</button>
            <button onClick={() => navigate('/chats')} className="tab-button">💬</button>
            <button onClick={() => navigate('/profile')} className="tab-button">👤</button>
          </div>
        </div>
      );
}

export default TherapistHome;