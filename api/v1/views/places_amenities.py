#!/usr/bin/python3
""" configuration of routes for places_amenity_views blueprint """


from api.v1.views import places_amenity_views
from flask import abort, jsonify
from models.place import Place
from models.amenity import Amenity
from models import storage
from models import storage_t


@places_amenity_views.route('places/<place_id>/amenities',
                            strict_slashes=False)
def get_all_amenities_of_a_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    if not storage.get(Place, place_id):
        abort(404)
    place = storage.get(Place, place_id)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@places_amenity_views.route('places/<place_id>/amenities/<amenity_id>',
                            methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """ deletes an amenity """
    if not storage.get(Place, place_id) or not storage.get(Amenity,
                                                           amenity_id):
        abort(404)
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if storage_t != "db" and amenity_id not in place.amenity_ids:
        abort(404)
    amenity.delete()
    if storage_t != "db":
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({})


@places_amenity_views.route('places/<place_id>/amenities/<amenity_id>',
                            methods=['POST'], strict_slashes=False)
def create_an_amenity(place_id, amenity_id):
    """ creates an amenity and links it to a place """
    if not storage.get(Place, place_id) or not storage.get(Amenity,
                                                           amenity_id):
        abort(404)
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if storage_t != "db" and amenity_id in place.amenity_ids:
        return jsonify(
                    amenity.to_dict()
                ), 201
    dct = amenity.to_dict()
    if storage_t == "db":
        place.amenities.append(amenity)
    else:
        place.amenities = amenity
    place.save()
    return jsonify(
                dct
            ), 201
