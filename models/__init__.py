#!/usr/bin/python3
"""
initialize the models package
"""


from os import getenv


def get_classes():
    """ returns a dict of all classes """
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.user import User
    from models.state import State
    from models.review import Review

    class_dict = {
            "Amenity": Amenity,
            "City": City,
            "Place": Place,
            "User": User,
            "State": State,
            "Review": Review
            }
    return class_dict


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
