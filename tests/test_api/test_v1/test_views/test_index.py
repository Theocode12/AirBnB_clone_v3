#!/usr/bin/python3
""" tests index route """


from unittest import TestCase
from models import get_classes, storage, storage_t
from api.v1.app import app
from flask import jsonify
class_dict = get_classes()
kw = {
        "name": "test",
        "email": "testmail@ya.com",
        "password": "test_passwd"
        }


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
            self.assertEqual("OK", js.get("status"))

    def test_404(self):
        """ checks formatted 404 json """
        with app.test_client() as c:
            res = c.get("api/v1/no_page")
            js = res.get_json()
            self.assertEqual("Not found", js.get("error"))
