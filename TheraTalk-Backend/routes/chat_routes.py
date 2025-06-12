# Chat Routes
# Original Author: Sanna Ascard Soederstroem

from flask import Blueprint, request, jsonify, session
from models import db, Message, Therapist, Patient

chat_routes = Blueprint('chat_routes', __name__)

def get_user_type(user_id):
    # Check Patient table first
    patient = Patient.query.filter_by(patient_id=user_id).first()
    if patient:
        return 'patient'
    # Check Therapist table
    therapist = Therapist.query.filter_by(therapist_id=user_id).first()
    if therapist:
        return 'therapist'
    return None  # user not found

@chat_routes.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    therapist_id = data.get('therapist_id')
    patient_id = data.get('patient_id')
    sender_type = data.get('sender_type')
    content = data.get('content')

    if not all([therapist_id, patient_id, sender_type, content]):
        return jsonify({'error': 'Missing data'}), 400

    sender_id = therapist_id if sender_type == 'therapist' else patient_id

    # Save to database
    new_message = Message(
        therapist_id=therapist_id,
        patient_id=patient_id,
        sender_id=sender_id,
        content=content
    )
    db.session.add(new_message)
    db.session.commit()

    return jsonify({'message': 'Message saved'}), 201

@chat_routes.route('/<therapist_id>/<patient_id>', methods=['GET'])
def get_chat_history(therapist_id, patient_id):
    messages = Message.query.filter_by(
        therapist_id=therapist_id,
        patient_id=patient_id
    ).order_by(Message.timestamp.asc()).all()

    return jsonify([message.to_dict() for message in messages])

@chat_routes.route('/partners/<user_id>', methods=['GET'])
def get_chat_partners(user_id):
    user_type = get_user_type(user_id)
    if not user_type:
        return jsonify({'error': 'User not found'}), 404

    if user_type == 'patient':
        therapist_ids = db.session.query(Message.therapist_id)\
            .filter_by(patient_id=user_id).distinct().all()
        therapist_ids = [tid[0] for tid in therapist_ids]
        therapists = Therapist.query.filter(Therapist.therapist_id.in_(therapist_ids)).all()

        partners = []
        for t in therapists:
            last_msg = Message.query.filter_by(
                therapist_id=t.therapist_id,
                patient_id=user_id
            ).order_by(Message.timestamp.desc()).first()
            partner_dict = t.to_dict()
            partner_dict['lastMessage'] = last_msg.content if last_msg else None
            partners.append(partner_dict)

        return jsonify(partners)

    elif user_type == 'therapist':
        patient_ids = db.session.query(Message.patient_id)\
            .filter_by(therapist_id=user_id).distinct().all()
        patient_ids = [pid[0] for pid in patient_ids]
        patients = Patient.query.filter(Patient.patient_id.in_(patient_ids)).all()

        partners = []
        for p in patients:
            last_msg = Message.query.filter_by(
                therapist_id=user_id,
                patient_id=p.patient_id
            ).order_by(Message.timestamp.desc()).first()
            partner_dict = p.to_dict()
            partner_dict['lastMessage'] = last_msg.content if last_msg else None
            partners.append(partner_dict)

        return jsonify(partners)

