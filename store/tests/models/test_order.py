from django.test import TestCase
from store.models import User, Product, Order, Payment, CartItem, Cart

class OrderModelTest(TestCase):
    def test_order_creation(self):
        order = Order.objects.create(total_price=50.99)
        self.assertEqual(order.total_price, 50.99)

    def test_order_status_default(self):
        order = Order.objects.create(total_price=50.99)
        self.assertEqual(order.status, 'pending')

    def test_order_status_update(self):
        order = Order.objects.create(total_price=50.99)
        order.status = 'shipped'
        order.save()
        self.assertEqual(order.status, 'shipped')

    def test_order_str_representation(self):
        order = Order.objects.create(total_price=50.99)
        self.assertEqual(str(order), f"Order #{order.id}")

    def test_order_total_price_calculation(self):
        order = Order.objects.create(total_price=0)
        product1 = Product.objects.create(name='Product 1', price=10.99)
        product2 = Product.objects.create(name='Product 2', price=20.99)
        order.cartitems.create(product=product1, quantity=1)
        order.cartitems.create(product=product2, quantity=2)
        self.assertEqual(order.calculate_total_price(), 52.97)

    def test_order_save_method(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        cart = Cart.objects.create(user=user)
        product1 = Product.objects.create(name='Product 1', price=10.99)
        product2 = Product.objects.create(name='Product 2', price=20.99)
        cart.cartitems.create(product=product1, quantity=1)
        cart.cartitems.create(product=product2, quantity=2)

        order = Order(user=user, total_price=0)
        self.assertEqual(order.total_price, 52.97)
        self.assertEqual(order.cartitems.count(), 2)
        order.save()
        self.assertEqual(cart.cartitems.count(), 0)

