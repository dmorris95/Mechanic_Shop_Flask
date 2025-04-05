from app import create_app
from app.models import db, Mechanic, Ticket, Customer
import unittest

class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanic(name="test_mechanic", email="test@email.com", phone="1234567890", salary=50000)
        self.mechanic2 = Mechanic(name="test2", email='test2@email.com', phone='1231234567', salary=20000)
        self.customer = Customer(name="test_customer", email="test@email.com", phone="1234567890", password="test")
        self.ticket = Ticket(VIN="1111111111", service_date="2025-01-01", service_desc="Test ticket", customer_id=1)

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.add(self.mechanic2)
            db.session.add(self.customer)
            db.session.add(self.ticket)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "James Jones",
            "email": "jjones@email.com",
            "phone": "1122334455",
            "salary": 60000
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'James Jones')
    
    def test_invalid_create_mechanic(self):
        bad_mechanic_payload = {
            "email": "bad_test@email.com",
            "phone": "1122334455",
            "salary": 60000
        }
        
        response = self.client.post('/mechanics/', json=bad_mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['name'], ['Missing data for required field.'])

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_mechanic')

    def test_update_mechanic(self):
        mechanic_payload = {
            "name": "Jimmy Jones",
            "email": "test@email.com",
            "phone": "1234567890",
            "salary": 55000
        }

        response = self.client.put('/mechanics/1', json=mechanic_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Jimmy Jones')
        self.assertEqual(response.json['email'], 'test@email.com')

    def test_delete_mechanic(self):
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)

    def test_experienced_mechanics(self):
        ticket_modify = {
            "add_ids": [2],
            "remove_ids": [] 
        }

        self.client.put('/tickets/1/edit', json=ticket_modify)
        
        response = self.client.get('/mechanics/experience')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[1]['name'], 'test_mechanic')
        self.assertEqual(response.json[0]['name'], 'test2')
