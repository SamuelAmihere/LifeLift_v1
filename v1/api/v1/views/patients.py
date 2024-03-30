#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Hospitals """
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger import Swagger, swag_from
from models.hosp_operator import Hospital
from models.incident import Incident
from models.system_user import Patient
from datetime import date, datetime

from models.utils.delete_data import delete_patient
from models.utils.post_data import post_patient
from models.utils.retrieve_data import close_hosp, get_by_distance, get_nearby, get_patient_incident, get_patient_request
from models.utils.update_data import modify_patient


ignore_keys = ['id', 'created_at', 'updated_at']

# GETs
@app_views.route('/patients', methods=['GET'])
@app_views.route('/patients/<string:patient_id>', methods=['GET'])
@swag_from('documentation/patients/get_patient.yml', methods=['GET'])
def get_patient(patient_id=None):
    """Get all patients"""
    pat = get_patient_request(patient_id)
    return jsonify(pat)

@app_views.route('/patients/<string:patient_id>/incident', methods=['GET'])
@swag_from('documentation/patients/patient_incident.yml', methods=['GET'])
def patient_incident(patient_id=None):
    """Get patient incident"""
    incident = get_patient_incident(patient_id)
    return jsonify(incident.to_dict())

@app_views.route('/patient/<string:patient_id>/hospitals/', methods=['GET'],
                    strict_slashes=False)
@app_views.route('/patient/hospitals', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/incident/close_hosp.yml', methods=['GET'])
def p_close_hosp(patient_id=None, top=3):
    """Close a hospital"""
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    
    if lat != None and lng != None and patient_id != None:
        hospitals = close_hosp(patient_id, lat, lng, top)
        return jsonify(hospitals)
    elif lat == None and lng == None and patient_id != None:
        hospitals = close_hosp(patient_id, top)
        return jsonify(hospitals)
    elif lat != None and lng != None and patient_id == None:
        hospitals = close_hosp(lat, lng, top)
        return jsonify({"error": "Missing patient id"}), 400
    else:
        return jsonify({"error": "Missing latitude or longitude"}), 400


# PUT
@app_views.route('/patients/<string:patient_id>', methods=['PUT'])
@swag_from('documentation/patients/update_patient.yml', methods=['PUT'])
def update_patient(patient_id):
    """Modify a patient"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    patient = modify_patient(data, patient_id)
    return jsonify(patient)

# POST
@app_views.route('/patients', methods=['POST'])
@swag_from('documentation/patients/create_patient.yml', methods=['POST'])
def create_patient():
    """Create a new patient"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    patient = post_patient(data)
    if not patient:
        return jsonify({"error": "patient not created"}), 400
    return jsonify(patient), 201

# DELETE
@app_views.route('/patients/<string:patient_id>', methods=['DELETE'])
@swag_from('documentation/patients/remove_patient.yml', methods=['DELETE'])
def remove_patient(patient_id):
    """Delete a patient"""
    patient = delete_patient(patient_id)
    if 'error' in patient:
        return jsonify({"error": "patient not found"}), 404
    return jsonify({}), 200