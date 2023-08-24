#!/usr/bin/python3
"""
    This module contains the view for User
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models import storage


@app_views.route("/users", methods=["GET"])
def all_users():
    """Returns a json of all User objects"""
    user_list = []
    users = storage.all(User).values()

    for user in users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Returns a User object based on its id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deletes a User object based on its id"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", methods=["POST"])
def create_user():
    """Creates a User object"""
    data = request.get_json()

    if not data:
        abort(400, {"error": "Not a JSON"})
    if 'email' not in data:
        abort(400, {"error": "Missing email"})
    if 'password' not in data:
        abort(400, {"error": "Missing password"})

    new_user = User(**data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, {"error": "Not a JSON"})

    # Ignores keys: id, email, createf_at, updated_at
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    user.save()

    return jsonify(user.to_dict()), 200
