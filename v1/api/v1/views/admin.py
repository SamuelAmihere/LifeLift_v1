#! /usr/bin/env python3
"""This is the api endpoints for the admin templates 
"""

from flask_login import login_required
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger import Swagger, swag_from
from models.user import User
from models.utils.delete_data import delete_user
from models.utils.post_data import post_user
from models.utils.retrieve_data import get_user, get_user_by_email
from models.utils.update_data import modify_user
from flask import render_template, redirect, url_for


def admin_user(user_id=None):
    """Get templates for the admin user page
    depending on the user_id (used to get a specific user and
    give page based on the user type) or not (used to get all users
    """
    if user_id:
        user = get_user(user_id)
        return render_template('admin/user.html', user=user)
    users = get_user()
    return render_template('admin/users.html', users=users)

@app_views.route('/home/admin/<string:user_id>', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/admin/admin_home.yml', methods=['GET'])
@login_required
def admin_home(user_id=None):
    """This is the admin home"""
    if not user_id:
        return render_template('admin/home.html')
    return admin_user(user_id)

@app_views.route('/admin/user', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/admin/admin_user.yml', methods=['GET'])
def admin_user_all():
    """Get all users"""
    return admin_user()

@app_views.route('/home/admin/user/<string:user_id>', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/admin/admin_user.yml', methods=['GET'])
def admin_user(user_id=None):
    """Get all users"""
    if user_id:
        user = get_user(user_id)
        return jsonify(user)
    users = get_user()
    return jsonify(users)

@app_views.route('/home/admin/user/email/<string:email>', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/admin/admin_user_email.yml', methods=['GET'])
def admin_user_email(email=None):
    """Get user by email"""
    if not email:
        return jsonify({"error": "email is missing"})
    user = get_user_by_email(email)
    return jsonify(user)

# POSTs
@app_views.route('/home/admin/user', methods=['POST'], strict_slashes=False)
@swag_from('documentation/admin/admin_create_user.yml', methods=['POST'])
def admin_create_user():
    """Create a new user
    Must have email, password, first_name, last_name
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    user = post_user(data)
    if not user:
        return jsonify({"error": "user not created"}), 400
    return jsonify(user), 201

# PUTs
@app_views.route('/home/admin/user/<string:user_id>', methods=['PUT'],
                  strict_slashes=False)
@swag_from('documentation/admin/admin_update_user.yml', methods=['PUT'])
def admin_update_user(user_id):
    """Modify a user"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    user = modify_user(user_id, data)
    if not user:
        return jsonify({"error": "user not modified"}), 400
    return jsonify(user), 200

# DELETEs
@app_views.route('/home/admin/user/<string:user_id>', methods=['DELETE'],
                  strict_slashes=False)
@swag_from('documentation/admin/admin_remove_user.yml', methods=['DELETE'])
def admin_remove_user(user_id):
    """Delete a user"""
    user = delete_user(user_id)
    if not user:
        return jsonify({"error": "user not deleted"}), 400
    return jsonify(user), 200