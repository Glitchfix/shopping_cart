from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from store.models import Product
from store.serializers import ProductSerializer

class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name='Test Product', price=10.99)

    def test_update_product(self):
        url = reverse('product-detail', args=[self.product.pk])
        data = {'name': 'Updated Product', 'price': 15.99}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.price, 15.99)

    def test_update_nonexistent_product(self):
        url = reverse('product-detail', args=[999])
        data = {'name': 'Updated Product', 'price': 15.99}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_product_data(self):
        url = reverse('product-detail', args=[self.product.pk])
        data = {'name': '', 'price': -5.99}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.product.refresh_from_db()
        self.assertNotEqual(self.product.name, '')
        self.assertNotEqual(self.product.price, -5.99)