#!/usr/bin/python3
"""
Routes for handling Place objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places_by_city(city_id):
    """
    Retrieves all Place objects of a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = storage.all(Place).values()
    place_list = []
    for place in places:
        if place.city_id == city_id:
            place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """
    Retrieves a specific Place object by ID
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Create place route
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")
    if 'user_id' not in place_data:
        abort(400, "Missing user_id")
    if 'name' not in place_data:
        abort(400, "Missing name")
    user = storage.get(User, place_data['user_id'])
    if not user:
        abort(404)
    new_place = Place(**place_data, city_id=city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place_by_id(place_id):
    """
    Updates a specific Place object by ID
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place_data = request.get_json()
    if place_data is None:
        abort(400, "Not a JSON")
    for key, value in place_data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_by_id(place_id):
    """
    Deletes Place by ID
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200
