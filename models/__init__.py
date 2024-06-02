#!/usr/bin/python3
"""This module instantiates storage object and reloads all objects from the storage engines"""
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()

else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()