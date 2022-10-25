#!/usr/bin/python3
""" index module """


from api.v1.views import city_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@city_views.route('cities', strict_slashes=False)
def get_cities():
    """ returns a list of all the cities in db """
    cities = storage.all(City)
    lst = [city.to_dict() for city in cities.values()]
    return jsonify(lst)


@city_views.route('cities/<city_id>', strict_slashes=False)
def get_city_with_id_eq_city_id(city_id):
    """ returns a city with id == city_id """
    city = storage.get(City, city_id)
    return jsonify(city.to_dict()) if city else abort(404)


@city_views.route('cities/<city_id>', strict_slashes=False,
                  methods=["DELETE"])
def delete_city_with_id_eq_city_id(city_id):
    """ deletes a city with id == city_id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@city_views.route('cities', strict_slashes=False,
                  methods=["POST"])
def create_city():
    """ creates a new city """
    abort(404)
    try:
        data = request.get_json()
        if type(data) is not dict:
            raise TypeError
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400
    name = data.get("name")
    if not name:
        return jsonify({
            "error": "Missing name"
            }), 400
    city = City(name=name)
    city.save()
    return jsonify(
        city.to_dict()
        ), 201


@city_views.route('cities/<city_id>', strict_slashes=False,
                  methods=["PUT"])
def update_city_with_id_eq_city_id(city_id):
    """ updates a city's record """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
        if type(data) is not dict:
            raise TypeError
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400

    city_dict = city.to_dict()
    dont_update = ["id", "created_at", "updated_at"]
    for skip in dont_update:
        if data.get(skip):
            del data[skip]

    for item in data:
        setattr(city, item, data[item])
    city.save()
    dct = city.to_dict()
    return jsonify(dct)


@city_views.route('states/<state_id>/cities', strict_slashes=False)
def get_cities_of_state(state_id):
    """ returns list of cities associated with state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    ls = [city.to_dict() for city in state.cities]
    return jsonify(ls)


@city_views.route('states/<state_id>/cities', strict_slashes=False,
                  methods=["POST"])
def create_linked_to_state_city(state_id):
    """ returns list of cities associated with state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        data = request.get_json()
        if type(data) is not dict:
            raise TypeError
    except Exception:
        return jsonify({
                "error": "Not a JSON"
            }), 400
    name = data.get("name")
    if not name:
        return jsonify({
                "error": "Missing name"
            }), 400

    city = City(**data)
    # state.cities.append(city)
    city.state_id = state.id
    city.save()
    state.save()
    dct = city.to_dict()
    return(
        jsonify(dct)
        ), 201
