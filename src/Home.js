// Created by Sanna Ascard Soederstroem 2025.04.08

import React from 'react';
import { useNavigate } from 'react-router-dom';
import './home.css'; // for shared styling

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-wrapper">
      <div className="home-form">
        <h1>Welcome to TheraTalk!</h1>

        <button className="home-button sage" onClick={() => navigate('/login')}>Login</button>
        <button className="home-button forest" onClick={() => navigate('/signup')}>Sign Up</button>
        <button className="home-button sage" onClick={() => navigate('/chat')}>Go to Chat</button>
        <button className="home-button forest" onClick={() => navigate('/resources')}>Mental Health Resources</button>
        <button className="home-button sage" onClick={() => navigate('/adminlogin')}>Admin Login</button>

      </div>
    </div>
  );
}

export default Home;
