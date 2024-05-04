#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb"""

from os import getenv
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.user import User
from models.place import Place

load_dotenv()

db_url = "mysql+mysqldb://{}:{}@{}/{}".format(
getenv('HBNB_MYSQL_USER'), getenv('HBNB_MYSQL_PWD'),
getenv('HBNB_MYSQL_HOST'), getenv('HBNB_MYSQL_DB'))

class DBStorage:
    """new engine class
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the engine and drop all the tables if in test mode"""
        from sqlalchemy import create_engine
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all()

    def all(self, cls=None):
        """query on the current db and return a dictionary"""
        if cls is not None:
            objs = self.__session.query(cls).all()
            obj_dict = {}
            d = {}
            for obj in objs:
                obj_dict = obj.to_dict()
                rm_keys = ['_sa_instance_state', '__class__']
                for k in rm_keys:
                    obj_dict.pop(k, None)
                    d[obj.id] = obj_dict
            return d        
        else:
            return {}

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)
    
    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)
    
    def reload(self):
        """Create all tables in the database and initialize a session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))