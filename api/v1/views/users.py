#!/usr/bin/python3
"""Users module of the project Api Restfull Holberton"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


def get_user_by_id(user_id):
    """Get a user by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return user


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieve the list of all Users"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_obj_users(user_id):
    """Retrieves a User Object"""
    user = get_user_by_id(user_id)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_an_user(user_id):
    """Delete a User object"""
    user = get_user_by_id(user_id)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


def validate_and_create_user(data):
    """Validates and creates a new user"""
    if not data:
        abort(400, "Not a JSON")
    if 'password' not in data:
        abort(400, "Missing password")
    if 'email' not in data:
        abort(400, "Missing email")
    user = User(**data)
    storage.new(user)
    storage.save()
    return user


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_an_user():
    """Creates a User"""
    data = request.get_json()
    user = validate_and_create_user(data)
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_an_user(user_id):
    """Updates a User object"""
    user = get_user_by_id(user_id)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
