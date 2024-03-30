#! /usr/bin/env python3
"""This is the contact api"""
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger import Swagger, swag_from
from models.company import Company
from models.contact import Contact
from models.utils.delete_data import delete_company, delete_company_address, delete_company_contact
from models.utils.post_data import post_company, post_contact
from models.utils.retrieve_data import get, get_company, get_company_address, get_company_contact, get_contact, get_contact_by

# GETs
ignore_keys = ['id', 'created_at', 'updated_at']

@app_views.route('/contact', methods=['GET'],
                    strict_slashes=False)
@app_views.route('/contact/<contact_id>', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/contact/contact.yml', methods=['GET'])
def contact(contact_id=None):
    """Get all contacts"""
    if contact_id:
        contact = get_contact(contact_id)
        return jsonify(contact)
    contacts = get_contact()
    return jsonify(contacts)

@app_views.route('/contact/address/<address_id>', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/contact/contact_address.yml', methods=['GET'])
def contact_address(address_id=None):
    """Get contact address"""
    contact = get_contact_by(address_id)
    return jsonify(contact)

# POSTs
@app_views.route('/contact', methods=['POST'], strict_slashes=False)
@swag_from('documentation/contact/create_contact.yml', methods=['POST'])
def create_contact():
    """Create a new contact
    Must have address_id
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    contact = post_contact(data)
    if not contact:
        return jsonify({"error": "contact not created"}), 400
    return jsonify(contact), 201