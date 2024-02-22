#!/usr/bin/python3
"""
Defines routes for API v1 status endpoint
"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def get_status():
    """
    Returns status in JSON format
    """
    return jsonify({"status": "OK"})
