// MatchResults.js
// Created by Sanna Ascard Soederstroem 2025.04.09

import React from "react";
import { useLocation } from "react-router-dom";
import { useNavigate } from 'react-router-dom';

function MatchResults() {
  const location = useLocation();
  const { therapists } = location.state || { therapists: [] };
  const navigate = useNavigate();

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

      <h2>🎯 Your Matched Therapists</h2>
      {therapists.length === 0 ? (
        <p>No matches found.</p>
      ) : (
        therapists.map((therapist, index) => (
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
            <p><strong>Focus Areas:</strong> {therapist.matched_attributes?.focus_areas?.join(", ") || "None"}</p>
            <p><strong>Languages:</strong> {therapist.matched_attributes?.languages?.join(", ") || "None"}</p>
            <p><strong>Available:</strong></p>
            <ul>
              {therapist.matched_attributes?.availability &&
                Object.entries(therapist.matched_attributes.availability).map(([day, time], i) => (
                  <li key={i}>{day}: {time}</li>
                ))}
            </ul>
          </div>
        ))
      )}
    </div>
  );
}

export default MatchResults;
