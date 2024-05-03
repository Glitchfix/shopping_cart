from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from store.models import Payment
from store.serializers import PaymentSerializer

class PaymentViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_payment(self):
        url = reverse('payment-list')
        data = {'amount': 100, 'method': 'credit_card'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.first()
        self.assertEqual(payment.amount, 100)
        self.assertEqual(payment.method, 'credit_card')

    def test_create_invalid_payment(self):
        url = reverse('payment-list')
        data = {'amount': -100, 'method': 'credit_card'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Payment.objects.count(), 0)