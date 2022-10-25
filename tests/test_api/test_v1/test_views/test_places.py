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
        "password": "test_passwd",
        "text": "random text"
        }
place_ids = []
city_id_list = []


class test_places_sroute(TestCase):
    """ tests index route """
    def test_test(self):
        """ confirms test is discoverable """
        self.assertEqual("a", "a")

    def test_01_get_places(self):
        """ tests GET /api/v1/cities/<city_id>/places """
        user = class_dict["User"](**kw)
        kw["user_id"] = user.id
        user.save()
        state = class_dict["State"](**kw)
        kw["state_id"] = state.id
        state.save()
        city = class_dict["City"](**kw)
        city.save()
        city_id = city.id
        city_id_list.append(city_id)
        with app.test_client() as c:
            place1 = class_dict["Place"](**kw)
            place2 = class_dict["Place"](**kw)
            place1.city_id = city_id
            place2.city_id = city_id
            place1.save()
            place2.save()
            place_ids.append(place1.id)
            place_ids.append(place2.id)
            res = c.get("api/v1/cities/{}/places".format(city_id))
            js = res.get_json()
            self.assertEqual(list, type(js))
            assert len(js) > 0

    def test_get_place_by_id(self):
        """ tests GET /api/v1/cities/<city_id>/places/<id> """
        with app.test_client() as c:
            id_ = place_ids[0]
            s_id = city_id_list[0]
            res = c.get("api/v1/places/{}".format(id_))
            js = res.get_json()
            self.assertEqual(js.get("__class__"), "Place")

    def test_get_place_by_id_falsy(self):
        """ tests GET /api/v1/cities/<city_id>/places/<id> """
        with app.test_client() as c:
            id_ = place_ids[0]
            id_ = id_ + "0"
            s_id = city_id_list[0]
            res = c.get("api/v1/cities/{}/places/{}".format(s_id, id_))
            js = res.get_json()
            self.assertEqual(js.get("error"), "Not found")

    def test_z_del_place_by_id(self):
        """ tests DELETE /api/v1/places/<id> """
        with app.test_client() as c:
            id_ = place_ids[0]
            res = c.delete("api/v1/places/" + id_)
            js = res.get_json()
            self.assertEqual(len(js), 0)
            assert res.status_code == 200
            # confirm it is deleted
            s_id = city_id_list[0]
            res = c.get("api/v1/cities/{}/places/{}".format(s_id, id_))
            js = res.get_json()
            self.assertEqual(js.get("error"), "Not found")
            assert res.status_code == 404

    def test_z_del_place_by_id_falsy(self):
        """ tests DELETE /api/v1/places/<id> """
        with app.test_client() as c:
            id_ = place_ids[0]
            id_ = id_ + "wrong"
            res = c.delete("api/v1/places/" + id_)
            js = res.get_json()
            assert res.status_code == 404
            self.assertEqual(js.get("error"), "Not found")

    def test_put_place_by_id(self):
        """ tests PUT /api/v1/places/<id> """
        with app.test_client() as c:
            data = {
                    "name": "new_name",
                    "id": "fake_id",
                    }
            id_ = place_ids[0]
            res = c.put("api/v1/places/" + id_, json=data)
            js = res.get_json()
            self.assertEqual(js.get("name"), "new_name")
            # confirm id is not updated
            res = c.get("api/v1/places/" + id_)
            js = res.get_json()
            self.assertNotEqual(js.get("id"), "fake_id")

    def test_post_place(self):
        """ tests Post /api/v1/cities/<city_id>/places """
        with app.test_client() as c:
            c_id = city_id_list[0]
            user = class_dict["User"](**kw)
            user.save()
            user_id = user.id
            data = {
                    "name": "new_place",
                    "city_id": c_id,
                    "user_id": user_id
                    }
            res = c.post("api/v1/cities/{}/places/".format(c_id), json=data)
            js = res.get_json()
            print(js, c_id)
            self.assertEqual(js.get("name"), "new_place")
            id_ = js.get("id")
            place_ids.append(id_)
