from flask import Blueprint, request, jsonify, session
from models import db, Admin, Therapist, Patient
from werkzeug.security import generate_password_hash, check_password_hash

admin_routes = Blueprint('admin_routes', __name__)

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
        new_admin = Admin(username=username, password=hashed_password)

        # Add to the database
        db.session.add(new_admin)
        db.session.commit()

        return jsonify({"message": "Admin registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_routes.route('/login_admin', methods=['POST'])
def login_admin():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Find admin by username
    admin = Admin.query.filter_by(username=username).first()

    if admin and check_password_hash(admin.password, password):
        # Set admin session using the secret key
        session['admin_id'] = admin.id
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401


# Admin Logout
@admin_routes.route('/logout_admin', methods=['POST'])
def logout_admin():
    session.pop('admin_id', None)  # Clear admin session
    return jsonify({"message": "Logged out successfully!"}), 200


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


@admin_routes.route('/reject_therapist/<int:id>', methods=['POST'])
def reject_therapist(id):
    if 'admin_id' not in session:
        return jsonify({"message": "Access denied. Admins only."}), 403

    therapist = Therapist.query.get(id)
    if not therapist:
        return jsonify({"message": "Therapist not found!"}), 404

    therapist.status = "rejected"
    db.session.commit()

    return jsonify({"message": "Therapist rejected successfully!"}), 200
