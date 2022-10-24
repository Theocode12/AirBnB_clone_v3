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
city_ids = []
state_id_list = []


class test_cities_sroute(TestCase):
    """ tests index route """
    def test_test(self):
        """ confirms test is discoverable """
        self.assertEqual("a", "a")

    def test_01_get_cities(self):
        """ tests GET /api/v1/states/<state_id>/cities """
        state = class_dict["State"](**kw)
        state.save()
        state_id = state.id
        state_id_list.append(state_id)
        with app.test_client() as c:
            city1 = class_dict["City"](**kw)
            city2 = class_dict["City"](**kw)
            city1.state_id = state_id
            city2.state_id = state_id
            city1.save()
            city2.save()
            city_ids.append(city1.id)
            city_ids.append(city2.id)
            res = c.get("api/v1/states/{}/cities".format(state_id))
            js = res.get_json()
            self.assertEqual(list, type(js))
            assert len(js) > 0

    def test_get_city_by_id(self):
        """ tests GET /api/v1/states/<state_id>/cities/<id> """
        with app.test_client() as c:
            id_ = city_ids[0]
            s_id = state_id_list[0]
            res = c.get("api/v1/cities/{}".format(id_))
            js = res.get_json()
            self.assertEqual(js.get("__class__"), "City")

    def test_get_city_by_id_falsy(self):
        """ tests GET /api/v1/states/<state_id>/cities/<id> """
        with app.test_client() as c:
            id_ = city_ids[0]
            id_ = id_ + "0"
            s_id = state_id_list[0]
            res = c.get("api/v1/states/{}/cities/{}".format(s_id, id_))
            js = res.get_json()
            self.assertEqual(js.get("error"), "Not found")

    def test_z_del_city_by_id(self):
        """ tests DELETE /api/v1/cities/<id> """
        with app.test_client() as c:
            id_ = city_ids[0]
            res = c.delete("api/v1/cities/" + id_)
            js = res.get_json()
            self.assertEqual(len(js), 0)
            assert res.status_code == 200
            # confirm it is deleted
            s_id = state_id_list[0]
            res = c.get("api/v1/states/{}/cities/{}".format(s_id, id_))
            js = res.get_json()
            self.assertEqual(js.get("error"), "Not found")
            assert res.status_code == 404

    def test_z_del_city_by_id_falsy(self):
        """ tests DELETE /api/v1/cities/<id> """
        with app.test_client() as c:
            id_ = city_ids[0]
            id_ = id_ + "wrong"
            res = c.delete("api/v1/cities/" + id_)
            js = res.get_json()
            assert res.status_code == 404
            self.assertEqual(js.get("error"), "Not found")

    def test_put_city_by_id(self):
        """ tests PUT /api/v1/cities/<id> """
        with app.test_client() as c:
            data = {
                    "name": "new_name",
                    "id": "fake_id",
                    }
            id_ = city_ids[0]
            res = c.put("api/v1/cities/" + id_, json=data)
            js = res.get_json()
            self.assertEqual(js.get("name"), "new_name")
            # confirm id is not updated
            res = c.get("api/v1/cities/" + id_)
            js = res.get_json()
            self.assertNotEqual(js.get("id"), "fake_id")

    def test_post_city(self):
        """ tests Post /api/v1/states/<state_id>/cities """
        with app.test_client() as c:
            s_id = state_id_list[0]
            data = {
                    "name": "new_city",
                    "state_id": s_id
                    }
            res = c.post("api/v1/states/{}/cities/".format(s_id), json=data)
            js = res.get_json()
            print(js, s_id)
            self.assertEqual(js.get("name"), "new_city")
            id_ = js.get("id")
            city_ids.append(id_)
