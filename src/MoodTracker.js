// MoodTracker.js
// Original writer: Issa Batoul
// Edited by Sanna Ascard Soederstroem 2025.04.09
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const MoodTracker = () => {
  const [mood, setMood] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [moodHistory, setMoodHistory] = useState([]);
  const [streak, setStreak] = useState(null);
  const navigate = useNavigate();

  const VALID_MOODS = [
    'Happy 😊',
    'Sad 😢',
    'Stressed 😫',
    'Angry 😡',
    'Calm 😌',
    'Tired 😴',
    'Excited 🤩',
    'Anxious 😰',
    'Relaxed 😌',
    'Neutral 😐'
  ];

  const handleSelect = (e) => {
    setMood(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!mood) return;

    // Extract the actual mood (without emoji)
    const moodOnly = mood.split(' ')[0];

    try {
      const response = await fetch(`http://127.0.0.1:5000/mood_log/log_mood`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ mood: moodOnly })
      });

      const data = await response.json();

      if (response.ok) {
        setSubmitted(true);
        fetchMoodData();
      } else {
        alert(data.message || data.error);
      }
    } catch (error) {
      console.error('Error logging mood:', error);
      alert('Something went wrong!');
    }
  };

  const fetchMoodData = async () => {
    try {
      const historyRes = await fetch(`http://127.0.0.1:5000/mood_log/get_logged_moods`, {
        credentials: 'include'
      });
      const streakRes = await fetch(`http://127.0.0.1:5000/mood_log/get_streak`, {
        credentials: 'include'
      });

      const historyData = await historyRes.json();
      const streakData = await streakRes.json();

      setMoodHistory(historyData);
      setStreak(streakData.streak);
    } catch (error) {
      console.error('Error fetching mood data:', error);
    }
  };

  useEffect(() => {
    fetchMoodData();
  }, []);

  return (
    <div style={styles.container}>
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

      <h2 style={styles.heading}>📝 Mood Tracker</h2>

      {streak !== null && (
        <p style={styles.streak}>🔥 Current Streak: <strong>{streak}</strong> days</p>
      )}

      {!submitted ? (
        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>How are you feeling today?</label>
          <select value={mood} onChange={handleSelect} style={styles.select}>
            <option value="">-- Select Mood --</option>
            {VALID_MOODS.map((m, index) => (
              <option key={index} value={m}>{m}</option>
            ))}
          </select>
          <button type="submit" style={styles.button}>Submit</button>
        </form>
      ) : (
        <div style={styles.result}>
          <p>You said you're feeling: <strong>{mood}</strong></p>
          <button onClick={() => setSubmitted(false)} style={styles.resetBtn}>Change Mood</button>
        </div>
      )}

      <div style={styles.history}>
        <h3>Mood History</h3>
        {moodHistory.length === 0 ? (
          <p>No moods logged yet.</p>
        ) : (
          <ul>
            {moodHistory.map((entry, index) => (
              <li key={index}>
                {entry.mood} - {new Date(entry.timestamp).toLocaleString()}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '500px',
    margin: '60px auto',
    textAlign: 'center',
    fontFamily: 'Arial, sans-serif',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '10px',
    backgroundColor: '#fdfdfd'
  },
  heading: {
    marginBottom: '20px'
  },
  form: {
    display: 'flex',
    flexDirection: 'column'
  },
  label: {
    marginBottom: '10px'
  },
  select: {
    padding: '10px',
    marginBottom: '20px',
    fontSize: '16px'
  },
  button: {
    padding: '10px',
    backgroundColor: '#4CAF50',
    border: 'none',
    color: 'white',
    borderRadius: '5px',
    fontSize: '16px',
    cursor: 'pointer'
  },
  result: {
    fontSize: '18px'
  },
  resetBtn: {
    marginTop: '20px',
    backgroundColor: '#888',
    padding: '8px',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  history: {
    marginTop: '30px',
    textAlign: 'left'
  },
  streak: {
    fontSize: '16px',
    fontWeight: 'bold',
    color: '#d35400'
  }
};

export default MoodTracker;
