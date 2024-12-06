from flask import Flask, jsonify
from flask_cors import CORS
import sys, os
sys.path.append(os.getcwd())

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.route('/hello')
def hello():
    return jsonify({"status": "not okay"})


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not found"
    }), 404

@app.teardown_appcontext
def close_db(exc):
    """closes the current session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True, threaded=True)

