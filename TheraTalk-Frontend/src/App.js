// Original author: Issa Batoul
// Edited by: Sanna Ascard Soderstroem 17.05.25

import React from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import MatchPage from "./MatchPage";
import MatchResults from "./MatchResults";
import TherapyQuestionnaire from "./TherapyQuestionnaire"; // Import the TherapyQuestionnaire component
import TherapistSignup from "./TherapistSignup"; // Import the TherapistSignup component
import Home from "./Home"; // Import the Home component
import Login from "./Login"; // Import Login
import Signup from "./Signup"; // Import Signup
import LoginPatient from "./LoginPatient"; // Import LoginPatient
import LoginTherapist from "./LoginTherapist"; // Import LoginTherapist
import PatientSignup from "./PatientSignup"; // Import PatientSignup
import AIChatbot from './AIChatbot';
import MoodTracker from './MoodTracker';
import PatientHome from './PatientHome';
import TherapistHome from './TherapistHome';
import ChatLandingPage from "./ChatLandingPage";
import SignUpResult from "./SignUpResult";
import Booking from "./Booking"



function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Home />} />

        {/* Routes for Login */}
        <Route path="/login" element={<Login />} />
        <Route path="/login/patient" element={<LoginPatient />} />
        <Route path="/login/therapist" element={<LoginTherapist />} />

        {/* Routes for Signup */}
        <Route path="/signup" element={<Signup />} />
        <Route path="/signup/patient" element={<PatientSignup />} />
        <Route path="/signup/therapist" element={<TherapistSignup />} />
        <Route path="/signup-result" element={<SignUpResult />} />

        {/* Route for the Therapy Questionnaire */}
        <Route path="/therapy-questionnaire" element={<TherapyQuestionnaire/>} />

        {/* Routes for AI Matching */}
        <Route path="/match-page" element={<MatchPage />} />
        <Route path="/match-results" element={<MatchResults />} />

        {/* Other routes needed for the application to work...  / Sanna */}
        <Route path="/patient/home" element={<PatientHome />} />
        <Route path="/therapist/home" element={<TherapistHome />} />
        <Route path="/aichatbot" element={<AIChatbot />} />
        <Route path="/moodtracker" element={<MoodTracker />} />
        <Route path="/chats" element={<ChatLandingPage />} />
        <Route path="/booking" element={<Booking />} />

      </Routes>
    </Router>
  );
}

export default App;
