// Original writer: Issa Batoul
import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import AIChatbot from './AIChatbot';
import Login from './Login';
import MatchPage from "./MatchPage";
import MoodTracker from './MoodTracker';
import Signup from './Signup';

// Added imports by Sanna Ascard Soederstroem
import PatientSignup from './PatientSignup';
import TherapistSignup from './TherapistSignup';
import Home from './Home';
import LoginPatient from './LoginPatient';
import LoginTherapist from './LoginTherapist';
import PatientHome from './PatientHome';
import TherapistHome from './TherapistHome';
import MatchResults from "./MatchResults";
import Chat from "./Chat";

function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/match-therapist" element={<MatchPage />} />
        <Route path="/aichatbot" element={<AIChatbot />} />
        <Route path="/moodtracker" element={<MoodTracker />} />
        
        <Route path="/signup/patient" element={<PatientSignup />} />
        <Route path="/signup/therapist" element={<TherapistSignup />} />
        <Route path="/login/patient" element={<LoginPatient />} />
        <Route path="/login/therapist" element={<LoginTherapist />} />
        <Route path="/patient/home" element={<PatientHome />} />
        <Route path="/therapist/home" element={<TherapistHome />} />
        <Route path="/match-results" element={<MatchResults />} />
        <Route path="/chat" element={<Chat />} />

      </Routes>
    </Router>
  );
}

export default App;
