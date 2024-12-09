def calculate_match_score(patient, therapist):
    score = 0

    # Availability Match (1 if match, 0 if no match)
    if therapist.availability == patient.preferred_availability:
        score += 1
    
    # Language Match (1 if there's an overlap, 0 if no match)
    patient_languages = set(patient.languages.split(','))
    therapist_languages = set(therapist.languages.split(','))
    
    # If there's any overlap in languages
    if patient_languages & therapist_languages:
        score += 1

    # Focus Areas vs. Therapy Needs (1 if match, 0 if no match)
    if patient.therapy_need in therapist.focus_areas:
        score += 1

    # Optional Age and Gender Match
    if hasattr(therapist, 'age_group') and therapist.age_group == patient.age_group:  # If applicable
        score += 1

    if hasattr(patient, 'gender') and patient.gender == therapist.gender:
        score += 1

    # Optional Medical History Match
    if hasattr(patient, 'medical_history') and patient.medical_history in therapist.specialties:
        score += 1
        
    # Availability Match (1 if there's overlap, 0 if no overlap)
    patient_availability = set(patient.availability.split(','))
    therapist_availability = set(therapist.availability.split(','))
    
    if patient_availability & therapist_availability:
        score += 1
        
    return score
