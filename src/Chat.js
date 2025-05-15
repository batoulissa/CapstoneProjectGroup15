// Created by Sanna Ascard Soederstroem 2025.05.13

import React, { useState, useEffect } from 'react';
import './SignupForm.css';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [error, setError] = useState('');

  const userType = sessionStorage.getItem('user_type'); // 'patient' or 'therapist'
  const therapistId = sessionStorage.getItem('therapist_id');
  const patientId = sessionStorage.getItem('patient_id');
  const senderType = userType;

  // 🔁 Load chat history
  useEffect(() => {
    if (!therapistId || !patientId) {
      setError('User IDs not found.');
      return;
    }

    fetch(`http://127.0.0.1:5000/chat/${therapistId}/${patientId}`, {
      method: 'GET',
      credentials: 'include'
    })
      .then(response => response.json())
      .then(data => setMessages(data))
      .catch(err => {
        console.error('Failed to load messages:', err);
        setError('Could not load chat history.');
      });
  }, [therapistId, patientId]);

  // 📨 Send message
  const handleSend = () => {
    if (!newMessage.trim()) return;

    fetch('http://127.0.0.1:5000/chat/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        therapist_id: therapistId,
        patient_id: patientId,
        sender_type: senderType,
        content: newMessage.trim()
      })
    })
      .then(res => res.json())
      .then(data => {
        if (data.message === 'Message saved') {
          setMessages(prev => [...prev, {
            content: newMessage,
            sender_type: senderType
          }]);
          setNewMessage('');
        } else {
          setError(data.error || 'Failed to send message.');
        }
      })
      .catch(err => {
        console.error('Send error:', err);
        setError('Could not send message.');
      });
  };

  return (
    <div className="chat-container">
      <h2>TheraTalk Chat</h2>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender_type === 'therapist' ? 'therapist' : 'patient'}`}
          >
            {msg.content}
          </div>
        ))}
      </div>
      <textarea
        placeholder="Type your message..."
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
      />
      <button onClick={handleSend}>Send</button>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Chat;
