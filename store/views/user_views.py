from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.encoding import smart_str
from rest_framework_simplejwt.authentication import JWTAuthentication

from store.models import User

from store.serializers import UserSerializer
import jwt

class UserView(APIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_token(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        decoded_token = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})
        return decoded_token
    def get_user_id(self, request):
        decoded_token = self.get_token(request)
        
        user_id = decoded_token.get('user_id')
        return user_id
    
    def get(self, request):
        # Get user info for the authenticated user
        # Fetch the request id from the bearer token
        user_id = self.get_user_id(request)
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        user_id = self.get_user_id(request)
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        user_id = self.get_user_id(request)
        user = User.objects.get(pk=user_id)
        user.delete()
        return Response(status=204)
