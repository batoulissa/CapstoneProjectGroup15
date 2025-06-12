# Therapist Routes
# Original Author: Sanna Ascard Soederstroem

import os
from flask import Blueprint, request, jsonify, session
from models import db, Therapist, PronounsEnum
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
import time

therapist_routes = Blueprint('therapist_routes', __name__)

# Therapist registration
@therapist_routes.route('/register_therapist', methods=['POST'])
def register_therapist():
    data = request.form

    name = data.get('name')
    username = data.get('username')  # Get the username
    pronouns = data.get('pronouns')
    experience_years = data.get('experience_years')
    availability = data.get('availability')
    languages = data.get('languages', [])
    focus_areas = data.get('focus_areas', [])
    password = data.get('password')

    # Check if username is unique
    existing_therapist = Therapist.query.filter_by(username=username).first()
    if existing_therapist:
        return jsonify({"message": "Username already taken!"}), 400

    # Handle file upload (proof of education)
    file = request.files.get('proof_of_education')
    
    if not file:
        return jsonify({"message": "Proof of education is required!"}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({"message": "Invalid file type. Please upload a PDF file."}), 400

    filename = f"{username}_{int(time.time())}.pdf"
    file_path_therapist = os.path.join('uploads', filename)
    file.save(file_path_therapist)
    
    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    # Initialize a new therapist
    new_therapist = Therapist(
        name=name,
        username=username,
        pronouns=pronouns,
        experience_years=experience_years,
        languages=languages,
        focus_areas=focus_areas,
        password=hashed_password,
        proof_of_education=file_path_therapist
    )

    # Check availability and set the corresponding columns for each day
    for day_of_week in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        start_time_key = f"availability[{day_of_week}][start_time]"
        end_time_key = f"availability[{day_of_week}][end_time]"
        
        # If both start and end times exist for the day
        if start_time_key in data and end_time_key in data:
            start_time_str = data.get(start_time_key)
            end_time_str = data.get(end_time_key)

            if start_time_str and end_time_str:
                # Validate and convert the time strings to time objects
                try:
                    start_time = datetime.strptime(start_time_str, '%H:%M').time()
                    end_time = datetime.strptime(end_time_str, '%H:%M').time()
                    # Set the corresponding day's availability as a string (e.g., "09:00-17:00")
                    setattr(new_therapist, day_of_week, f"{start_time}-{end_time}")
                except ValueError:
                    return jsonify({"error": f"Invalid time format for {day_of_week}. Use HH:MM format."}), 400
            else:
                # If either start_time or end_time is missing, set the availability to None (NULL)
                setattr(new_therapist, day_of_week, None)
        else:
            # If no availability for the day, set it to None (NULL)
            setattr(new_therapist, day_of_week, None)

    # Add therapist to the session and commit the changes
    db.session.add(new_therapist)
    db.session.commit()

    return jsonify({"message": "Therapist registration is pending approval!"}), 201


# Therapist Login
@therapist_routes.route('/login_therapist', methods=['POST'])
def login_therapist():
    data = request.get_json()

    username = data.get('username')  # Use username for login
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    therapist = Therapist.query.filter_by(username=username).first()  # Find therapist by username

    if not therapist:
        return jsonify({"message": "Therapist not found!"}), 404
    
    if therapist.status == 'banned':  # Check if therapist is banned
        return jsonify({"message": "Your account has been banned. Contact support for assistance."}), 403

    if check_password_hash(therapist.password, password):  # Validate password
        if therapist.status != "approved":
            return jsonify({"message": "Account not approved. Please wait for approval."}), 403
        
        # Store therapist ID in session
        session['therapist_id'] = therapist.therapist_id
        return jsonify({"message": "Login successful!"}), 200

    return jsonify({"message": "Invalid credentials!"}), 401


# Therapist Logout
@therapist_routes.route('/logout_therapist', methods=['POST'])
def logout_therapist():
    data = request.get_json()

    username = data.get('username')  # Use username to verify
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    therapist = Therapist.query.filter_by(username=username).first()

    if therapist and check_password_hash(therapist.password, password):
        # If using session-based login, you can clear the session here
        session.pop('therapist_id', None)  # Remove therapist ID from session
        
        return jsonify({"message": "Logged out successfully!"}), 200

    return jsonify({"message": "Invalid credentials!"}), 401

@therapist_routes.route('/update_therapist/<username>', methods=['PUT'])
def update_therapist(username):
    data = request.form

    therapist_id = session.get('therapist_id')  # Get the therapist ID from session

    if not therapist_id:
        return jsonify({"message": "You must be logged in to update your information!"}), 401

    therapist = Therapist.query.filter_by(username=username).first()
    
    # Initialize status_updated to False for file upload checking only
    status_updated = False
    
    if not therapist:
        return jsonify({"message": "Therapist not found!"}), 404

    # Get new values from the request and update the therapist's information
    name = data.get('name')
    pronouns = data.get('pronouns')
    experience_years = data.get('experience_years')
    languages = data.get('languages')
    focus_areas = data.get('focus_areas')
    password = data.get('password')  # If therapist wants to change the password
    
    # Check if a proof of education file was uploaded
    if 'proof_of_education' in request.files:
        education_file = request.files['proof_of_education']
        if education_file:
            # Make sure the file has a valid name and save it
            filename = f"{username}_{int(time.time())}.pdf"
            file_path_therapist = os.path.join('uploads', filename)
            education_file.save(file_path_therapist)
            therapist.proof_of_education = file_path_therapist  # Update the therapist's proof of education file path in the database

            # Set status to pending for verification
            therapist.status = 'pending'
            status_updated = True

    # Check availability and set the corresponding columns for each day
    for day_of_week in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        start_time_key = f"availability[{day_of_week}][start_time]"
        end_time_key = f"availability[{day_of_week}][end_time]"

        start_time_str = data.get(start_time_key)
        end_time_str = data.get(end_time_key)

        if start_time_str == '' or end_time_str == '':
            # If both times are empty, set the availability for that day to NULL
            setattr(therapist, day_of_week, None)  # Assuming the database column can accept NULL
        elif start_time_str and end_time_str:
            # Validate and convert the time strings to time objects
            try:
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()
                # Set the corresponding day's availability as a string (e.g., "09:00-17:00")
                setattr(therapist, day_of_week, f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}")
            except ValueError:
                return jsonify({"error": f"Invalid time format for {day_of_week}. Use HH:MM format."}), 400

    # Update other fields if provided
    if name:
        therapist.name = name
    if pronouns:
        therapist.pronouns = PronounsEnum(pronouns)  # Ensure valid Enum
    if experience_years:
        therapist.experience_years = experience_years
    if languages:
        therapist.languages = languages  # Store languages as a comma-separated string
    if focus_areas:
        therapist.focus_areas = focus_areas
    if password:
        therapist.password = generate_password_hash(password)  # Update password with hashed value

    db.session.commit()  # Save the changes to the database

    # Return response based on whether the proof_of_education file was updated
    if status_updated:
        return jsonify({"message": "Therapist information updated successfully! Account status set to 'pending' for verification because of updated Proof of Education."}), 200
    else:
        return jsonify({"message": "Therapist information updated successfully!"}), 200

   
# Delete Therapist Account
@therapist_routes.route('/delete_therapist/<username>', methods=['DELETE'])
def delete_therapist(username):
    data = request.get_json()

    therapist_id = session.get('therapist_id')  # Get the therapist ID from session

    if not therapist_id:
        return jsonify({"message": "You must be logged in to delete your account!"}), 401

    therapist = Therapist.query.filter_by(username=username).first()

    if not therapist:
        return jsonify({"message": "Therapist not found!"}), 404

    # Ask for confirmation before proceeding with account deletion
    confirmation = data.get('confirmation')
    if confirmation != 'DELETE':
        return jsonify({"message": "Confirmation required to delete the account!"}), 400

    db.session.delete(therapist)  # Delete the therapist record from the database
    db.session.commit()  # Commit the changes to the database

    session.pop('therapist_id', None)  # Clear the session (therapist is logged out)

    return jsonify({"message": "Therapist account deleted successfully!"}), 200
