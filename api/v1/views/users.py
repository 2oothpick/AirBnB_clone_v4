import os, sys
sys.path.append(os.getcwd())
from flask import jsonify, request, abort

from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def users(user_id=None):
    if user_id is not None:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(user.to_dict())
        if request.method == 'DELETE':
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
        if request.method == "PUT":
            if not request.is_json:
                abort(400, description="Not a JSON")
            data = request.get_json()
            ignore = ['id', 'email', 'created_at', 'updated_at']
            for key, value in data.items():
                if key not in ignore:
                    setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict()), 200

    if request.method == 'POST':
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'email' not in request.get_json():
            abort(400, description="Missing email")
        if 'password' not in request.get_json():
            abort(400, description="Missing password")
        data = request.get_json()
        new_state = User(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


    if user_id is None and request.method == 'GET':
        users = storage.all(User)
        states_list = [value.to_dict() for value in users.values()]
        return jsonify(states_list)
