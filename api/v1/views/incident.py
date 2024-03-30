#! /usr/bin/env python3
"""This is the incident api"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, request
from flasgger import Swagger, swag_from
from models.utils.retrieve_data import close_hosp, get_incident
from models.utils.update_data import modify_incident


ignore_keys = ['id', 'created_at', 'updated_at']

# GETs
@app_views.route('/incidents', methods=['GET'])
@app_views.route('/incidents/<string:incident_id>', methods=['GET'])
@swag_from('documentation/incidents/incident.yml', methods=['GET'])
def incident(incident_id=None):
    """Get all incidents"""
    if incident_id:
        incident = get_incident(incident_id)
        if 'error' in incident:
            return jsonify(incident), 404
        return jsonify(incident)
    inc = get_incident()
    if not inc:
        return jsonify({"error": "no incidents found"}), 404
    return jsonify(inc)

@app_views.route('/incident/hospitals', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/incident/close_hosp.yml', methods=['GET'])
def incidence_close_hosp(top=3):
    """Close a hospital"""
    data = request.args
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    lat = data.get('lat')
    lng = data.get('lng')
    top = data.get('top')

    try:
        lat = float(lat)
    except ValueError:
        return jsonify({"error": "Latitude must be a number"}), 400
    try:
        lng = float(lng)
    except ValueError:
        return jsonify({"error": "Longitude must be a number"}), 400
    try:
        top = int(top)
    except ValueError:
        return jsonify({"error": "Top must be a number"}), 400


    lat, lng = float(lat), float(lng)
    top = int(top)

    hospitals = close_hosp(patient_id=None, lat=lat, lng=lng, top=top, incident=True)

    if 'error' in hospitals:
        return jsonify({}), 400
    return jsonify(hospitals)



# PUTs
@app_views.route('/incidents/<string:incident_id>', methods=['PUT'])
@swag_from('documentation/incidents/update_incident.yml', methods=['PUT'])
def update_incident(incident_id=None):
    """Modify an incident"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    incident = modify_incident(data, incident_id)
    return jsonify(incident)