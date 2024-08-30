from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@gmail.com',
            'first_name': 'test',
            'last_name': 'test',
            'password1': 'test12345',
            'password2': 'test12345',
        }

    def test_user_register_page(self):
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_register_success(self):
        user_model = get_user_model()
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        redirect_uri = reverse('users:register_success')

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())

    def test_user_register_password_error(self):
        self.data['password2'] = 'test1234'

        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Введенные пароли не совпадают.')

    def test_user_register_exists_error(self):
        user_model = get_user_model()
        user_model.objects.create_user(username=self.data['username'])

        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.')
