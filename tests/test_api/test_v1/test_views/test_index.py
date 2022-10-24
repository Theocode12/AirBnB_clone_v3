#!/usr/bin/python3
""" tests index route """


from unittest import TestCase
from models import get_classes
from api.v1.app import app
from flask import jsonify
class_dict = get_classes()


class test_index_route(TestCase):
    """ tests index route """
    def test_test(self):
        """ confirms test is discoverable """
        self.assertEqual("a", "a")

    def test_status(self):
        """ checks status of api """
        with app.test_client() as c:
            res = c.get("api/v1/status")
            js = res.get_json()
            print(js)
            self.assertEqual("OK", js.get("status"))
