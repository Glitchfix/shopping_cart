from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from store.serializers import ProductSerializer
from store.models import Product
import jwt

class ProductView(APIView):
    # permission_classes = [IsAuthenticated]
    def dispatch(self, request, *args, **kwargs):
        # Check for authentication token and attach user id to the request
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        if token:
            # Perform authentication logic here
            decoded_token = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})
            user_id = decoded_token.get('user_id')
            
            if user_id:
                request.user_id = user_id
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk=None):
        if pk is not None:
            try:
                product = Product.objects.get(pk=pk)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

    def post(self, request):
        product = Product.objects.create(**request.data)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)