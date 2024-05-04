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
            """ Getter method that returns the list of City instances
            with state_id equals to the current State.id"""
            from models.city import City
            from models import storage
            city_instances = storage.all(City)
            filtered_cities = [city for city in city_instances.values() if city.state_id == self.id]
            return filtered_cities

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)