from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from store.models import Product, Cart, Order, Payment


class CartFlowTest(APITestCase):
    def setUp(self):
        # Setup initial data if needed
        self.baseurl = "http://localhost:8000/store"
        self.register_url = f"{self.baseurl}/register"
        self.login_url = f"{self.baseurl}/login"
        self.user_url = f"{self.baseurl}/user"
        self.product_url = f"{self.baseurl}/product"
        self.cart_url = f"{self.baseurl}/cart"
        self.order_url = f"{self.baseurl}/order"
        self.payment_url = f"{self.baseurl}/payment"
        
        self.baseurl = "http://localhost:8000/store"
        self.register_view = reverse('register')
        self.login_view = reverse('login')
        self.user_view = reverse('users')
        self.product_view = reverse('product')
        self.cart_view = reverse('cart')
        self.order_view = reverse('orders')
        self.payment_view = reverse('payment')
        
        
        self.username = "testuser"
        self.password = "testpass1234"
        self.email = 'test@example.com'
        self.product_ids = []
        self.order_id = None
        self.payment_id = None

    def test_cart_flow(self):
        register_data = {
            'username': self.username,
            'password': self.password,
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
            'price': 1900.99
        }))
        
        self.product_ids.append(self.add_product({
            'name': 'LAPTOP',
            'description': 'RTX 3090',
            'price': 999.99
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
        self.get_order(self.order_id, 'PENDING')
    
    def add_items_place_order_then_cancel(self):
        self.add_items_and_place_order()
        self.payment_id = self.get_order_payment_details(self.order_id)
        self.cancel_payment(self.payment_id)
        self.get_order('CANCELED')
        self.clear_cart()
    
    def add_items_place_order_and_pay(self):
        self.add_items_and_place_order()
        self.payment_id = self.get_order_payment_details(self.order_id)
        self.pay_for_order()
        self.get_order('PAID')
    
    def register_user(self, register_data):
        response = self.client.post(self.register_url, register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def login_user(self, login_data):
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def get_user_profile(self):
        response = self.client.get(f"{self.user_url}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def add_product(self, product_data):
        response = self.client.get(f"{self.product_url}/", product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['id']

    def list_products(self):
        response = self.client.get(f"{self.product_url}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def add_to_cart(self, cart_data):
        response = self.client.post(f"{self.cart_url}/", cart_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_cart(self):
        response = self.client.get(f"{self.cart_url}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['cartitems']), 1)
        cart_total = response.data['total_price']
        expected_total_amount = 999.99 + 1900.99
        self.assertEqual(cart_total, expected_total_amount)

    def clear_cart(self):
        response = self.client.delete(f"{self.cart_url}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['cartitems']), 0)
        cart_total = response.data['total_price']
        self.assertEqual(cart_total, 0)

    def place_order(self):
        # response = self.client.put(self.order_url)
        response = self.client.put(self.order_view)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order_id = response.data['id']
        order_status = response.data['status']
        self.assertEqual(order_status, 'PENDING')
        return order_id

    def get_order(self, status='PENDING'):
        response = self.client.get(f"{self.order_url}/{self.order_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_status = response.data['status']
        self.assertEqual(order_status, status)

    def get_order_payment_details(self):
        response = self.client.get(f"{self.order_url}/{self.order_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment_id = response.data['id']
        payment_status = response.data['status']
        self.assertEqual(payment_status, 'PENDING')
        return payment_id

    def pay_for_order(self):
        response = self.client.post(f"{self.payment_url}/{self.payment_id}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def cancel_payment(self, order_id):
        response = self.client.delete(reverse('cancel-payment', args=[order_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def list_orders(self):
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        orders = response.data
        self.assertEqual(len(orders), 3)
        pending_orders = [order for order in orders if order['status'] == 'PENDING']
        paid_orders = [order for order in orders if order['status'] == 'PAID']
        canceled_orders = [order for order in orders if order['status'] == 'CANCELED']
        self.assertEqual(len(pending_orders), 1)
        self.assertEqual(len(paid_orders), 1)
        self.assertEqual(len(canceled_orders), 1)
