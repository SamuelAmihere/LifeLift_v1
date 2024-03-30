#! /usr/bin/env python3
"""This is the user api"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger import Swagger, swag_from
from models.utils.delete_data import delete_user
from models.utils.post_data import post_user
from models.utils.retrieve_data import get_user, get_user_by_email
from models.utils.update_data import modify_user

ignore_keys = ['id', 'created_at', 'updated_at']

# GETs
@app_views.route('/user', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/user/<string:user_id>', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/user/user.yml', methods=['GET'])
def user(user_id=None):
    """Get all users"""
    if user_id:
        user = get_user(user_id)
        return jsonify(user)
    users = get_user()
    return jsonify(users)

@app_views.route('/user/email/<string:email>', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/user/user_email.yml', methods=['GET'])
def user_email(email=None):
    """Get user by email"""
    if not email:
        return jsonify({"error": "email is missing"})
    user = get_user_by_email(email)
    return jsonify(user)

# POSTs
@app_views.route('/user', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/create_user.yml', methods=['POST'])
def create_user():
    """Create a new user
    Must have email, password, first_name, last_name
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    user = post_user(data)
    if 'error' in user:
        return jsonify(user), 400
    return jsonify(user), 201

# PUTs
@app_views.route('/user/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/user/update_user.yml', methods=['PUT'])
def update_user(user_id):
    """Modify a user"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    user = modify_user(user_id, data)
    if not user:
        return jsonify({"error": "user not modified"}), 400
    return jsonify(user), 200

# DELETEs
@app_views.route('/user/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/remove_user.yml', methods=['DELETE'])
def remove_user(user_id=None):
    """Delete a user"""
    user = delete_user(user_id)
    if not user:
        return jsonify({"error": "user not deleted"}), 400
    return jsonify({}), 200


# ----------------- Staff -----------------
# GETs
@app_views.route('/staff', methods=['GET'])
@app_views.route('/staff/<string:staff_id>', methods=['GET'])
@swag_from('documentation/staff/get_staff.yml', methods=['GET'])
def get_staff(staff_id=None):
    """Get all staff"""
    staff = get_user(staff_id)
    return jsonify(staff)

# POST
@app_views.route('/staff', methods=['POST'])
@swag_from('documentation/staff/post_staff.yml', methods=['POST'])
def post_staff():
    """Create a new staff"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400
    staff = post_user(data)
    return jsonify(staff)

# DELETE
@app_views.route('/staff/<string:staff_id>', methods=['DELETE'])
@swag_from('documentation/staff/delete_staff.yml', methods=['DELETE'])
def delete_staff(staff_id):
    """Delete a staff"""
    staff = delete_user(staff_id)
    return jsonify(staff)

# PUT
@app_views.route('/staff/<string:staff_id>', methods=['PUT'])
@swag_from('documentation/staff/update_staff.yml', methods=['PUT'])
def update_staff(staff_id):
    """Update a staff"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    staff = modify_user(data, staff_id)
    return jsonify(staff)