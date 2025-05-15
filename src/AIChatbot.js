// AIChatbot.js
// Original writer: Issa Batoul
// Edited by Sanna Ascard Soederstroem 2025.04.09
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; 

const AIChatbot = () => {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: '👋 Hi there! How can I support you today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate(); 

  const handleSend = async () => {
    if (input.trim() === '') return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:5000/gemini/gemini_chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();

      const botMessage = { sender: 'bot', text: data.response || '🤖 Something went wrong.' };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error talking to AI:', error);
      setMessages(prev => [
        ...prev,
        { sender: 'bot', text: '⚠️ Unable to reach the server. Please try again later.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

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

      <h2 style={styles.heading}>🤖 Gemini – AI Chatbot</h2>
      <div style={styles.chatBox}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: msg.sender === 'user' ? '#d4f8d4' : '#eee'
            }}
          >
            {msg.text}
          </div>
        ))}
        {loading && (
          <div style={{ ...styles.message, alignSelf: 'flex-start', fontStyle: 'italic' }}>
            Gemini is typing...
          </div>
        )}
      </div>
      <div style={styles.inputArea}>
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          style={styles.input}
        />
        <button onClick={handleSend} style={styles.sendButton}>Send</button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: 600,
    margin: '50px auto',
    fontFamily: 'Arial, sans-serif',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '10px'
  },
  heading: {
    textAlign: 'center'
  },
  chatBox: {
    display: 'flex',
    flexDirection: 'column',
    height: '300px',
    overflowY: 'auto',
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    marginBottom: '10px',
    backgroundColor: '#fafafa'
  },
  message: {
    maxWidth: '80%',
    padding: '10px',
    margin: '5px 0',
    borderRadius: '8px'
  },
  inputArea: {
    display: 'flex'
  },
  input: {
    flex: 1,
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc'
  },
  sendButton: {
    padding: '10px 15px',
    marginLeft: '10px',
    backgroundColor: '#4CAF50',
    color: '#fff',
    border: 'none',
    borderRadius: '5px'
  }
};

export default AIChatbot;
