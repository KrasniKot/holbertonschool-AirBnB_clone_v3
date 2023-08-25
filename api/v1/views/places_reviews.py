#!/usr/bin/python3
"""This module contains the view for places_review"""

from api.v1.views import app_views
from flask import abort
from models import storage
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def place_reviews(place_id):
    """Returns all the reviews for the given place_id"""

    revs_list = []

    if not storage.get(Place, place_id):
        abort(404)

    for rev in storage.all(Review).values():
        if rev.place_id == place_id:
            revs_list.append(rev.to_dict())

    return jsonify(revs_list)

@app_views.route("/api/v1/reviews/<review_id>", methods=["GET"])
def review(review_id):
    """Returns a review based on its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route("/api/v1/reviews/<review_id>", methods=["DELETE"])
def del_review(review_id):
    """Deletes a review based on its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200
