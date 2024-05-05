from django.db import models
from store.models.user import User
from store.models.product import Product
import json
class Cart(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cartitems = models.ManyToManyField('CartItem')  # Add this line
    
    @property
    def products(self):
        # product_ids = []
        if self.cartitems.exists():
            # product_ids = [cart_item.product.id for cart_item in self.cartitems.all()]
            return [cart_item.product for cart_item in self.cartitems.all()]
        # return Product.objects.filter(id__in=product_ids)
        return []
    
    
    @property
    def price(self):
        total_price = 0
        if self.cartitems.exists():
           for cart_item in self.cartitems.all():
               total_price += cart_item.get_total_price()
        return total_price
    
    @classmethod
    def get_cart_for_user(cls, user) -> 'Cart':
        try:
            cls = Cart.objects.get(user=user)
            return cls
        except Cart.DoesNotExist:
            cls = Cart.objects.create(user=user)
            return cls
    
    def add_product(self, product, quantity=1):
        if not self.cartitems.exists():
            cart_item = CartItem.objects.create(product=product, quantity=quantity)
            self.cartitems.add(cart_item)
            cart_item.save()
        else:
            exists = False
            for cart_item in self.cartitems.all():
                if cart_item.product.id == product.id:
                    cart_item.quantity += quantity
                    cart_item.save()
                    exists = True
            if not exists:
                cart_item = CartItem.objects.create(product=product, quantity=quantity)
                self.cartitems.add(cart_item)
                cart_item.save()
        self.save()
    
    def clear_cart(self):
        self.cartitems.clear()
        CartItem.objects.filter(cart=self).delete()

    def remove_product(self, product, quantity=1):
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
            if cart_item.quantity > quantity:
                cart_item.quantity -= quantity
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            pass

    def generate_checkout_link(self, payment):
        self.checkout_link = payment
        self.save()

    def proceed_with_order(self, order):
        self.order = order
        self.save()

class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_total_price(self):
        return self.product.price * self.quantity