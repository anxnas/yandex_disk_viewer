from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponse
from unittest.mock import patch
import requests

class IndexViewTests(TestCase):
    """
    Тесты для IndexView.
    """

    def setUp(self):
        """
        Настройка перед каждым тестом.
        Создает клиент и определяет URL для IndexView.
        """
        self.client = Client()
        self.url = reverse('index')  # Предполагается, что URL для IndexView называется 'index'

    @patch('undisk.views.requests.get')
    def test_get_request_success(self, mock_get):
        """
        Тест для успешного GET запроса.

        Настраивает mock для успешного ответа от Yandex Disk API.
        Проверяет, что статус ответа 200, используется правильный шаблон,
        и содержится заголовок "UnDisk" и текст "Public key:".
        """
        # Настройка mock для успешного ответа от Yandex Disk API
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"_embedded": {"items": []}}'
        mock_get.return_value = mock_response

        response = self.client.get(self.url, {'public_key': 'test_key'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'undisk/index.html')
        self.assertContains(response, 'Un<span class="highlight">Disk</span>', html=True)
        self.assertContains(response, 'Public key:', html=True)

    @patch('undisk.views.requests.get')
    def test_get_request_failure(self, mock_get):
        """
        Тест для неудачного GET запроса.

        Настраивает mock для неудачного ответа от Yandex Disk API.
        Проверяет, что отображается сообщение об ошибке.
        """
        # Настройка mock для неудачного ответа от Yandex Disk API
        mock_response = requests.Response()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        response = self.client.get(self.url, {'public_key': 'test_key'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'undisk/index.html')
        self.assertContains(response, 'Произошла ошибка при запросе к Yandex Disk API.', html=True)

    @patch('undisk.views.requests.get')
    def test_post_request_success(self, mock_get):
        """
        Тест для успешного POST запроса.

        Настраивает mock для успешного ответа от Yandex Disk API.
        Проверяет, что ответ имеет статус 200 и тип содержимого application/zip.
        """
        # Настройка mock для успешного ответа от Yandex Disk API
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"href": "http://example.com/download"}'
        mock_get.return_value = mock_response

        response = self.client.post(self.url, {'public_key': 'test_key', 'download_selected': 'true', 'selected_files': ['file1', 'file2']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')

    @patch('undisk.views.requests.get')
    def test_post_request_failure(self, mock_get):
        """
        Тест для неудачного POST запроса.

        Настраивает mock для неудачного ответа от Yandex Disk API.
        Проверяет, что отображается сообщение об ошибке.
        """
        # Настройка mock для неудачного ответа от Yandex Disk API
        mock_response = requests.Response()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        response = self.client.post(self.url, {'public_key': 'test_key', 'download_selected': 'true', 'selected_files': ['file1', 'file2']})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'undisk/index.html')
        self.assertContains(response, 'Произошла ошибка при запросе к Yandex Disk API.', html=True)