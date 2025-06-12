# App.py - Main file
# Original Author: Sanna Ascard Soederstroem

from flask import Flask, jsonify, request, session
from flask_session import Session
from flask_socketio import SocketIO, send, join_room, emit
from models import db
from dotenv import load_dotenv
import os
from flask_cors import CORS
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///theratalk_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecretkey')

# Configure session
app.secret_key = "supersecretkey"  # Change this to a strong secret key
app.config["SESSION_TYPE"] = "filesystem"  # Store sessions in files
Session(app)  # Initialize Flask-Session

db.init_app(app)

# Create tables if they don't exist already
with app.app_context():
    db.create_all()

from models import Admin, Therapist, Patient , Message, Booking # Import db and models
from routes.patient_routes import patient_routes
from routes.therapist_routes import therapist_routes
from routes.admin_routes import admin_routes
from routes.gemini_chatbot_routes import gemini_chatbot_routes
from routes.booking_routes import booking_routes
from routes.mood_log_routes import mood_log_routes
from routes.matching_routes import matching_routes
from routes.chat_routes import chat_routes

# Register blueprints
app.register_blueprint(patient_routes, url_prefix='/patient')
app.register_blueprint(therapist_routes, url_prefix='/therapist')
app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(gemini_chatbot_routes, url_prefix='/gemini')
app.register_blueprint(booking_routes, url_prefix='/booking')
app.register_blueprint(mood_log_routes, url_prefix='/mood_log')
app.register_blueprint(matching_routes, url_prefix='/match_ai')
app.register_blueprint(chat_routes, url_prefix='/chat')

# Enable CORS for all routes
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})

app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True,  # True only if using HTTPS
)

# Initialize Socket.IO
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:3000")

# WebSocket Event: Join a Private Chat
@socketio.on('join')
def handle_join(data):
    therapist_id = data['therapist_id']
    patient_id = data['patient_id']
    room = f"chat_{therapist_id}_{patient_id}"
    join_room(room)
    print(f"Joined chat: {room}")

# WebSocket Event: Send new message notification (Not stored in DB!)
@socketio.on('notify_message')
def handle_notify(data):
    therapist_id = data['therapist_id']
    patient_id = data['patient_id']
    sender_type = data['sender_type']
    
    room = f"chat_{therapist_id}_{patient_id}"
    emit('new_message', {
        'sender_type': sender_type,
        'content': data['content']
    }, room = room)

@app.route('/me', methods=['GET'])
def get_current_user():
    # Check if a patient is logged in
    patient_id = session.get('patient_id')
    if patient_id:
        patient = Patient.query.filter_by(patient_id=patient_id).first()
        if patient:
            return jsonify({
                "role": "patient",
                "user_id": patient.patient_id,
                "username": patient.username,
                "name": patient.name
            })

    # Check if a therapist is logged in
    therapist_id = session.get('therapist_id')
    if therapist_id:
        therapist = Therapist.query.filter_by(therapist_id=therapist_id).first()
        if therapist:
            return jsonify({
                "role": "therapist",
                "user_id": therapist.therapist_id,
                "username": therapist.username,
                "name": therapist.name
            })

    return jsonify({"message": "Not logged in"}), 401

@app.route('/get_all_therapists', methods=['GET'])
def get_all_therapists():
    therapists = Therapist.query.filter_by(status='approved').all()
    result = [
        {
            'therapist_id': t.therapist_id,
            'name': t.name,
            'username': t.username
        }
        for t in therapists
    ]
    return jsonify(result)


if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)

