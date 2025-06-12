// MatchPage.js
// Original writer: Issa Batoul
// Edited by Sanna Ascard Soederstroem

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function MatchPage() {
  const navigate = useNavigate();
  const [therapists, setTherapists] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);

  const [availability, setAvailability] = useState({
    monday: { start_time: '', end_time: '' },
    tuesday: { start_time: '', end_time: '' },
    wednesday: { start_time: '', end_time: '' },
    thursday: { start_time: '', end_time: '' },
    friday: { start_time: '', end_time: '' },
    saturday: { start_time: '', end_time: '' },
    sunday: { start_time: '', end_time: '' },
  });

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/me", { withCredentials: true })
      .then(res => setUser(res.data))
      .catch(err => {
        console.error("User not logged in:", err);
        setError("You must be logged in to view this page.");
      });
  }, []);

  const handleAvailabilityChange = (day, field, value) => {
    setAvailability(prev => ({
      ...prev,
      [day]: { ...prev[day], [field]: value }
    }));
  };

  const handleMatchClick = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/match_ai/matching_therapist_with_user",
        {
          username: user?.username,
          availability: Object.fromEntries(
            Object.entries(availability)
              .filter(([_, value]) => value.start_time && value.end_time)
              .map(([day, value]) => [day, `${value.start_time}-${value.end_time}`])
          ),
        },
        { withCredentials: true }
      );
  
      if (response.data.message) {
        setError(response.data.message);
        setTherapists([]);
      } else {
        navigate("/match-results", { state: { therapists: response.data } }); // 👈 navigate here!
      }
    } catch (err) {
      console.error("Match fetch failed:", err);
      setError("Failed to fetch matched therapists.");
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div style={{ padding: "25px" }}>
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

      <h2>🎯 Matched Therapists</h2>

      {user && (
        <p style={{ fontStyle: "italic", color: "#555" }}>
          Logged in as: <strong>{user.name}</strong>
        </p>
      )}

      {user?.role === "patient" && (
        <>
          <h4>🕒 Your Availability</h4>
          {Object.keys(availability).map((day) => (
            <div key={day} style={{ marginBottom: "10px" }}>
              <label><strong>{day.charAt(0).toUpperCase() + day.slice(1)}:</strong></label><br />
              <input
                type="time"
                value={availability[day].start_time}
                onChange={(e) => handleAvailabilityChange(day, 'start_time', e.target.value)}
                style={{ marginRight: "10px" }}
              />
              <input
                type="time"
                value={availability[day].end_time}
                onChange={(e) => handleAvailabilityChange(day, 'end_time', e.target.value)}
              />
            </div>
          ))}
          <button onClick={handleMatchClick}>Match with a Therapist</button>
        </>
      )}

      {loading && <p>Loading matches...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {therapists.map((therapist, index) => (
        <div
          key={index}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            marginBottom: "10px",
            borderRadius: "8px",
          }}
        >
          <h3>{therapist.name}</h3>
          <p><strong>Match Score:</strong> {therapist.match_score}</p>
          <p><strong>Matched Focus Areas:</strong> {therapist.matched_attributes?.focus_areas?.join(", ") || "None"}</p>
          <p><strong>Languages:</strong> {therapist.matched_attributes?.languages?.join(", ") || "None"}</p>
          <p><strong>Available:</strong></p>
          <ul>
            {therapist.matched_attributes?.availability &&
              Object.entries(therapist.matched_attributes.availability).map(([day, time], i) => (
                <li key={i}>{day}: {time}</li>
              ))}
          </ul>
        </div>
      ))}

      {therapists.length > 0 && user?.role === "patient" && (
        <button onClick={() => navigate("/chat")}>Start Chat</button>
      )}
    </div>
  );
}

export default MatchPage;
