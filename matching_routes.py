# Matching Algorithm Routes
# Original Author: Sanna Ascard Soederstroem

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, Blueprint, session
from models import db, Patient, Therapist
from collections import OrderedDict

matching_routes = Blueprint('matching_routes', __name__)

# Utility functions 

# Normalize both values into lowercase sets
def get_matched_values(patient_values, therapist_values):
    def clean(values):
        if isinstance(values, str):
            return set(val.strip().lower() for val in values.split(',') if val.strip())
        elif isinstance(values, list):
            return set(val.strip().lower() for val in values if isinstance(val, str))
        return set()

    # Get intersection of clean sets
    patient_cleaned = clean(patient_values)
    therapist_cleaned = clean(therapist_values)

    print("Patient Values (cleaned):", patient_cleaned)
    print("Therapist Values (cleaned):", therapist_cleaned)

    return list(patient_cleaned.intersection(therapist_cleaned))

# Compare availability day-by-day to find overlaps
def check_availability(therapist_schedule, patient_schedule):
    matched_times = {}

    for day, patient_time in patient_schedule.items():
        therapist_time = therapist_schedule.get(day)
        if therapist_time:
            t_start, t_end = therapist_time.split('-')
            p_start, p_end = patient_time.split('-')

            # Convert times to comparable format (HH:MM)
            t_start, t_end = t_start[:5], t_end[:5]
            p_start, p_end = p_start[:5], p_end[:5]

            # Check for overlaps
            if t_end >= p_start and t_start <= p_end:
                matched_times[day] = f"{t_start}-{t_end}"

    return matched_times if matched_times else None

# Preprocess function to clean and prepare data
def preprocess_list(values):
    if isinstance(values, str):
        return [v.strip().lower() for v in values.split(',') if v.strip()]
    elif isinstance(values, list):
        return [v.strip().lower() for v in values if isinstance(v, str)]
    return []

# Count how many matches for each attribute
def count_area_matches(patient_therapy_need, therapist_focus):
    return len(set(patient_therapy_need).intersection(set(therapist_focus)))

def count_pronoun_matches(patient_pronouns, therapist_pronouns):
    return len(patient_pronouns.intersection(therapist_pronouns))

def count_language_matches(patient_list, therapist_list):
    return len(set(patient_list).intersection(set(therapist_list)))

# Main route for AI-based matching

@matching_routes.route('/matching_therapist_with_user', methods=['POST'])
def matching_therapist_with_user():
    
    # Basic checks and patient retrieval
    data = request.json
    patient_availability = data.get('availability')

    patient_id = session.get('patient_id')
    if not patient_id:
        return jsonify({"message": "You must be logged in to match with a therapist!"}), 401

    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"message": "Patient not found!"}), 404

    if not patient_availability:
        return jsonify({'error': 'Availability not provided'}), 400
    
    # Get relevant patient data
    patient_therapy_need = patient.therapy_need or ""
    patient_languages = patient.languages or ""
    patient_pronouns = patient.pronouns or ""

    # Load all therapists from database
    therapists = Therapist.query.all()

    # Convert therapist info to a DataFrame for processing
    therapist_data = pd.DataFrame([
        {
            "id": t.therapist_id,
            "name": t.name,
            "focus_areas": t.focus_areas,
            "languages": t.languages,
            "experience_years": t.experience_years,
            "pronouns": t.pronouns,
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

    # Filter therapists by availability
    therapist_data["matched_times"] = therapist_data["availability"].apply(
        lambda t_avail: check_availability(t_avail, patient_availability)
    )
    therapist_data = therapist_data[therapist_data["matched_times"].notnull()]

    if therapist_data.empty:
        return jsonify({"message": "No therapists available for the requested times."})
   
    # Calculate availability strength (number of matched days)
    therapist_data["availability_strength"] = therapist_data["matched_times"].apply(lambda x: len(x))

    # Compute similarity scores

    # Focus area similarity using TF-IDF + match count
    patient_therapy_need = preprocess_list(patient_therapy_need)
    therapist_data['therapist_focus'] = therapist_data['focus_areas'].apply(preprocess_list)
    therapist_focus_texts = [", ".join(areas) for areas in therapist_data["therapist_focus"]]
    
    focus_area_vectorizer = TfidfVectorizer()
    focus_area_vectors = focus_area_vectorizer.fit_transform([", ".join(patient_therapy_need)] + therapist_focus_texts)
    focus_area_sim = cosine_similarity(focus_area_vectors[0], focus_area_vectors[1:]).flatten()
    therapist_data["focus_area_sim"] = focus_area_sim

    therapist_data["areas_match_count"] = therapist_data["therapist_focus"].apply(
        lambda areas: count_area_matches(patient_therapy_need, areas))
    
    # Language similarity using TF-IDF + match count
    patient_language_list = preprocess_list(patient_languages)
    therapist_data["language_list"] = therapist_data["languages"].apply(preprocess_list)
    therapist_language_texts = [", ".join(langs) for langs in therapist_data["language_list"]]
    
    language_vectorizer = TfidfVectorizer()
    language_vectors = language_vectorizer.fit_transform([", ".join(patient_language_list)] + therapist_language_texts)
    language_sim = cosine_similarity(language_vectors[0], language_vectors[1:]).flatten()
    therapist_data["language_match_count"] = therapist_data["language_list"].apply(
        lambda langs: count_language_matches(patient_language_list, langs))

    # Pronoun matching
    patient_pronouns = set(preprocess_list(patient_pronouns))
    therapist_data["pronoun_set"] = therapist_data["pronouns"].apply(lambda pronouns: set(preprocess_list(pronouns)))
    therapist_data["pronoun_match_count"] = therapist_data["pronoun_set"].apply(
        lambda pronouns: count_pronoun_matches(patient_pronouns, pronouns))
    
    # Normalize scores to range 0-1
    max_exp = max(therapist_data["experience_years"].max(), 1)
    max_avail = max(therapist_data["availability_strength"].max(), 1)
    max_lang = max(therapist_data["language_match_count"].max(), 1)
    max_pronoun = max(therapist_data["pronoun_match_count"].max(), 1)

    therapist_data["experience_score"] = therapist_data["experience_years"] / max_exp
    therapist_data["availability_score"] = therapist_data["availability_strength"] / max_avail
    therapist_data["language_score"] = therapist_data["language_match_count"] / max_lang
    therapist_data["pronoun_score"] = therapist_data["pronoun_match_count"] / max_pronoun


    # Compute the weighted match score
    therapist_data["match_score"] = (
        0.40 * therapist_data["focus_area_sim"] +
        0.20 * therapist_data["language_score"] +
        0.25 * therapist_data["availability_score"] +
        0.10 * therapist_data["pronoun_score"] +
        0.05 * therapist_data["experience_score"]
    )

    # Format, sort and return the top matches
    result = therapist_data.sort_values(by="match_score", ascending=False).apply(
        lambda row: OrderedDict([
            ("name", row["name"]),
            ("pronouns", str(row["pronouns"].value)),
            ("match_score", round(row["match_score"], 2)),
            ("matched_attributes", {
                "focus_areas": list(set(patient_therapy_need).intersection(set(row["therapist_focus"]))),
                "languages": list(set(patient_language_list).intersection(set(row["language_list"]))),
                "availability": row["matched_times"]
            })
        ]), axis=1
    ).tolist()

    return jsonify(result)
