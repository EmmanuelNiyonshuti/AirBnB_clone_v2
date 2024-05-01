#!/usr/bin/python3
""" Place Module for HBNB project """
from os import environ as env
from dotenv import load_dotenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models import storage
from review import Review

"""Define the association table 'place_amenity"""
place_amenity = Table('place_amenity', Base.metadata,
                        Column('place_id', String(60), ForeignKey('places.id'), nullable=False, primary_key=True),
                        Column('amenity_id', String(60), ForeignKey('amenities.id'), nullable=False, primary_key=True)

)

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False, )
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    user = relationship('User', back_populates='places')
    cities = relationship('City', back_populates='places')


    load_dotenv()
    if env['HBNB_TYPE_STORAGE'] == "db":
        reviews = relationship('Review', back_populates='place', cascade='delete')
        amenities = relationship('Amenity', secondary='place_amenity', viewobly=False)
    else:
        @property
        def reviews(self):
            r_instances = storage.all(Review)
            reviews_list = [r for r in r_instances.values() if r.place_id == self.id]
            return reviews_list

        # def amenities(self):
