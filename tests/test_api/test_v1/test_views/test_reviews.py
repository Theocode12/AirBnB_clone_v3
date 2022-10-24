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
        "text": "random_text"
        }
review_ids = []
place_id_list = []


class test_reviews_sroute(TestCase):
    """ tests index route """
    def test_test(self):
        """ confirms test is discoverable """
        self.assertEqual("a", "a")

    def test_01_get_reviews(self):
        """ tests GET /api/v1/places/<place_id>/reviews """
        user = class_dict["User"](**kw)
        kw["user_id"] = user.id
        user.save()
        state = class_dict["State"](**kw)
        kw["state_id"] = state.id
        state.save()
        city = class_dict["City"](**kw)
        kw["city_id"] = city.id
        city.save()
        place = class_dict["Place"](**kw)
        place.save()
        place_id = place.id
        place_id_list.append(place_id)
        with app.test_client() as c:
            review1 = class_dict["Review"](**kw)
            review2 = class_dict["Review"](**kw)
            review1.place_id = place_id
            review2.place_id = place_id
            review1.save()
            review2.save()
            review_ids.append(review1.id)
            review_ids.append(review2.id)
            res = c.get("api/v1/places/{}/reviews".format(place_id))
            js = res.get_json()
            self.assertEqual(list, type(js))
            assert len(js) > 0

    def test_get_review_by_id(self):
        """ tests GET /api/v1/places/<place_id>/reviews/<id> """
        with app.test_client() as c:
            id_ = review_ids[0]
            s_id = place_id_list[0]
            res = c.get("api/v1/reviews/{}".format(id_))
            js = res.get_json()
            self.assertEqual(js.get("__class__"), "Review")

    def test_get_review_by_id_falsy(self):
        """ tests GET /api/v1/places/<place_id>/reviews/<id> """
        with app.test_client() as c:
            id_ = review_ids[0]
            id_ = id_ + "0"
            s_id = place_id_list[0]
            res = c.get("api/v1/places/{}/reviews/{}".format(s_id, id_))
            js = res.get_json()
            self.assertEqual(js.get("error"), "Not found")

    def test_z_del_review_by_id(self):
        """ tests DELETE /api/v1/reviews/<id> """
        with app.test_client() as c:
            id_ = review_ids[0]
            res = c.delete("api/v1/reviews/" + id_)
            js = res.get_json()
            self.assertEqual(len(js), 0)
            assert res.status_code == 200
            # confirm it is deleted
            s_id = place_id_list[0]
            res = c.get("api/v1/places/{}/reviews/{}".format(s_id, id_))
            js = res.get_json()
            self.assertEqual(js.get("error"), "Not found")
            assert res.status_code == 404

    def test_z_del_review_by_id_falsy(self):
        """ tests DELETE /api/v1/reviews/<id> """
        with app.test_client() as c:
            id_ = review_ids[0]
            id_ = id_ + "wrong"
            res = c.delete("api/v1/reviews/" + id_)
            js = res.get_json()
            assert res.status_code == 404
            self.assertEqual(js.get("error"), "Not found")

    def test_put_review_by_id(self):
        """ tests PUT /api/v1/reviews/<id> """
        with app.test_client() as c:
            data = {
                    "name": "new_name",
                    "id": "fake_id",
                    }
            id_ = review_ids[0]
            res = c.put("api/v1/reviews/" + id_, json=data)
            js = res.get_json()
            self.assertEqual(js.get("name"), "new_name")
            # confirm id is not updated
            res = c.get("api/v1/reviews/" + id_)
            js = res.get_json()
            self.assertNotEqual(js.get("id"), "fake_id")

    def test_post_review(self):
        """ tests Post /api/v1/places/<place_id>/reviews """
        with app.test_client() as c:
            c_id = place_id_list[0]
            user = class_dict["User"](**kw)
            user.save()
            user_id = user.id
            data = {
                    "name": "new_review",
                    "place_id": c_id,
                    "user_id": user_id,
                    "text": "random text"
                    }
            res = c.post("api/v1/places/{}/reviews/".format(c_id), json=data)
            js = res.get_json()
            print(js, c_id)
            self.assertEqual(js.get("name"), "new_review")
            id_ = js.get("id")
            review_ids.append(id_)
