#!/usr/bin/python3
"""Main application file for API v1"""

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)