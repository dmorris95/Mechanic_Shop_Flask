from app import create_app
from app.models import db, Customer, Ticket
import unittest

class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(name="test_customer", email="test@email.com", phone="1234567890", password="test")
        self.ticket = Ticket(VIN="1111111111", service_date="2025-01-01", service_desc="Test ticket", customer_id=1)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.add(self.ticket)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {
            "name": "John Smith",
            "email": "jsmith@email.com",
            "phone": "1234567890",
            "password": "test123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Smith")

    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    def test_invalid_login(self):
        credentials = {
            "email": "wrong@email.com",
            "password": "wrong_pass"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid email or password')

    def test_update_customer(self):
        update_payload = {
            "name": "John Doe",
            "email": "jdoe@email.com",
            "phone": "1234567890",
            "password": "test123"
        }

        headers = {'Authorization': "Bearer " + self.test_login_customer()}

        response = self.client.put('/customers/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "John Doe")
        self.assertEqual(response.json['email'], "jdoe@email.com")
    
    def test_get_all_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_customer')
    
    def test_delete_customer(self):
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_customers_tickets(self):
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['VIN'], '1111111111')