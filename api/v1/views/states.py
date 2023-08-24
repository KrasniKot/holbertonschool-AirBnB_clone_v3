#!/usr/bin/python3
"""This module contains the view for State"""

from api.v1.views import app_views
from flask import abort, jsonify
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"])
def all_states():
    """Returns a json of all of all State objects"""
    state_list = []
    states = storage.all(State).values()

    for state in states:
        state_list.append(state.to_dict())
    return jsonify(state_list), 202


@app_views.route("/states/<state_id>", methods=["GET"])
def a_state(state_id):
    """Returns a State object based on its id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)
