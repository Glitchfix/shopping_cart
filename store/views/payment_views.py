from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from store.serializers import PaymentSerializer
from store.models import Payment, User
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt

class PaymentView(APIView):
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

    def get(self, request, payment_id=None):
        if payment_id is not None:
            payment = Payment.objects.get(pk=payment_id)
            if payment.user_id == request.user_id:
                serializer = PaymentSerializer(payment)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            payments = Payment.objects.filter(user_id=request.user_id)
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)

    def post(self, request, payment_id=None):
        if payment_id:
            payment = Payment.objects.get(pk=payment_id)
            payment.pay()
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, payment_id):
        payment = Payment.objects.get(pk=payment_id)
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, payment_id):
        payment = Payment.objects.get(pk=payment_id)
        payment.cancel()
        return Response(status=status.HTTP_204_NO_CONTENT)