#!/usr/bin/python3
""" index module """


from api.v1.views import place_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.user import User


@place_views.route('places', strict_slashes=False)
def get_places():
    """ returns a list of all the places in db """
    places = storage.all(Place)
    lst = [place.to_dict() for place in places.values()]
    return jsonify(lst)


@place_views.route('places/<place_id>', strict_slashes=False)
def get_place_with_id_eq_place_id(place_id):
    """ returns a place with id == place_id """
    place = storage.get(Place, place_id)
    return jsonify(place.to_dict()) if place else abort(404)


@place_views.route('places/<place_id>', strict_slashes=False,
                   methods=["DELETE"])
def delete_place_with_id_eq_place_id(place_id):
    """ deletes a place with id == place_id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@place_views.route('places', strict_slashes=False,
                   methods=["POST"])
def create_place():
    """ creates a new place """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400
    abort(405)
    name = data.get("name")
    if not name:
        return jsonify({
            "error": "Missing name"
            }), 400
    place = Place(name=name)
    place.save()
    return jsonify(
        place.to_dict()
        ), 201


@place_views.route('places/<place_id>', strict_slashes=False,
                   methods=["PUT"])
def update_place_with_id_eq_place_id(place_id):
    """ updates a place's record """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400

    place_dict = place.to_dict()
    dont_update = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for skip in dont_update:
        try:
            data[skip] = place_dict[skip]
        except Exception:
            pass
    place_dict.update(data)
    place.delete()
    storage.save()
    updated_place = Place(**place_dict)
    updated_place.save()
    return jsonify(
            updated_place.to_dict()
            )


@place_views.route('cities/<city_id>/places', strict_slashes=False)
def get_places_of_city(city_id):
    """ returns list of places associated with city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(
                [place.to_dict() for place in city.places]
            )


@place_views.route('cities/<city_id>/places', strict_slashes=False,
                   methods=["POST"])
def create_linked_to_city_place(city_id):
    """ returns list of places associated with city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
                "error": "Not a JSON"
            }), 400
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({
                "error": "Missing user_id"
            }), 400

    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not data.get("name"):
        return jsonify({
                "error": "Missing name"
            }), 400

    place = Place(**data)
    dct = place.to_dict()
    city.places.append(place)
    # place.city_id = city.id
    place.save()
    city.save()
    return(
        jsonify(dct)
        ), 201


@place_views.route('places_search', strict_slashes=False,
                   methods=["POST"])
def search_for_place():
    """ retrieves all places that match search criteria """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400
    state_ids = data.get("states")
    city_ids = data.get("cities")
    amenity_ids = data.get("amenities")
    places = storage.all(Place)
    places = [place for place in places.values()]
    if not state_ids and not city_ids and not amenity_ids:
        res = [place.to_dict() for place in places]
        return jsonify(res)

    res = []

    if state_ids:
        for id_ in state_ids:
            state = storage.get(State, id_)
            if state:
                for city in state.cities:
                    for p in city.places:
                        dct = p.to_dict()
                        if dct not in res:
                            res.append(dct)

    if city_ids:
        for id_ in city_ids:
            city = storage.get(City, id_)
            if city:
                for p in city.places:
                    dct = p.to_dict()
                    if dct not in res:
                        res.append(dct)
    if amenity_ids:
        size = len(amenity_ids)
        for p in places:
            dct = p.to_dict()
            count = 0
            p_amenities = p.amenities
            for amenity in p_amenities:
                if amenity.id in amenity_ids:
                    count += 1
            if count == size and dct not in res:
                res.append(dct)
            elif dct in res and count != size:
                res.remove(dct)

    return jsonify(res)
