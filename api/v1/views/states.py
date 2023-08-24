#!/usr/bin/python3
"""This module contains the view for State"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"])
def all_states():
    """Returns a json of all of all State objects"""
    state_list = []
    states = storage.all(State).values()

    for state in states:
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Returns a State object based on its id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a State object based on its id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", methods=["POST"])
def create_state():
    """Creates a State object"""
    data = request.get_json()

    if not data:
        abort(400, {"error": "Not a JSON"})
    if 'name' not in data:
        abort(400, {"error": "Missing name"})

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, {"error": "Not a JSON"})

    # Ignore keys: id, created_at, updated_at
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state, key, value)
    state.save()

    return jsonify(state.to_dict()), 200
