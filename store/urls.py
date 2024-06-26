from django.urls import path, re_path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    # path('swagger/', views.swagger.SwaggerView, name='swagger_doc'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    
    path('user/', views.UserView.as_view(), name='users'),
    path('user/<int:pk>/', views.UserView.as_view(), name='user'),
    
    path('product/', views.ProductView.as_view(), name='product'),
    
    path('cart/', views.CartView.as_view(), name='cart'),
    
    path('payments/', views.PaymentView.as_view(), name='payment'),
    path('payment/<int:payment_id>', views.PaymentView.as_view(), name='payment'),
    
    path('orders/', views.OrderView.as_view(), name='orders'),
    path('order/<int:order_id>', views.OrderView.as_view(), name='order'),
]