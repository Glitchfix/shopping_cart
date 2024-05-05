from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from store.serializers import OrderSerializer, PaymentSerializer
from store.models import Order, User, Payment
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt

class OrderView(APIView):
    # permission_classes = [IsAuthenticated]
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

    def get(self, request, order_id=None):
        if order_id is not None:
            order = Order.objects.get(id=order_id)
            if request.user != order.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = OrderSerializer(order)
        else:
            orders = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id)
        payment = Payment.objects.create(user=request.user, order=order, amount=order.total_price)
        payment.save()
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        order = Order.place_order(user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, order_id):
        order = Order.cancel_order(order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
