#!/usr/bin/python3
"""This module contains the view for City"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def cities_of_state(state_id):
    """Returns a json of all City objects in a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """Returns a City object based on its id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object based on its id"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """Creates a City object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, {"error": "Not a JSON"})
    if 'name' not in data:
        abort(400, {"error": "Missing name"})

    new_city = City(state_id=state_id, **data)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, {"error": "Not a JSON"})

    # Ignore keys: id, state_id, created_at, updated_at
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200
