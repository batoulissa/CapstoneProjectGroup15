// Created by Sanna Ascard Soederstroem 2025.05.13
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './ChatLandingPage.css'; 

function ChatLandingPage() {
  const [chats, setChats] = useState([]); // Chat partners list
  const [selectedChat, setSelectedChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [error, setError] = useState('');
  const [user, setUser] = useState(null); // user info from /me
  const navigate = useNavigate();

  // Helper to get partner's unique ID depending on chat object shape
  const getPartnerId = (chat) => chat.therapist_id || chat.patient_id || chat.username;

  // 1️⃣ Fetch logged-in user info from /me
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/me', { withCredentials: true })
      .then(res => {
        setUser(res.data);
        console.log('User loaded:', res.data); // DEBUG
        setError('');
      })
      .catch(() => {
        setError('You must be logged in to view this page.');
      });
  }, []);

  // 2️⃣ Once user is loaded, fetch chat partners
  useEffect(() => {
    if (!user || !user.user_id || !user.role) return;

    axios.get(`http://127.0.0.1:5000/chat/partners/${user.user_id}`, { withCredentials: true })
      .then(res => {
        setChats(res.data);
        setError('');
      })
      .catch(() => setError('Failed to load chat partners.'));
  }, [user]);

  // 3️⃣ Fetch messages when selectedChat changes
  useEffect(() => {
    if (!selectedChat || !user) return;

    // Determine therapist and patient IDs based on user role and selected chat
    const therapistId = selectedChat.therapist_id || (user.role === 'therapist' ? user.user_id : selectedChat.id);
    const patientId = selectedChat.patient_id || (user.role === 'patient' ? user.user_id : selectedChat.id);

    axios.get(`http://127.0.0.1:5000/chat/${therapistId}/${patientId}`, { withCredentials: true })
      .then(res => {
        setMessages(res.data);
        setError('');
      })
      .catch(() => setError('Failed to load chat messages.'));
  }, [selectedChat, user]);

  // 4️⃣ Handle sending new messages
  const handleSend = () => {
    if (!newMessage.trim() || !selectedChat || !user) return;

    const therapistId = selectedChat.therapist_id || (user.role === 'therapist' ? user.user_id : selectedChat.id);
    const patientId = selectedChat.patient_id || (user.role === 'patient' ? user.user_id : selectedChat.id);

    axios.post('http://127.0.0.1:5000/chat/send', {
        therapist_id: therapistId,
        patient_id: patientId,
        sender_type: user.role,
        content: newMessage.trim()
    }, { withCredentials: true })
      .then(res => {
        if (res.data.message === 'Message saved') {
          setMessages(prev => [...prev, { content: newMessage, sender_type: user.role }]);
          setNewMessage('');
          setError('');
        } else {
          setError('Failed to send message.');
        }
      })
      .catch(() => setError('Failed to send message.'));
  };

  return (
    <div className="chat-landing-page" style={{ paddingTop: '60px' }}>
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

      <div className="chat-sidebar">
        <h2>Chats</h2>
        {error && <p className="error">{error}</p>}
        <ul>
          {chats.map(chat => (
            <li
              key={getPartnerId(chat)}
              className={selectedChat && getPartnerId(selectedChat) === getPartnerId(chat) ? 'selected' : ''}
              onClick={() => setSelectedChat(chat)}
            >
              <strong>{chat.name}</strong>
              <p>{chat.lastMessage || 'No messages yet'}</p>
            </li>
          ))}
        </ul>
      </div>

      <div className="chat-main">
        {selectedChat ? (
          <div>
            <h2>{selectedChat.name}</h2>
            <div className="chat-messages">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={msg.sender_type === user.role ? 'message user' : 'message partner'}
                >
                  <span>{msg.sender_type === user.role ? 'You' : selectedChat.name}:</span> {msg.content}
                </div>
              ))}
            </div>
            <textarea
              placeholder="Type your message..."
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
            />
            <button onClick={handleSend}>Send</button>
          </div>
        ) : (
          <p>Select a chat to view the conversation</p>
        )}
      </div>
    </div>
  );
}

export default ChatLandingPage;
