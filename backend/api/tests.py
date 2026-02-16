from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer, Loan
import datetime

class CreditSystemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'monthly_income': 50000,
            'phone_number': '1234567890'
        }
        self.register_url = reverse('register')
        self.check_eligibility_url = reverse('check-eligibility')

    def test_register_customer(self):
        response = self.client.post(self.register_url, self.customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('customer_id', response.data)
        # Check approved limit calculation: 36 * 50000 = 1800000. Rounded to nearest lakh = 1800000.
        self.assertEqual(response.data['approved_limit'], 1800000)

    def test_check_eligibility_new_customer(self):
        # Register first
        reg_response = self.client.post(self.register_url, self.customer_data, format='json')
        customer_id = reg_response.data['customer_id']

        # Check eligibility
        data = {
            'customer_id': customer_id,
            'loan_amount': 100000,
            'interest_rate': 12,
            'tenure': 12
        }
        response = self.client.post(self.check_eligibility_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # New customer should be approved (default score logic)
        self.assertTrue(response.data['approval'])

    def test_create_customer_invalid_data(self):
        invalid_data = self.customer_data.copy()
        del invalid_data['monthly_income']
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
