#!/usr/bin/python3
"""This module defines initializes the server"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(E):
    """Calls storage.close() when server stops"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST"),
        port=getenv("HBNB_API_PORT"),
        threaded=True)
