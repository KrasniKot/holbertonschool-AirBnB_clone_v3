#!/usr/bin/python3
"""This module contains the routes for app_views"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """Returns a JSON string"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    """Returns the number of objects of each type"""
    sta = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
          }
    return jsonify(sta)
