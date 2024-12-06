import os, sys
sys.path.append(os.getcwd())
from flask import jsonify, request, abort

from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City

@app_views.route('/cities', methods=['GET'], strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def cities(city_id=None):
    if city_id is not None:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(city.to_dict())
        if request.method == 'DELETE':
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
        if request.method == "PUT":
            if not request.is_json:
                abort(400, description="Not a JSON")
            data = request.get_json()
            ignore = ['id', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore:
                    setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200

    if city_id is None and request.method == 'GET':
        cities = storage.all(City)
        cities_list = [value.to_dict() for value in cities.values()]
        return jsonify(cities_list)

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def state_cities(state_id=None):
    if state_id is not None:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        if request.method == 'GET':
            return jsonify([cities.to_dict() for cities in state.cities])
        if request.method == 'POST':
            if not request.is_json:
                abort(400, description="Not a JSON")
            if 'name' not in request.get_json():
                abort(400, description="Missing name")
            data = request.get_json()
            data['state_id'] = state_id
            new_city = City(**data)
            new_city.save()
            return jsonify(new_city.to_dict()), 201
