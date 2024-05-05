# store/views/cart_views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from store.models import Product, Cart, CartItem, User
from store.serializers import CartSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt

class CartView(APIView):
    authentication_classes = [JWTAuthentication]
    def dispatch(self, request, *args, **kwargs):
        # Check for authentication token and attach user id to the request
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        if token:
            # Perform authentication logic here
            decoded_token = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})
            user_id = decoded_token.get('user_id')
            
            if user_id:
                request.user_id = user_id
                request.user = User.objects.get(pk=user_id)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_user_cart(self, user):
        cart = Cart.get_cart_for_user(user=user)
        return cart
    
    def get_cart(self, request):
        cart = self.get_user_cart(request.user)
        return cart
    
    def get(self, request):
        cart = self.get_user_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        product = Product.objects.get(id=request.data['product_id'])
        cart = self.get_cart(request)
        cart.add_product(product, request.data['quantity'])
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        cart = self.get_cart(request)
        cart.clear_cart()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
