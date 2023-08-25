#!/usr/bin/python3
"""This module contains the view for places_review"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/reviews", methods=["GET"])
def get_reviews():
    """Returns a JSON string"""
    rev_li = []
    reviews = storage.all(Review).values()
    for review in reviews:
        rev_li.append(review.to_dict())
    return jsonify(rev_li), 200


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def place_reviews(place_id):
    """Returns all the reviews for the given place_id"""
    
    revs_list = []
    
    if not storage.get(Place, place_id):
        abort(404)
    
    for rev in storage.all(Review).values():
        if rev.place_id == place_id:
            revs_list.append(rev.to_dict())
    
    return jsonify(revs_list), 200


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


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Creates a Review object"""

    krgs = request.get_json()
    if not storage.get("Place", place_id):
        abort(404)
    if not krgs:
        abort(400, {"Not a JSON"})
    if 'user_id' not in krgs:
        abort(400, {"Missing user_id"})
    if not storage.get("User", krgs["user_id"]):
        abort(404)
    if 'text' not in krgs:
        abort(400, {"Missing text"})

    krgs["place_id"] = place_id
    rev = Review(**krgs)
    storage.new(rev)
    storage.save()
    return jsonify(rev.to_dict()), 201


@app_views.route("/api/v1/reviews/<review_id>", methods=["PUT"])
def up_review(review_id):
    """Updates an existing review based in itrs id"""
    krgs = request.get_json()
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not krgs:
        abort(400, {"Not a JSON"})
    for key, value in krgs.items():
        if k == 'text':
            setattr(review, key, value)
            storage.save()

    return jsonify(review.to_dict()), 200
