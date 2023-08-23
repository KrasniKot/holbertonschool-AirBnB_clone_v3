#!/usr/bin/python3
"""This module contains the routes for app_views"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Returns a JSON string"""
    return jsonify({"status": "OK"})
