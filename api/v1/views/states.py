#!/usr/bin/python3
"""Module for handling State objects through RESTful API"""

from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False,
                 methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["GET"])
def states(state_id=None):
    """show states with id <state_id>"""
    states_list = []
    if state_id is None:
        all_objs = storage.all(State).values()
        for v in all_objs:
            states_list.append(v.to_dict())
        return jsonify(states_list)
    else:
        result = storage.get(State, state_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def states_delete(state_id):
    """Deletes a State object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False,
                 methods=["POST"])
def create_state():
    """Creates a State"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["PUT"])
def update_state(state_id):
    """Updates a State object""""""update state"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
