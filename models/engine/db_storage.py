#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""

from os import environ as env
from dotenv import load_dotenv

load_dotenv()

db_url = "mysql+mysqldb://{}:{}@{}/{}".format(
    env['HBNB_MYSQL_USER'], env['HBNB_MYSQL_PWD'],
    env['HBNB_MYSQL_HOST'], env['HBNB_MYSQL_DB'])

class DBStorage:
    """new engine class
    """
    __engine = None
    __session = None

    def __init__(self):
        from sqlalchemy import create_engine, MetaData
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        """drop all the tables if the env var HBNB_ENV == test"""
        metadata = MetaData(bind=self.__engine)
        metadata.reflect()
        if env.get('HBNB_ENV') == 'test':
            metadata.drop_all()

    def all(self, cls=None):
        """query on the current db and return a dictionary"""
        if cls is not None:
            return {f"{self.__session.query(cls.name).all()}.{self.id}": self}
        else:
            return {f"{self.__session.query(cls).all()}.{self.id}": self}

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
        """Create all tables in the database"""
        from sqlalchemy.orm import sessionmaker, scoped_session
        from models.base_model import Base
        from models.state import State
        from models.city import City
        Base.metadata.create_all(self.__engine)
        self.__session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(self.__session)