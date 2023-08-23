#!/usr/bin/python3
"""This module defines initializes the server"""

from api.v1.views import app_views
from flask import Blueprint, Flask
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close():
    """Calls storage.close() when server stops"""
    storage.close()

if __name__ == "__main__":
    # not if not defined
    # not threaded
    app.run(host="0.0.0.0", port="5000")
