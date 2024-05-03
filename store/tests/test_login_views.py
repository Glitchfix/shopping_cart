from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.response import Response
from store.views.login_views import LoginView

class LoginViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = LoginView.as_view()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'test@example.com'

    def test_user_registration(self):
        request = self.factory.post('/register', {'username': self.username, 'password': self.password, 'email': self.email})
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': 'Registration successful'})
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_existing_username(self):
        User.objects.create_user(username=self.username, password=self.password, email=self.email)
        request = self.factory.post('/login', {'username': self.username, 'password': self.password, 'email': self.email})
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'message': 'Username already taken'})
        self.assertFalse(User.objects.filter(username=self.username).exists())

    def test_user_login(self):
        user = User.objects.create_user(username=self.username, password=self.password, email=self.email)
        request = self.factory.post('/login', {'username': self.username, 'password': self.password})
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': 'Registration successful'})
        self.assertEqual(request.user, user)
        self.assertTrue(request.user.is_authenticated)
