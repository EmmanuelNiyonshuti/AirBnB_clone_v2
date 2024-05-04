#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import os

"""Define the association table 'place_amenity"""
if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                            Column('place_id', String(60), ForeignKey('places.id'),
                                nullable=False, primary_key=True),
                            Column('amenity_id', String(60), ForeignKey('amenities.id'),
                                nullable=False, primary_key=True)

    )

class Place(BaseModel, Base):
    """ A place to stay """
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
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

        reviews = relationship('Review', back_populates='place', cascade='delete')
        amenities = relationship('Amenity', secondary='place_amenity', viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            from models import storage
            from models.review import Review
            r_instances = storage.all(Review)
            reviews_list = [review for review in r_instances.values() if review.place_id == self.id]
            return reviews_list

        @property
        def amenities(self):
            """Getter attribute for amenities"""
            from models import storage
            from models.amenity import Amenity
            amenity_instances = []
            for obj in storage.all(Amenity).values():
                if obj.id in self.amenity_ids:
                    amenity_instances.append(obj)
            return amenity_instances

        @amenities.setter
        def amenities(self, amenity):
            """Setter attribute for amenities"""
            from models import storage
            from models.amenity import Amenity
            if isinstance(amenity, Amenity):
                if amenity.id not in self.amenity_ids:
                    self.amenity_ids.append(amenity.id)
                    storage.save()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)