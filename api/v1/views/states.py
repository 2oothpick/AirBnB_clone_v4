import os, sys
sys.path.append(os.getcwd())
from flask import jsonify, request, abort

from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def states(state_id=None):
    if state_id is not None:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(state.to_dict())
        if request.method == 'DELETE':
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
        if request.method == "PUT":
            if not request.is_json:
                abort(400, description="Not a JSON")
            data = request.get_json()
            ignore = ['id', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore:
                    setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict()), 200

    if request.method == 'POST':
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.get_json():
            abort(400, description="Missing name")
        data = request.get_json()
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


    if state_id is None and request.method == 'GET':
        states = storage.all(State)
        states_list = [value.to_dict() for value in states.values()]
        return jsonify(states_list)
