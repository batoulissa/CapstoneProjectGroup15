# Booking Routes
# Original Author: Sanna Ascard Soederstroem

from flask import Flask, request, jsonify, Blueprint, session
from flask_sqlalchemy import SQLAlchemy
from models import Booking, db, Therapist, Patient
from datetime import datetime

booking_routes = Blueprint('booking_routes', __name__)

# Book an appointment (PATIENT only)
@booking_routes.route('/book', methods=['POST'])
def book_appointment():
    patient_id = session.get('patient_id')  # 👈 Session check for patient

    if not patient_id:
        return jsonify({"error": "You must be logged in as a patient to book!"}), 401

    data = request.json
    therapist_id = data.get('therapist_id')
    appointment_time = data.get('appointment_time')

    if not all([therapist_id, appointment_time]):
        return jsonify({"error": "Missing data"}), 400

    try:
        appointment_time = datetime.strptime(appointment_time, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    new_booking = Booking(
        therapist_id=therapist_id,
        patient_id=patient_id,
        appointment_time=appointment_time
    )
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": "Appointment booked successfully!"})


# View booked appointments (BOTH patients & therapists can view their own)
@booking_routes.route('/bookings', methods=['GET'])
def get_user_bookings():
    therapist_id = session.get('therapist_id')
    patient_id = session.get('patient_id')

    if not therapist_id and not patient_id:
        return jsonify({"error": "You must be logged in to view bookings"}), 401

    if patient_id:
        bookings = Booking.query.filter_by(patient_id=patient_id).all()
    else:
        bookings = Booking.query.filter_by(therapist_id=therapist_id).all()
    
    return jsonify([{
        "booking_id": booking.booking_id,
        "therapist_id": booking.therapist_id,
        "patient_id": booking.patient_id,
        "appointment_time": booking.appointment_time.strftime("%Y-%m-%d %H:%M"),
        "booking_status": booking.booking_status
    } for booking in bookings])


# Cancel appointment (PATIENT only)
@booking_routes.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    patient_id = session.get('patient_id')
    if not patient_id:
        return jsonify({"error": "Only patients can cancel bookings"}), 401

    booking = Booking.query.get(booking_id)
    if not booking or booking.patient_id != patient_id:
        return jsonify({"error": "Booking not found or unauthorized"}), 403

    booking.booking_status = "canceled"
    db.session.commit()

    return jsonify({"message": "Booking canceled"})

# Change appointment (PATIENT only)
@booking_routes.route('/change/<int:booking_id>', methods=['POST'])
def change_booking(booking_id):
    patient_id = session.get('patient_id')
    if not patient_id:
        return jsonify({"error": "Only patients can change bookings"}), 401

    data = request.json
    new_time = data.get("appointment_time")

    booking = Booking.query.get(booking_id)
    if not booking or booking.patient_id != patient_id:
        return jsonify({"error": "Booking not found or unauthorized"}), 403

    try:
        new_time = datetime.strptime(new_time, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    booking.appointment_time = new_time
    db.session.commit()

    return jsonify({"message": "Booking updated", "new_time": new_time.strftime("%Y-%m-%d %H:%M")})

# Approve or reject (THERAPIST only)
@booking_routes.route('/approve/<int:booking_id>', methods=['POST'])
def approve_or_reject_booking(booking_id):
    therapist_id = session.get('therapist_id')
    if not therapist_id:
        return jsonify({"error": "Only therapists can approve/reject"}), 401

    data = request.json
    action = data.get("action")  # expected values: "approve", "reject"

    if not action or action not in ["approve", "reject"]:
        return jsonify({"error": "Invalid action"}), 400

    booking = Booking.query.get(booking_id)
    if not booking or booking.therapist_id != therapist_id:
        return jsonify({"error": "Booking not found or unauthorized"}), 403

    booking.booking_status = "confirmed" if action == "approve" else "rejected"
    db.session.commit()

    return jsonify({"message": f"Booking {booking.booking_status}"})
