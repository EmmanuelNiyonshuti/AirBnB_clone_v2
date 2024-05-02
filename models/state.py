#!/usr/bin/python3
""" State Module for HBNB project """
from os import environ as env
from dotenv import load_dotenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    load_dotenv()
    if env.get('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', back_populates='state', cascade='delete')
    else:
        @property
        def cities(self):
            """ Getter method that returns the list of City instances
            with state_id equals to the current State.id"""
            from models import storage
            city_instances = storage.all(City)
            filtered_cities = [city for city in city_instances.values() if city.state_id == self.id]
            return filtered_cities