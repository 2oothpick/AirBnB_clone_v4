import os, sys
sys.path.append(os.getcwd())
from flask import jsonify, request, abort

from models import storage
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE', 'POST'], strict_slashes=False)
@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def place_amenities(place_id=None, amenity_id=None):
    if place_id is not None:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        if request.method == 'GET':
            return jsonify([amenity.to_dict() for amenity in place.amenities])
        if amenity_id is not None:
            amenity = storage.get(Amenity, amenity_id)
            if amenity is None:
                abort(404)
            if request.method == 'DELETE':
                if amenity not in place.amenities:
                    abort(404)
                place.amenities.remove(amenity)
                storage.save()
                return jsonify({}), 200
            
            if request.method == 'POST':
                if amenity in place.amenities:
                    return jsonify(amenity.to_dict()), 201
                else:
                    place.amenities.append(amenity)
                    storage.save()
                    return jsonify(amenity.to_dict()), 201

