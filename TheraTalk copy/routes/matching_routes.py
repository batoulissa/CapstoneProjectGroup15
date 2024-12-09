from flask import Blueprint, jsonify
from models import Therapist, Patient

matching_routes = Blueprint('matching_routes', __name__)

@matching_routes.route('/match_patient', methods=['POST'])
def match_patient():
    data = request.get_json()
    patient_id = data.get('patient_id')

    if not patient_id:
        return jsonify({"error": "Patient ID is required"}), 400

    best_match = match_patient_with_therapist(patient_id)

    if best_match:
        return jsonify(best_match.to_dict())
    else:
        return jsonify({"message": "No matching therapist found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
