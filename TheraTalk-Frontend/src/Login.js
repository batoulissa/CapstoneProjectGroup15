// Original writer: Issa Batoul
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

// Login function changed by Sanna Ascard Soederstroem
import './SignupForm.css'; 

function Login() {
  const [userType, setUserType] = useState('patient');
  const navigate = useNavigate();

  const handleContinue = () => {
    if (userType === 'patient') {
      navigate('/login/patient');
    } else {
      navigate('/login/therapist');
    }
  };

  return (
    <div className="signup-wrapper"> 
      <div className="signup-form">
        <h2>Select User Type</h2>
        <label htmlFor="userType">I am logging in as a:</label>
        <select id="userType" onChange={(e) => setUserType(e.target.value)} value={userType}>
          <option value="patient">Patient</option>
          <option value="therapist">Therapist</option>
        </select>
        <button onClick={handleContinue}>Continue</button>
      </div>
    </div>
  );
}

export default Login;
