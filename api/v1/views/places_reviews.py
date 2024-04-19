#!/usr/bin/python3
"""
Routes for handling Review objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_all_reviews_by_place(place_id):
    """
    Retrieves all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = storage.all(Review).values()
    review_list = []
    for review in reviews:
        if review.place_id == place_id:
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """
    Retrieves a specific Review object by ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Create review route
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_data = request.get_json()
    if not review_data:
        abort(400, "Not a JSON")
    if 'user_id' not in review_data:
        abort(400, "Missing user_id")
    if 'text' not in review_data:
        abort(400, "Missing text")
    user = storage.get(User, review_data['user_id'])
    if not user:
        abort(404)
    new_review = Review(**review_data, place_id=place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review_by_id(review_id):
    """
    Updates a specific Review object by ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review_data = request.get_json()
    if review_data is None:
        abort(400, "Not a JSON")
    for key, value in review_data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review_by_id(review_id):
    """
    Deletes Review by ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200
