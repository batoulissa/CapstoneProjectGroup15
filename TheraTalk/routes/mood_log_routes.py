from flask import Blueprint, request, jsonify, session
from models import db, MoodLog, Patient
from datetime import datetime, timedelta
from collections import Counter

mood_log_routes = Blueprint('mood_log_routes', __name__)

VALID_MOODS = {"Happy", "Sad", "Anxious", "Stressed", "Relaxed", "Excited", "Tired", "Neutral"}

# Log mood
@mood_log_routes.route('/log_mood', methods=['POST'])
def log_mood():
    patient_id = session.get('patient_id')  # Session-based authentication

    if not patient_id:
        return jsonify({"message": "You must be logged in to log your mood!"}), 401

    data = request.json
    mood = data.get('mood')

    if not mood or mood not in VALID_MOODS:
        return jsonify({"error": "Invalid mood."}), 400

    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if not patient:
        return jsonify({"message": "Patient not found!"}), 404

    new_log = MoodLog(patient_id=patient_id, mood=mood)
    db.session.add(new_log)
    db.session.commit()

    return jsonify({"message": "Mood logged successfully! 😊"})


# Get all logged moods
@mood_log_routes.route('/get_logged_moods', methods=['GET'])
def get_logged_moods():
    patient_id = session.get('patient_id')

    if not patient_id:
        return jsonify({"message": "You must be logged in to view your mood history."}), 401

    moods = MoodLog.query.filter_by(patient_id=patient_id).order_by(MoodLog.timestamp.desc()).all()
    mood_list = [{"mood": m.mood, "timestamp": m.timestamp} for m in moods]

    return jsonify(mood_list)


# Get current streak
@mood_log_routes.route('/get_streak', methods=['GET'])
def get_streak():
    patient_id = session.get('patient_id')

    if not patient_id:
        return jsonify({"message": "You must be logged in to view your streak."}), 401

    moods = MoodLog.query.filter_by(patient_id=patient_id).order_by(MoodLog.timestamp.desc()).all()

    if not moods:
        return jsonify({"streak": 0})

    streak = 1
    prev_date = moods[0].timestamp.date()

    for log in moods[1:]:
        log_date = log.timestamp.date()
        if prev_date - timedelta(days=1) == log_date:
            streak += 1
            prev_date = log_date
        else:
            break

    return jsonify({"streak": streak})


# Optional: Mood trend (most frequent mood)
@mood_log_routes.route('/get_trend', methods=['GET'])
def get_trend():
    patient_id = session.get('patient_id')

    if not patient_id:
        return jsonify({"message": "You must be logged in to view your trend."}), 401

    moods = MoodLog.query.filter_by(patient_id=patient_id).all()

    if not moods:
        return jsonify({"trend": "No data."})

    mood_counts = Counter([m.mood for m in moods])
    most_common = mood_counts.most_common(1)[0]

    return jsonify({
        "mood": most_common[0],
        "count": most_common[1]
    })
