from django.test import TestCase
from store.models import User, Product, Order, Payment, Cart, CartItem

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

    def test_user_str_representation(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        self.assertEqual(str(user), 'testuser')

class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(name='Test Product', price=10.99)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 10.99)

class OrderModelTest(TestCase):
    def test_order_creation(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        order = Order.objects.create(user=user, total_price=50.99)
        self.assertEqual(order.total_price, 50.99)

    def test_order_status_default(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        order = Order.objects.create(user=user, total_price=50.99)
        self.assertEqual(order.status, 'pending')

    def test_order_status_update(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        order = Order.objects.create(user=user, total_price=50.99)
        order.status = 'completed'
        order.save()
        self.assertEqual(order.status, 'completed')

    def test_order_str_representation(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        order = Order.objects.create(user=user, total_price=50.99)
        self.assertEqual(str(order), f"Order #{order.id} - {order.user.username}")

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

class CartItemModelTest(TestCase):
    def test_cartitem_creation(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        cart = Cart.objects.create(user=user)
        product = Product.objects.create(name='Test Product', price=10.99)
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.product, product)
        self.assertEqual(cart_item.quantity, 2)

    def test_cartitem_total_price_calculation(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        cart = Cart.objects.create(user=user)
        product = Product.objects.create(name='Test Product', price=10.99)
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=3)
        self.assertEqual(cart_item.calculate_total_price(), 32.97)


class PaymentModelTest(TestCase):
    def test_payment_creation(self):
        payment = Payment.objects.create(amount=100.0, status='completed')
        self.assertEqual(payment.amount, 100.0)
        self.assertEqual(payment.status, 'completed')

    def test_payment_str_representation(self):
        payment = Payment.objects.create(amount=100.0, status='completed')
        self.assertEqual(str(payment), f"Payment #{payment.id}")

    def test_payment_status_update(self):
        payment = Payment.objects.create(amount=100.0, status='completed')
        payment.status = 'refunded'
        payment.save()
        self.assertEqual(payment.status, 'refunded')

