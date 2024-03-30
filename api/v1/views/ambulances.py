#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Ambulances """
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models.ambulance import Ambulance
from models.location import Site
from models.system_user import AmbulanceStaff

ignore_keys = ['id', 'created_at', 'updated_at']

@app_views.route('/ambulances', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/ambulances/get_ambulances.yml')
def get_ambulances():
    """ Retrieves the list of all Ambulances """
    ambulances = storage.all(Ambulance)
    return jsonify([ambulance.to_dict() for ambulance in ambulances.values()])

@app_views.route('/ambulances/<ambulance_id>', methods=['GET'],
                    strict_slashes=False)
@swag_from('swagger_yaml/ambulances/get_ambulance.yml')
def get_ambulance(ambulance_id=None):
    """ Retrieves a specific Ambulance """
    ambulance = storage.get(Ambulance, ambulance_id)
    if ambulance is None:
        abort(404)
    return jsonify(ambulance.to_dict())

@app_views.route('/ambulances', methods=['POST'], strict_slashes=False)
@swag_from('swagger_yaml/ambulances/post_ambulances.yml')
def post_ambulance():
    """ Creates an Ambulance """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'site_id' not in data:
        abort(400, 'Missing site_id')
    if 'company_id' not in data:
        abort(400, 'Missing company_id')
    for k, v in Ambulance.fields_errMSG.items():
        if k not in data:
            abort(400, v)
    site = storage.get(Site, data['site_id'])
    if site is None:
        abort(404)
    data['site_id'] = site.id
    ambulance = Ambulance(**data)
    storage.new(ambulance)
    storage.save()
    return make_response(jsonify(ambulance.to_dict()), 201)

@app_views.route('/ambulances/<ambulance_id>', methods=['PUT'],
                    strict_slashes=False)
@swag_from('swagger_yaml/ambulances/put_ambulance.yml')
def put_ambulance(ambulance_id=None):
    """ Updates an Ambulance """
    ambulance = storage.get(Ambulance, ambulance_id)
    if ambulance is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(ambulance, k, v)
    storage.save()
    return jsonify(ambulance.to_dict())

@app_views.route('/ambulances/<ambulance_id>', methods=['DELETE'],
                    strict_slashes=False)
@swag_from('swagger_yaml/ambulances/delete_ambulance.yml')
def delete_ambulance(ambulance_id=None):
    """ Deletes an Ambulance """
    ambulance = storage.get(Ambulance, ambulance_id)
    if ambulance is None:
        abort(404)
    storage.delete(ambulance)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/ambulances/<ambulance_id>/staff', methods=['GET'],
                    strict_slashes=False)
@swag_from('swagger_yaml/ambulances/get_ambulance_staff.yml')
def get_ambulance_staff(ambulance_id=None):
    """ Retrieves the list of all Ambulance Staff """
    ambulance = storage.get(Ambulance, ambulance_id)
    if ambulance is None:
        abort(404)
    return jsonify([staff.to_dict() for staff in ambulance.staff])

@app_views.route('/ambulances/<ambulance_id>/staff/<staff_id>',
                    methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/ambulances/get_ambulance_staff_id.yml')
def get_ambulance_staff_id(ambulance_id=None, staff_id=None):
    """ Retrieves a specific Ambulance Staff """
    ambulance = storage.get(Ambulance, ambulance_id)
    if ambulance is None:
        abort(404)
    staff = storage.get(AmbulanceStaff, staff_id)
    if staff is None:
        abort(404)
    return jsonify(staff.to_dict())

@app_views.route('/ambulances/<ambulance_id>/staff', methods=['POST'],
                    strict_slashes=False)
@swag_from('swagger_yaml/ambulances/post_ambulance_staff.yml')
def post_ambulance_staff(ambulance_id=None):
    """ Creates an Ambulance Staff """
    ambulance = storage.get(Ambulance, ambulance_id)
    if ambulance is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in AmbulanceStaff.fields_errMSG.items():
        if k not in data:
            abort(400, v)
    data['ambulance_id'] = ambulance.id
    staff = AmbulanceStaff(**data)
    storage.new(staff)
    storage.save()
    return make_response(jsonify(staff.to_dict()), 201)

@app_views.route('/ambulances/<ambulance_id>/staff/<staff_id>',
                    methods=['PUT'], strict_slashes=False)
@swag_from('swagger_yaml/ambulances/put_ambulance_staff.yml')
def put_ambulance_staff(ambulance_id=None, staff_id=None):
    """ Updates an Ambulance Staff """
    ambulance = storage.get(Ambulance, ambulance_id)
    if ambulance is None:
        abort(404)
    staff = storage.get(AmbulanceStaff, staff_id)
    if staff is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(staff, k, v)
    storage.save()
    return jsonify(staff.to_dict())

@app_views.route('/ambulances/<ambulance_id>/staff/<staff_id>',
                    methods=['DELETE'], strict_slashes=False)
@swag_from('swagger_yaml/ambulances/delete_ambulance_staff.yml')
def delete_ambulance_staff(ambulance_id=None, staff_id=None):
    """ Deletes an Ambulance Staff """
    ambulance = storage.get(Ambulance, ambulance_id)
    if ambulance is None:
        abort(404)
    staff = storage.get(AmbulanceStaff, staff_id)
    if staff is None:
        abort(404)
    
    if staff not in ambulance.staff:
        abort(404)
    storage.delete(staff)
    storage.save()
    return make_response(jsonify({}), 200)