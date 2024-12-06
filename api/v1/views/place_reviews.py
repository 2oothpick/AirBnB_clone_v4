import os, sys
sys.path.append(os.getcwd())
from flask import jsonify, request, abort

from models import storage
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def reviews(review_id=None):
    if review_id is not None:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(review.to_dict())
        if request.method == 'DELETE':
            storage.delete(review)
            storage.save()
            return jsonify({}), 200
        if request.method == "PUT":
            if not request.is_json:
                abort(400, description="Not a JSON")
            data = request.get_json()
            ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict()), 200

    if review_id is None and request.method == 'GET':
        reviews = storage.all(Review)
        reviews_list = [value.to_dict() for value in reviews.values()]
        return jsonify(reviews_list)


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'], strict_slashes=False)
def place_reviews(place_id):
    if place_id is not None:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        if request.method == 'GET':
            return jsonify([reviews.to_dict() for reviews in place.reviews])
        
        if request.method == 'POST':
            if not request.is_json:
                abort(400, description="Not a JSON")
            if 'text' not in request.get_json():
                abort(400, description="Missing text")

            if 'user_id' not in request.get_json():
                abort(400, description="Missing user_id")

            data = request.get_json()
            user_id = storage.get(User, data['user_id'])
            if user_id is None:
                abort(404)

            data['place_id'] = place_id
            new_review = Review(**data)
            new_review.save()
            return jsonify(new_review.to_dict()), 201
