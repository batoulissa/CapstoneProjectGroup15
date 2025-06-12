// SignupResult.js
// Created by Sanna Ascard Soederstroem

import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import './SignupForm.css';

function SignupResult() {
  const location = useLocation();
  const { success, message } = location.state || {};

  return (
    <div className="signup-result">
      <h2>{success ? "Signup Successful!" : "Signup Failed"}</h2>
      <p>{message}</p>
      <Link to="/">Go to Homepage</Link>
    </div>
  );
}

export default SignupResult;
