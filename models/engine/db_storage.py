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
        """
        Query on the current database session (self.__session)
            and return all objects as a dictionary:
        - If cls is None, query all types of objects (i.e. all tables)
        - If cls is not None, query all objects of cls type
        """
        obj_dict = {}
        if cls is not None:
            cls_objs = self.__session.query(cls)
            for obj in cls_objs:
                """key = f"{obj.__class__.__name__}.{obj.id}"""
                obj_dict[obj] = obj
            return obj_dict
        else:
            for all_objs in Base.__subclasses__():
                objs = self.__session.query(all_objs)
                for obj in objs:
                    """key = f"{obj.__class__.__name__}.{obj.id}"""
                    obj_dict[obj] = obj
                return obj_dict

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
        self.__session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))

    def close(self):
        """Clean up the session"""
        self.__session.remove()
