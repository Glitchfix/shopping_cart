from rest_framework import serializers
from .models import User, Product, Order, Payment, Cart, CartItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'id']  # Replace '__all__' with the desired fields

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']  # Replace '__all__' with the desired fields

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status', 'user', 'products']
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CartIemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    def get_price(self, obj: Cart):
        return obj.get_total_price()
    class Meta:
        model = CartItem
        fields = '__all__'
class CartSerializer(serializers.ModelSerializer):
    cartitems = CartIemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj: Cart):
        return obj.price

    class Meta:
        model = Cart
        fields = '__all__'