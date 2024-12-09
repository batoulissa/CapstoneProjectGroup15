from db import db
import json
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }



class Therapist(db.Model):
    __tablename__ = 'therapists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.String, nullable=False)
    languages = db.Column(db.String, nullable=False)  # Store as JSON-encoded string
    focus_areas = db.Column(db.String, nullable=False)  # Store as JSON-encoded string
    password = db.Column(db.String(100), nullable=False)
    proof_of_education = db.Column(db.String(255), nullable=False)  # Store file path
    status = db.Column(db.String(50), default="pending")  # Track registration status ('pending' or 'approved')

    def __init__(self, name, experience_years, availability, languages, focus_areas, password, proof_of_education, status="pending"):
        self.name = name
        self.experience_years = experience_years
        self.availability = availability
        self.languages = json.dumps(languages)  # Encode list as JSON string
        self.focus_areas = json.dumps(focus_areas)  # Encode list as JSON string
        self.password = password  # Store password directly
        self.proof_of_education = proof_of_education  # Path to proof of education
        self.status = status  # Default to "pending" if not provided

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "experience_years": self.experience_years,
            "availability": self.availability,
            "languages": json.loads(self.languages),  # Decode JSON string back to list
            "focus_areas": json.loads(self.focus_areas),  # Decode JSON string back to list
            "proof_of_education": self.proof_of_education,  # Path to proof of education
            "status": self.status  # Registration status (pending/approved)
        }

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    medical_history = db.Column(db.Text)
    therapy_need = db.Column(db.String(500))  # Reason for seeking therapy
    languages = db.Column(db.String(200))  # Comma-separated list of languages spoken
    availability = db.Column(db.String(200))  # Comma-separated list of availability (e.g., "Monday, Wednesday")
    password = db.Column(db.String(256))  # Password hash
    status = db.Column(db.String(50), default='pending')  # Patient status (e.g., pending, approved)
    patient_id_card = db.Column(db.String(255))  # Path to the uploaded ID card file

    def __init__(self, name, age, gender, medical_history, therapy_need, languages, availability, password, status="pending"):
        self.name = name
        self.age = age
        self.gender = gender
        self.therapy_need = therapy_need  # Reason for therapy
        self.medical_history = medical_history
        self.languages = languages  # Store languages as a comma-separated string
        self.availability = availability  # Store availability as a comma-separated string
        self.password = password  # Store password directly
        self.status = status  # Default to "pending" if not provided

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "therapy_need": self.therapy_need,  # Reason for therapy
            "medical_history": self.medical_history,
            "languages": self.languages,  # Include languages in the dictionary
            "availability": self.availability,  # Include availability in the dictionary
            "status": self.status  # Registration status (pending/approved)
        }
