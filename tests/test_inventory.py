from app import create_app
from app.models import db, Inventory
import unittest

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.part = Inventory(name='Test', price=19.99)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.part)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_part(self):
        part_payload = {
            "name": "Brake Pads",
            "price": 15.49
        }

        response = self.client.post('/inventory/', json=part_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Brake Pads')

    def test_get_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'Test')

    def test_update_part(self):
        update_payload = {
            "name": "Test Pads",
            "price": 19.99
        }

        response = self.client.put('/inventory/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Pads')
        self.assertEqual(response.json['price'], 19.99)

    def test_bad_update(self):
        update_payload = {
            "name": "Test Pads"
        }

        response = self.client.put('/inventory/1', json=update_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['price'], ['Missing data for required field.'])

    def test_delete_part(self):
        response = self.client.delete('/inventory/1')
        self.assertEqual(response.status_code, 200)
