import os, sys
sys.path.append(os.getcwd())
from flask import jsonify, request, abort

from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenities(amenity_id=None):
    if amenity_id is not None:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(amenity.to_dict())
        if request.method == 'DELETE':
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
        if request.method == "PUT":
            if not request.is_json:
                abort(400, description="Not a JSON")
            data = request.get_json()
            ignore = ['id', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore:
                    setattr(amenity, key, value)
            amenity.save()
            return jsonify(amenity.to_dict()), 200

    if request.method == 'POST':
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.get_json():
            abort(400, description="Missing name")
        data = request.get_json()
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201
        

    if amenity_id is None and request.method == 'GET':
        amenities = storage.all(Amenity)
        amenities_list = [value.to_dict() for value in amenities.values()]
        return jsonify(amenities_list)
