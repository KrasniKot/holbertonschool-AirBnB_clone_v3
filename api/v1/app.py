#!/usr/bin/python3
"""This module defines initializes the server"""

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(E):
    """Calls storage.close() when server stops"""
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST"),
        port=getenv("HBNB_API_PORT"),
        threaded=True)
