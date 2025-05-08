from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy

booking_routes = Blueprint('booking_routes', __name__)

# Book an appointment
@booking_routes.route('/book', methods=['POST'])
def book_appointment():
    data = request.json
    therapist_id = data.get('therapist_id')
    patient_id = data.get('patient_id')
    appointment_time = data.get('appointment_time')
    
    if not all([therapist_id, patient_id, appointment_time]):
        return jsonify({"error": "Missing data"}), 400
    
    try:
        appointment_time = datetime.strptime(appointment_time, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
    
    new_booking = Booking(
        therapist_id = therapist_id,
        patient_id = patient_id,
        appointment_time = appointment_time
    )
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({"message": "Appointment booked successfully!"})

# View booked appointments
@booking_routes.route('/bookings/<int:user_id>', methods=['GET'])
def get_user_bookings(user_id):
    bookings = Booking.query.filter((Booking.patient_id == user_id) | (Booking.therapist_id == user_id)).all()
    
    return jsonify([{
        "booking_id": booking.booking_id,
        "therapist_id": booking.therapist_id,
        "patient_id": booking.patient_id,
        "appointment_time": booking.appointment_time.strftime("%Y-%m-%d %H:%M"),
        "status": booking.status
    } for booking in bookings])

# Cancel booked appointment
@booking_routes.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    
    booking.status = "canceled"
    db.session.commit()
    
    return jsonify({"message": "Booking canceled"})

# Change a booked appointment
@booking_routes.route('/change/<int:booking_id>', methods=['POST'])
def change_booking(booking_id):
    data = request.json
    new_time = data.get("appointment_time")
    
    if not new_time:
        return jsonify({"error": "New appointment time required"}), 400
    
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    
    try:
        new_time = datetime.strptime(new_time, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
    
    booking.appointment_time = new_time
    db.session.commit()
    
    return jsonify({"message": "Booking updated successfully", "new_time": new_time.strptime("%Y-%m-%d %H:%M")})

