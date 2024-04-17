#!/usr/bin/python3
"""
Routes for handling City objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """
    Retrieves all City objects of a State
    """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    dict = []
    for obj in states.cities:
        dict.append(obj.to_dict())
    return jsonify(dict)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Create city route
    """
    state_info = storage.get(State, state_id)
    if state_info is None:
        abort(400, 'Not a JSON')
    if "name" not in request.get_json():
        abort(400, 'Missing name')

    dict = request.get_json()
    new_city_obj = City(**dict)
    new_city_obj.state_id = state_info.id
    storage.new(new_city_obj)
    new_city_obj.save()
    return jsonify(new_city_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """
    Retrieves a specific City object by ID
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state_by_id(state_id):
    """
    Updates a specific City object by ID
    """
    city_info = storage.get(City, city_id)
    if not city_info:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key != "id":
            if key != "created_at":
                if key != "updated_at":
                    setattr(city_info, key, value)
                    storage.save()
    return jsonify(city_info.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(city_id):
    """
    Deletes City by ID
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)
