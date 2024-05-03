from django.db import models
from .cart import Cart, User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cartitems = models.ManyToManyField('CartItem')
    order_date = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='related_order')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_total_price(self):
        # Calculate the total price based on the cart items in the order
        total_price = 0
        for item in self.cartitems.all():
            total_price += item.product.price * item.quantity
        return total_price

    def save(self, *args, **kwargs):
        # Calculate and set the total price before saving the order
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

        # Fetch list of cart items based on the current cart
        cart = Cart.objects.get(user=self.user)
        self.cart_items = cart.cartitems.all()

        # Clear the cart after saving the order
        cart.cartitems.clear()

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
