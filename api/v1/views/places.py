#!/usr/bin/python3
"""
    This module contains the view for Place
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def places_of_city(city_id):
    """Returns a json of all Place objects in a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """Returns a Place object based on its id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a Place object based on its id"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Creates a Place object"""
    city = storate.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, {"error": "Not a JSON"})
    if 'user_id' not in data:
        abort(400, {"error": "Missing user_id"})
    if 'name' not in data:
        abort(400, {"error": "Missing name"})

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    new_place = Place(city_id=city_id, **data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, {"error": "Not a JSON"})
    
    # Ignore keys: id, user_id, city_id, created_at, updated_at
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()
    
    return jsonify(place.to_dict()), 200
    
