from unittest import TestCase

from app import create_app
from models import db, connect_db, Cupcake

app = create_app("cupcakes_test", testing=True)
connect_db(app)

with app.app_context():
    db.drop_all()
    db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image_url": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image_url": "http://test.com/cupcake2.jpg"
}

PATCH_DATA_1 = {
    "flavor": "EditedFlavor",
    "size": "EditedSize",
    "rating": 8.5,
    "image_url": "http://test.com/edited/cupcake.jpg"
}

PATCH_DATA_2 = {
    "size": "EditedSize",
    "rating": 8.5
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        with app.app_context():

            Cupcake.query.delete()

            cupcake = Cupcake(**CUPCAKE_DATA)
            db.session.add(cupcake)
            db.session.commit()

            self.cupcake = Cupcake.query.first()

    def tearDown(self):
        """Clean up fouled transactions."""

        with app.app_context():
            db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            # Remove the timestamp from the json so that we can test (assertEqual) the rest of the json
            del data['cupcakes'][0]['created_at']


            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image_url": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json

            # Remove the timestamp from the json so that we can test (assertEqual) the rest of the json
            del data['cupcake']['created_at']

            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })

    def test_get_cupcake_404(self):
        with app.test_client() as client:
            url = "/api/cupcakes/99999"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 404)

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # Remove the timestamp from the json so that we can test (assertEqual) the rest of the json
            del data['cupcake']['created_at']

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image_url": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)


    def test_edit_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json=PATCH_DATA_1)

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            # Remove the timestamp from the json so that we can test (assertEqual) the rest of the json
            del data['cupcake']['created_at']

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "EditedFlavor",
                    "size": "EditedSize",
                    "rating": 8.5,
                    "image_url": "http://test.com/edited/cupcake.jpg"
                }
            })

    def test_edit_cupcake_partial(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json=PATCH_DATA_2)

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            # Remove the timestamp from the json so that we can test (assertEqual) the rest of the json
            del data['cupcake']['created_at']

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor",
                    "size": "EditedSize",
                    "rating": 8.5,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })

    def test_edit_cupcake_404(self):
        with app.test_client() as client:
            url = "/api/cupcakes/999999"
            resp = client.patch(url, json=PATCH_DATA_2)

            self.assertEqual(resp.status_code, 404)


    def test_delete_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            self.assertEqual(data, {
                "message": "deleted"
            })

    def test_delete_cupcake_404(self):
        with app.test_client() as client:
            url = "/api/cupcakes/999999"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 404)



