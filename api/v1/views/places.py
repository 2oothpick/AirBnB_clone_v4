import os, sys
sys.path.append(os.getcwd())
from flask import jsonify, request, abort

from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def places(place_id=None):
    if place_id is not None:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(place.to_dict())
        if request.method == 'DELETE':
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
        if request.method == "PUT":
            if not request.is_json:
                abort(400, description="Not a JSON")
            data = request.get_json()
            ignore = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
            for key, value in data.items():
                if key not in ignore:
                    setattr(place, key, value)
            place.save()
            return jsonify(place.to_dict()), 200

    """ place search """
    if place_id is None and request.method == 'POST':
        if not request.is_json:
            abort(400, description="Not a JSON")
        data:dict = request.get_json()
        if len(data) > 0:
            if len(data.get('states', [])) > 0:
                state_ids = data['states']
                state_obj_list = [storage.get(State, state_id) for state_id in state_ids]
                #print([state.name for state in state_obj_list])
            else:
                state_obj_list = [] #list(storage.all(State).values())
            state_places = [places for states in state_obj_list for cities in states.cities for places in cities.places]
            if len(data.get('cities', [])) > 0:
                city_ids = data['cities']
                city_obj_list = [storage.get(City, city_id) for city_id in city_ids]
                
            else:
                city_obj_list = [] #list(storage.all(City).values())
                print('hello2')
            city_places = [places for cities in city_obj_list for places in cities.places]
            all_places = []
            all_places.extend((state_places))
            all_places.extend((city_places))
        else:
            all_places = list(storage.all(Place).values())
            return jsonify([place.to_dict() for place in all_places ])
        all_places = list(set(all_places))
        if len(data.get('amenities', [])) > 0:
            amenity_ids = data['amenities']
            amenities_obj_list = [storage.get(Amenity, amenity) for amenity in amenity_ids]
        else:
            amenities_obj_list = [] #list(storage.all(Amenity).values())
        filtered_places = []
        for places in all_places:
            if all([amenity in places.amenities for amenity in amenities_obj_list]):
                filtered_places.append(places)
        return_places = []
        for places in filtered_places:
            places = places.to_dict()
            del places['amenities']
            return_places.append(places)
        return jsonify(return_places)

@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def city_places(city_id=None):
    if city_id is not None:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if request.method == 'GET':
            return jsonify([places.to_dict() for places in city.places])

        if request.method == 'POST':
            if not request.is_json:
                abort(400, description="Not a JSON")
            if 'name' not in request.get_json():
                abort(400, description="Missing name")
            if 'number_rooms' not in request.get_json():
                abort(400, description="Missing number_rooms")
            if 'number_bathrooms' not in request.get_json():
                abort(400, description="Missing number_bathrooms")
            if 'max_guest' not in request.get_json():
                abort(400, description="Missing max_guest")
            if 'price_by_night' not in request.get_json():
                abort(400, description="Missing price_by_night")
            if 'user_id' not in request.get_json():
                abort(400, description="Missing user_id")
            data = request.get_json()
            user_id = storage.get(User, data['user_id'])
            if user_id is None:
                abort(404)
            data['city_id'] = city_id
            new_place = Place(**data)
            new_place.save()
            return jsonify(new_place.to_dict()), 201
