from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from women.models import Women


class GetPageTestCase(TestCase):
    def setUp(self):
        """Инициализация перед выполнением каждого теста"""

    def test_home_page(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # self.assertIn('women/index.html', response.template_name)
        self.assertTemplateUsed(response, 'women/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def tearDown(self):
        """Действие после выполнения каждого теста"""
