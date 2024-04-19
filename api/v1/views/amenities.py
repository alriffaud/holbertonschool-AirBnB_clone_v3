#!/usr/bin/python3
"""
Routes for handling Amenity objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """
    Retrieves all Amenity objects
    """
    amenities = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Retrieves a specific Amenity object by ID
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Create amenity route
    """
    amenity_data = request.get_json()
    if amenity_data is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_data:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_data)
    storage.new(new_amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity_by_id(amenity_id):
    """
    Updates a specific Amenity object by ID
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity_data = request.get_json()
    if amenity_data is None:
        abort(400, "Not a JSON")
    for key, value in amenity_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """
    Deletes Amenity by ID
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
