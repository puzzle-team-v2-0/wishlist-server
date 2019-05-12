from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .models import Wish


class AccountsTest(APITestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user('test-user', 'test@example.com', 'test-password')
        self.create_url = reverse('user-list')

    def test_create_user(self) -> None:
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }
        response = self.client.post(self.create_url, data, format='json')
        user = User.objects.get(email='foobar@example.com')
        token = Token.objects.get(user=user)

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
        self.assertEqual(response.data['auth_token'], token.key)

    def test_create_user_with_short_password(self):
        data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': 'foo'
        }
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': ''
        }
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'foo' * 30,
            'email': 'foobarbaz@example.com',
            'password': 'foobar'
        }
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
            'username': '',
            'email': 'foobarbaz@example.com',
            'password': 'foobar'
        }
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
            'username': self.test_user.username,
            'email': 'user@example.com',
            'password': 'testuser'
        }
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            'username': 'testuser2',
            'email': self.test_user.email,
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email': 'testing',
            'passsword': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
            'username': 'foobar',
            'email': '',
            'password': 'foobarbaz'
        }
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)


class WishesTest(APITestCase):
    def setUp(self) -> None:
        self.test_user_1 = User.objects.create_user('test-user-1', 'test_1@example.com', 'test-password-1')
        self.test_user_2 = User.objects.create_user('test-user-2', 'test_2@example.com', 'test-password-2')
        self.create_url = reverse('wish-list')

    def _check_wish(self, data: dict, wish: Wish, check_id: bool = False) -> None:
        self.assertEqual(data['title'], wish.title)
        self.assertEqual(data['price'], wish.price)
        self.assertEqual(data['link'], wish.link)
        self.assertEqual(data['description'], wish.description)
        if check_id:
            self.assertEqual(data['id'], wish.id)

    def test_create_wish(self):
        data = {
            'title': 'Test Wish',
            'price': 100.0,
            'link': 'https://ya.ru',
            'description': 'Test desc'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_user_1.auth_token.key}')
        response = self.client.post(self.create_url, data, format='json')
        wish = Wish.objects.latest('id')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_user_1.wishes.count(), 1)
        self.assertEqual(self.test_user_2.wishes.count(), 0)

        self._check_wish(data, wish)
        self._check_wish(response.data, wish)

    def test_create_emtpy_wish(self):
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_user_1.auth_token.key}')
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.test_user_1.wishes.count(), 0)
        self.assertEqual(len(response.data['title']), 1)

    def test_create_wish_with_defaults(self):
        data = {
            'title': 'Test Wish'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_user_1.auth_token.key}')
        response = self.client.post(self.create_url, data, format='json')
        wish = Wish.objects.latest('id')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_user_1.wishes.count(), 1)
        self.assertEqual(self.test_user_2.wishes.count(), 0)

        self._check_wish({**data, 'price': 0.0, 'link': '', 'description': ''}, wish)
        self._check_wish(response.data, wish)

    def test_create_wish_with_too_long_title(self):
        data = {
            'title': 'Test Wish' * 100
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_user_1.auth_token.key}')
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.test_user_1.wishes.count(), 0)
        self.assertEqual(len(response.data['title']), 1)

    def test_create_wish_with_too_long_link(self):
        data = {
            'title': 'Test Wish',
            'link': 'link' * 100
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_user_1.auth_token.key}')
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.test_user_1.wishes.count(), 0)
        self.assertEqual(len(response.data['link']), 1)

    def test_create_wish_with_invalid_price(self):
        data = {
            'title': 'Test Wish',
            'price': -100
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_user_1.auth_token.key}')
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.test_user_1.wishes.count(), 0)
        self.assertEqual(len(response.data['price']), 1)

    def test_get_wish_detail(self):
        data = {
            'title': 'Test Wish',
            'price': 100.0,
            'link': 'https://ya.ru',
            'description': 'Test desc'
        }
        wish = Wish.objects.create(**data, owner=self.test_user_1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_user_1.auth_token.key}')
        response = self.client.get(reverse('wish-detail', args=[wish.id]), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._check_wish({**data, 'id': wish.id}, wish, check_id=True)
        self._check_wish(response.data, wish, check_id=True)
