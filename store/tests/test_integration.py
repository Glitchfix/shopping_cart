from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from store.models import Product, Cart, Order, Payment
from decimal import Decimal


class CartFlowTest(APITestCase):
    def setUp(self):
        self.register_view = reverse('register')
        self.login_view = reverse('login')
        self.user_view = reverse('users')
        self.product_view = reverse('product')
        self.cart_view = reverse('cart')
        self.order_view = reverse('orders')
        self.payment_view = reverse('payment')
        
        
        self.username = "testuser"
        self.first_name = "test"
        self.last_name = "user"
        self.password = "testpass1234"
        self.email = 'test@example.com'
        self.product_ids = []
        self.order_id = None
        self.payment_id = None

    def test_cart_flow(self):
        register_data = {
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
        self.register_user(register_data)

        login_data = {
            'username': self.username,
            'password': self.password,
        }
        self.login_user(login_data)

        self.get_user_profile()

        self.product_ids.append(self.add_product({
            'name': 'PC',
            'description': 'RTX 4090',
            'price': 1900
        }))

        self.product_ids.append(self.add_product({
            'name': 'LAPTOP',
            'description': 'RTX 3090',
            'price': 999
        }))

        self.list_products()

        self.add_items_and_clear_cart()

        self.add_items_place_order_then_cancel()

        self.add_items_place_order_and_pay()

        self.add_items_and_place_order()

        self.list_orders()
    
    def add_items_and_clear_cart(self):
        self.add_items_to_cart()
        self.clear_cart()
    
    def add_items_to_cart(self):
        for product_id in self.product_ids:
            cart_data = {'product_id': product_id, 'quantity': 1}
            self.add_to_cart(cart_data)

        self.get_cart()
        self.clear_cart()
    
    def add_items_and_place_order(self):
        self.add_items_to_cart()

        self.order_id = self.place_order()
        self.get_order('PENDING')
    
    def add_items_place_order_then_cancel(self):
        self.add_items_and_place_order()
        self.payment_id = self.get_order_payment_details()
        self.cancel_payment()
        self.get_order('CANCELED')
        self.clear_cart()
    
    def add_items_place_order_and_pay(self):
        self.add_items_and_place_order()
        self.payment_id = self.get_order_payment_details()
        self.pay_for_order()
        self.get_order('PAID')
    
    def register_user(self, register_data):
        response = self.client.post(reverse('register'), register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def login_user(self, login_data):
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def get_user_profile(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def add_product(self, product_data):
        product_data['price'] = "{:.2f}".format(product_data['price'])
        response = self.client.post(reverse('product'), product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['id']

    def list_products(self):
        response = self.client.get(reverse('product'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def add_to_cart(self, cart_item):
        print("cart_item", cart_item)
        response = self.client.post(reverse('cart'), cart_item)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_cart(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['cartitems']), 2)
        cart_total = float(response.data['total_price'])
        expected_total_amount = 999 + 1900
        self.assertEqual(cart_total, expected_total_amount)

    def clear_cart(self):
        response = self.client.delete(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['cartitems']), 0)
        cart_total = response.data['total_price']
        self.assertEqual(cart_total, 0)

    def place_order(self):
        response = self.client.put(reverse('orders'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order_id = response.data['id']
        order_status = response.data['status']
        self.assertEqual(order_status, 'PENDING')
        return order_id

    def get_order(self, expected_status='PENDING'):
        response = self.client.get(reverse('order', kwargs={'order_id': self.order_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_status = response.data['status']
        self.assertEqual(order_status, expected_status)

    def get_order_payment_details(self):
        response = self.client.post(reverse('order', kwargs={'order_id': self.order_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment_id = response.data['id']
        payment_status = response.data['status']
        self.assertEqual(payment_status, 'PENDING')
        return payment_id

    def pay_for_order(self):
        response = self.client.post(reverse('payment', kwargs={'payment_id': self.payment_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def cancel_payment(self):
        response = self.client.delete(reverse('payment', kwargs={'payment_id': self.payment_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def list_orders(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        orders = response.data
        self.assertEqual(len(orders), 3)
        pending_orders = [order for order in orders if order['status'] == 'PENDING']
        paid_orders = [order for order in orders if order['status'] == 'PAID']
        canceled_orders = [order for order in orders if order['status'] == 'CANCELED']
        self.assertEqual(len(pending_orders), 1)
        self.assertEqual(len(paid_orders), 1)
        self.assertEqual(len(canceled_orders), 1)
