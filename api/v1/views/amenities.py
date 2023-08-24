#!/usr/bin/python3
"""This module contains the view for Amenity"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=["GET"])
def all_amenities():
    """Returns a json of all Amenity objects"""
    amenity_list = []
    amenities = storage.all(Amenity).values()

    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """Returns an Amenity object based on its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes an Amenity object based on its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """Creates an Amenity object"""
    data = request.get_json()

    if not data:
        abort(400, {"error": "Not a JSON"})
    if 'name' not in data:
        abort(400, {"error": "Missing name"})

    new_amenity = Amenity(**data)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, {"error": "Not a JSON"})

    # Ignore keys: id, created_at, updated_at
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    amenity.save()

    return jsonify(amenity.to_dict()), 200
