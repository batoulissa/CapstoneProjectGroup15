// Created by Sanna Ascard Soederstroem 2025.04.08

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

function LoginPatient() {
  const navigate = useNavigate();
  const [username, setUsername] = useState(''); // changed from email
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:5000/patient/login_patient', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include', // include cookies for session
        body: JSON.stringify({ username, password }) // match backend field names
      });

      const data = await response.json();
      if (response.ok) {
        sessionStorage.setItem('username', username);
        sessionStorage.setItem('password', password);

        sessionStorage.setItem('patient_id', data.patient_id);
        sessionStorage.setItem('user_type', 'patient');
        
        alert('Login successful!');
        navigate('/patient/home');
      } else {
        setError(data.message || 'Login failed');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('Something went wrong. Please try again.');
    }
  };

  return (
    <div className="login-container">
      <h2>TheraTalk Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
      {error && <p className="error">{error}</p>}
      <p>
        Don’t have an account?{' '}
        <span className="link" onClick={() => navigate('/signup')}>Sign Up</span>
      </p>
    </div>
  );
}

export default LoginPatient;
