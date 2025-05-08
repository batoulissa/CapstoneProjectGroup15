from db import db
import json
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import time

class Admin(db.Model):
    __tablename__ = 'admins'
    
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)  # Securely hash the password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "admin_id": self.admin_id,
            "username": self.username
        }

class PronounsEnum(enum.Enum):
    SHE_HER = "she/her"
    HE_HIM = "he/him"
    THEY_THEM = "they/them"

class Therapist(db.Model):
    __tablename__ = 'therapists'
    
    therapist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  # Full name for display
    username = db.Column(db.String(100), unique=True, nullable=False)  # Username for login
    pronouns = db.Column(db.Enum(PronounsEnum), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    languages = db.Column(db.String, nullable=False)  
    focus_areas = db.Column(db.String, nullable=False)  
    password = db.Column(db.String(256), nullable=False)  # Increased password hash length
    proof_of_education = db.Column(db.String(255), nullable=False)  # Store file path
    status = db.Column(db.String(50), default="pending")  # Track registration status ('pending' or 'approved')
    
    # Availability columns for each day of the week as a string "HH:MM-HH:MM"
    monday = db.Column(db.String(50), nullable=True)  # e.g., "09:00-17:00"
    tuesday = db.Column(db.String(50), nullable=True)
    wednesday = db.Column(db.String(50), nullable=True)
    thursday = db.Column(db.String(50), nullable=True)
    friday = db.Column(db.String(50), nullable=True)
    saturday = db.Column(db.String(50), nullable=True)
    sunday = db.Column(db.String(50), nullable=True)
    
    def __init__(self, name, username, pronouns, experience_years, languages, focus_areas, password, proof_of_education, status="pending", availability=None):
        self.name = name
        self.username = username
        self.pronouns = PronounsEnum(pronouns)
        self.experience_years = experience_years
        self.languages = languages  
        self.focus_areas = focus_areas
        self.password = password  # Securely hash the password
        self.proof_of_education = proof_of_education  # Path to proof of education
        self.status = status  # Default to "pending" if not provided
        
        # Process availability and store in the appropriate columns as strings
        if availability:
            for day, times in availability.items():
                start_time, end_time = times
                setattr(self, day, f"{start_time}-{end_time}")
                
    def to_dict(self):
        return {
            "therapist_id": self.therapist_id,
            "name": self.name,
            "username": self.username,
            "pronouns": self.pronouns.value,
            "experience_years": self.experience_years,
            "languages": self.languages,
            "focus_areas": self.focus_areas,
            "status": self.status,
            "availability": {
                "monday": self.monday,
                "tuesday": self.tuesday,
                "wednesday": self.wednesday,
                "thursday": self.thursday,
                "friday": self.friday,
                "saturday": self.saturday,
                "sunday": self.sunday
            },
            "proof_of_education": self.proof_of_education  # File path
        }

class Patient(db.Model):
    __tablename__ = 'patients'
    
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    pronouns = db.Column(db.Enum(PronounsEnum), nullable=False)
    medical_history = db.Column(db.Text)
    therapy_need = db.Column(db.String(500))  # Reason for seeking therapy
    languages = db.Column(db.String(200))  # Comma-separated list of languages spoken
    password = db.Column(db.String(256))  # Password hash
    status = db.Column(db.String(50), default='pending')  # Patient status (e.g., pending, approved, rejected, banned)
    patient_id_card = db.Column(db.String(255), nullable=False)  # Path to the uploaded ID card file

    def __init__(self, name, username, birthdate, pronouns, medical_history, therapy_need, languages, password, status, patient_id_card):
        self.name = name
        self.username = username
        self.birthdate = birthdate
        self.pronouns = PronounsEnum(pronouns)
        self.therapy_need = therapy_need  # Reason for therapy
        self.medical_history = medical_history
        self.languages = languages  # Store languages as a comma-separated string
        self.password = password  # Securely hash the password
        self.status = status  # Default to "pending" if not provided
        self.patient_id_card = patient_id_card

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def calculate_age(self):
        """Calculate age from date of birth."""
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "username": self.username,
            "birthdate": self.birthdate.strftime('%Y-%m-%d'),
            "age": self.calculate_age(),
            "pronouns": self.pronouns.value,
            "therapy_need": self.therapy_need,  # Reason for therapy
            "medical_history": self.medical_history,
            "languages": self.languages,  # Include languages in the dictionary
            "status": self.status,  # Registration status (pending/approved)
            "patient_id_card": self.patient_id_card
        }


class Message(db.Model):
    __tablename__ = 'private_chat'
    
    private_chat_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)  # Id of the sender
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to Patient
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    patient = db.relationship('Patient', backref=db.backref('patient_messages', lazy='dynamic'))

    # Relationship to Therapist
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapists.therapist_id'))
    therapist = db.relationship('Therapist', backref=db.backref('therapist_messages', lazy='dynamic'))
    
    def __init__(self, therapist_id, patient_id, sender_id, content):
        self.therapist_id = therapist_id
        self.patient_id = patient_id
        self.sender_id = sender_id
        self.content = content

    def to_dict(self):
        return {
            "private_chat_id": self.private_chat_id,
            "therapist_id": self.therapist_id,
            "patient_id": self.patient_id,
            "sender_id": self.sender_id,
            "content": self.content,
            "timestamp": self.timestamp
        }


class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapists.therapist_id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    booking_status = db.Column(db.String(20), default='pending')  # pending, confirmed, canceled
    
    therapist = db.relationship('Therapist', backref='bookings')
    patient = db.relationship('Patient', backref='bookings')

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "therapist_id": self.therapist_id,
            "patient_id": self.patient_id,
            "appointment_time": self.appointment_time,
            "booking_status": self.booking_status
        }
  

class MoodLog(db.Model):
    mood_log_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __ref__(self):
        return f"<MoodLog {self.mood} at {self.timestamp}>"
    