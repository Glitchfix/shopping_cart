from django.db import models
from store.models.user import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')
    checkout_link = models.OneToOneField('Payment', on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField('Order', on_delete=models.SET_NULL, null=True)

    def add_product(self, product):
        self.products.add(product)

    def remove_product(self, product):
        self.products.remove(product)

    def generate_checkout_link(self, payment):
        self.checkout_link = payment
        self.save()

    def proceed_with_order(self, order):
        self.order = order
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity