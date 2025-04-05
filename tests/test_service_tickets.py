from app import create_app
from app.models import db, Inventory, Mechanic, Customer, Ticket
import unittest

class TestTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanic(name="test_mechanic", email="test@email.com", phone="1234567890", salary=50000)
        self.mechanic2 = Mechanic(name="test2", email='test2@email.com', phone='1231234567', salary=20000)
        self.customer = Customer(name="test_customer", email="test@email.com", phone="1234567890", password="test")
        self.ticket = Ticket(VIN="1111111111", service_date="2025-01-01", service_desc="Test ticket", customer_id=1)
        self.part = Inventory(name='Test', price=19.99)

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.add(self.mechanic2)
            db.session.add(self.customer)
            db.session.add(self.ticket)
            db.session.add(self.part)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_ticket(self):
        ticket_payload = {
            "VIN": "1234567891234567890",
            "service_date": "2025-02-04",
            "service_desc": "Test description",
            "customer_id": 1,
            "mechanic_ids": [1]
        }

        response = self.client.post('/tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['service_date'], "2025-02-04")
        self.assertEqual(response.json['customer_id'], 1)
        self.assertEqual(response.json['mechanic'][0]['name'], 'test_mechanic')

    def test_get_tickets(self):
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['service_desc'], 'Test ticket')

    def test_edit_ticket(self):
        edit_ticket_payload = {
            "add_ids": [2],
            "remove_ids": []
        }

        response = self.client.put('/tickets/1/edit', json=edit_ticket_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['mechanic'][0]['name'], 'test2')
    
    def test_add_part_ticket(self):
        part_ticket_payload = {
            "add_ids": [1]
        }

        response = self.client.put('/tickets/1/add-part', json=part_ticket_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['parts'][0]['name'], 'Test')
        self.assertEqual(response.json['customer_id'], 1)
    
    def test_bad_part(self):
        bad_payload = {
            "wrong_data": [1]
        }
        
        response = self.client.put('/tickets/1/add-part', json=bad_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['add_ids'], ['Missing data for required field.'])