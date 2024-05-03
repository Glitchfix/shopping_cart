from django.test import TestCase, RequestFactory
from rest_framework.test import APIRequestFactory
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from store.models import User
from store.serializers import UserSerializer
from store.views.user_views import UserView

class UserViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserView.as_view()
        self.user = User.objects.create(username='testuser', email='test@example.com')

    def test_get_users(self):
        request = self.factory.get('/users/')
        response = self.view(request)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create_user(self):
        request = self.factory.post('/users/', {'username': 'newuser', 'email': 'newuser@example.com'})
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)

    def test_create_user_invalid_data(self):
        request = self.factory.post('/users/', {'username': 'newuser'})
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 1)

    def test_update_user(self):
        request = self.factory.put('/users/1', {'username': 'updateduser', 'email': 'updateduser@example.com'})
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(pk=1).username, 'updateduser')

    def test_update_user_invalid_data(self):
        request = self.factory.put('/users/1', {'username': 'updateduser'})
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(User.objects.get(pk=1).username, 'updateduser')

    def test_delete_user(self):
        request = self.factory.delete('/users/1')
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 0)