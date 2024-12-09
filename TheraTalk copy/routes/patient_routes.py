import os
from flask import Blueprint, request, jsonify
from models import db, Patient
from hashlib import sha256

patient_routes = Blueprint('patient_routes', __name__)

# Hash Password
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Patient Registration
@patient_routes.route('/register', methods=['POST'])
def register_patient():
    data = request.get_json()

    # Get patient details
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    medical_history = data.get('medical_history')
    contact_info = data.get('contact_info')
    password = data.get('password')

    hashed_password = hash_password(password)

    # Create new patient
    new_patient = Patient(
        name=name,
        age=age,
        gender=gender,
        medical_history=medical_history,
        contact_info=contact_info,
        password=hashed_password
    )

    # Add to DB
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({"message": "Patient registered successfully!"}), 201

# Patient Login
@patient_routes.route('/login', methods=['POST'])
def login_patient():
    data = request.get_json()

    name = data.get('name')
    password = data.get('password')

    hashed_password = hash_password(password)

    patient = Patient.query.filter_by(name=name).first()

    if patient and patient.password == hashed_password:
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401
