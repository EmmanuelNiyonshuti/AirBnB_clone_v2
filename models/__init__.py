#!/usr/bin/python3
"""This module instantiates an object"""
from os import environ as env

from dotenv import load_dotenv

load_dotenv()

"""Add a conditional depending of the value of the environment variable"""

if env.get('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
