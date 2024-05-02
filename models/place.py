#!/usr/bin/python3
""" Place Module for HBNB project """
from os import environ as env
from dotenv import load_dotenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models import storage
from models.review import Review
from models.amenity import Amenity

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
    if env.get('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', back_populates='place', cascade='delete')
        amenities = relationship('Amenity', secondary='place_amenity', viewonly=False)
    else:
        @property
        def reviews(self):
            r_instances = storage.all(Review)
            reviews_list = [review for review in r_instances.values() if review.place_id == self.id]
            return reviews_list
        @property
        def amenities(self):
            """Getter attribute for amenities"""
            amenity_instances = []
            for obj in storage.all(Amenity).values():
                if obj.id in self.amenity_ids:
                    amenity_instances.append(obj)
            return amenity_instances

        @amenities.setter
        def amenities(self, amenity):
            """Setter attribute for amenities"""
            if isinstance(amenity, Amenity):
                if amenity.id not in self.amenity_ids:
                    self.amenity_ids.append(amenity.id)
                    storage.save()