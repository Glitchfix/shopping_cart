from django.db import models
from .cart import Cart, User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default='PENDING')

    last_update = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    @classmethod
    def place_order(cls, user):
        # Fetch list of cart items based on the current cart
        # Calculate and set the total price before saving the order
        cart = Cart.get_cart_for_user(user)
        order = Order.objects.create(user=user, total_price=cart.price)
        order.products.set(cart.products)
        order.save()
        return order
    
    @classmethod
    def pay_order(cls, user, order_id):
        order = Order.objects.get(id=order_id)
        if order.status != 'PENDING':
            raise Exception("Order is not pending")
        if order.user.id != user.id:
            raise Exception("You are not authorized to pay this order")
        # cart = Cart.get_cart_for_user(order.user)
        # for product in cart.products:
        #     order.products.add(product)
        
        return order
    
    @classmethod
    def cancel_order(cls, order_id):
        order = Order.objects.get(id=order_id)
        if order.status != 'PENDING':
            raise Exception("Order is not pending")
        order.status = 'CANCELED'
        order.save()
        return order
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} {self.total_price} {self.products.all()}"
