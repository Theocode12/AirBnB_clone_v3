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
amenity_ids = []


class test_amenities_sroute(TestCase):
    """ tests index route """
    def test_test(self):
        """ confirms test is discoverable """
        self.assertEqual("a", "a")

    def test_01_get_amenities(self):
        """ tests GET /api/v1/amenities """
        with app.test_client() as c:
            amenity1 = class_dict["Amenity"](**kw)
            amenity2 = class_dict["Amenity"](**kw)
            amenity1.save()
            amenity2.save()
            amenity_ids.append(amenity1.id)
            amenity_ids.append(amenity2.id)
            res = c.get("api/v1/amenities")
            js = res.get_json()
            self.assertEqual(list, type(js))
            assert len(js) > 0

    def test_get_amenity_by_id(self):
        """ tests GET /api/v1/amenities/<id> """
        with app.test_client() as c:
            id_ = amenity_ids[0]
            res = c.get("api/v1/amenities/" + id_)
            js = res.get_json()
            self.assertEqual(js.get("__class__"), "Amenity")

    def test_get_amenity_by_id_falsy(self):
        """ tests GET /api/v1/amenities/<id> """
        with app.test_client() as c:
            id_ = amenity_ids[0]
            id_ = id_ + "0"
            res = c.get("api/v1/amenities/" + id_)
            js = res.get_json()
            self.assertEqual(js.get("error"), "Not found")

    def test_z_del_amenity_by_id(self):
        """ tests DELETE /api/v1/amenities/<id> """
        with app.test_client() as c:
            id_ = amenity_ids[0]
            res = c.delete("api/v1/amenities/" + id_)
            js = res.get_json()
            self.assertEqual(len(js), 0)
            assert res.status_code == 200
            # confirm it is deleted
            res = c.get("api/v1/amenities/" + id_)
            js = res.get_json()
            self.assertEqual(js.get("error"), "Not found")
            assert res.status_code == 404

    def test_z_del_amenity_by_id_falsy(self):
        """ tests DELETE /api/v1/amenities/<id> """
        with app.test_client() as c:
            id_ = amenity_ids[0]
            id_ = id_ + "wrong"
            res = c.delete("api/v1/amenities/" + id_)
            js = res.get_json()
            assert res.status_code == 404
            self.assertEqual(js.get("error"), "Not found")

    def test_put_amenity_by_id(self):
        """ tests PUT /api/v1/amenities/<id> """
        with app.test_client() as c:
            data = {
                    "name": "new_name",
                    "id": "fake_id"
                    }
            id_ = amenity_ids[0]
            res = c.put("api/v1/amenities/" + id_, json=data)
            js = res.get_json()
            self.assertEqual(js.get("name"), "new_name")
            # confirm id is not updated
            res = c.get("api/v1/amenities/" + id_)
            js = res.get_json()
            self.assertNotEqual(js.get("id"), "fake_id")

    def test_post_amenity(self):
        """ tests Post /api/v1/amenities/ """
        with app.test_client() as c:
            data = {
                    "name": "new_amenity"
                    }
            res = c.post("api/v1/amenities/", json=data)
            js = res.get_json()
            self.assertEqual(js.get("name"), "new_amenity")
            id_ = js.get("id")
            amenity_ids.append(id_)
