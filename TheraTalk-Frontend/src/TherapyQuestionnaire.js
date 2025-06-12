// Original author: Issa Batoul

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './TherapyQuestionnaire.css';

function TherapyQuestionnaire() {
  const navigate = useNavigate();

  // Store the user's therapy preferences
  const [therapyType, setTherapyType] = useState("");
  const [issues, setIssues] = useState("");
  const [other, setOther] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    // Store preferences (you could send these to the backend or save them temporarily)
    const preferences = {
      therapyType,
      issues,
      other,
    };

    // Navigate to the MatchPage with the preferences (if needed)
    navigate("/match-page", { state: { preferences } });
  };

  return (
    <div style={styles.container}>
      <h2>Therapy Questionnaire</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>What type of therapy are you looking for?</label>
          <select
            value={therapyType}
            onChange={(e) => setTherapyType(e.target.value)}
            required
          >
            <option value="">Select Therapy Type</option>
            <option value="Relationship">Relationship Therapy</option>
            <option value="Anxiety">Anxiety Therapy</option>
            <option value="Depression">Depression Therapy</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div>
          <label>What issues would you like to address in therapy?</label>
          <textarea
            value={issues}
            onChange={(e) => setIssues(e.target.value)}
            placeholder="Describe your issues..."
            required
          />
        </div>

        {therapyType === "Other" && (
          <div>
            <label>Other therapy preferences?</label>
            <input
              type="text"
              value={other}
              onChange={(e) => setOther(e.target.value)}
              placeholder="Other preferences"
            />
          </div>
        )}

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "500px",
    margin: "60px auto",
    padding: "20px",
    backgroundColor: "#f4f4f4",
    borderRadius: "10px",
    textAlign: "center",
  },
};

export default TherapyQuestionnaire;
