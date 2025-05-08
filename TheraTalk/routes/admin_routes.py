from flask import Blueprint, request, jsonify, session
from models import db, Admin, Therapist, Patient
from werkzeug.security import generate_password_hash, check_password_hash

admin_routes = Blueprint('admin_routes', __name__)

############################ Admin Related API Routes ############################

# Register New Admin
@admin_routes.route('/register_admin', methods=['POST'])
def register_admin():
    try:
        data = request.get_json()

        # Extract username and password
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new admin object
        new_admin = Admin(username=username, password=password)  # No need to pre-hash

        # Add to the database
        db.session.add(new_admin)
        db.session.commit()

        return jsonify({"message": "Admin registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Admin Login
@admin_routes.route('/login_admin', methods=['POST'])
def login_admin():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Find admin by username
    admin = Admin.query.filter_by(username=username).first()

    if admin and check_password_hash(admin.password, password):
        # Set admin session using the secret key
        session['admin_id'] = admin.admin_id
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401


# Admin Logout 
@admin_routes.route('/logout_admin', methods=['POST'])
def logout_admin():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    admin = Admin.query.filter_by(username=username).first()
    
    if admin and check_password_hash(admin.password, password):
        session.pop('admin_id', None)  # Clear admin session 
        return jsonify({"message": "Logged out successfully!"}), 200

# Delete Admin
@admin_routes.route('/delete_admin', methods=['DELETE'])
def delete_admin():
    try:
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Find admin by username
        admin = Admin.query.filter_by(username=username).first()

        if not admin or not check_password_hash(admin.password, password):
            return jsonify({"error": "Invalid credentials!"}), 401

        # Delete the admin account
        db.session.delete(admin)
        db.session.commit()

        return jsonify({"message": "Admin account deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


############################ Admin API Related to Therapists ############################

# Approve therapists func
@admin_routes.route('/approve_therapist/<int:id>', methods=['POST'])
def approve_therapist(id):
    # Check for admin authentication
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    # Query the database for the therapist
    therapist = Therapist.query.get(id)
    if not therapist:
        return jsonify({"message": "Therapist not found!"}), 404

    # Approve the therapist
    therapist.status = "approved"
    db.session.commit()

    return jsonify({"message": f"Therapist with ID {id} approved successfully!"}), 200

# Reject Therapist func.
@admin_routes.route('/reject_therapist/<int:id>', methods=['POST'])
def reject_therapist(id):
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    therapist = Therapist.query.get(id)
    if not therapist:
        return jsonify({"message": "Therapist not found!"}), 404

    try:
        therapist.status = "rejected"
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Ensure the transaction is rolled back if something fails
        return jsonify({"message": f"An error occurred while rejecting the therapist: {str(e)}"}), 500

    return jsonify({"message": "Therapist rejected successfully!"}), 200

# Get All Therapists func.
@admin_routes.route('/get_all_therapists', methods=['GET'])
def get_all_therapists():
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    therapists = Therapist.query.all()
    therapist_list = [therapist.to_dict() for therapist in therapists]
    return jsonify(therapist_list)

# Get Pending Therapists func.
@admin_routes.route('/get_pending_therapists', methods=['GET'])
def get_pending_therapists():
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    pending_therapists = Therapist.query.filter_by(status="pending").all()
    return jsonify([{"id": t.id, "username": t.username, "status": t.status} for t in pending_therapists])

# Ban Therapist
@admin_routes.route('/ban_therapist/<int:id>', methods=['POST'])
def ban_therapist(id):
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    therapist = Therapist.query.get(id)
    if not therapist:
        return jsonify({"message": "Therapist not found!"}), 404

    therapist.status = "banned"
    db.session.commit()

    return jsonify({"message": f"Therapist with ID {id} has been banned."}), 200

@admin_routes.route('/get_banned_therapists', methods=['GET'])
def get_banned_therapists():
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    banned_therapists = Therapist.query.filter_by(status="banned").all()
    return jsonify([{"id": t.id, "name": t.name, "status": t.status} for t in banned_therapists])


############################ Admin API Related to Patients ############################

# Approve patient func
@admin_routes.route('/approve_patient/<int:id>', methods=['POST'])
def approve_patient(id):
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"message": "Patient not found!"}), 404

    patient.status = "approved"
    db.session.commit()

    return jsonify({"message": f"Patient with ID {id} approved successfully!"}), 200

# Reject patient func
@admin_routes.route('/reject_patient/<int:id>', methods=['POST'])
def reject_patient(id):
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"message": "Patient not found!"}), 404

    try:
        patient.status = "rejected"
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred while rejecting the patient: {str(e)}"}), 500

    return jsonify({"message": "Patient rejected successfully!"}), 200

# Get all patients func
@admin_routes.route('/get_all_patients', methods=['GET'])
def get_all_patients():
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    patients = Patient.query.all()
    return jsonify([patient.to_dict() for patient in patients])

# Get pending patients func
@admin_routes.route('/get_pending_patients', methods=['GET'])
def get_pending_patients():
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    pending_patients = Patient.query.filter_by(status="pending").all()
    return jsonify([{"id": p.id, "username": p.username, "status": p.status} for p in pending_patients])

@admin_routes.route('/ban_patient/<int:id>', methods=['POST'])
def ban_patient(id):
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"message": "Patient not found!"}), 404

    patient.status = "banned"
    db.session.commit()

    return jsonify({"message": f"Patient with ID {id} has been banned."}), 200


@admin_routes.route('/get_banned_patients', methods=['GET'])
def get_banned_patients():
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    banned_patients = Patient.query.filter_by(status="banned").all()
    return jsonify([{"id": p.id, "username": p.username, "status": p.status} for p in banned_patients])

