import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, Blueprint, session
from models import db, Patient, Therapist
from collections import OrderedDict

matching_routes = Blueprint('matching_routes', __name__)

def get_matched_values(patient_values, therapist_values):
    def clean(values):
        if isinstance(values, str):
            return set(val.strip().lower() for val in values.split(',') if val.strip())
        elif isinstance(values, list):
            return set(val.strip().lower() for val in values if isinstance(val, str))
        return set()

    patient_cleaned = clean(patient_values)
    therapist_cleaned = clean(therapist_values)

    print("Patient Values (cleaned):", patient_cleaned)
    print("Therapist Values (cleaned):", therapist_cleaned)

    return list(patient_cleaned.intersection(therapist_cleaned))


def check_availability(therapist_schedule, patient_schedule):
    """Checks if there's any overlap in availability between therapist and patient."""
    matched_times = {}

    for day, patient_time in patient_schedule.items():
        therapist_time = therapist_schedule.get(day)
        if therapist_time:
            t_start, t_end = therapist_time.split('-')
            p_start, p_end = patient_time.split('-')

            # Convert times to comparable format (HH:MM)
            t_start, t_end = t_start[:5], t_end[:5]
            p_start, p_end = p_start[:5], p_end[:5]

            if t_end >= p_start and t_start <= p_end:
                matched_times[day] = f"{t_start}-{t_end}"

    return matched_times if matched_times else None

def preprocess_languages(languages):
    if isinstance(languages, str):
        return [lang.strip().lower() for lang in languages.split(',') if lang.strip()]
    elif isinstance(languages, list):
        return [lang.strip().lower() for lang in languages if isinstance(lang, str)]
    else:
        return []


@matching_routes.route('/matching_therapist_with_user', methods=['POST'])
def matching_therapist_with_user():
    """AI-based therapist matching with flexible pronoun matching, availability filtering, and fallback options."""
    data = request.json
    patient_availability = data.get('availability')

    patient_id = session.get('patient_id')
    if not patient_id:
        return jsonify({"message": "You must be logged in to update your information!"}), 401

    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"message": "Patient not found!"}), 404

    if not patient_availability:
        return jsonify({'error': 'Availability not provided'}), 400
    
    patient_therapy_need = patient.therapy_need or ""
    patient_languages = patient.languages or ""

    therapists = Therapist.query.all()

    therapist_data = pd.DataFrame([
        {
            "id": t.therapist_id,
            "name": t.name,
            "focus_areas": t.focus_areas,
            "languages": t.languages,
            "experience_years": t.experience_years,
            "pronouns": t.pronouns,
            "rating": 0,
            "availability": {
                "monday": t.monday,
                "tuesday": t.tuesday,
                "wednesday": t.wednesday,
                "thursday": t.thursday,
                "friday": t.friday,
                "saturday": t.saturday,
                "sunday": t.sunday
            }
        } for t in therapists
    ])

    # Step 1: Filter therapists by availability
    therapist_data["matched_times"] = therapist_data["availability"].apply(
        lambda t_avail: check_availability(t_avail, patient_availability)
    )
    therapist_data = therapist_data[therapist_data["matched_times"].notnull()]

    if therapist_data.empty:
        return jsonify({"message": "No therapists available for the requested times."})

    # Step 2: Compute similarity scores
    vectorizer = TfidfVectorizer()

    # Focus areas similarity
    focus_areas_texts = therapist_data["focus_areas"].fillna("").tolist()
    patient_focus_text = [patient_therapy_need]
    focus_area_vectors = vectorizer.fit_transform(patient_focus_text + focus_areas_texts)
    focus_area_sim = cosine_similarity(focus_area_vectors[0], focus_area_vectors[1:]).flatten()

    # Preprocess languages
    patient_language_list = preprocess_languages(patient_languages)
    therapist_data["language_list"] = therapist_data["languages"].apply(preprocess_languages)

    therapist_language_texts = [", ".join(langs) for langs in therapist_data["language_list"]]
    patient_language_text = [", ".join(patient_language_list)]

    language_vectors = vectorizer.fit_transform(patient_language_text + therapist_language_texts)
    language_sim = cosine_similarity(language_vectors[0], language_vectors[1:]).flatten()

    # Normalize experience and rating
    max_experience = max(therapist_data["experience_years"].max(), 1)
    experience_scores = therapist_data["experience_years"] / max_experience
    rating_scores = therapist_data["rating"].fillna(0) / 5.0

    # Step 3: Final matching score
    therapist_data["focus_area_match"] = focus_area_sim
    therapist_data["language_match"] = language_sim
    therapist_data["experience_score"] = experience_scores
    therapist_data["rating_score"] = rating_scores

    therapist_data["match_score"] = (
        0.3 * focus_area_sim +
        0.2 * language_sim +
        0.2 * experience_scores +
        0.2 * rating_scores
    )

    # Step 4: Sort and format output
    result = therapist_data.sort_values(by="match_score", ascending=False).apply(
        lambda row: OrderedDict([
            ("name", row["name"]),
            ("match_score", round(row["match_score"], 2)),
            ("matched_attributes", {
                "focus_areas": get_matched_values(patient_therapy_need, row["focus_areas"]),
                "languages": get_matched_values(patient_language_list, row["language_list"]),
                "availability": row["matched_times"]
            })
        ]), axis=1
    ).tolist()

    return jsonify(result)
