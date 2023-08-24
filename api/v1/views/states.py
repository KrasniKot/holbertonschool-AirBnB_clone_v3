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
def a_state(state_id):
    """Returns a State object based on its id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def del_a_state(state_id):
    """Deletes a State object based on its id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", methods=["POST"])
def make_a_state():
    """Creates a State object"""
    krgs = request.get_json()

    if not krgs:
        abort(400, {"Not a JSON"})
    if 'name' not in krgs:
        abort(400, {"Missing name"})

    state = State(**krgs)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route("states/<state_id>", methods=["PUT"])
def up_a_state(state_id):
    """Updates a State object"""
    obj = storage.get(State, state_id)
    krgs = request.get_json()

    if not obj:
        abort(400, {"Not a JSON"})

    for key, value in krgs.items():
        setattr(obj, key, value)
    obj.save()

    return jsonify(obj.to_dict()), 200
