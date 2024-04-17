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
    states = storage.all("State")
    for instance in state.values():
        states.append(instance.to_json())

    return jsonify(states)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Create state route
    """
    state_info = request.get_json(silent=True)
    if state_info is None:
        abort(400, 'Not a JSON')
    if "name" not in state_info:
        abort(400, 'Missing name')

    new_state_obj = State(**state_info)
    new_state_obj.save()
    response_obj = jsonify(new_state_obj.to_json())
    response_obj.status_code = 201

    return response_obj


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    """
    Retrieves a specific State object by ID
    """

    obj = storage.get("State", str(state_id))

    if obj is None:
        abort(404)

    return jsonify(obj.to_json())


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state_by_id(state_id):
    """
    Updates a specific State object by ID
    """
    state_info = request.get_json(silent=True)
    if state_info is None:
        abort(400, 'Not a JSON')
    obj = storage.get("State", str(state_id))
    if obj is None:
        abort(404)
    for key, val in state_info.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, val)
    obj.save()
    return jsonify(obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """
    Deletes State by ID
    """

    obj = storage.get("State", str(state_id))

    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return jsonify({})
