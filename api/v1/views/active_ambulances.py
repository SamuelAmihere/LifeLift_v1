#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Ambulances """
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models.alert import Alert
from models.ambulance import ActiveAmbulance, Ambulance
from models.hosp_operator import Hospital


ignore_keys = ['id', 'created_at', 'updated_at']

@app_views.route('/active_ambulances', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/active_ambulances/get_active_ambulances.yml')
def get_active_ambulances():
    """ Retrieves the list of all Active Ambulances """
    active_ambulances = storage.all(ActiveAmbulance)
    return jsonify([active_ambulance.to_dict() for active_ambulance in active_ambulances.values()])

@app_views.route('/active_ambulances/<active_ambulance_id>', methods=['GET'],
                    strict_slashes=False)
@swag_from('swagger_yaml/active_ambulances/get_active_ambulance.yml')
def get_active_ambulance(active_ambulance_id=None):
    """ Retrieves a specific Active Ambulance """
    active_ambulance = storage.get(ActiveAmbulance, active_ambulance_id)
    if active_ambulance is None:
        abort(404)
    return jsonify(active_ambulance.to_dict())

@app_views.route('/active_ambulances', methods=['POST'], strict_slashes=False)
@swag_from('swagger_yaml/active_ambulances/post_active_ambulances.yml')
def post_active_ambulance():
    """ Creates an Active Ambulance """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    
    if 'ambulance_id' not in data:
        abort(400, 'Missing ambulance_id')
    if 'alert_id' not in data:
        abort(400, 'Missing alert_id')
    if 'destination' not in data:
        abort(400, 'Missing Hostpital ID')
    
    for k, v in ActiveAmbulance.fields_errMSG.items():
        if k not in data:
            abort(400, v)
    active_ambulance = ActiveAmbulance(**data)
    storage.new(active_ambulance)
    storage.save()
    return make_response(jsonify(active_ambulance.to_dict()), 201)

@app_views.route('/active_ambulances/<active_ambulance_id>', methods=['PUT'],
                    strict_slashes=False)
@swag_from('swagger_yaml/active_ambulances/put_active_ambulance.yml')
def put_active_ambulance(active_ambulance_id=None):
    """ Updates an Active Ambulance """
    active_ambulance = storage.get(ActiveAmbulance, active_ambulance_id)
    if active_ambulance is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(active_ambulance, k, v)
    storage.save()
    return jsonify(active_ambulance.to_dict())

@app_views.route('/active_ambulances/<active_ambulance_id>', methods=['DELETE'],
                    strict_slashes=False)
@swag_from('swagger_yaml/active_ambulances/delete_active_ambulance.yml')
def delete_active_ambulance(active_ambulance_id=None):
    """ Deletes an Active Ambulance """
    active_ambulance = storage.get(ActiveAmbulance, active_ambulance_id)
    if active_ambulance is None:
        abort(404)
    storage.delete(active_ambulance)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/active_ambulances/<active_ambulance_id>/dispatch', methods=['PUT'],
                    strict_slashes=False)
@swag_from('swagger_yaml/active_ambulances/put_active_ambulance_dispatch.yml')
def put_active_ambulance_dispatch(active_ambulance_id=None):
    """ Updates the dispatch of an Active Ambulance """
    active_ambulance = storage.get(ActiveAmbulance, active_ambulance_id)
    if active_ambulance is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(active_ambulance, k, v)
    storage.save()
    return jsonify(active_ambulance.to_dict())

@app_views.route('/active_ambulances/<active_ambulance_id>/<ambulance_id>', methods=['GET'],
                    strict_slashes=False)
@swag_from('swagger_yaml/active_ambulances/get_active_ambulance_ambulance.yml')
def get_ambulance_active_ambulance(active_ambulance_id=None, ambulance_id=None):
    """ Retrieves a specific Active Ambulance """
    active_ambulance = storage.get(ActiveAmbulance, active_ambulance_id)
    if active_ambulance is None:
        abort(404)
    if ambulance_id not in [ambulance.id for ambulance in active_ambulance.ambulance_id]:
        abort(404)
    ambulance = storage.get(Ambulance, ambulance_id)
    if ambulance is None:
        abort(404)
    return jsonify(ambulance.to_dict())

@app_views.route('/active_ambulances/<active_ambulance_id>/alert', methods=['GET'],
                    strict_slashes=False)
@swag_from('swagger_yaml/active_ambulances/get_active_ambulance_alert.yml')
def get_alert_active_ambulance(active_ambulance_id=None):
    """ Retrieves Alert from a specific Active Ambulance """
    active_ambulance = storage.get(ActiveAmbulance, active_ambulance_id)
    if active_ambulance is None:
        abort(404)
    alert = storage.get(Alert, active_ambulance.alert_id)
    if alert is None:
        abort(404)
    return jsonify(alert.to_dict())

@app_views.route('/active_ambulances/<active_ambulance_id>/destination', methods=['GET'],
                    strict_slashes=False)
@swag_from('swagger_yaml/active_ambulances/get_active_ambulance_destination.yml')
def get_destination_active_ambulance(active_ambulance_id=None):
    """ Retrieves the destination of a specific Active Ambulance """
    active_ambulance = storage.get(ActiveAmbulance, active_ambulance_id)
    if active_ambulance is None:
        abort(404)
    destination = storage.get(Hospital, active_ambulance.destination)
    if destination is None:
        abort(404)
    return jsonify(destination.to_dict())

@app_views.route('/active_ambulances/<active_ambulance_id>/destination', methods=['PUT'],
                    strict_slashes=False)
@swag_from('swagger_yaml/active_ambulances/put_active_ambulance_destination.yml')
def put_destination_active_ambulance(active_ambulance_id=None):
    """ Updates the destination of a specific Active Ambulance """
    active_ambulance = storage.get(ActiveAmbulance, active_ambulance_id)
    if active_ambulance is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(active_ambulance, k, v)
    storage.save()
    return jsonify(active_ambulance.to_dict())