import os
from flask import Blueprint, request, jsonify
from models import db, Therapist
from hashlib import sha256

therapist_routes = Blueprint('therapist_routes', __name__)

# Hash Password
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Therapist Registration (Pending Approval)
@therapist_routes.route('/register', methods=['POST'])
def register_therapist():
    data = request.form

    # Get therapist details
    name = data.get('name')
    experience_years = data.get('experience_years')
    availability = data.get('availability')
    languages = data.get('languages')
    focus_areas = data.get('focus_areas')
    password = data.get('password')

    # Handle file upload (proof of education)
    file = request.files.get('proof_of_education')
    
    if not file:
        return jsonify({"message": "Proof of education is required!"}), 400

    # Check if the file is a PDF
    if not file.filename.endswith('.pdf'):
        return jsonify({"message": "Invalid file type. Please upload a PDF file."}), 400

    # Define the upload path and save the file
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
@therapist_routes.route('/login', methods=['POST'])
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
