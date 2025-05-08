import os
import json
from flask import Blueprint, request, jsonify, session
from models import db, Patient, PronounsEnum
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import time

patient_routes = Blueprint('patient_routes', __name__)


# Patient Registration
@patient_routes.route('/register_patient', methods=['POST'])
def register_patient():
    data = request.form

    # Get patient details
    name = data.get('name')
    username = data.get('username')
    birthdate = data.get('birthdate')
    pronouns = data.get('pronouns')
    medical_history = data.get('medical_history')
    theraphy_need = data.get('theraphy_need')
    languages = data.get('languages')
    password = data.get('password')
    
    # Check if username is unique
    existing_patient = Patient.query.filter_by(username=username).first()
    if existing_patient:
        return jsonify({"message": "Username already taken!"}), 400
    
    # Handle file upload (proof of education)
    file = request.files.get('patient_id_card')
    
    if not file:
        return jsonify({"message": "Identification is required!"}), 400

    # Check if the file is a PDF
    if not file.filename.endswith('.pdf'):
        return jsonify({"message": "Invalid file type. Please upload a PDF file."}), 400

    # Define the upload path and save the file
    filename = f"{username}_{int(time.time())}.pdf"
    file_path_patient = os.path.join('uploads', filename)
    file.save(file_path_patient)

    hashed_password = generate_password_hash(password)

    # Convert the birthdate string into a date object
    birthdate = datetime.strptime(data['birthdate'], "%Y-%m-%d").date()
    
    # Create new patient
    new_patient = Patient(
        name=name,
        username=username,
        birthdate=birthdate,
        pronouns=pronouns,
        medical_history=medical_history,
        therapy_need=theraphy_need,
        languages=languages,
        password=hashed_password,
        status="pending",
        patient_id_card=file_path_patient
    )

    # Add to DB
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({"message": "User registration is pending approval!"}), 201

# Patient Login
@patient_routes.route('/login_patient', methods=['POST'])
def login_patient():
    data = request.get_json()

    username = data.get('username')  # Use username for login
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    patient = Patient.query.filter_by(username=username).first()  # Find patient by username

    if not patient:
        return jsonify({"message": "User not found!"}), 404
    
    if patient.status == 'banned':  # Check if patient is banned
        return jsonify({"message": "Your account has been banned. Contact support for assistance."}), 403

    if check_password_hash(patient.password, password):  # Validate password
        if patient.status != "approved":
            return jsonify({"message": "Account not approved. Please wait for approval."}), 403
        
        # Store patient ID in session
        session['patient_id'] = patient.patient_id
        return jsonify({"message": "Login successful!"}), 200

    return jsonify({"message": "Invalid credentials!"}), 401

# Patient Logout 
@patient_routes.route('/logout_patient', methods=['POST'])
def logout_patient():
    data = request.get_json()

    username = data.get('username')  # Use username to verify
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    patient = Patient.query.filter_by(username=username).first()

    if patient and check_password_hash(patient.password, password):
        # If using session-based login, you can clear the session here
        session.pop('patient_id', None)  # Remove patient ID from session
        
        return jsonify({"message": "Logged out successfully!"}), 200

    return jsonify({"message": "Invalid credentials!"}), 401


# Update Patient Information
@patient_routes.route('/update_patient/<username>', methods=['PUT'])
def update_patient(username):
    data = request.form

    patient_id = session.get('patient_id')  # Get the patient ID from session

    if not patient_id:
        return jsonify({"message": "You must be logged in to update your information!"}), 401

    patient = Patient.query.filter_by(username=username).first()

    # Initialize status_updated to False
    status_updated = False
    
    if not patient:
        return jsonify({"message": "Patient not found!"}), 404

    # Get new values from the request and update the patient's information
    name = data.get('name')
    pronouns = data.get('pronouns')
    medical_history = data.get('medical_history')
    therapy_need = data.get('therapy_need')
    languages = data.get('languages')
    password = data.get('password')  # If patient wants to change the password

    # Check if an ID file was uploaded
    if 'patient_id_card' in request.files:
        id_file = request.files['patient_id_card']
        if id_file:
            # Make sure the file has a valid name and save it
            filename = f"{username}_{int(time.time())}.pdf"
            file_path_patient = os.path.join('uploads', filename)
            id_file.save(file_path_patient)
            patient.patient_id_card = file_path_patient  # Update the patient's ID file path in the database

            # Set status to pending for verification
            patient.status = 'pending'
            status_updated = True

    # Update other fields if provided
    if name:
        patient.name = name
    if pronouns:
        patient.pronouns = PronounsEnum(pronouns)  # Ensure valid Enum
    if medical_history:
        patient.medical_history = medical_history
    if therapy_need:
        patient.therapy_need = therapy_need
    if languages:
        patient.languages = languages  # Store languages as a comma-separated string
    if password:
        patient.password = generate_password_hash(password)  # Update password with hashed value

    db.session.commit()  # Save the changes to the database

    if status_updated:
        return jsonify({"message": "Patient information updated successfully! Account status set to 'pending' for verification because of updated ID."}), 200
    else:
        return jsonify({"message": "Patient information updated successfully!"}), 200
    
# Delete Patient Account
@patient_routes.route('/delete_patient/<username>', methods=['DELETE'])
def delete_patient(username):
    data = request.get_json()

    patient_id = session.get('patient_id')  # Get the patient ID from session

    if not patient_id:
        return jsonify({"message": "You must be logged in to update your information!"}), 401

    patient = Patient.query.filter_by(username=username).first()

    if not patient:
        return jsonify({"message": "Patient not found!"}), 404

    # Ask for confirmation before proceeding with account deletion
    confirmation = data.get('confirmation')
    if confirmation != 'DELETE':
        return jsonify({"message": "Confirmation required to delete the account!"}), 400

    db.session.delete(patient)  # Delete the patient record from the database
    db.session.commit()  # Commit the changes to the database

    session.pop('patient_id', None)  # Clear the session (patient is logged out)

    return jsonify({"message": "Patient account deleted successfully!"}), 200
