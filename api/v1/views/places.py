#!/usr/bin/python3
"""Defines routes for Place objects"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id',
                       'user_id',
                       'city_id',
                       'created_at',
                       'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_places():
    """
    Retrieves all Place objects depending on the
    JSON in the request body
    """
    if not request.json:
        abort(400, 'Not a JSON')

    states = request.json.get('states', [])
    cities = request.json.get('cities', [])
    amenities = request.json.get('amenities', [])

    if not states and not cities:
        places = storage.all(Place).values()
    else:
        places = []

        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city and city not in [place.city for place in places]:
                places.extend(city.places)

    if amenities:
        filtered_places = []
        for place in places:
            if all(amenity_id in place.amenity_ids() for amenity_id in amenities):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])
