from flask import Blueprint, request, jsonify
from models import db, Therapist, Patient
import hashlib
import os

auth_routes = Blueprint('auth_routes', __name__)

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Therapist Registration (Pending Admin Approval)
@auth_routes.route('/register_therapist', methods=['POST'])
def register_therapist():
    data = request.form

    # Get therapist details
    name = data.get('name')
    experience_years = data.get('experience_years')
    availability = data.get('availability')
    languages = data.get('languages')
    focus_areas = data.get('focus_areas')
    password = data.get('password')

    # Handle file upload (proof of education/license)
    file = request.files.get('proof_of_education')
    if not file:
        return jsonify({"message": "Proof of education/license is required!"}), 400

    file_path = os.path.join('uploads', file.filename)  # Save the file
    file.save(file_path)

    # Hash the password
    hashed_password = hash_password(password)

    # Create new therapist
    new_therapist = Therapist(
        name=name,
        experience_years=experience_years,
        availability=availability,
        languages=languages,
        focus_areas=focus_areas,
        password=hashed_password,
        proof_of_education=file_path,
        status="pending"  # Default to pending status
    )

    # Add to DB
    db.session.add(new_therapist)
    db.session.commit()

    return jsonify({"message": "Therapist registration is pending approval!"}), 201


# Therapist Login
@auth_routes.route('/login_therapist', methods=['POST'])
def login_therapist():
    data = request.get_json()

    name = data.get('name')
    password = data.get('password')

    # Hash the password
    hashed_password = hash_password(password)

    therapist = Therapist.query.filter_by(name=name).first()

    if therapist and therapist.password == hashed_password:
        if therapist.status != "approved":
            return jsonify({"message": "Account not approved. Please wait for approval."}), 403
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401


# Patient Registration
@auth_routes.route('/register_patient', methods=['POST'])
def register_patient():
    data = request.form

    # Get patient details
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    medical_history = data.get('medical_history')
    password = data.get('password')

    # Handle file upload for identification proof (ID card)
    id_card_file = request.files.get('patient_id_card')
    if not id_card_file:
        return jsonify({"message": "Patient ID card is required!"}), 400

    id_card_path = os.path.join('uploads', id_card_file.filename)  # Save the file
    id_card_file.save(id_card_path)

    # Hash the password
    hashed_password = hash_password(password)

    # Create new patient
    new_patient = Patient(
        name=name,
        age=age,
        gender=gender,
        medical_history=medical_history,
        password=hashed_password,
        patient_id_card=id_card_path,  # Save the path to the ID card file
        status="pending"  # Default to pending status for review (admin approval)
    )

    # Add to DB
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({"message": "Patient registration is pending approval!"}), 201



# Patient Login
@auth_routes.route('/login_patient', methods=['POST'])
def login_patient():
    data = request.get_json()

    name = data.get('name')
    password = data.get('password')

    hashed_password = hash_password(password)

    patient = Patient.query.filter_by(name=name).first()

    if patient and patient.password == hashed_password:
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401
