#!/usr/bin/python3
"""
Routes for handling State objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """
    Retrieves all State objects
    """
    state = []
    for obj in storage.all(State).values():
        state.append(obj.to_dict())
    return jsonify(state), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Create state route
    """
    state_info = request.get_json()
    if not state_info:
        abort(400, {"Not a JSON"})
    if "name" not in state_info:
        abort(400, {"Missing name"})

    new_state_obj = State(**state_info)
    storage.new(new_state_obj)
    storage.save()
    return jsonify(new_state_obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    """
    Retrieves a specific State object by ID
    """
    d = storage.get(State, state_id)
    if d:
        return jsonify(d.to_dict()), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state_by_id(state_id):
    """
    Updates a specific State object by ID
    """
    state_info = storage.get(State, state_id)
    if not state_info:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key != "id":
            if key != "created_at":
                if key != "updated_at":
                    setattr(state_info, key, value)
                    storage.save()
    return jsonify(state_info.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """
    Deletes State by ID
    """
    for instance in storage.all(State).values():
        if instance.id == state_id:
            storage.delete(instance)
            storage.save()
            return jsonify({}), 200
    abort(404)
