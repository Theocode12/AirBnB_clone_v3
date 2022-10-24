#!/usr/bin/python
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of city """
    if models.storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60),
                          ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities")
        __table_args__ = (
                {'mysql_default_charset': 'latin1'}
                )

    else:
        state_id = ""
        name = ""

        @property
        def places(self):
            """ gets places associated with city """
            from models.place import Place
            places = models.storage.all(Place)
            ls = []
            for obj in places.values():
                if obj.city_id == self.id:
                    ls.append(obj)
            return ls

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
