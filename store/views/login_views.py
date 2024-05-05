from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.models import User, Cart
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        user.save()
        cart = Cart.get_cart_for_user(user)
        token = get_tokens_for_user(user)
        
        return Response({'message': 'Registration successful', 'tokens': token}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'message': 'Login successful', 'tokens': token})
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
