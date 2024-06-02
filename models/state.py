#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', back_populates='state', cascade='delete')
    else:
        name = ""

        @property
        def cities(self):
            """
            Getter method that returns the list of City instances
            with state_id equals to the State.id
            (returns the cities of a particular state)
            """
            from models.city import City
            from models import storage
            c_objs = storage.all(City).values()
            state_city = [c for c in c_objs if c.state_id == self.id]
            return state_city

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
