from flask import Flask, jsonify, request, session
from flask_session import Session
from flask_socketio import SocketIO, send, join_room
from db import db
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
CORS(app, supports_credentials=True)

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

# Register blueprints
app.register_blueprint(patient_routes, url_prefix='/patient')
app.register_blueprint(therapist_routes, url_prefix='/therapist')
app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(gemini_chatbot_routes, url_prefix='/gemini')
app.register_blueprint(booking_routes, url_prefix='/booking')
app.register_blueprint(mood_log_routes, url_prefix='/mood_log')
app.register_blueprint(matching_routes, url_prefix='/match_ai')

# Enable CORS for all routes
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})

app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True,  # True only if using HTTPS
)

socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:3000")

# WebSocket Event: Join a Private Chat Room
@socketio.on('join')
def handle_join(data):
    therapist_id = data['therapist_id']
    patient_id = data['patient_id']
    room = f"chat_{therapist_id}_{patient_id}"
    join_room(room)
    print(f"User joined room: {room}")

# WebSocket Event: Handle Messages
@socketio.on('send_message')
def handle_message(data):
    therapist_id = data['therapist_id']
    patient_id = data['patient_id']
    sender_id = therapist_id if data.get('sender type') == 'therapist' else patient_id
    content = data['content']
    room = f"chat_{therapist_id}_{patient_id}"
    
    # Store Messages in the Database
    new_message = Message(therapist_id=therapist_id, patient_id=patient_id, sender_id=sender_id, content=content)
    db.session.add(new_message)
    db.session.commit()
    
    # Send message to all users in the room
    send({"sender": sender_id, "content": content}, room=room)

#API Endpoint: Fetch Chat History
@app.route('/chat/<therapist_id>/<patient_id>', methods=['GET'])
def get_chat_history(therapist_id, patient_id):
    messages = Message.query.filter_by(therapist_id=therapist_id, patient_id=patient_id).order_by(Message.timestamp.asc()).all()
    return jsonify([message.to_dict() for message in messages])

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

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)

