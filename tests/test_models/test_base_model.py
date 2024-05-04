#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except:
            pass

    def test_default(self):
        """ """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.pop('__class__', None)
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        n = {'Name': 'test'}
        new = self.value(**n)
        self.assertIsInstance(new, self.value)

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)


    def test_dict_key_remove(self):
        """"""
        my_i = self.value()
        my_n = my_i.to_dict()
        self.assertIsInstance(my_n, dict)
        self.assertNotIn('_sa_instance_state', my_n)

    def test_dict_keys(self):
        """"""
        my_i = self.value()
        my_n = my_i.to_dict()
        self.assertIn('__class__', my_n)
        self.assertEqual(my_n['__class__'], self.name)
        self.assertIn('created_at', my_n)
        self.assertIn('updated_at', my_n)
    
    # def test_delete(self):
    #     """"""
    #     from models import storage
    #     i = self.value()
    #     i.save()
    #     self.assertIn(i, storage.all(self.value))
    #     i.delete()
    #     self.assertNotIn(i, storage.all(self.value))