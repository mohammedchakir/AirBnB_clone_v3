#!/usr/bin/python3
"""
Defines routes for API v1 status endpoint
"""
from flask import Flask
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', strict_slashes=False, methods=['GET'])
def get_status():
    """Returns status in JSON format"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """Returns the number of each object by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
