# store/views/cart_views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from store.models import Product, Cart
from store.serializers import CartSerializer

class CartView(APIView):
    def get(self, request, pk=None):
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)

    def post(self, request):
        product = Product.objects.get(id=request.data['product_id'])
        cart = Cart.objects.create(user=request.user, product=product, quantity=request.data['quantity'])
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        cart = Cart.objects.get(id=pk)
        if request.user != cart.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        cart.quantity = request.data['quantity']
        cart.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def delete(self, request, pk):
        cart = Cart.objects.get(id=pk)
        if request.user != cart.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)