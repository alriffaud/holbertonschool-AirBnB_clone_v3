#!/usr/bin/python3
"""
Routes for handling User objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    Retrieves all User objects
    """
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """
    Retrieves a specific User object by ID
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create user route
    """
    user_data = request.get_json()
    if user_data is None:
        abort(400, 'Not a JSON')
    if "email" not in user_data or "password" not in user_data:
        abort(400, 'Missing email or password')

    new_user = User(**user_data)
    storage.new(new_user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_by_id(user_id):
    """
    Updates a specific User object by ID
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user_data = request.get_json()
    if user_data is None:
        abort(400, "Not a JSON")
    for key, value in user_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id):
    """
    Deletes User by ID
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
