from models import Patient, Therapist, db
from utils import calculate_match_score

def match_patient_with_therapist(patient_id):
    patient = Patient.query.get(patient_id)  # Fetch the patient from the database
    therapists = Therapist.query.all()  # Fetch all therapists from the database

    best_match = None
    highest_score = 0

    # Loop through all therapists and calculate the match score
    for therapist in therapists:
        score = calculate_match_score(patient, therapist)

        # Update the best match if a higher score is found
        if score > highest_score:
            best_match = therapist
            highest_score = score

    return best_match
